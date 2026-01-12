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

    def action_approve(self):
        """ 审批并分摊成本 [US-13-04] """
        for log in self:
            # 获取员工时薪（示例：从员工档案获取或固定值）
            hourly_rate = getattr(log.employee_id, 'hourly_cost', 50.0) 
            amount = log.quantity * hourly_rate
            
            # 找到任务关联的核算账户
            analytic_account = log.task_id.analytic_account_id
            if analytic_account:
                self.env['account.analytic.line'].create({
                    'name': _('Labor: %s on %s') % (log.employee_id.name, log.task_id.name),
                    'account_id': analytic_account.id,
                    'amount': -amount, # 支出为负
                    'unit_amount': log.quantity,
                    'product_id': False, 
                    'employee_id': log.employee_id.id,
                })
        return True

class ProjectTask(models.Model):
    _inherit = 'project.task'

    worklog_ids = fields.One2many('farm.worklog', 'task_id', string="Labor Worklogs")
    total_harvested_qty = fields.Float("Total Harvested (kg)", compute='_compute_total_worklog_qty', store=True)
    
    # 技能要求 [US-04-02]
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
    
    # 资质要求 [US-17-08]
    requires_certificate = fields.Boolean("Requires Certificate", default=False)

class FarmEmployeeCertificate(models.Model):
    _name = 'farm.employee.certificate'
    _description = 'Employee Skill Certificate'

    employee_id = fields.Many2one('hr.employee', required=True)
    skill_id = fields.Many2one('farm.agri.skill', string="Skill/Qualification", required=True)
    certificate_number = fields.Char("Cert No.")
    date_expiry = fields.Date("Expiry Date")
    
    state = fields.Selection([
        ('valid', 'Valid'),
        ('expired', 'Expired')
    ], compute='_compute_state', store=True)

    @api.depends('date_expiry')
    def _compute_state(self):
        today = fields.Date.today()
        for cert in self:
            if cert.date_expiry and cert.date_expiry < today:
                cert.state = 'expired'
            else:
                cert.state = 'valid'

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    is_seasonal = fields.Boolean("Seasonal Laborer", default=False, help="Identify external or seasonal workers.")
    hourly_cost = fields.Float("Hourly Cost", default=0.0)
    agri_skill_ids = fields.Many2many('farm.agri.skill', string="Agricultural Skills")
    piece_rate_total = fields.Float("Total Piece-rate Performance", compute='_compute_piece_rate')
    
    certificate_ids = fields.One2many('farm.employee.certificate', 'employee_id', string="Certificates")

    def _compute_piece_rate(self):
        for employee in self:
            logs = self.env['farm.worklog'].search([('employee_id', '=', employee.id)])
            employee.piece_rate_total = sum(logs.mapped('quantity'))
