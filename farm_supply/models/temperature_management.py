from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class ShelfLifePrediction(models.Model):
    """
    基于温度的货架期预测模型 [US-09-07]
    """
    _name = 'shelf.life.prediction'
    _description = 'Shelf Life Prediction Based on Temperature'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'prediction_date desc'

    name = fields.Char('Prediction Reference', required=True, copy=False, readonly=True,
                       default=lambda self: _('New'))
    lot_id = fields.Many2one('stock.lot', string='Batch/Lot', required=True)
    product_id = fields.Many2one('product.product', string='Product', related='lot_id.product_id', store=True)
    initial_shelf_life = fields.Float('Initial Shelf Life (Days)')
    accumulated_temperature_deviation = fields.Float('Accumulated Temperature Deviation (°C*days)')
    last_updated = fields.Datetime('Last Updated', default=fields.Datetime.now)
    quality_warning_threshold = fields.Float('Quality Warning Threshold (%)', default=20.0,
                                           help='When predicted shelf life drops below this percentage, trigger warning activity')
    is_warning_triggered = fields.Boolean('Warning Triggered', default=False)
    initial_temperature = fields.Float('Initial Temperature (°C)', required=True)
    storage_temperature = fields.Float('Storage Temperature (°C)', required=True)
    humidity_level = fields.Float('Humidity Level (%)', required=True)
    predicted_shelf_life = fields.Float('Predicted Shelf Life (Days)', compute='_compute_predicted_shelf_life', store=True)
    prediction_date = fields.Datetime('Prediction Date', default=fields.Datetime.now)
    temperature_readings = fields.One2many('temperature.reading', 'prediction_id', string='Temperature Readings')

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('shelf.life.prediction') or '/'
        return super().create(vals)

    @api.depends('initial_shelf_life', 'accumulated_temperature_deviation')
    def _compute_predicted_shelf_life(self):
        for record in self:
            # Simplified Arrhenius equation implementation
            # In real implementation, this would use more sophisticated temperature compensation models
            if record.initial_shelf_life and record.accumulated_temperature_deviation:
                # Simple degradation model - the higher the accumulated deviation, the shorter the shelf life
                degradation_factor = min(record.accumulated_temperature_deviation / 100.0, 0.9)  # Max 90% degradation
                record.predicted_shelf_life = record.initial_shelf_life * (1 - degradation_factor)
            else:
                record.predicted_shelf_life = record.initial_shelf_life

    def update_temperature_reading(self, temperature, timestamp=None):
        """Update with new temperature reading and recalculate shelf life"""
        if timestamp is None:
            timestamp = fields.Datetime.now()

        self.env['temperature.reading'].create({
            'prediction_id': self.id,
            'temperature': temperature,
            'timestamp': timestamp,
            'location_id': self.env.context.get('location_id', False)
        })

        # Update accumulated temperature deviation (simplified calculation)
        # In real implementation, this would integrate temperature over time
        if self.current_temperature:
            deviation = abs(temperature - self.current_temperature)
            self.accumulated_temperature_deviation += deviation

        self.current_temperature = temperature

        # Check if warning threshold is reached
        if self.initial_shelf_life > 0:
            remaining_percentage = (self.predicted_shelf_life / self.initial_shelf_life) * 100
            if remaining_percentage <= self.quality_warning_threshold and not self.is_warning_triggered:
                self._trigger_quality_warning()

    def _trigger_quality_warning(self):
        """Trigger quality warning activity when shelf life drops below threshold"""
        self.is_warning_triggered = True
        # Create activity to prioritize discount promotion
        self.env['mail.activity'].create({
            'res_model_id': self.env.ref('stock.model_stock_lot').id,
            'res_id': self.lot_id.id,
            'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
            'summary': _('Priority Discount Promotion Required'),
            'note': _('Predicted shelf life has dropped below %s%%. Product %s (Lot: %s) requires immediate discount promotion action.') % (
                self.quality_warning_threshold, self.product_id.name, self.lot_id.name
            ),
            'user_id': self.env.user.id,
            'date_deadline': fields.Date.add(fields.Date.today(), days=1),
        })


class TemperatureReading(models.Model):
    """
    温度读数记录 [US-09-07]
    """
    _name = 'temperature.reading'
    _description = 'Temperature Reading for Shelf Life Prediction'
    _order = 'timestamp desc'

    prediction_id = fields.Many2one('shelf.life.prediction', string='Shelf Life Prediction', required=True, ondelete='cascade')
    temperature = fields.Float('Temperature (°C)', required=True)
    timestamp = fields.Datetime('Timestamp', required=True)
    location_id = fields.Many2one('stock.location', string='Location')
    humidity = fields.Float('Humidity (%)')
    notes = fields.Text('Notes')


class PrecoolingProcess(models.Model):
    """
    产后预冷过程追踪 [US-09-08]
    """
    _name = 'precooling.process'
    _description = 'Post-harvest Pre-cooling Process Tracking'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'start_time desc'

    name = fields.Char('Pre-cooling Batch', required=True, default=lambda self: _('New'))
    lot_id = fields.Many2one('stock.lot', string='Harvest Lot', required=True)
    product_id = fields.Many2one('product.product', string='Product', related='lot_id.product_id', store=True)
    initial_temperature = fields.Float('Initial Temperature (°C)', required=True)
    target_temperature = fields.Float('Target Temperature (°C)', required=True)
    cooling_duration_hours = fields.Float('Required Cooling Duration (Hours)', required=True)
    start_time = fields.Datetime('Cooling Start Time')
    end_time = fields.Datetime('Cooling End Time')
    actual_duration_hours = fields.Float('Actual Duration (Hours)', compute='_compute_actual_duration', store=True)
    cooling_status = fields.Selection([
        ('pending', 'Pending'),
        ('cooling', 'Cooling in Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ], string='Cooling Status', default='pending', required=True)
    temperature_readings = fields.One2many('precooling.temperature', 'process_id', string='Temperature Readings')
    cooling_notes = fields.Text('Cooling Notes')
    can_proceed_to_warehouse = fields.Boolean('Can Proceed to Warehouse', compute='_compute_can_proceed', store=True)

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('precooling.process') or '/'
        return super().create(vals)

    @api.depends('start_time', 'end_time')
    def _compute_actual_duration(self):
        for record in self:
            if record.start_time and record.end_time:
                diff = fields.Datetime.from_string(record.end_time) - fields.Datetime.from_string(record.start_time)
                record.actual_duration_hours = diff.total_seconds() / 3600.0
            else:
                record.actual_duration_hours = 0.0

    @api.depends('cooling_status', 'target_temperature', 'temperature_readings')
    def _compute_can_proceed(self):
        for record in self:
            # Can proceed only if cooling is completed and temperature is at or below target
            record.can_proceed_to_warehouse = (
                record.cooling_status == 'completed' and
                record.temperature_readings and
                record.temperature_readings[0].temperature <= record.target_temperature
            )

    def action_start_cooling(self):
        """Start the pre-cooling process"""
        for process in self:
            if process.cooling_status == 'pending':
                process.start_time = fields.Datetime.now()
                process.cooling_status = 'cooling'

    def action_complete_cooling(self):
        """Complete the pre-cooling process"""
        for process in self:
            if process.cooling_status == 'cooling':
                process.end_time = fields.Datetime.now()

                # Check if final temperature is at or below target
                if process.temperature_readings:
                    final_temp = process.temperature_readings[0].temperature
                    if final_temp <= process.target_temperature:
                        process.cooling_status = 'completed'
                    else:
                        process.cooling_status = 'failed'
                        # Add a note about the failure
                        process.cooling_notes = process.cooling_notes or ""
                        process.cooling_notes += f"\nCooling failed: Target {process.target_temperature}°C not reached. Final temp: {final_temp}°C"
                else:
                    process.cooling_status = 'failed'


class PrecoolingTemperature(models.Model):
    """
    预冷温度读数 [US-09-08]
    """
    _name = 'precooling.temperature'
    _description = 'Pre-cooling Temperature Reading'
    _order = 'timestamp desc'

    process_id = fields.Many2one('precooling.process', string='Pre-cooling Process', required=True, ondelete='cascade')
    temperature = fields.Float('Temperature (°C)', required=True)
    timestamp = fields.Datetime('Timestamp', required=True, default=fields.Datetime.now)
    humidity = fields.Float('Humidity (%)')
    notes = fields.Text('Notes')