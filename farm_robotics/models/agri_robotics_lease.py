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

    def action_request_lease(self):
        """ Check if any other lease is currently active on the resource, otherwise queue it """
        self.ensure_one()
        active_lease = self.search([
            ('res_model', '=', self.res_model),
            ('res_id', '=', self.res_id),
            ('state', '=', 'active')
        ], limit=1)
        
        if active_lease:
            self.write({'state': 'queued'})
        else:
            self.write({'state': 'active'})

    def action_release(self):
        """ Release lease and wake up next queued lease in order of creation """
        for lease in self:
            if lease.state not in ['active', 'queued']:
                continue
            lease.write({'state': 'released'})
            
            # Atomic Wakeup Chain
            next_lease = self.search([
                ('res_model', '=', lease.res_model),
                ('res_id', '=', lease.res_id),
                ('state', '=', 'queued')
            ], order='create_date asc', limit=1)
            
            if next_lease:
                next_lease.write({'state': 'active'})

    @api.model
    def _cron_check_expired_leases(self):
        """ Find active leases that are expired, force set to 'expired' and wake up queue """
        expired_leases = self.search([
            ('state', '=', 'active'),
            ('expiration_date', '<', fields.Datetime.now())
        ])
        for lease in expired_leases:
            lease.write({'state': 'expired'})
            
            # Atomic Wakeup Chain
            next_lease = self.search([
                ('res_model', '=', lease.res_model),
                ('res_id', '=', lease.res_id),
                ('state', '=', 'queued')
            ], order='create_date asc', limit=1)
            
            if next_lease:
                next_lease.write({'state': 'active'})
