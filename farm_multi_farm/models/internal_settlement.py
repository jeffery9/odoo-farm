from odoo import models, fields, api, _

class InternalSettlement(models.Model):
    _name = 'internal.settlement'
    _description = 'Internal Settlement'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Settlement Reference', required=True, copy=False, readonly=True, default=lambda self: _('New'))
    code = fields.Char('Code', copy=False)
    
    from_entity_id = fields.Many2one('res.partner', string='From Entity (Debtor)', required=True)
    to_entity_id = fields.Many2one('res.partner', string='To Entity (Creditor)', required=True)
    
    settlement_type = fields.Selection([
        ('general', 'General'),
        ('resource_rental', 'Resource Rental'),
        ('service_fee', 'Service Fee')
    ], string='Type', default='general', required=True)
    
    amount = fields.Float('Amount', required=True)
    invoice_id = fields.Many2one("account.move", string="Invoice")
    currency_id = fields.Many2one("res.currency", string="Currency", default=lambda self: self.env.company.currency_id)
    # Removing hard dependency on resource.sharing for abstract settlement flexibility
    # resource_sharing_id = fields.Many2one("resource.sharing", string="Resource Sharing")
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

    def action_confirm(self):
        self.write({'state': 'confirmed'})
        # Automatically generate internal invoice entries when confirmed
        self.action_generate_invoice()

    def action_generate_invoice(self):
        """
        [US-UBER-01] Generates twin invoices for Multi-Farm settlement:
        1. AP (Accounts Payable) for the Debtor (from_entity_id).
        2. AR (Accounts Receivable) for the Creditor (to_entity_id).
        """
        self.ensure_one()
        if self.invoice_id:
            return True
            
        # Simplified: We just create one Vendor Bill for the from_entity (B) to pay to_entity (A)
        # In a real multi-company setup, this would be two linked entries
        move_vals = {
            'move_type': 'in_invoice', # Vendor Bill for Farm B
            'partner_id': self.to_entity_id.id, # Pay to Farm A
            'invoice_date': self.settlement_date,
            'invoice_line_ids': [(0, 0, {
                'name': self.description or self.name,
                'price_unit': self.amount,
                'quantity': 1,
            })],
        }
        invoice = self.env['account.move'].create(move_vals)
        self.write({'invoice_id': invoice.id})
        self.message_post(body=_("Generated Internal Settlement Invoice: %s") % invoice.name)
        return True
