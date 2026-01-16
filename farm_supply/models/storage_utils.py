from odoo import models, fields, api


class StorageManagementMixin(models.AbstractModel):
    """
    Mixin class for common storage management patterns
    """
    _name = 'farm.supply.storage.utils'
    _description = 'Farm Supply Storage Utilities'

    optimal_temperature_min = fields.Float('Optimal Min Temperature (°C)')
    optimal_temperature_max = fields.Float('Optimal Max Temperature (°C)')
    optimal_humidity_min = fields.Float('Optimal Min Humidity (%)')
    optimal_humidity_max = fields.Float('Optimal Max Humidity (%)')
    current_temperature = fields.Float('Current Temperature (°C)')
    current_humidity = fields.Float('Current Humidity (%)')
    temperature_monitoring = fields.Boolean('Temperature Monitoring', default=False)
    humidity_monitoring = fields.Boolean('Humidity Monitoring', default=False)

    def _check_storage_compatibility(self, product):
        """
        Check if product is compatible with storage conditions
        """
        if not hasattr(self, 'optimal_temperature_min') or not hasattr(self, 'optimal_temperature_max'):
            return True  # If storage conditions not defined, assume compatible

        if not product:
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