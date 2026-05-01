# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class AgriPrecisionMixin(models.AbstractModel):
    """
    [Level 0 DNA] Bridge for Precision Manufacturing & Agriculture.
    Handles uncertainty, grading, and reactive intervention.
    Enhanced with IoT integration capabilities.
    """
    _name = 'agri.precision.mixin'
    _description = 'Precision & Agri Bridge DNA'

    # 1. Uncertainty: Dynamic Yield Tracking
    expected_yield_accuracy = fields.Float("Yield Confidence (%)", default=100.0)
    last_metrology_date = fields.Datetime("Last Calibration/Sampling")

    # 2. Grading: Binning Attributes
    quality_grade = fields.Selection([
        ('premium', 'Premium / Grade A'),
        ('standard', 'Standard / Grade B'),
        ('substandard', 'Substandard / Fail')
    ], string="Precision Grade", default='standard')

    # 3. Intervention: Skill Hooks
    intervention_count = fields.Integer("Intervention Cycles", default=0)
    is_critical_status = fields.Boolean("Critical Condition", default=False)

    # 4. IoT Integration: Sensor and Device Tracking
    iot_device_ids = fields.Many2many(
        'iiot.device',
        string='IoT Devices',
        help='IoT devices associated with this record for environmental monitoring'
    )
    iot_status = fields.Selection([
        ('normal', 'Normal'),
        ('monitoring', 'Monitoring'),
        ('warning', 'Warning'),
        ('critical', 'Critical')
    ], string="IoT Status", default='normal')

    def get_environmental_readings(self):
        """Get environmental readings from associated IoT devices"""
        self.ensure_one()
        if hasattr(self, 'iot_device_ids') and self.iot_device_ids:
            return self.env['iiot.telemetry'].search([
                ('device_id', 'in', self.iot_device_ids.ids)
            ], order='read_datetime desc', limit=10)  # Last 10 readings
        else:
            return self.env['iiot.telemetry'].browse()

    def action_apply_corrective_skill(self, action_name, params):
        """ [Skill-Style] Generic reactive intervention logic. """
        self.ensure_one()
        self.intervention_count += 1
        self.message_post(body=_("INTERVENTION [%s] applied with parameters: %s") % (action_name, params))
        return True

    def action_trigger_iot_based_intervention(self, sensor_readings_summary):
        """
        Trigger intervention based on IoT sensor readings
        """
        self.ensure_one()

        # Create precision intervention record if the module is available
        if 'precision.intervention' in self.env:
            intervention_description = f"Auto-triggered due to sensor readings: {sensor_readings_summary}"
            intervention = self.env['precision.intervention'].create({
                'name': f"Auto-Intervention from IoT",
                'intervention_type': 'auto',
                'description': intervention_description,
                'status': 'open'
            })

            # Set critical status if needed
            if any(keyword in sensor_readings_summary.lower() for keyword in ['critical', 'deviation', 'error', 'emergency']):
                self.is_critical_status = True
                self.iot_status = 'critical'
            elif any(keyword in sensor_readings_summary.lower() for keyword in ['warning', 'alert', 'high', 'low']):
                self.iot_status = 'warning'
            else:
                self.iot_status = 'monitoring'

            self.message_post(body=_("IoT-Based Intervention Triggered: %s") % intervention_description)
            return intervention

        return False
