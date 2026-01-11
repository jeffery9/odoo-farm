from odoo import models, fields

class AgriIntervention(models.Model):
    _inherit = 'mrp.production'

    agri_task_id = fields.Many2one(
        'project.task', 
        string="Production Task",
        help="The specific production task this intervention belongs to."
    )
    
    # 工时追踪 [US-42]
    work_start_datetime = fields.Datetime("Work Start")
    is_working = fields.Boolean("In Progress", default=False)

    def action_start_work(self):
        """ 一键打卡：开始作业 """
        self.ensure_one()
        self.write({
            'work_start_datetime': fields.Datetime.now(),
            'is_working': True
        })
        self.message_post(body=_("Labor: Work started at %s") % self.work_start_datetime)

    def action_stop_work(self):
        """ 一键打卡：停止作业并自动创建工时记录 """
        self.ensure_one()
        if not self.work_start_datetime:
            return
            
        now = fields.Datetime.now()
        # 创建 farm.worklog (如果 HR 模块已安装)
        if hasattr(self.env['farm.worklog'], 'create'):
            self.env['farm.worklog'].create({
                'employee_id': self.env.user.employee_id.id or self.env.user.id, # 适配无员工档案情况
                'task_id': self.agri_task_id.id,
                'date': fields.Date.today(),
                'work_type': self.intervention_type or 'other',
                'quantity': 1.0, # 默认记录一次作业
                'notes': _('Auto-recorded from intervention %s') % self.name
            })
            
        self.write({
            'is_working': False,
            'work_start_datetime': False
        })
        self.message_post(body=_("Labor: Work stopped and recorded at %s") % now)

    def action_confirm(self):
        # ... (原有代码保持不变)
        return super().action_confirm()

    def button_mark_done(self):
        """ 扩展完成逻辑，触发质量检查 [US-49] """
        res = super(AgriIntervention, self).button_mark_done()
        for mo in self:
            if mo.intervention_type == 'harvesting':
                # 尝试创建质检单 (如果质量模块已安装)
                try:
                    self.env['farm.quality.check'].create({
                        'lot_id': mo.move_finished_ids.mapped('lot_ids')[:1].id,
                        'task_id': mo.agri_task_id.id,
                        'name': _('Harvest QC: %s') % mo.name,
                    })
                except Exception:
                    pass 
        return res
