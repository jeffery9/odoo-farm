from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    requires_cold_chain = fields.Boolean("Cold Chain Required", default=False)
    target_temperature_min = fields.Float("Min Temp (℃)")
    target_temperature_max = fields.Float("Max Temp (℃)")

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    is_cold_chain = fields.Boolean("Is Cold Chain Transport", compute='_compute_is_cold_chain', store=True)
    actual_transport_temp = fields.Float("Actual Transport Temp (℃)")
    
    # Transport Details [US-03-03]
    vehicle_id = fields.Many2one('farm.vehicle', string="Vehicle")
    driver_id = fields.Many2one('res.partner', string="Driver", domain="[('is_company', '=', False)]")
    
    packaging_level = fields.Selection([
        ('box', 'Box/Carton'),
        ('crate', 'Crate'),
        ('pallet', 'Pallet')
    ], string="Primary Packaging")

    temperature_log_ids = fields.One2many('farm.transport.temperature', 'picking_id', string="Temperature History")

    @api.depends('move_ids.product_id')
    def _compute_is_cold_chain(self):
        for picking in self:
            picking.is_cold_chain = any(picking.move_ids.mapped('product_id.requires_cold_chain'))

class FarmVehicle(models.Model):
    _name = 'farm.vehicle'
    _description = 'Farm Transport Vehicle'

    name = fields.Char("License Plate", required=True)
    model = fields.Char("Model")
    vehicle_type = fields.Selection([
        ('refrigerated', 'Refrigerated Truck'),
        ('tractor', 'Tractor'),
        ('van', 'Van'),
        ('other', 'Other')
    ], string="Type", default='refrigerated')
    capacity_weight = fields.Float("Max Payload (kg)")

class FarmTransportTemperature(models.Model):
    _name = 'farm.transport.temperature'
    _description = 'Transport Temperature Log'
    _order = 'timestamp desc'

    picking_id = fields.Many2one('stock.picking', ondelete='cascade')
    timestamp = fields.Datetime("Timestamp", default=fields.Datetime.now)
    temperature = fields.Float("Temperature (℃)", required=True)
    location_name = fields.Char("Location/Milestone")
