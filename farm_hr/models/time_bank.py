from odoo import models, fields, api, _

class FarmTimeBankLedger(models.Model):
    _name = 'farm.time.bank.ledger'
    _description = 'Rural Time Bank Ledger'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Transaction Ref", required=True, default=lambda self: _('New'))
    member_id = fields.Many2one('res.partner', string="Villager (Member)", required=True)
    credit_amount = fields.Float("Labor Credits (Hours)", required=True)
    transaction_type = fields.Selection([
        ('earn', 'Earned (Helped others)'),
        ('spend', 'Spent (Received help)'),
        ('elderly_care', 'Elderly Care Subsidy')
    ], string="Type", required=True)
    
    source_worklog_id = fields.Many2one('farm.worklog', string="Source Worklog")
    description = fields.Text("Description")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('farm.time.bank') or _('TB')
        return super().create(vals_list)

class FarmWorklog(models.Model):
    _inherit = 'farm.worklog'

    is_mutual_aid = fields.Boolean("Mutual Aid (Time Bank)", default=False)
    beneficiary_partner_id = fields.Many2one('res.partner', string="Beneficiary (Who was helped)")
    time_bank_ledger_id = fields.Many2one('farm.time.bank.ledger', string="Time Bank Ledger", readonly=True)

    def action_approve(self):
        res = super().action_approve()
        for log in self:
            if log.is_mutual_aid and log.beneficiary_partner_id and not log.time_bank_ledger_id:
                # 1. Credit the worker (A helps B)
                ledger_earn = self.env['farm.time.bank.ledger'].create({
                    'member_id': log.employee_id.user_id.partner_id.id or log.employee_id.address_home_id.id,
                    'credit_amount': log.quantity, # Assuming quantity is hours
                    'transaction_type': 'earn',
                    'source_worklog_id': log.id,
                    'description': f"Helped {log.beneficiary_partner_id.name}"
                })
                log.time_bank_ledger_id = ledger_earn.id
                
                # 2. Debit the beneficiary (B received help)
                self.env['farm.time.bank.ledger'].create({
                    'member_id': log.beneficiary_partner_id.id,
                    'credit_amount': -log.quantity,
                    'transaction_type': 'spend',
                    'source_worklog_id': log.id,
                    'description': f"Received help from {log.employee_id.name}"
                })
                
                log.message_post(body=_("TIME BANK: %s earned %s Labor Credits for helping %s.") % (
                    log.employee_id.name, log.quantity, log.beneficiary_partner_id.name
                ))
        return res
