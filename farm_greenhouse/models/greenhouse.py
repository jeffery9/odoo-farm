from odoo import models, fields, api, _

class FarmLocation(models.Model):
    _inherit = 'farm.location'

    is_greenhouse = fields.Boolean("Is Greenhouse", default=False)
    greenhouse_type = fields.Selection([
        ('glass', 'Glass Greenhouse'),
        ('film', 'Plastic Film'),
        ('poly', 'Polycarbonate')
    ], string="Structure Type")
    
    # Environmental Status
    current_temp = fields.Float("Internal Temp (°C)")
    current_humidity = fields.Float("Humidity (%)")
    current_co2 = fields.Float("CO2 (ppm)")
    current_light = fields.Float("Light Intensity (Lux)")
    
    # Nutrient Stats
    current_ec = fields.Float("Nutrient EC (mS/cm)")
    current_ph = fields.Float("Nutrient pH")

class FarmGreenhouseControlRule(models.Model):
    _name = 'farm.greenhouse.control.rule'
    _description = 'Greenhouse Automation Rule'

    name = fields.Char("Rule Name", required=True)
    greenhouse_id = fields.Many2one('farm.location', string="Greenhouse", domain=[('is_greenhouse', '=', True)], required=True)
    
    parameter = fields.Selection([
        ('temp', 'Temperature'),
        ('hum', 'Humidity'),
        ('co2', 'CO2 Level'),
        ('light', 'Light')
    ], required=True)
    
    threshold_low = fields.Float("Low Threshold")
    threshold_high = fields.Float("High Threshold")
    
    action_ids = fields.One2many('farm.greenhouse.control.action', 'rule_id', string="Control Actions")
    active = fields.Boolean(default=True)

class FarmGreenhouseControlAction(models.Model):
    _name = 'farm.greenhouse.control.action'
    _description = 'Greenhouse Control Action'

    rule_id = fields.Many2one('farm.greenhouse.control.rule', ondelete='cascade')
    device_id = fields.Many2one('iiot.device', string="Control Device", required=True)
    command = fields.Char("MQTT Command", required=True)
    value = fields.Char("Value/Setting")

class FarmGreenhouseEnergyLog(models.Model):
    _name = 'farm.greenhouse.energy.log'
    _description = 'Greenhouse Energy Consumption'

    greenhouse_id = fields.Many2one('farm.location', string="Greenhouse", required=True)
    date = fields.Date("Date", default=fields.Date.today)
    
    kwh_consumed = fields.Float("Electricity (kWh)")
    water_consumed = fields.Float("Water (L)")
    carbon_footprint = fields.Float("Estimated Carbon (kg CO2e)", compute='_compute_carbon')

    @api.depends('kwh_consumed')
    def _compute_carbon(self):
        for rec in self:
            # Simulated factor: 0.5kg CO2 per kWh
            rec.carbon_footprint = rec.kwh_consumed * 0.5
