from odoo import models, fields, api, _

class FarmServiceTeam(models.Model):
    _name = 'farm.service.team'
    _description = 'Agri-Service Team'

    name = fields.Char("Team Name", required=True)
    leader_id = fields.Many2one('hr.employee', string="Team Leader")
    member_ids = fields.Many2many('hr.employee', 'farm_service_team_hr_employee_rel', 'team_id', 'employee_id', string="Team Members")
    equipment_ids = fields.Many2many('maintenance.equipment', 'farm_service_team_maintenance_equipment_rel', 'team_id', 'equipment_id', string="Specialized Equipment")

class ProjectTask(models.Model):
    _inherit = 'project.task'

    service_team_id = fields.Many2one('farm.service.team', string="Dispatched Service Team")

    def action_dispatch_service_team(self, team_id):
        """
        [US-SCENARIO-27] Mobile Agri-Service Teams
        Dispatches a specialized mobile team to handle a complex task (e.g., Drone Spraying)
        for a smallholder. Automatically assigns the team members and tracks their equipment.
        """
        self.ensure_one()
        team = self.env['farm.service.team'].browse(team_id)
        if not team:
            return False
            
        self.service_team_id = team.id
        # Assign all team members to the task
        self.user_ids = [(6, 0, team.member_ids.mapped('user_id').ids)]
        
        # Log the equipment dispatched
        eq_names = ", ".join(team.equipment_ids.mapped('name'))
        self.message_post(body=_("Dispatched Service Team '%s' with equipment: %s") % (team.name, eq_names))
        
        return True

