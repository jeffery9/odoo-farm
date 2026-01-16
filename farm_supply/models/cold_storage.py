from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class StockLocationExtension(models.Model):
    """
    扩展库存位置模型以支持冷库多温区管理 [US-09-09]
    Consolidated from both supply_chain_management.py and cold_storage_extension.py
    """
    _inherit = 'stock.location'

    storage_type = fields.Selection([
        ('ambient', 'Ambient Temperature'),
        ('chilled', 'Chilled (0-4°C)'),
        ('frozen', 'Frozen (-18°C)'),
        ('controlled_atmosphere', 'Controlled Atmosphere'),
        ('humidity_controlled', 'Humidity Controlled'),
    ], string='Storage Type')

    optimal_temperature_min = fields.Float('Optimal Min Temperature (°C)')
    optimal_temperature_max = fields.Float('Optimal Max Temperature (°C)')
    optimal_humidity_min = fields.Float('Optimal Min Humidity (%)')
    optimal_humidity_max = fields.Float('Optimal Max Humidity (%)')

    current_temperature = fields.Float('Current Temperature (°C)')
    current_humidity = fields.Float('Current Humidity (%)')
    temperature_monitoring = fields.Boolean('Temperature Monitoring', default=False)
    humidity_monitoring = fields.Boolean('Humidity Monitoring', default=False)
    temperature_readings = fields.One2many('cold.storage.reading', 'location_id', string='Temperature Readings')

    # For US-09-10: Energy efficiency tracking
    energy_meter_id = fields.Char('Energy Meter ID')
    last_energy_reading = fields.Float('Last Energy Reading (kWh)')
    total_energy_consumption = fields.Float('Total Energy Consumption (kWh)', compute='_compute_total_energy', store=True)

    # For US-09-10: Efficiency reports
    energy_efficiency_score = fields.Float('Energy Efficiency Score', compute='_compute_efficiency_score', store=True)

    def _compute_total_energy(self):
        """Compute total energy consumption"""
        for record in self:
            # In a real implementation, this would aggregate from readings
            record.total_energy_consumption = record.last_energy_reading or 0.0

    def _compute_efficiency_score(self):
        """Compute energy efficiency score"""
        for record in self:
            # Placeholder implementation
            record.energy_efficiency_score = 85.0  # Default score

    def _check_storage_compatibility(self, product):
        """Check if product is compatible with storage conditions"""
        if not self.storage_type or not product:
            return True

        # This would have more complex logic in a real implementation
        product_temp_min = getattr(product, 'optimal_storage_temp_min', 0)
        product_temp_max = getattr(product, 'optimal_storage_temp_max', 25)

        # Check if location's temperature range is suitable for product
        if (self.optimal_temperature_min and self.optimal_temperature_max and
            (product_temp_min > self.optimal_temperature_max or
             product_temp_max < self.optimal_temperature_min)):
            return False

        return True


class ColdStorageReading(models.Model):
    """
    冷库环境读数 [US-09-09 & US-09-10]
    Consolidated from both supply_chain_management.py and cold_storage_extension.py
    """
    _name = 'cold.storage.reading'
    _description = 'Cold Storage Environment Reading'
    _order = 'timestamp desc'

    location_id = fields.Many2one('stock.location', string='Storage Location', required=True)
    temperature = fields.Float('Temperature (°C)', required=True)
    humidity = fields.Float('Humidity (%)', required=True)
    timestamp = fields.Datetime('Timestamp', required=True, default=fields.Datetime.now)
    energy_reading = fields.Float('Energy Reading (kWh)')
    equipment_status = fields.Selection([
        ('running', 'Running'),
        ('standby', 'Standby'),
        ('maintenance', 'Maintenance'),
        ('fault', 'Fault'),
    ], string='Equipment Status', default='running')
    notes = fields.Text('Notes')

    @api.model
    def create(self, vals):
        reading = super().create(vals)
        # Update the parent location's current readings
        if reading.location_id:
            reading.location_id.write({
                'current_temperature': reading.temperature,
                'current_humidity': reading.humidity,
                'last_energy_reading': reading.energy_reading
            })
        return reading


class StockMoveExtension(models.Model):
    """
    扩展库存移动以支持冷库存储兼容性检查 [US-09-09]
    """
    _inherit = 'stock.move'

    @api.model
    def _action_done(self):
        """Override to check storage compatibility before moving products"""
        for move in self:
            if move.location_dest_id.storage_type and move.product_id:
                # Check if destination storage is compatible with product requirements
                if not move.location_dest_id._check_storage_compatibility(move.product_id):
                    raise ValidationError(
                        _("The product %s is not compatible with the storage conditions "
                          "of location %s. Please select a different destination location.") %
                        (move.product_id.name, move.location_dest_id.display_name)
                    )
        return super()._action_done()


class ProductTemplateExtension(models.Model):
    """
    扩展产品模板以支持存储要求 [US-09-09]
    """
    _inherit = 'product.template'

    optimal_storage_temp_min = fields.Float('Optimal Storage Min Temp (°C)')
    optimal_storage_temp_max = fields.Float('Optimal Storage Max Temp (°C)')
    optimal_storage_humidity_min = fields.Float('Optimal Storage Min Humidity (%)')
    optimal_storage_humidity_max = fields.Float('Optimal Storage Max Humidity (%)')
    requires_cold_storage = fields.Boolean('Requires Cold Storage', default=False)