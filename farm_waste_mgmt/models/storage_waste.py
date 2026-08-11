from odoo import models, fields, api, _

class ProcessingWaste(models.Model):
    """US-037-12: Waste Management"""
    _name = 'farm.processing.waste'
    _description = 'Processing Waste Management'

    name = fields.Char('Waste Reference', required=True, copy=False, readonly=True, default=lambda self: _('New'))
    production_id = fields.Many2one('mrp.production', string='Processing Order')
    product_id = fields.Many2one('product.product', string='Waste Product')
    quantity = fields.Float('Quantity')
    uom_id = fields.Many2one('uom.uom', string='Unit of Measure')
    
    disposal_method = fields.Selection([
        ('field', 'Return to Field (Fertilizer)'),
        ('feed', 'Animal Feed'),
        ('recycling', 'Third Party Recycling'),
        ('disposal', 'Safe Disposal')
    ], string='Disposal Method', required=True)
    
    notes = fields.Text('Disposal Details')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('farm.processing.waste') or _('New')
        return super().create(vals_list)
