from odoo import models, fields


class CommonFieldMixin(models.AbstractModel):
    """
    Abstract model to define common field patterns used across farm supply models
    """
    _name = 'farm.supply.common.fields'
    _description = 'Farm Supply Common Fields'

    # Common timestamp field
    timestamp = fields.Datetime('Timestamp', default=fields.Datetime.now)

    # Common notes field
    notes = fields.Text('Notes')

    # Common temperature fields
    temperature = fields.Float('Temperature (°C)')
    current_temperature = fields.Float('Current Temperature (°C)')

    # Common humidity fields
    humidity = fields.Float('Humidity (%)')
    current_humidity = fields.Float('Current Humidity (%)')

    # Common energy fields
    energy_reading = fields.Float('Energy Reading (kWh)')
    total_energy_consumption = fields.Float('Total Energy Consumption (kWh)')
    energy_efficiency_score = fields.Float('Energy Efficiency Score')

    # Common status fields
    equipment_status = fields.Selection([
        ('running', 'Running'),
        ('standby', 'Standby'),
        ('maintenance', 'Maintenance'),
        ('fault', 'Fault'),
    ], string='Equipment Status', default='running')

    # Common compliance fields
    is_compliance_warning = fields.Boolean("Compliance Warning")
    total_amount = fields.Float('Total Amount')