from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)

class AIAutonomousMissionLogExtension(models.Model):    _inherit = 'ai.autonomous.mission.log'
    
    mission_id = fields.Many2one('farm.robot.mission', string="Dispatched Mission")

class AIAutonomousOrchestratorExtension(models.Model):    _inherit = 'ai.autonomous.orchestrator'

    def _dispatch_remediation_mission(self, twin):
        # The base implementation does nothing if robotics isn't installed.
        # This extension injects the robotics dispatch logic.
        mission_type = 'scout'
        
        robot = self.env['farm.robot'].search([
            ('robot_type', '=', mission_type),
            ('robot_status', '=', 'idle')
        ], limit=1)
        
        if not robot:
            _logger.warning("No idle %s robot available for twin %s", mission_type, twin.name)
            super()._dispatch_remediation_mission(twin)
            return

        task = self.env['project.task'].create({
            'name': _("Autonomous Scouting: %s") % twin.location_id.name,
            'project_id': self.env.ref('farm_operation.project_farm_operations').id,
            'land_parcel_id': twin.location_id.id,
            'description': _("Automatically dispatched by AI Orchestrator due to low health score (%s)") % twin.health_score
        })

        mission = self.env['farm.robot.mission'].create({
            'robot_id': robot.id,
            'task_id': task.id,
            'location_id': twin.location_id.id,
            'state': 'scheduled'
        })

        mission.action_start_mission()

        self.env['ai.autonomous.mission.log'].create({
            'orchestrator_id': self.id,
            'twin_id': twin.id,
            'mission_id': mission.id,
            'status': 'dispatched',
            'detail': _("Dispatched %s robot to address health score of %s") % (mission_type, twin.health_score)
        })

        self.message_post(body=_("L5 AUTO-DISPATCH: Mission %s assigned to Robot %s for Location %s.") % 
                         (mission.name, robot.name, twin.location_id.name))

class A2ANegotiationMessageExtension(models.Model):    _inherit = 'agri.a2a.negotiation'

    def _evaluate_proposal_logic(self, incoming_payload):
        if self.receiver_agent_id and self.receiver_agent_id.startswith('robot:'):
            robot = self.env['farm.robot'].search([('agent_id', '=', self.receiver_agent_id)], limit=1)
            if robot:
                return robot.evaluate_a2a_proposal(incoming_payload)
        return super()._evaluate_proposal_logic(incoming_payload)
