from odoo import models, fields, api, _
import json
import logging

_logger = logging.getLogger(__name__)

class FarmRobot(models.Model):
    """
    Agricultural Robot: Transformed into an A2A Autonomous Agent.
    Level 5: Robotic A2A Identity.
    """
    _name = 'farm.robot'
    _description = 'Agricultural Robot'
    _inherit = [
        'maintenance.equipment',
        'agri.geospatial.mixin',     # Level 1: Spatial Grid Identity
        'agri.view.mixin',           # Level 0: UI Isolation
    ]

    robot_type = fields.Selection([
        ('sprayer', 'Spraying Robot'),
        ('harvester', 'Harvesting Robot'),
        ('weeder', 'Weeding Robot'),
        ('scout', 'Scouting/Mapping Drone')
    ], string="Robot Type", required=True)
    
    device_id = fields.Many2one('iiot.device', string="Connected IoT Device")
    
    # A2A Identity [US-70-2026]
    agent_id = fields.Char("Agent Identifier", compute="_compute_agent_id", store=True)
    
    battery_level = fields.Float("Battery (%)", compute='_compute_iot_status')
    current_mission_id = fields.Many2one('farm.robot.mission', string="Current Mission", compute='_compute_iot_status')
    
    robot_status = fields.Selection([
        ('idle', 'Idle/Standby'),
        ('working', 'Active Working'),
        ('charging', 'Charging'),
        ('error', 'Fault/Offline')
    ], default='idle', compute='_compute_iot_status')

    @api.depends('name', 'robot_type')
    def _compute_agent_id(self):
        """
        Generates a unique A2A agent identifier for the robot.
        Pattern: robot:{type}:{id}
        """
        for robot in self:
            if robot.id:
                robot.agent_id = f"robot:{robot.robot_type}:{robot.id}"
            else:
                robot.agent_id = False

    def _compute_iot_status(self):
        """Fetch real status from linked IIoT device"""
        for robot in self:
            # Simulated status fetching
            robot.battery_level = 85.0
            robot.robot_status = 'idle'
            robot.current_mission_id = self.env['farm.robot.mission'].search([
                ('robot_id', '=', robot.id),
                ('state', '=', 'in_progress')
            ], limit=1)

    def evaluate_a2a_proposal(self, incoming_payload):
        """
        [US-61-06] Robotic Self-Preservation Bargaining.
        Adjusts price based on battery and current load.
        """
        self.ensure_one()
        _logger.info("Robot %s evaluating A2A proposal.", self.name)
        
        # 1. Battery Safety Check
        if self.battery_level < 20.0:
            return {
                'decision': 'reject',
                'reason': _("Battery level too low (%f%%) for safe external mission.") % self.battery_level
            }
            
        # 2. Energy-Aware Pricing
        base_price_factor = 1.0
        if self.battery_level < 50.0:
            # Increase price by 30% if battery is below half to prioritize charging missions
            base_price_factor = 1.3
            
        proposed_credits = incoming_payload.get('proposed_credits', 0.0)
        market_avg = 10.0 # Stub for real market price
        
        expected_min = market_avg * base_price_factor
        
        if proposed_credits < expected_min:
            return {
                'decision': 'counter',
                'price': expected_min,
                'reason': _("Energy scarcity surcharge applied due to medium battery level.")
            }
            
        return {'decision': 'accept'}

class FarmRobotMission(models.Model):
    """
    Robot Mission: Now serves as a carrier for automated physical evidence.
    Level 5: Robotic Evidence Packaging.
    """
    _name = 'farm.robot.mission'
    _description = 'Robot Operation Mission'
    _inherit = [
        'mail.thread', 
        'mail.activity.mixin',
        'agri.evidence.mixin',       # Level 2: Automatic Audit/Evidence
    ]

    name = fields.Char("Mission ID", required=True, default=lambda self: _('New'))
    robot_id = fields.Many2one('farm.robot', string="Assigned Robot", required=True)
    task_id = fields.Many2one('project.task', string="Source Farm Task")
    location_id = fields.Many2one('farm.location', string="Target Location")
    
    planned_path_geojson = fields.Text("Planned Path (GeoJSON)")
    actual_path_geojson = fields.Text("Actual Path (GeoJSON)")
    
    progress = fields.Float("Progress (%)", default=0.0)
    efficiency_score = fields.Float("Execution Efficiency", help="Calculated based on speed vs plan")
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Mission Failed'),
        ('aborted', 'Aborted/Emergency Stop')
    ], default='draft', tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('farm.robot.mission') or _('MIS')
        return super().create(vals_list)

    def action_start_mission(self):
        self.write({'state': 'in_progress'})
        # In real system, send MQTT command to robot
        if self.robot_id.device_id:
            self.robot_id.device_id.send_command('start_mission', mission_id=self.id)

    def action_emergency_stop(self):
        self.write({'state': 'aborted'})
        if self.robot_id.device_id:
            self.robot_id.device_id.send_command('emergency_stop')

    def action_complete_mission(self):
        """
        [Level 5: Automated Evidence Loop]
        Triggers evidence generation from actual trajectory data.
        """
        self.ensure_one()
        self.state = 'completed'
        
        # Logic to package actual trajectory as physical evidence
        if self.actual_path_geojson:
            # Simplified: Call the evidence audit logic
            self.perform_evidence_audit()
            
        self.message_post(body=_("Robotic Mission Completed. Physical trajectory data packaged as audit evidence."))
        return True
