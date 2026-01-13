from odoo import models, fields, api, _

class StorageEnvironment(models.Model):
    """US-14-06: Storage Environment Monitoring"""
    _name = 'farm.storage.env'
    _description = 'Storage Environment Log'
    _order = 'timestamp desc'

    location_id = fields.Many2one('stock.location', string='Storage Location', required=True)
    timestamp = fields.Datetime('Timestamp', default=fields.Datetime.now)
    temperature = fields.Float('Temperature (℃)')
    humidity = fields.Float('Humidity (%)')
    co2_level = fields.Float('CO2 Level (ppm)')
    
    is_alert = fields.Boolean('Is Alert', default=False)
    alert_message = fields.Char('Alert Message')

class ProcessingWaste(models.Model):
    """US-14-12: Waste Management"""
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
