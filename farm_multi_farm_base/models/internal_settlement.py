from odoo import models, fields, api, _

class InternalSettlement(models.Model):
    _name = 'internal.settlement'
    _description = 'Internal Settlement'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Settlement Reference', required=True, copy=False, readonly=True, default=lambda self: _('New'))
    code = fields.Char('Code', copy=False)
    
    from_entity_id = fields.Many2one('res.partner', string='From Entity', required=True)
    to_entity_id = fields.Many2one('res.partner', string='To Entity', required=True)
    
    settlement_type = fields.Selection([
        ('general', 'General'),
    ], string='Type', default='general', required=True, ondelete={'general': 'set default'})
    
    amount = fields.Float('Amount', required=True)
    invoice_id = fields.Many2one("account.move", string="Invoice")
    currency_id = fields.Many2one("res.currency", string="Currency", default=lambda self: self.env.company.currency_id)
    resource_sharing_id = fields.Many2one("resource.sharing", string="Resource Sharing")
    settlement_date = fields.Date("Settlement Date", default=fields.Date.context_today)
    description = fields.Text('Description')
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', required=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('internal.settlement') or _('New')
        return super().create(vals_list)

    def action_generate_invoice(self):
        return True
