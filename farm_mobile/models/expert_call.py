from odoo import models, fields, api, _

class FarmExpertCall(models.Model):
    """
    US-26-05: 远程专家实时连线记录
    """
    _name = 'farm.expert.call'
    _description = 'Remote Expert Consultation Call'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'start_time desc'

    name = fields.Char("Call ID", readonly=True, default=lambda self: _('New'))
    intervention_id = fields.Many2one('mrp.production', string="Related Intervention", required=True)
    expert_id = fields.Many2one('res.users', string="Expert/Support")
    worker_id = fields.Many2one('hr.employee', string="Field Worker", default=lambda self: self.env.user.employee_id)
    
    start_time = fields.Datetime("Start Time", default=fields.Datetime.now)
    end_time = fields.Datetime("End Time")
    duration = fields.Integer("Duration (seconds)", compute='_compute_duration', store=True)
    
    call_type = fields.Selection([
        ('video', 'Video Call'),
        ('audio', 'Audio Call'),
        ('chat', 'Chat/Messages')
    ], string="Call Type", default='video')
    
    status = fields.Selection([
        ('missed', 'Missed'),
        ('completed', 'Completed'),
        ('ongoing', 'In Progress')
    ], string="Status", default='ongoing')
    
    notes = fields.Text("Consultation Notes")
    recording_url = fields.Char("Recording Link")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('farm.expert.call') or _('CALL')
        return super().create(vals_list)

    @api.depends('start_time', 'end_time')
    def _compute_duration(self):
        for rec in self:
            if rec.start_time and rec.end_time:
                diff = rec.end_time - rec.start_time
                rec.duration = int(diff.total_seconds())
            else:
                rec.duration = 0
