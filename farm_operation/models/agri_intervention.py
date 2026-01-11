from odoo import models, fields

class AgriIntervention(models.Model):
    _inherit = 'mrp.production'

    agri_task_id = fields.Many2one(
        'project.task', 
        string="Production Task",
        help="The specific production task this intervention belongs to."
    )
    
    # 增加农业特有的作业分类（可选，基于 mrp 原生字段扩展）
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

    def action_confirm(self):
        """ 扩展确认逻辑，进行安全拦截 [US-36] """
        for mo in self:
            # 1. 检查有机拦截
            if mo.agri_task_id.land_parcel_id.certification_level in ['organic', 'organic_transition']:
                for move in mo.move_raw_ids:
                    if move.product_id.is_agri_input and not move.product_id.is_safety_approved:
                        raise UserError(_("COMPLIANCE ERROR: Product %s is not approved for organic production!") % move.product_id.name)
            
            # 2. 触发休药期更新 (调用 farm_safety 注入的方法)
            if hasattr(mo.agri_task_id, 'action_confirm_intervention_safety'):
                mo.agri_task_id.action_confirm_intervention_safety(mo.move_raw_ids.mapped('product_id').ids)
                
        return super().action_confirm()
