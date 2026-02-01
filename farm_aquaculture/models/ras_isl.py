# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging
import json

_logger = logging.getLogger(__name__)

class FarmAquacultureLSS(models.Model):
    """
    [ISL Layer] Life Support System (LSS) Unit.
    Proxies mrp.workcenter to manage pumps, filters, and UV systems.
    """
    _name = 'farm.aquaculture.lss'
    _description = 'Life Support System Unit'
    _inherits = {'mrp.workcenter': 'workcenter_id'}
    _inherit = ['agri.resource.consumption.mixin']

    workcenter_id = fields.Many2one('mrp.workcenter', required=True, ondelete='cascade')

    lss_type = fields.Selection([
        ('biofilter', 'Biological Filter'),
        ('drum_filter', 'Mechanical Drum Filter'),
        ('uv_sterilizer', 'UV Sterilization'),
        ('chiller', 'Temperature Control Unit'),
        ('ozone', 'Ozone Generator')
    ], string="System Type", required=True)

    # Component Lifecycle [US-122-01]
    last_service_date = fields.Date("Last Maintenance")
    uv_bulb_hours = fields.Integer("UV Bulb Hours")
    filter_backwash_frequency = fields.Integer("Backwash Frequency (Daily)")

class FarmRasProduction(models.Model):
    """
    [ISL Layer] RAS Culture Batch Order.
    Extends base aquaculture with precise energy and waste tracking.
    """
    _name = 'farm.ras.production'
    _description = 'RAS Culture Order'
    _inherits = {'mrp.production': 'production_id'}
    _inherit = [
        'farm.agri.production.mixin',
        'agri.quality.gate.mixin',
        'agri.agent.instruction.mixin'
    ]

    production_id = fields.Many2one('mrp.production', string='Base Order', required=True, ondelete='cascade')

    # [US-122-02] Metabolic Load Tracking
    predicted_ammonia_load = fields.Float("Predicted TAN Load (mg/L)", compute='_compute_metabolic_waste')
    total_energy_kwh = fields.Float("Total Energy Used (kWh)", related='electricity_consumed_kwh')

    @api.depends('production_id.move_raw_ids.product_uom_qty')
    def _compute_metabolic_waste(self):
        """ Calculates ammonia load based on feed protein content. """
        for rec in self:
            total_feed = sum(rec.production_id.move_raw_ids.mapped('product_uom_qty'))
            # Simplified formula: 1kg feed (40% protein) -> ~30g TAN
            rec.predicted_ammonia_load = total_feed * 0.03

    def handle_lss_telemetry(self, data):
        """ 
        [Authoring-Style: On Damaged] 
        Active defense for LSS failure. 
        """
        self.ensure_one()
        pump_status = data.get('pump_current')
        flow_rate = data.get('flow_rate')
        
        if flow_rate and flow_rate < 5.0: # m3/h redline
            # 1. Alert (Level 2 DNA)
            self.report_incident('critical', 'LSS Flow Failure', 
                                _("CRITICAL: RAS Unit %s flow dropped below safety limit!") % self.name)
            # 2. Skill: Survival Mode (Level 4 DNA)
            self.apply_survival_mode_skill()
        return True

    def apply_survival_mode_skill(self):
        """ Level 4 DNA: Shut down non-essential systems and maximize oxygen. """
        self.ensure_one()
        payload = {
            'action': 'emergency_survival',
            'aeration': 'max',
            'feeding_auto': 'off',
            'priority': 'critical'
        }
        self.agent_instruction_json = json.dumps(payload, indent=2)
        self.agent_status_feedback = 'executing'
        _logger.error("RAS SURVIVAL SKILL: Emergency protocol activated for %s", self.name)

    def action_confirm(self):
        """ Check biofilter health before confirming a new high-density batch. """
        self.validate_quality_gate()
        return super(FarmRasProduction, self).action_confirm()
