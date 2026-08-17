from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class AgriSwarmCoord(models.Model):
    _name = 'agri.swarm.coord'
    _description = 'Swarm Robotics Coordination'

    name = fields.Char('Reference')
    workorder_id = fields.Many2one('mrp.workorder', string='Workorder')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('ready', 'Ready'),
        ('progress', 'In Progress'),
        ('done', 'Done'),
        ('canceled', 'Canceled')
    ], string='State', default='draft')

    # US-133-01
    speed_alpha = fields.Float('Speed Alpha (mm/s)')
    coordinates_beta = fields.Float('Coordinates Beta (distance in m)')
    is_clear = fields.Boolean('Is Clear', default=True)
    target_speed = fields.Float('Target Speed (mm/s)')

    # US-133-02
    gps_coordinates = fields.Char('GPS Coordinates / SOM Zone')
    nozzle_flow_rate = fields.Float('Nozzle Flow Rate (%)')

    # US-133-03
    sensor_status = fields.Selection([
        ('online', 'Online'),
        ('offline', 'Offline')
    ], string='Sensor Status', default='online')
    safe_mode = fields.Boolean('Safe Mode', default=False)

    # US-133-04 & US-133-06
    is_active = fields.Boolean('Is Active', default=False)
    obstacle_distance = fields.Float('Obstacle Distance (m)')
    is_solenoid_closed = fields.Boolean('Is Solenoid Closed', default=False)

    # US-133-05
    wind_limit = fields.Float('Wind Limit (m/s)')
    wind_speed = fields.Float('Wind Speed (m/s)')
    
    # US-133-06
    coordination_state = fields.Selection([
        ('optimal', 'Optimal'),
        ('degraded', 'Degraded')
    ], string='Coordination State', default='optimal')
    bypass_active = fields.Boolean('Bypass Active', default=False)
    
    # US-133-07
    obstacle_proximity = fields.Float('Obstacle Proximity (m)')

    def write(self, vals):
        for record in self:
            # US-133-01
            if 'coordinates_beta' in vals:
                if vals['coordinates_beta'] <= 1.2:
                    vals['is_clear'] = False
                    vals['target_speed'] = 0.0

            # US-133-02
            if 'gps_coordinates' in vals:
                if vals['gps_coordinates'] == 'Low-SOM':
                    vals['nozzle_flow_rate'] = 85.0

            # US-133-03
            if 'sensor_status' in vals:
                if vals['sensor_status'] == 'offline':
                    vals['safe_mode'] = True

            # US-133-04 and US-133-06
            if 'obstacle_distance' in vals:
                if vals['obstacle_distance'] <= 2.5:
                    vals['is_solenoid_closed'] = True
                
                if vals['obstacle_distance'] == 4.5 and record.coordination_state == 'optimal':
                    vals['bypass_active'] = True
                    
            # US-133-05
            if 'wind_speed' in vals:
                wind_limit = record.wind_limit if not 'wind_limit' in vals else vals['wind_limit']
                if vals['wind_speed'] > wind_limit:
                    vals['state'] = 'canceled'
                    raise ValidationError(_("Wind speed exceeds safety limits for swarm spray mission"))

            # US-133-07
            if 'obstacle_proximity' in vals:
                if vals['obstacle_proximity'] < 3.0:
                    vals['target_speed'] = max(0.0, record.target_speed - 50.0) # scaling down
                    raise ValidationError(_("OBSTACLE_DETECTED_MISSION_PAUSED"))

        return super().write(vals)
