from odoo import models, fields, api, _
from datetime import timedelta

class ProjectTask(models.Model):
    _inherit = 'project.task'

    prevention_template_id = fields.Many2one(
        'farm.prevention.template', 
        string="Prevention Plan",
        help="Select a template to auto-generate prevention tasks."
    )

    def action_apply_prevention_template(self):
        """ 根据模板生成子任务 """
        self.ensure_one()
        if not self.prevention_template_id or not self.planned_date_begin:
            return False
        
        task_obj = self.env['project.task']
        for line in self.prevention_template_id.line_ids:
            deadline = self.planned_date_begin + timedelta(days=line.delay_days)
            task_obj.create({
                'name': _('Prevention: %s') % line.name,
                'parent_id': self.id,
                'project_id': self.project_id.id,
                'date_deadline': deadline,
                'user_ids': self.user_ids.ids,
                # 未来可在此处预填 MO 逻辑
            })
        return True
