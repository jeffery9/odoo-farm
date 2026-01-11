from odoo import models, fields, api, _
from odoo.exceptions import UserError

class AgriIntervention(models.Model):
    _inherit = 'mrp.production'

    agri_task_id = fields.Many2one(
        'project.task', 
        string="Production Task",
        help="The specific production task this intervention belongs to."
    )
    
    # 农业特有的作业分类 [核心字段 - 已恢复]
    intervention_type = fields.Selection([
        ('tillage', 'Soil Preparation (耕作)'),
        ('sowing', 'Sowing/Planting (播种/移栽)'),
        ('fertilizing', 'Fertilizing (施肥)'),
        ('irrigation', 'Irrigation (灌溉)'),
        ('protection', 'Crop Protection (植保)'),
        ('harvesting', 'Harvesting (收获)'),
        ('feeding', 'Feeding (饲喂)'),
        ('medical', 'Medical/Prevention (医疗/防疫)'),
    ], string="Intervention Type")

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
        if hasattr(self.env['farm.worklog'], 'create'):
            employee = self.env.user.employee_id
            self.env['farm.worklog'].create({
                'employee_id': employee.id if employee else False,
                'task_id': self.agri_task_id.id,
                'date': fields.Date.today(),
                'work_type': self.intervention_type or 'harvesting',
                'quantity': 1.0, 
                'notes': _('Auto-recorded from intervention %s') % self.name
            })
            
        self.write({
            'is_working': False,
            'work_start_datetime': False
        })
        self.message_post(body=_("Labor: Work stopped and recorded at %s") % now)

    def action_confirm(self):
        """ 扩展确认逻辑，进行安全拦截 [US-36] 并传递任务 ID 到供应端 [US-29] """
        for mo in self:
            # 1. 检查有机拦截
            if mo.agri_task_id.land_parcel_id.certification_level in ['organic', 'organic_transition']:
                for move in mo.move_raw_ids:
                    if move.product_id.is_agri_input and not move.product_id.is_safety_approved:
                        raise UserError(_("COMPLIANCE ERROR: Product %s is not approved for organic production!") % move.product_id.name)
            
            # 2. 传递 agri_task_id 到采购逻辑 (通过 procurement_group)
            if mo.agri_task_id and mo.procurement_group_id:
                mo.procurement_group_id.agri_task_id = mo.agri_task_id.id

            # 3. 触发休药期更新 (调用 farm_safety 注入的方法)
            if hasattr(mo.agri_task_id, 'action_confirm_intervention_safety'):
                mo.agri_task_id.action_confirm_intervention_safety(mo.move_raw_ids.mapped('product_id').ids)
                
        return super(AgriIntervention, self).action_confirm()

class ProcurementGroup(models.Model):
    _inherit = 'procurement.group'

    agri_task_id = fields.Many2one('project.task', string="Agri Task")

    def button_mark_done(self):
        """ 扩展完成逻辑，触发质量检查 [US-49] """
        res = super(AgriIntervention, self).button_mark_done()
        for mo in self:
            if mo.intervention_type == 'harvesting':
                try:
                    self.env['farm.quality.check'].create({
                        'lot_id': mo.move_finished_ids.mapped('lot_ids')[:1].id,
                        'task_id': mo.agri_task_id.id,
                        'name': _('Harvest QC: %s') % mo.name,
                    })
                except Exception:
                    pass 
        return res