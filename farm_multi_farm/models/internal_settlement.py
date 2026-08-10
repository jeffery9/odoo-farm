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
    
    # Twin Invoices [US-UBER-01]
    debtor_invoice_id = fields.Many2one("account.move", string="Debtor Invoice (AP)", readonly=True)
    creditor_invoice_id = fields.Many2one("account.move", string="Creditor Invoice (AR)", readonly=True)
    
    # Legacy field for compatibility (points to debtor invoice)
    invoice_id = fields.Many2one("account.move", string="Invoice", related='debtor_invoice_id', readonly=True)
    
    currency_id = fields.Many2one("res.currency", string="Currency", default=lambda self: self.env.company.currency_id)
    # Removing hard dependency on resource.sharing for abstract settlement flexibility
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

    def action_confirm(self):
        """
        Confirms settlement after verifying governance requirements.
        """
        for rec in self:
            # 1. Check for mandatory multi-sign approval [US-042-18]
            if hasattr(rec, '_check_multi_sign_status'):
                rec._check_multi_sign_status()
                
            rec.write({'state': 'confirmed'})
            
            # 2. Automatically generate internal invoice entries
            rec.action_generate_invoice()
        return True

    def _check_multi_sign_status(self):
        """ Stub for extension in farm_multi_farm_financial """
        return True

    def action_generate_invoice(self):
        """
        [US-UBER-01] Generates twin invoices for Multi-Farm settlement:
        1. AP (Accounts Payable) for the Debtor (from_entity_id).
        2. AR (Accounts Receivable) for the Creditor (to_entity_id).
        """
        self.ensure_one()
        if self.debtor_invoice_id or self.creditor_invoice_id:
            return True
            
        # Strategy: Create linked entries in a single transaction
        move_obj = self.env['account.move']
        
        # Determine companies based on partners
        debtor_farm = self.env['farm.entity'].search([('company_id.partner_id', '=', self.from_entity_id.id)], limit=1)
        creditor_farm = self.env['farm.entity'].search([('company_id.partner_id', '=', self.to_entity_id.id)], limit=1)
        
        # 1. Create Vendor Bill (AP) for Debtor Farm
        ap_vals = {
            'move_type': 'in_invoice',
            'partner_id': self.to_entity_id.id,
            'company_id': debtor_farm.company_id.id if debtor_farm else self.env.company.id,
            'invoice_date': self.settlement_date,
            'invoice_line_ids': [(0, 0, {
                'name': _("Internal Settlement (AP): %s") % (self.description or self.name),
                'price_unit': self.amount,
                'quantity': 1,
            })],
        }
        ap_invoice = move_obj.create(ap_vals)
        
        # 2. Create Customer Invoice (AR) for Creditor Farm
        ar_vals = {
            'move_type': 'out_invoice',
            'partner_id': self.from_entity_id.id,
            'company_id': creditor_farm.company_id.id if creditor_farm else self.env.company.id,
            'invoice_date': self.settlement_date,
            'invoice_line_ids': [(0, 0, {
                'name': _("Internal Settlement (AR): %s") % (self.description or self.name),
                'price_unit': self.amount,
                'quantity': 1,
            })],
        }
        ar_invoice = move_obj.create(ar_vals)
        
        self.write({
            'debtor_invoice_id': ap_invoice.id,
            'creditor_invoice_id': ar_invoice.id,
        })
        
        self.message_post(body=_(
            "Dual Invoices Generated: AP (%s) for %s and AR (%s) for %s"
        ) % (ap_invoice.name, self.from_entity_id.name, ar_invoice.name, self.to_entity_id.name))
        
        return True
