from odoo import models, fields, api, _
import logging
import json

_logger = logging.getLogger(__name__)

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
    workflow_id = fields.Many2one('ai.agent.workflow', string="Decision Workflow", 
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
