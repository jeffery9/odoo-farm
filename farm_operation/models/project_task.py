from odoo import models, fields

class ProjectTask(models.Model):
    _inherit = 'project.task'

    campaign_id = fields.Many2one(
        'agricultural.campaign', 
        string="Campaign/Season",
        help="Link this production task to a specific season."
    )
    
    # 继承 farm_core 中的地块/资产逻辑
    land_parcel_id = fields.Many2one('stock.location', string="Land Parcel/Pond", domain=[('is_land_parcel', '=', True)])
    gps_lat = fields.Float(related='land_parcel_id.gps_lat', store=True)
    gps_lng = fields.Float(related='land_parcel_id.gps_lng', store=True)
    
    # Weather Forecast [US-Weather]
    forecast_ids = fields.One2many(
        'farm.weather.forecast', 
        compute='_compute_weather_forecasts', 
        string="Weather Forecasts"
    )

    def _compute_weather_forecasts(self):
        for task in self:
            if task.planned_date_begin and task.land_parcel_id:
                # Find forecasts for the planned period
                task.forecast_ids = self.env['farm.weather.forecast'].search([
                    ('location_id', '=', task.land_parcel_id.id),
                    ('date', '>=', task.planned_date_begin),
                    ('date', '<=', task.date_deadline or task.planned_date_begin)
                ])
            else:
                task.forecast_ids = False

    biological_lot_id = fields.Many2one('stock.lot', string="Biological Asset/Lot", domain="[('is_animal', '=', True)]")

    # 需求驱动关联 [US-28]
    sale_order_id = fields.Many2one('sale.order', string="Source Sale Order")

    intervention_ids = fields.One2many(
        'mrp.production', 
        'agri_task_id', 
        string="Agri Interventions"
    )

    # 养分汇总 [US-07]
    total_n = fields.Float("Total Nitrogen (kg)", compute='_compute_nutrients', store=True)
    total_p = fields.Float("Total Phosphorus (kg)", compute='_compute_nutrients', store=True)
    total_k = fields.Float("Total Potassium (kg)", compute='_compute_nutrients', store=True)

    def action_view_telemetry(self):
        """ 跳转至该任务关联的遥测趋势图 [US-11] """
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("farm_iot.action_farm_telemetry")
        action['domain'] = [('production_id', '=', self.id)]
        action['context'] = {
            'default_production_id': self.id,
            'default_land_parcel_id': self.land_parcel_id.id,
            'group_by': 'timestamp:hour'
        }
        return action

    @fields.depends('intervention_ids.state', 'intervention_ids.move_raw_ids.product_uom_qty')
    def _compute_nutrients(self):
        for task in self:
            n = p = k = 0.0
            # 仅统计已完成或确认的施肥类型干预
            fertilizing_ops = task.intervention_ids.filtered(lambda i: i.intervention_type == 'fertilizing' and i.state != 'cancel')
            for op in fertilizing_ops:
                for move in op.move_raw_ids:
                    n += (move.product_uom_qty * (move.product_id.n_content / 100.0))
                    p += (move.product_uom_qty * (move.product_id.p_content / 100.0))
                    k += (move.product_uom_qty * (move.product_id.k_content / 100.0))
            task.total_n = n
            task.total_p = p
            task.total_k = k

    def _update_nutrient_balance(self):
        """ 手动触发更新的方法，供测试或特定流程调用 """
        self._compute_nutrients()
