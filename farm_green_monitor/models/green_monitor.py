from odoo import models, fields, api, _

class StockLocation(models.Model):
    _inherit = 'stock.location'

    # 减量目标 [US-70]
    fertilizer_reduction_target = fields.Float("Fertilizer Reduction Target (%)", default=0.0)
    pesticide_reduction_target = fields.Float("Pesticide Reduction Target (%)", default=0.0)

class ProjectTask(models.Model):
    _inherit = 'project.task'

    # 化肥农药使用量汇总 (kg) [US-70]
    total_fertilizer_used = fields.Float("Total Fertilizer Used (kg)", compute='_compute_green_monitor_stats', store=True)
    total_pesticide_used = fields.Float("Total Pesticide Used (kg)", compute='_compute_green_monitor_stats', store=True)
    
    # 单位面积使用量 (kg/亩)
    fertilizer_per_mu = fields.Float("Fertilizer (kg/mu)", compute='_compute_green_monitor_stats', store=True)
    pesticide_per_mu = fields.Float("Pesticide (kg/mu)", compute='_compute_green_monitor_stats', store=True)

    @api.depends('intervention_ids.move_raw_ids.product_id.input_type', 'intervention_ids.move_raw_ids.product_uom_qty', 'size_value')
    def _compute_green_monitor_stats(self):
        sqm_per_mu = 666.67 # 1亩 = 666.67平方米
        for task in self:
            total_fertilizer = 0.0
            total_pesticide = 0.0
            for op in task.intervention_ids:
                for move in op.move_raw_ids:
                    if move.product_id.input_type == 'fertilizer':
                        total_fertilizer += move.product_uom_qty
                    elif move.product_id.input_type == 'pesticide':
                        total_pesticide += move.product_uom_qty
            
            task.total_fertilizer_used = total_fertilizer
            task.total_pesticide_used = total_pesticide
            
            area_mu = (task.size_value or task.land_parcel_id.land_area or 0.0) / sqm_per_mu
            task.fertilizer_per_mu = total_fertilizer / area_mu if area_mu > 0 else 0.0
            task.pesticide_per_mu = total_pesticide / area_mu if area_mu > 0 else 0.0

class FarmGreenMonitorReport(models.AbstractModel):
    _name = 'report.farm_green_monitor.reduction_trend_report'
    _description = 'Fertilizer/Pesticide Reduction Trend Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['agricultural.campaign'].browse(docids)
        # 这里需要更复杂的逻辑来获取历史数据和计算趋势
        # 简化示例：假设docids是campaigns
        return {
            'doc_ids': docids,
            'doc_model': 'agricultural.campaign',
            'docs': docs,
            'get_reduction_data': self._get_reduction_data,
        }

    def _get_reduction_data(self, campaign):
        # 实际应从历史数据中计算，这里只返回当前季度的指标
        return {
            'fertilizer_this_season': sum(campaign.project_ids.mapped('task_ids.fertilizer_per_mu')),
            'pesticide_this_season': sum(campaign.project_ids.mapped('task_ids.pesticide_per_mu')),
            # 这里需要进一步查询上一个同期campaign的数据
            'fertilizer_prev_season': 100, # 模拟数据
            'pesticide_prev_season': 50, # 模拟数据
        }
