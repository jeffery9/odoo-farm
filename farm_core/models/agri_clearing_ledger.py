from odoo import models, fields, api, _

class AgriClearingLedger(models.Model):
    """
    Level 3+: Community Clearing Ledger.
    Records every transaction of sustainability credits and reputation score changes.
    """
    _name = 'agri.clearing.ledger'
    _description = 'Agricultural Clearing Ledger'
    _order = 'create_date desc'
    _inherit = ['mail.thread']

    name = fields.Char("Entry ID", required=True, copy=False, readonly=True, default=lambda self: _('New'))
    partner_id = fields.Many2one('res.partner', string="Community Member", required=True, index=True)
    
    # Value Changes
    credit_change = fields.Float("Impact Credit Change", digits=(12, 2), help="Change in monetized sustainability credits.")
    score_change = fields.Integer("Reputation Score Change", help="Change in reputation credit score.")
    
    # Source & Description
    source_ref = fields.Reference(
        selection=[
            ('mrp.production', 'Intervention'),
            ('stock.lot', 'Lot'),
            ('agri.value.bridge', 'Value Bridge'),
            ('agri.a2a.negotiation', 'A2A Negotiation')
        ],
        string="Source Reference"
    )
    description = fields.Text("Transaction Description")
    
    # Human Audit State
    state = fields.Selection([
        ('draft', 'Pending Audit'),
        ('confirmed', 'Confirmed'),
        ('rejected', 'Rejected')
    ], default='draft', tracking=True, string="Transaction State")

    def action_confirm(self):
        """
        [Human Audit Redline]
        Manually approves a transaction. This will trigger compute field updates.
        """
        for record in self:
            record.state = 'confirmed'
            # Force recompute of linked records
            if record.partner_id:
                record.partner_id._compute_reputation_credit_score()
        return True

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('agri.clearing.ledger') or '/'
        return super(AgriClearingLedger, self).create(vals_list)