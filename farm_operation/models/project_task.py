from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class ProjectTask(models.Model):
    _inherit = 'project.task'
    _description = 'Multi-Industry Activity Production'

    # Industry type to support multi-industry operations
    industry_type = fields.Selection([
        ('field_crops', 'Field Crops'),
        ('protected_cultivation', 'Protected Cultivation'),
        ('orchard_horticulture', 'Orchard Horticulture'),
        ('livestock', 'Livestock'),
        ('aquaculture', 'Aquaculture'),
        ('medicinal_plants', 'Medicinal Plants'),
        ('mushroom', 'Mushroom Cultivation'),
        ('apiculture', 'Apiculture'),
        ('agricultural_processing', 'Agricultural Processing'),
        ('agritourism', 'Agritourism'),
        ('mixed', 'Mixed Operations'),
    ], string='Industry Type',
       help='Type of agricultural industry this task belongs to',
       default='field_crops')

    campaign_id = fields.Many2one(
        'agricultural.campaign',
        string="Campaign/Season",
        help="Link this production task to a specific season."
    )

    # 继承 farm_core 资产逻辑
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

    # Ekylibre Mapping: ActivityProduction [US-Mapping]
    support_id = fields.Many2one('product.product', string="Support Object", help="The land parcel, animal or group this task is performed on.")
    size_value = fields.Float("Production Size", help="Area in sqm/mu or quantity of individuals.")

    # 需求驱动关联 [US-03-01]
    sale_order_id = fields.Many2one('sale.order', string="Source Sale Order")

    intervention_ids = fields.One2many(
        'mrp.production',
        'agri_task_id',
        string="Agri Interventions"
    )

    # 养分汇总 [US-01-03]
    total_n = fields.Float("Total Nitrogen (kg)", compute='_compute_nutrients', store=True)
    total_p = fields.Float("Total Phosphorus (kg)", compute='_compute_nutrients', store=True)
    total_k = fields.Float("Total Potassium (kg)", compute='_compute_nutrients', store=True)

    # 养分密度 (kg/mu) [US-01-03 Algorithm]
    n_density = fields.Float("N Density (kg/mu)", compute='_compute_agri_math')
    p_density = fields.Float("P Density (kg/mu)", compute='_compute_agri_math')
    k_density = fields.Float("K Density (kg/mu)", compute='_compute_agri_math')

    # 安全收获检查 [US-11-03 Algorithm]
    is_safe_to_harvest = fields.Boolean("Safe to Harvest", compute='_compute_agri_math')
    days_to_safety = fields.Integer("Days to Safety", compute='_compute_agri_math')

    def _compute_agri_math(self):
        for task in self:
            # 1. 养分密度计算
            area = task.size_value or task.land_parcel_id.land_area or 1.0
            task.n_density = task.total_n / area
            task.p_density = task.total_p / area
            task.k_density = task.total_k / area

            # 2. 安全检查
            today = fields.Datetime.now()
            lot = task.biological_lot_id
            if lot and hasattr(lot, 'withdrawal_end_datetime') and lot.withdrawal_end_datetime:
                if lot.withdrawal_end_datetime > today:
                    task.is_safe_to_harvest = False
                    task.days_to_safety = (lot.withdrawal_end_datetime - today).days + 1
                else:
                    task.is_safe_to_harvest = True
                    task.days_to_safety = 0
            else:
                task.is_safe_to_harvest = True
                task.days_to_safety = 0

    def action_view_telemetry(self):
        """ 跳转至该任务关联的遥测趋势图 [US-11-03] """
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

    @api.model
    def cron_generate_feeding_proposals(self):
        """ 每日定时任务：水产生成建议的饲喂干预 [US-01-03 Algorithm] """
        # 寻找活跃的养殖任务
        tasks = self.search([
            ('project_id.activity_family', 'in', ['livestock', 'aquaculture']),
            ('state', '=', 'inprogress'), # 假定状态
            ('biological_lot_id', '!=', False)
        ])

        for task in tasks:
            lot = task.biological_lot_id
            product = lot.product_id

            # 计算年龄
            if lot.born_at:
                age = (fields.Datetime.now() - lot.born_at).days
                # 从生长曲线获取预期体重和饲喂率
                expected_weight = product.get_expected_weight(age)
                # 寻找匹配的生长曲线行以获取喂养率
                curve_line = product.growth_curve_ids.filtered(lambda c: c.age_days <= age).sorted('age_days', reverse=True)
                feed_rate = curve_line[0].daily_feed_rate if curve_line else 0.0

                if feed_rate > 0:
                    # 计算建议投喂量 = 估算生物总量 = 数量 * 平均体重
                    estimated_biomass = lot.animal_count * expected_weight
                    suggested_feed_qty = estimated_biomass * (feed_rate / 100.0)

                    # 发送建议消息或创建草稿 MO
                    task.message_post(body=_("DAILY FEED PROPOSAL: Age %s days. Estimated Biomass: %s kg. Suggested Feed: %s kg.") % (
                        age, estimated_biomass, suggested_feed_qty
                    ))

    # Required Qualifications for Task [US-17-08]
    required_skill_ids = fields.Many2many(
        'farm.training.skill',
        string="Required Skills",
        help="Skills required to perform this task."
    )
    required_certification_ids = fields.Many2many(
        'farm.training.certification',
        string="Required Certifications",
        help="Certifications required to perform this task."
    )

    @api.constrains('user_ids', 'required_skill_ids', 'required_certification_ids')
    def _check_employee_qualifications(self):
        for task in self:
            if not task.required_skill_ids and not task.required_certification_ids:
                continue # No specific qualifications required for this task

            for user in task.user_ids:
                employee = self.env['hr.employee'].search([('user_id', '=', user.id)], limit=1)
                if not employee:
                    # Depending on policy, either raise error or skip
                    # For now, we'll assume every assigned user should be an employee for qualification checks
                    continue

                try:
                    employee.check_qualification_for_task(
                        required_skills=task.required_skill_ids,
                        required_certifications=task.required_certification_ids
                    )
                except ValidationError as e:
                    raise ValidationError(_(f"Qualification Error for Task '{task.name}': {e.args[0]}"))

    @api.onchange('industry_type')
    def _onchange_industry_type(self):
        """When industry type changes, update task fields and behaviors"""
        if self.industry_type:
            # Update project or task based on industry type
            industry_project_mapping = {
                'field_crops': 'Field Crops Operations',
                'protected_cultivation': 'Protected Cultivation Operations',
                'orchard_horticulture': 'Orchard Operations',
                'livestock': 'Livestock Operations',
                'aquaculture': 'Aquaculture Operations',
                'medicinal_plants': 'Medicinal Plants Operations',
                'mushroom': 'Mushroom Operations',
                'apiculture': 'Apiculture Operations',
                'agricultural_processing': 'Processing Operations',
                'agritourism': 'Agritourism Operations',
            }

            # Update or create project if needed
            if self.industry_type in industry_project_mapping:
                project_name = industry_project_mapping[self.industry_type]
                project = self.env['project.project'].search([('name', '=', project_name)], limit=1)
                if project:
                    self.project_id = project.id


