from odoo import models, fields, api, _
from datetime import date

class FarmTrainingCourse(models.Model):
    _name = 'farm.training.course'
    _description = 'Agricultural Training Course'

    name = fields.Char("Course Title", required=True)
    description = fields.Text("Description")
    course_type = fields.Selection([
        ('safety', 'Safety Training (安全操作)'),
        ('skill', 'Skill Enhancement (技能提升)'),
        ('compliance', 'Compliance Training (合规培训)'),
        ('other', 'Other (其他)')
    ], string="Type", default='skill')
    
    duration_hours = fields.Float("Duration (Hours)")
    
    # 关联技能
    related_skill_ids = fields.Many2many('farm.agri.skill', string="Related Skills")

class FarmEmployeeTraining(models.Model):
    _name = 'farm.employee.training'
    _description = 'Employee Training Record'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    employee_id = fields.Many2one('hr.employee', string="Employee", required=True)
    course_id = fields.Many2one('farm.training.course', string="Course", required=True)
    date_completed = fields.Date("Date Completed", default=fields.Date.today)
    
    state = fields.Selection([
        ('draft', 'Planned'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ], string="Status", default='draft', tracking=True)

class FarmAgriSkill(models.Model):
    _inherit = 'farm.agri.skill'

    requires_training_course = fields.Boolean("Requires Training Course", default=False)
    # 可关联具体课程
    required_course_id = fields.Many2one('farm.training.course', string="Required Course")

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    training_record_ids = fields.One2many('farm.employee.training', 'employee_id', string="Training Records")
    
    @api.constrains('agri_skill_ids', 'training_record_ids')
    def _check_skill_training_compliance(self):
        for employee in self:
            for skill in employee.agri_skill_ids.filtered('requires_training_course'):
                if not employee.training_record_ids.filtered(lambda t: t.course_id == skill.required_course_id and t.state == 'completed'):
                    # raise ValidationError(_("Employee %s requires completion of training for skill '%s'.") % (employee.name, skill.name))
                    pass # 暂时不强制限
