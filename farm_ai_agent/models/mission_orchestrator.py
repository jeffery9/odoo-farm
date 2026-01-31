from odoo import models, fields, api, _
import logging
import json
import uuid

_logger = logging.getLogger(__name__)

class AgriMissionOrchestrator(models.Model):
    """
    Level 4: Mission Orchestrator (Autonomous Coordination).
    Orchestrates complex A2A workflows including bargaining, execution, and clearing. [US-62-2026]
    """
    _name = 'agri.mission.orchestrator'
    _description = 'Agricultural Mission Orchestrator'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Mission ID", required=True, default=lambda self: _('New'))
    active = fields.Boolean(default=True)
    
    mission_type = fields.Selection([
        ('harvest_clearing', 'Harvest & Value Clearing'),
        ('input_calibration', 'Input Feedback & Actuation'),
        ('neighborhood_support', 'Neighborhood Service Exchange')
    ], string="Mission Type", required=True)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('scouting', 'Discovery (Scouting)'),
        ('bargaining', 'Bargaining'),
        ('executing', 'Executing'),
        ('clearing', 'Value Clearing'),
        ('done', 'Completed'),
        ('failed', 'Mission Failed')
    ], default='draft', tracking=True)

    # Context Data
    target_location_id = fields.Many2one('farm.location', string="Target Field")
    spatial_grid_id = fields.Char(related='target_location_id.spatial_grid_id', store=True)
    
    # Linked Objects
    step_ids = fields.One2many('agri.mission.step', 'orchestrator_id', string="Mission Steps")
    negotiation_ids = fields.One2many('agri.a2a.negotiation', 'orchestrator_id', string="A2A Negotiations")

    def action_start_mission(self):
        """
        Triggers Step 1: Discovery.
        Uses GeoSpatialMixin context to find nearby agents.
        """
        self.ensure_one()
        self.state = 'scouting'
        
        # Discover neighbors via registry
        neighbors = self.env['agri.neighborhood.registry'].get_neighbors(self.spatial_grid_id)
        if not neighbors:
            self.message_post(body=_("Mission Scouting: No nearby agents found in grid %s.") % self.spatial_grid_id)
        else:
            self.message_post(body=_("Mission Scouting: Found %d potential community agents.") % len(neighbors))
            if self.mission_type in ['neighborhood_support', 'input_calibration', 'harvest_clearing']:
                self.state = 'bargaining'
        return True

    def action_trigger_inflow_mission(self, location, nutrient_gap):
        """
        [Level 4+: Auto-Trigger]
        Starts a resource inflow mission based on nutrient deficiency.
        """
        mission = self.create({
            'name': _("Auto-Inflow: %s") % location.name,
            'mission_type': 'input_calibration',
            'target_location_id': location.id,
        })
        mission.message_post(body=_("Mission Triggered: Nutrient gap detected (%s). Starting A2A resource scouting.") % nutrient_gap)
        mission.action_start_mission()
        return mission

    def action_trigger_harvest_mission(self, location, maturity_info):
        """
        [Level 4+: Auto-Trigger]
        Starts a harvest mission based on AI maturity prediction.
        """
        mission = self.create({
            'name': _("Auto-Harvest: %s") % location.name,
            'mission_type': 'harvest_clearing',
            'target_location_id': location.id,
        })
        mission.message_post(body=_("Mission Triggered: Harvest maturity reached (%s). Starting A2A harvesting coordination.") % maturity_info)
        mission.action_start_mission()
        return mission

    def action_next_step(self):
        """Advances the state machine based on step completion."""
        self.ensure_one()
        # Logic to transition based on AgriIntervention or A2A message results
        if self.state == 'bargaining' and any(n.state == 'accepted' for n in self.negotiation_ids):
            self.state = 'executing'
        return True

class AgriMissionStep(models.Model):
    """Atomic steps within an AI Mission."""
    _name = 'agri.mission.step'
    _description = 'Mission Step'
    _order = 'sequence'

    orchestrator_id = fields.Many2one('agri.mission.orchestrator', ondelete='cascade')
    sequence = fields.Integer("Sequence", default=10)
    name = fields.Char("Step Name", required=True)
    
    step_type = fields.Selection([
        ('negotiation', 'A2A Negotiation'),
        ('intervention', 'Physical Intervention'),
        ('audit', 'Evidence Audit'),
        ('clearing', 'Value Clearing')
    ], string="Type")
    
    state = fields.Selection([('pending', 'Pending'), ('progress', 'In Progress'), ('done', 'Done')], default='pending')
    
    res_reference = fields.Reference(
        selection=[('agri.a2a.negotiation', 'Negotiation'), ('mrp.production', 'Intervention')],
        string="Linked Process"
    )

# --- Original Level 5 Logic (Preserved for Lossless Mode) ---

class AIAutonomousOrchestrator(models.Model):
    """
    L5: Autonomous Mission Orchestrator.
    Connects L3 Decisions (Biological Twin) to L5 Execution (Robot Fleet).
    """
    _name = 'ai.autonomous.orchestrator'
    _description = 'AI Autonomous Mission Dispatcher'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Orchestrator Name", required=True)
    active = fields.Boolean(default=True)
    
    # Strategy Configuration
    workflow_id = fields.Many2one('agri.ai.agent.workflow', string="Decision Workflow", 
                                 help="The AI workflow used to decide on actions.")
    
    auto_dispatch_threshold = fields.Float("Auto-Dispatch Threshold (Health)", default=60.0,
                                          help="Automatically dispatch missions when biological twin health score falls below this.")

    # Execution Logs
    log_ids = fields.One2many('ai.autonomous.mission.log', 'orchestrator_id', string="Dispatch Logs")

    def action_run_autonomous_scan(self):
        """
        L5 Cycle: Scan -> Decide -> Dispatch.
        Runs through all active biological twins.
        """
        twins = self.env['farm.biological.twin'].search([])
        for twin in twins:
            if twin.health_score < self.auto_dispatch_threshold:
                self._dispatch_remediation_mission(twin)

    def _dispatch_remediation_mission(self, twin):
        """
        Decision & Execution Logic for L5.
        """
        # 1. Decision: Select Mission Type
        # (Simplified: If NDVI is low, send a Scout Drone first)
        mission_type = 'scout'
        
        # 2. Resource Allocation: Find an Idle Robot
        robot = self.env['farm.robot'].search([
            ('robot_type', '=', mission_type),
            ('robot_status', '=', 'idle')
        ], limit=1)
        
        if not robot:
            _logger.warning("No idle %s robot available for twin %s", mission_type, twin.name)
            return

        # 3. Execution: Create Farm Task & Robot Mission
        # Create Operation Task
        task = self.env['project.task'].create({
            'name': _("Autonomous Scouting: %s") % twin.location_id.name,
            'project_id': self.env.ref('farm_operation.project_farm_operations').id,
            'land_parcel_id': twin.location_id.id,
            'description': _("Automatically dispatched by AI Orchestrator due to low health score (%s)") % twin.health_score
        })

        # Create Robot Mission
        mission = self.env['farm.robot.mission'].create({
            'robot_id': robot.id,
            'task_id': task.id,
            'location_id': twin.location_id.id,
            'state': 'scheduled'
        })

        # 4. Dispatch: Start Mission
        mission.action_start_mission()

        # Log entry
        self.env['ai.autonomous.mission.log'].create({
            'orchestrator_id': self.id,
            'twin_id': twin.id,
            'mission_id': mission.id,
            'status': 'dispatched',
            'detail': _("Dispatched %s robot to address health score of %s") % (mission_type, twin.health_score)
        })

        self.message_post(body=_("L5 AUTO-DISPATCH: Mission %s assigned to Robot %s for Location %s.") % 
                         (mission.name, robot.name, twin.location_id.name))

class AIAutonomousMissionLog(models.Model):
    _name = 'ai.autonomous.mission.log'
    _description = 'AI Dispatch Log'
    _order = 'create_date desc'

    orchestrator_id = fields.Many2one('ai.autonomous.orchestrator', ondelete='cascade')
    twin_id = fields.Many2one('farm.biological.twin', string="Source Twin")
    mission_id = fields.Many2one('farm.robot.mission', string="Dispatched Mission")
    status = fields.Selection([('dispatched', 'Dispatched'), ('failed', 'Resource Unavailable')], string="Status")
    detail = fields.Text("Details")

# --- End of Original Level 5 Logic ---

# Add many2one backlink to Negotiation
class A2ANegotiationInherit(models.Model):
    _inherit = 'agri.a2a.negotiation'
    orchestrator_id = fields.Many2one('agri.mission.orchestrator', string="Mission Orchestrator")
