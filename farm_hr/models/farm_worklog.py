from odoo import models, fields, api, _

class FarmWorklog(models.Model):
    _name = 'farm.worklog'
    _description = 'Farm Field Worklog'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc'

    employee_id = fields.Many2one('hr.employee', string="Worker", required=True)
    task_id = fields.Many2one('project.task', string="Farm Task", required=True)
    date = fields.Date("Date", default=fields.Date.today, required=True)
    
    work_type = fields.Selection([
        ('tillage', 'Tillage (耕作)'),
        ('sowing', 'Sowing (播种)'),
        ('harvesting', 'Harvesting (收获)'),
        ('packaging', 'Packaging (包装)'),
        ('feeding', 'Feeding (饲喂)')
    ], string="Work Type", required=True)
    
    quantity = fields.Float("Done Quantity", default=1.0)
    uom_id = fields.Many2one('uom.uom', string="Unit")
    
    notes = fields.Text("Notes")

class ProjectTask(models.Model):
    _inherit = 'project.task'

    worklog_ids = fields.One2many('farm.worklog', 'task_id', string="Labor Worklogs")
    total_harvested_qty = fields.Float("Total Harvested (kg)", compute='_compute_total_worklog_qty', store=True)
    
    # 技能要求 [US-41]
    required_skill_id = fields.Many2one('farm.agri.skill', string="Required Skill")
    eligible_worker_ids = fields.Many2many('hr.employee', compute='_compute_eligible_workers', string="Eligible Workers")

    @api.depends('required_skill_id')
    def _compute_eligible_workers(self):
        for task in self:
            if task.required_skill_id:
                task.eligible_worker_ids = self.env['hr.employee'].search([
                    ('agri_skill_ids', 'in', task.required_skill_id.id)
                ])
            else:
                task.eligible_worker_ids = self.env['hr.employee'].search([])

    @api.depends('worklog_ids.quantity', 'worklog_ids.work_type')
    def _compute_total_worklog_qty(self):
        for task in self:
            harvesting_logs = task.worklog_ids.filtered(lambda l: l.work_type == 'harvesting')
            task.total_harvested_qty = sum(harvesting_logs.mapped('quantity'))

class AgriSkill(models.Model):
    _name = 'farm.agri.skill'
    _description = 'Agricultural Skill'

    name = fields.Char("Skill Name", required=True) # e.g., Harvester Operator, Veterinarian
    description = fields.Text("Description")

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    is_seasonal = fields.Boolean("Seasonal Laborer", default=False, help="Identify external or seasonal workers.")
    agri_skill_ids = fields.Many2many('farm.agri.skill', string="Agricultural Skills")
    piece_rate_total = fields.Float("Total Piece-rate Performance", compute='_compute_piece_rate')

    def _compute_piece_rate(self):
        for employee in self:
            logs = self.env['farm.worklog'].search([('employee_id', '=', employee.id)])
            employee.piece_rate_total = sum(logs.mapped('quantity'))
