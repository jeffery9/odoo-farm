from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class VmiAgreement(models.Model):
    """
    VMI (Vendor Managed Inventory) Agreement [US-09-14]
    """
    _name = 'vmi.agreement'
    _description = 'VMI Agreement'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Agreement Number', required=True, default=lambda self: _('New'))
    supplier_id = fields.Many2one('res.partner', string='Supplier', required=True)
    customer_id = fields.Many2one('res.partner', string='Customer', required=True)
    product_ids = fields.Many2many('product.product', string='VMI Products')
    agreement_start_date = fields.Date('Agreement Start Date', required=True)
    agreement_end_date = fields.Date('Agreement End Date')
    min_stock_level = fields.Float('Minimum Stock Level', help='Minimum stock level to maintain')
    max_stock_level = fields.Float('Maximum Stock Level', help='Maximum stock level to maintain')
    reorder_point = fields.Float('Reorder Point', help='Stock level that triggers reorder')
    lead_time_days = fields.Integer('Lead Time (Days)', help='Days from reorder to delivery')
    status = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('suspended', 'Suspended'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', required=True)
    is_active = fields.Boolean('Is Active', compute='_compute_is_active', store=True)

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('vmi.agreement') or '/'
        return super().create(vals)

    @api.depends('agreement_start_date', 'agreement_end_date', 'status')
    def _compute_is_active(self):
        for record in self:
            if record.status in ['suspended', 'cancelled']:
                record.is_active = False
            elif record.status == 'expired':
                record.is_active = False
            elif record.agreement_start_date and record.agreement_end_date:
                today = fields.Date.context_today(self)
                record.is_active = (record.agreement_start_date <= today <= record.agreement_end_date if record.agreement_end_date else record.agreement_start_date <= today)
            else:
                record.is_active = record.status == 'active'

    def action_activate(self):
        """Activate the VMI agreement"""
        self.write({'status': 'active'})

    def action_suspend(self):
        """Suspend the VMI agreement"""
        self.write({'status': 'suspended'})


class VmiStockMonitoring(models.Model):
    """
    VMI Stock Monitoring
    """
    _name = 'vmi.stock.monitoring'
    _description = 'VMI Stock Monitoring'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    vmi_agreement_id = fields.Many2one('vmi.agreement', string='VMI Agreement', required=True)
    product_id = fields.Many2one('product.product', string='Product', required=True)
    current_stock = fields.Float('Current Stock')
    forecast_demand = fields.Float('Forecast Demand')
    days_of_supply = fields.Float('Days of Supply', compute='_compute_days_of_supply', store=True)
    last_updated = fields.Datetime('Last Updated', default=fields.Datetime.now)
    reorder_suggested = fields.Boolean('Reorder Suggested', compute='_compute_reorder_suggested', store=True)
    suggested_reorder_qty = fields.Float('Suggested Reorder Quantity', compute='_compute_suggested_reorder', store=True)

    @api.depends('current_stock', 'forecast_demand')
    def _compute_days_of_supply(self):
        for record in self:
            if record.forecast_demand > 0:
                record.days_of_supply = (record.current_stock / record.forecast_demand) * 7  # Assuming weekly forecast
            else:
                record.days_of_supply = 0

    @api.depends('current_stock', 'vmi_agreement_id.reorder_point')
    def _compute_reorder_suggested(self):
        for record in self:
            if record.vmi_agreement_id:
                record.reorder_suggested = record.current_stock <= record.vmi_agreement_id.reorder_point
            else:
                record.reorder_suggested = False

    @api.depends('vmi_agreement_id.max_stock_level', 'current_stock', 'vmi_agreement_id.lead_time_days', 'forecast_demand')
    def _compute_suggested_reorder(self):
        for record in self:
            if record.vmi_agreement_id:
                # Calculate reorder quantity based on max level and lead time demand
                lead_time_demand = record.forecast_demand * (record.vmi_agreement_id.lead_time_days / 7)  # Convert daily to weekly
                suggested_qty = max(0, record.vmi_agreement_id.max_stock_level - record.current_stock + lead_time_demand)
                record.suggested_reorder_qty = suggested_qty
            else:
                record.suggested_reorder_qty = 0

    def action_trigger_reorder(self):
        """Trigger reorder for VMI items"""
        PurchaseOrder = self.env['purchase.order']
        PurchaseOrderLine = self.env['purchase.order.line']

        for record in self:
            if record.reorder_suggested and record.suggested_reorder_qty > 0:
                # Find or create purchase order for this supplier
                po = PurchaseOrder.search([
                    ('partner_id', '=', record.vmi_agreement_id.supplier_id.id),
                    ('state', '=', 'draft'),
                    ('vmi_agreement_id', '=', record.vmi_agreement_id.id),
                ], limit=1)

                if not po:
                    po = PurchaseOrder.create({
                        'partner_id': record.vmi_agreement_id.supplier_id.id,
                        'vmi_agreement_id': record.vmi_agreement_id.id,
                        'picking_type_id': self.env['stock.picking.type'].search([
                            ('code', '=', 'incoming'),
                            ('warehouse_id.company_id', '=', self.env.company.id)
                        ], limit=1).id,
                    })

                # Add line to purchase order
                PurchaseOrderLine.create({
                    'order_id': po.id,
                    'product_id': record.product_id.id,
                    'product_qty': record.suggested_reorder_qty,
                    'price_unit': record.product_id.standard_price,
                })