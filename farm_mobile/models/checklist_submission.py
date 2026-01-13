from odoo import models, fields, api, _
from odoo.exceptions import UserError

class FarmChecklistSubmission(models.Model):
    """
    US-26-03: 记录每一次设备启动前的实际点检结果
    """
    _name = 'farm.checklist.submission'
    _description = 'Equipment Checklist Submission'
    _inherit = ['mail.thread']

    name = fields.Char("Submission ID", readonly=True, default=lambda self: _('New'))
    equipment_id = fields.Many2one('maintenance.equipment', string="Equipment", required=True)
    task_id = fields.Many2one('mrp.production', string="Assigned Intervention")
    worker_id = fields.Many2one('hr.employee', string="Performed By", default=lambda self: self.env.user.employee_id)
    
    submission_date = fields.Datetime("Time", default=fields.Datetime.now)
    line_ids = fields.One2many('farm.checklist.submission.line', 'submission_id', string="Details")
    
    state = fields.Selection([
        ('pass', 'Pass'),
        ('fail', 'Fail')
    ], string="Result", compute='_compute_state', store=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('farm.checklist.submission') or _('SUB')
        return super().create(vals_list)

    @api.depends('line_ids.is_checked')
    def _compute_state(self):
        for rec in self:
            if all(line.is_checked for line in rec.line_ids):
                rec.state = 'pass'
            else:
                rec.state = 'fail'

class FarmChecklistSubmissionLine(models.Model):
    _name = 'farm.checklist.submission.line'
    _description = 'Checklist Submission Line'

    submission_id = fields.Many2one('farm.checklist.submission', ondelete='cascade')
    requirement_id = fields.Many2one('farm.equipment.checklist.line', string="Check Item")
    name = fields.Char(related='requirement_id.name')
    is_checked = fields.Boolean("Confirmed", default=False)
    evidence_photo = fields.Binary("Photo Proof", attachment=True)
