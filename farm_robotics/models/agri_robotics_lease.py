# -*- coding: utf-8 -*-
# filepath: odoo-farm-dev/farm_robotics/models/agri_robotics_lease.py
from odoo import models, fields, api, _

class AgriRoboticsLease(models.Model):
    _name = 'agri.robotics.lease'
    _description = 'Robotics Generic Resource Lease Lock'
    _order = 'create_date asc'

    name = fields.Char('Reference (租约参考号)', required=True, default=lambda self: _('New'))
    res_model = fields.Char('Resource Model (资源模型)', required=True, index=True)
    res_id = fields.Integer('Resource ID (资源 ID)', required=True, index=True)
    robot_id = fields.Many2one('farm.robot', string='Robot (机器人/智能体)', required=True)
    mission_id = fields.Many2one('farm.robot.mission', string='Associated Mission (关联任务单)')
    start_date = fields.Datetime('Start Date (开始时间)', default=fields.Datetime.now, required=True)
    expiration_date = fields.Datetime('Expiration Date (过期时间)', required=True)
    state = fields.Selection([
        ('draft', 'Draft (草稿)'),
        ('active', 'Active (已激活)'),
        ('queued', 'Queued (排队中)'),
        ('released', 'Released (已释放)'),
        ('expired', 'Expired (已到期)')
    ], string='Lease State', default='draft', required=True, index=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('agri.robotics.lease') or _('LEA')
        return super().create(vals_list)
