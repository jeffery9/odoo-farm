from odoo import models, fields, api, _
import json

class FarmRobot(models.Model):
    _name = 'farm.robot'
    _description = 'Agricultural Robot'
    _inherit = ['maintenance.equipment']

    robot_type = fields.Selection([
        ('sprayer', 'Spraying Robot'),
        ('harvester', 'Harvesting Robot'),
        ('weeder', 'Weeding Robot'),
        ('scout', 'Scouting/Mapping Drone')
    ], string="Robot Type", required=True)
    
    device_id = fields.Many2one('iiot.device', string="Connected IoT Device")
    
    battery_level = fields.Float("Battery (%)", compute='_compute_iot_status')
    current_mission_id = fields.Many2one('farm.robot.mission', string="Current Mission", compute='_compute_iot_status')
    
    robot_status = fields.Selection([
        ('idle', 'Idle/Standby'),
        ('working', 'Active Working'),
        ('charging', 'Charging'),
        ('error', 'Fault/Offline')
    ], default='idle', compute='_compute_iot_status')

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

class FarmRobotMission(models.Model):
    _name = 'farm.robot.mission'
    _description = 'Robot Operation Mission'
    _inherit = ['mail.thread', 'mail.activity.mixin']

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
