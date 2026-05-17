from odoo import models, fields, api, _

class FarmMicroLoan(models.Model):
    _name = 'farm.micro.loan'
    _description = 'Cooperative Micro-Credit Loan'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Loan Ref", default=lambda self: _('New'))
    farmer_id = fields.Many2one('res.users', string="Farmer", required=True)
    amount_requested = fields.Float("Requested Amount ($)", required=True)
    digital_trust_score = fields.Float("Digital Trust Score (0-100)", readonly=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('evaluating', 'AI Evaluating'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('disbursed', 'Disbursed')
    ], default='draft')
    
    settlement_id = fields.Many2one('internal.settlement', string="Disbursement Settlement", readonly=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('farm.micro.loan') or _('LOAN')
        return super().create(vals_list)

    def action_evaluate_and_approve(self):
        """
        [US-SCENARIO-18] Data-Backed Cooperative Micro-Credit
        Evaluates the farmer's digital farming records (trust_score of past tasks).
        If average score > 80, automatically approve.
        """
        for loan in self:
            loan.state = 'evaluating'
            
            # Fetch past farming tasks for this user
            tasks = self.env['project.task'].search([
                ('user_ids', 'in', [loan.farmer_id.id]),
                ('trust_verification_status', '=', 'verified')
            ])
            
            if not tasks:
                loan.digital_trust_score = 0.0
                loan.state = 'rejected'
                loan.message_post(body=_("Rejected: Insufficient digital farming records."))
                continue
                
            avg_score = sum(tasks.mapped('trust_score')) / len(tasks)
            loan.digital_trust_score = avg_score
            
            if avg_score >= 80.0:
                loan.state = 'approved'
                loan.message_post(body=_("Approved: Stellar digital farming record. Average Trust Score: %.2f") % avg_score)
                # Auto-disburse
                loan._disburse_loan()
            else:
                loan.state = 'rejected'
                loan.message_post(body=_("Rejected: Trust Score %.2f is below the 80.0 threshold.") % avg_score)

    def _disburse_loan(self):
        self.ensure_one()
        if 'internal.settlement' in self.env:
            settlement = self.env['internal.settlement'].create({
                'from_entity_id': self.env.company.partner_id.id,
                'to_entity_id': self.farmer_id.partner_id.id,
                'settlement_type': 'general',
                'amount': self.amount_requested,
                'description': f"Micro-Credit Disbursement: {self.name}"
            })
            settlement.action_confirm()
            self.settlement_id = settlement.id
            self.state = 'disbursed'
