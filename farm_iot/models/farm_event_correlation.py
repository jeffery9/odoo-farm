# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.tools.safe_eval import safe_eval
from datetime import timedelta
import logging

_logger = logging.getLogger(__name__)

class FarmEventCorrelation(models.Model):
    _name = 'farm.event.correlation'
    _description = 'Farm IoT Event Correlation (Business Logic)'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Correlation Name', required=True)
    active = fields.Boolean(default=True)
    
    rule_type = fields.Selection([
        ('all', 'All Conditions (AND)'),
        ('any', 'Any Condition (OR)')
    ], string='Logic Type', default='all', required=True)
    
    time_window = fields.Integer(
        'Time Window (seconds)', 
        default=300, 
        help="How far back to look for matching events"
    )
    
    condition_ids = fields.One2many(
        'farm.event.correlation.condition', 
        'correlation_id', 
        string='Conditions'
    )
    
    action_type = fields.Selection([
        ('activity', 'Create Activity'),
        ('notification', 'Internal Notification'),
        ('webhook', 'External Webhook'),
        ('method', 'Execute Method')
    ], string='Action Type', default='activity')
    
    # Action Config
    target_model_id = fields.Many2one('ir.model', string='Target Model')
    method_name = fields.Char('Method Name')
    webhook_url = fields.Char('Webhook URL')
    message_template = fields.Text('Message Template', default="Correlation detected: {{ name }}")

    def evaluate_telemetry(self, new_telemetry):
        """
        Check if the incoming telemetry triggers this correlation
        """
        self.ensure_one()
        if not self.condition_ids:
            return False

        # 1. Gather relevant telemetries within the time window
        start_time = fields.Datetime.now() - timedelta(seconds=self.time_window)
        
        # We need to know which sensor types we are interested in
        interested_types = self.condition_ids.mapped('sensor_type')
        
        # Optimization: Only search if the new telemetry is of an interested type
        if new_telemetry.sensor_type not in interested_types:
            return False

        # Find recent telemetries for these types
        recent_telemetries = self.env['iiot.telemetry'].search([
            ('sensor_type', 'in', interested_types),
            ('timestamp', '>=', start_time)
        ], order='timestamp desc')

        # Group by type to get the latest value for each
        latest_values = {}
        for t in recent_telemetries:
            if t.sensor_type not in latest_values:
                latest_values[t.sensor_type] = t.value

        # 2. Evaluate conditions
        condition_results = []
        for condition in self.condition_ids:
            val = latest_values.get(condition.sensor_type)
            if val is None:
                condition_results.append(False)
                continue
            
            res = condition.evaluate(val)
            condition_results.append(res)

        # 3. Apply logic
        triggered = False
        if self.rule_type == 'all':
            triggered = all(condition_results)
        else:
            triggered = any(condition_results)

        if triggered:
            self._trigger_action(new_telemetry, latest_values)
            return True
        
        return False

    def _trigger_action(self, telemetry, values):
        """Execute the configured action"""
        _logger.info(f"Farm Correlation Triggered: {self.name} by device {telemetry.device_id.name}")
        
        msg = self.message_template.replace('{{ name }}', self.name)
        for s_type, val in values.items():
            msg = msg.replace(f'{{{{ {s_type} }}}}', str(val))

        if self.action_type == 'activity':
            # Create activity on the device
            self.env['mail.activity'].create({
                'res_id': telemetry.device_id.id,
                'res_model_id': self.env['ir.model']._get('iiot.device').id,
                'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                'summary': self.name,
                'note': msg,
                'user_id': self.env.user.id,
            })
        
        elif self.action_type == 'notification':
            # Post message to device chatter
            telemetry.device_id.message_post(body=msg, message_type='notification')

        elif self.action_type == 'method' and self.target_model_id and self.method_name:
            # Attempt to call method on target model
            # This is a placeholder for more complex logic
            pass

class FarmEventCorrelationCondition(models.Model):
    _name = 'farm.event.correlation.condition'
    _description = 'Farm IoT Event Correlation Condition'

    correlation_id = fields.Many2one('farm.event.correlation', ondelete='cascade')
    sensor_type = fields.Selection([
        ('temperature', 'Temperature'),
        ('ph', 'pH Level'),
        ('dissolved_oxygen', 'Dissolved Oxygen'),
        ('humidity', 'Humidity'),
        ('soil_moisture', 'Soil Moisture'),
        ('flight_altitude', 'Flight Altitude'),
        ('chemical_level', 'Chemical Level'),
        ('battery_voltage', 'Drone Battery'),
        ('micro_sensor', 'Urban Micro-sensor')
    ], string="Sensor Type", required=True)
    
    operator = fields.Selection([
        ('==', '='),
        ('!=', '!='),
        ('>', '>'),
        ('<', '<'),
        ('>=', '>='),
        ('<=', '<=')
    ], string='Operator', default='>', required=True)
    
    threshold = fields.Float('Threshold', required=True)

    def evaluate(self, value):
        self.ensure_one()
        if self.operator == '==': return value == self.threshold
        if self.operator == '!=': return value != self.threshold
        if self.operator == '>': return value > self.threshold
        if self.operator == '<': return value < self.threshold
        if self.operator == '>=': return value >= self.threshold
        if self.operator == '<=': return value <= self.threshold
        return False
