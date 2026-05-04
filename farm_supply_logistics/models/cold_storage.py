from odoo import models, fields, api


class ColdStorageFacility(models.Model):
    """
    Cold Storage Management [US-009-09]
    """
    _name = 'cold.storage.facility'
    _description = 'Cold Storage Facility'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Facility Name', required=True)
    facility_code = fields.Char('Facility Code', required=True, copy=False)
    location_id = fields.Many2one('farm.location', string='Location')
    capacity_volume = fields.Float('Capacity (m3)')
    capacity_weight = fields.Float('Capacity (kg)')

    # Temperature zones
    min_temperature = fields.Float('Min Temperature (℃)')
    max_temperature = fields.Float('Max Temperature (℃)')
    humidity_min = fields.Float('Min Humidity (%)')
    humidity_max = fields.Float('Max Humidity (%)')

    # Multi-zone support
    zone_ids = fields.One2many('cold.storage.zone', 'facility_id', string='Storage Zones')
    current_utilization = fields.Float('Current Utilization %', compute='_compute_utilization', store=True, precompute=True)

    status = fields.Selection([
        ('operational', 'Operational'),
        ('maintenance', 'Under Maintenance'),
        ('out_of_service', 'Out of Service'),
    ], string='Status', default='operational')

    _facility_code_unique = models.Constraint(
        'UNIQUE(facility_code)',
        'Facility code must be unique!'
    )

    @api.depends('zone_ids.current_volume', 'zone_ids.current_weight', 'capacity_volume', 'capacity_weight')
    def _compute_utilization(self):
        for facility in self:
            if facility.capacity_volume > 0:
                total_current_volume = sum(zone.current_volume for zone in facility.zone_ids)
                facility.current_utilization = (total_current_volume / facility.capacity_volume) * 100
            else:
                facility.current_utilization = 0


class ColdStorageZone(models.Model):
    """
    Cold Storage Zone [US-009-09]
    """
    _name = 'cold.storage.zone'
    _description = 'Cold Storage Zone'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Zone Name', required=True)
    zone_code = fields.Char('Zone Code', required=True, copy=False)
    facility_id = fields.Many2one('cold.storage.facility', string='Facility', required=True)

    # Temperature specifications per zone
    target_temperature_min = fields.Float('Target Min Temp (℃)')
    target_temperature_max = fields.Float('Target Max Temp (℃)')
    current_temperature = fields.Float('Current Temperature (℃)')
    humidity_level = fields.Float('Current Humidity (%)')

    # Capacity
    capacity_volume = fields.Float('Capacity (m3)')
    capacity_weight = fields.Float('Capacity (kg)')
    current_volume = fields.Float('Current Volume (m3)')
    current_weight = fields.Float('Current Weight (kg)')

    # Product type restrictions
    allowed_product_categories = fields.Many2many('product.category', string='Allowed Product Categories')

    # Status
    status = fields.Selection([
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('maintenance', 'Under Maintenance'),
    ], string='Status', default='available')

    _zone_code_unique = models.Constraint(
        'UNIQUE(zone_code)',
        'Zone code must be unique!'
    )


class ColdStorageInventory(models.Model):
    """
    Cold Storage Inventory Tracking [US-009-09]
    """
    _name = 'cold.storage.inventory'
    _description = 'Cold Storage Inventory'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Inventory Reference', required=True, default='/')
    zone_id = fields.Many2one('cold.storage.zone', string='Storage Zone', required=True)
    product_id = fields.Many2one('product.product', string='Product', required=True)
    lot_id = fields.Many2one('stock.lot', string='Lot/Serial Number')

    quantity = fields.Float('Quantity')
    volume = fields.Float('Volume (m3)')
    weight = fields.Float('Weight (kg)')

    entry_date = fields.Datetime('Entry Date', default=fields.Datetime.now)
    expiry_date = fields.Date('Expiry Date')
    best_before_date = fields.Date('Best Before Date')

    # Temperature history during storage
    temperature_log_ids = fields.One2many('cold.storage.temperature.log', 'inventory_id', string='Temperature Logs')
    avg_temperature = fields.Float('Average Temperature (℃)', compute='_compute_avg_temperature', store=True, precompute=True)

    status = fields.Selection([
        ('stored', 'Stored'),
        ('released', 'Released'),
        ('expired', 'Expired'),
        ('quarantined', 'Quarantined'),
    ], string='Status', default='stored')

    @api.model
    def create(self, vals):
        if vals.get('name', '/') == '/':
            vals['name'] = self.env['ir.sequence'].next_by_code('cold.storage.inventory') or '/'
        return super().create(vals)

    @api.depends('temperature_log_ids.temperature')
    def _compute_avg_temperature(self):
        for inventory in self:
            if inventory.temperature_log_ids:
                avg_temp = sum(log.temperature for log in inventory.temperature_log_ids) / len(inventory.temperature_log_ids)
                inventory.avg_temperature = avg_temp
            else:
                inventory.avg_temperature = 0


class ColdStorageTemperatureLog(models.Model):
    """
    Cold Storage Temperature Log [US-009-07 & US-009-09]
    """
    _name = 'cold.storage.temperature.log'
    _description = 'Cold Storage Temperature Log'
    _order = 'timestamp desc'

    inventory_id = fields.Many2one('cold.storage.inventory', string='Inventory Item', ondelete='cascade')
    zone_id = fields.Many2one('cold.storage.zone', string='Storage Zone', required=True)

    timestamp = fields.Datetime('Timestamp', default=fields.Datetime.now, required=True)
    temperature = fields.Float('Temperature (℃)', required=True)
    humidity = fields.Float('Humidity (%)')

    # IoT sensor information
    sensor_id = fields.Char('Sensor ID')
    sensor_location = fields.Char('Sensor Location within Zone')

    # Alerts
    is_alert = fields.Boolean('Is Alert', compute='_compute_is_alert', store=True, precompute=True)
    alert_reason = fields.Char('Alert Reason', compute='_compute_is_alert', store=True, precompute=True)

    @api.depends('temperature', 'humidity', 'zone_id')
    def _compute_is_alert(self):
        for log in self:
            if log.zone_id:
                is_out_of_range = (log.temperature < log.zone_id.target_temperature_min or
                                  log.temperature > log.zone_id.target_temperature_max)
                is_humidity_out_of_range = (log.humidity < log.zone_id.humidity_min or
                                          log.humidity > log.zone_id.humidity_max)

                if is_out_of_range:
                    log.is_alert = True
                    log.alert_reason = f'Temperature out of range: {log.temperature}℃ (range: {log.zone_id.target_temperature_min}-{log.zone_id.target_temperature_max}℃)'
                elif is_humidity_out_of_range:
                    log.is_alert = True
                    log.alert_reason = f'Humidity out of range: {log.humidity}% (range: {log.zone_id.humidity_min}-{log.zone_id.humidity_max}%)'
                else:
                    log.is_alert = False
                    log.alert_reason = False
            else:
                log.is_alert = False
                log.alert_reason = False