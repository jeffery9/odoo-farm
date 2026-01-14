from odoo import models, fields, api


class ProtectedCultivationOperation(models.Model):
    """
    Protected Cultivation Operation model to manage greenhouse and controlled environment farming
    """
    _name = 'farm.protected.cultivation.operation'
    _description = 'Protected Cultivation Operation'
    _inherits = {'project.task': 'operation_id'}
    _inherit = ['mail.thread', 'mail.activity.mixin']

    operation_id = fields.Many2one(
        'project.task',
        required=True,
        ondelete='cascade',
        string='Operation Task'
    )

    # Protected cultivation specific fields
    temperature_target_min = fields.Float(
        string='Min Target Temperature (°C)',
        help='Minimum target temperature for the growing environment'
    )
    temperature_target_max = fields.Float(
        string='Max Target Temperature (°C)',
        help='Maximum target temperature for the growing environment'
    )
    humidity_target_min = fields.Float(
        string='Min Target Humidity (%)',
        help='Minimum target humidity percentage'
    )
    humidity_target_max = fields.Float(
        string='Max Target Humidity (%)',
        help='Maximum target humidity percentage'
    )
    co2_level_target = fields.Float(
        string='Target CO2 Level (ppm)',
        help='Target CO2 concentration in parts per million'
    )
    lighting_schedule = fields.Char(
        string='Lighting Schedule',
        help='Lighting schedule and duration'
    )

    # System management
    irrigation_fertigation_system = fields.Selection([
        ('drip', 'Drip Irrigation'),
        ('ebb_flow', 'Ebb and Flow'),
        ('nft', 'NFT (Nutrient Film Technique)'),
        ('dwt', 'Deep Water Culture'),
    ], string='Irrigation/Fertigation System')

    # Protected cultivation specific data
    structure_type = fields.Selection([
        ('greenhouse_glass', 'Glass Greenhouse'),
        ('greenhouse_poly', 'Polycarbonate Greenhouse'),
        ('polytunnel', 'Polytunnel'),
        ('growth_chamber', 'Growth Chamber'),
        ('vertical_farm', 'Vertical Farming System'),
    ], string='Structure Type')

    growing_method = fields.Selection([
        ('soil', 'Soil-based'),
        ('substrate', 'Substrate-based'),
        ('hydroponic', 'Hydroponic'),
        ('aeroponic', 'Aeroponic'),
        ('aquaponic', 'Aquaponic'),
    ], string='Growing Method')

    # Linked to specific crops and structures
    crop_type_id = fields.Many2one(
        'product.template',
        domain=[('is_agricultural_product', '=', True)],
        string='Crop Type',
        help='Type of crop being cultivated'
    )
    growing_structure_id = fields.Many2one(
        'stock.location',
        domain=[('is_growing_structure', '=', True)],
        string='Growing Structure',
        help='Protected growing structure for this operation'
    )
    growing_media_id = fields.Many2one(
        'product.product',
        domain=[('is_growing_media', '=', True)],
        string='Growing Media',
        help='Growing media used (soil, substrate, etc.)'
    )

    # Environmental monitoring
    environmental_log_ids = fields.One2many(
        'farm.environmental.log',
        'protected_operation_id',
        string='Environmental Logs'
    )
    nutrient_solution_ph = fields.Float(
        string='Nutrient Solution pH',
        help='pH level of the nutrient solution'
    )
    nutrient_solution_ec = fields.Float(
        string='Nutrient Solution EC',
        help='Electrical conductivity of the nutrient solution'
    )

    @api.model
    def create(self, vals):
        # Set default values based on crop type if available
        if vals.get('crop_type_id'):
            crop = self.env['product.template'].browse(vals['crop_type_id'])
            if crop.default_temperature_min:
                vals.setdefault('temperature_target_min', crop.default_temperature_min)
            if crop.default_temperature_max:
                vals.setdefault('temperature_target_max', crop.default_temperature_max)
            if crop.default_humidity_min:
                vals.setdefault('humidity_target_min', crop.default_humidity_min)
            if crop.default_humidity_max:
                vals.setdefault('humidity_target_max', crop.default_humidity_max)

        return super().create(vals)

    def action_view_environmental_logs(self):
        """Action to view environmental monitoring logs"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'farm.environmental.log',
            'view_mode': 'tree,form',
            'domain': [('protected_operation_id', '=', self.id)],
            'context': {
                'default_protected_operation_id': self.id,
                'default_location_id': self.growing_structure_id.id if self.growing_structure_id else False
            },
            'name': 'Environmental Logs',
        }


class FarmEnvironmentalLog(models.Model):
    """
    Environmental Log model to track conditions in protected cultivation
    """
    _name = 'farm.environmental.log'
    _description = 'Farm Environmental Log'
    _order = 'timestamp desc'

    protected_operation_id = fields.Many2one(
        'farm.protected.cultivation.operation',
        string='Protected Operation',
        required=True
    )
    location_id = fields.Many2one(
        'stock.location',
        string='Growing Structure',
        required=True
    )
    timestamp = fields.Datetime(
        string='Timestamp',
        default=fields.Datetime.now,
        required=True
    )
    temperature = fields.Float(string='Temperature (°C)')
    humidity = fields.Float(string='Humidity (%)')
    co2_level = fields.Float(string='CO2 Level (ppm)')
    light_intensity = fields.Float(string='Light Intensity (Lux)')
    ph_level = fields.Float(string='pH Level')
    ec_level = fields.Float(string='EC Level (dS/m)')
    notes = fields.Text(string='Notes')