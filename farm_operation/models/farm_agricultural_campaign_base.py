from odoo import models, fields, api, _
import datetime
from odoo.exceptions import ValidationError


class FarmAgriculturalCampaignBase(models.AbstractModel):
    """
    Abstract base model for agricultural campaign functionality.
    This serves as the shared base for both original and ISL implementations.
    """
    _name = 'farm.agricultural.campaign.base'
    _description = 'Farm Agricultural Campaign Base Logic'

    # Campaign basic information
    name = fields.Char("Season Name", required=True)
    date_start = fields.Date("Start Date")
    date_end = fields.Date("End Date")
    is_active = fields.Boolean("Active", default=True)
    description = fields.Text("Description")

    # GDD (Growing Degree Days) growth model
    base_temperature = fields.Float(
        "Base Temp (℃)",
        default=10.0,
        help="Lower threshold for crop growth."
    )
    target_gdd = fields.Float(
        "Target GDD",
        help="GDD required for harvest."
    )
    accumulated_gdd = fields.Float(
        "Current GDD",
        compute='_compute_gdd',
        store=True
    )
    predicted_harvest_date = fields.Date(  # Changed to Date type to match original
        "Predicted Harvest",
        compute='_compute_gdd',
        store=True
    )

    land_parcel_id = fields.Many2one(
        'stock.location',
        string="Land Parcel",
        domain="[('is_land_parcel', '=', True)]"
    )

    @api.depends('date_start', 'target_gdd', 'land_parcel_id')
    def _compute_gdd(self):
        """整合 IoT 遥测数据计算积温 - Integrated IoT telemetry data for GDD calculation"""
        for rec in self:
            if not rec.date_start or not rec.land_parcel_id:
                rec.accumulated_gdd = 0
                continue

            # 1. 从 farm_iot 模块获取该地块的每日均温
            # 简化逻辑：查询该地块关联设备的 'air_temp' 遥测记录
            telemetries = self.env['iiot.telemetry'].search([
                ('parcel_id', '=', rec.land_parcel_id.id),
                ('timestamp', '>=', fields.Datetime.to_string(rec.date_start)),
                ('key', '=', 'air_temp')
            ])

            # 按天计算积温：Sum(Max(0, DailyAvgTemp - BaseTemp))
            # 注意：实际生产中应使用 SQL 分组聚合以提升性能
            daily_avgs = {}
            for t in telemetries:
                d = t.timestamp.date()
                daily_avgs.setdefault(d, []).append(t.value_float)

            total_gdd = 0.0
            days_count = 0
            for d, vals in daily_avgs.items():
                avg = sum(vals) / len(vals)
                total_gdd += max(0, avg - rec.base_temperature)
                days_count += 1

            rec.accumulated_gdd = total_gdd

            # 2. 预测收获日期
            rec.predicted_harvest_date = False
            if total_gdd > 0 and days_count > 0 and rec.target_gdd:
                gdd_per_day = total_gdd / days_count
                remaining_gdd = rec.target_gdd - total_gdd
                if gdd_per_day > 0:
                    remaining_days = remaining_gdd / gdd_per_day
                    rec.predicted_harvest_date = fields.Date.today() + datetime.timedelta(days=int(remaining_days))

    def action_calculate_gdd(self):
        """Calculate GDD based on actual weather data"""
        # Implementation would connect to weather API or IoT sensors
        pass

    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        """Validate that campaign dates are logical"""
        for record in self:
            if record.date_start and record.date_end and record.date_start > record.date_end:
                raise ValidationError("Campaign start date must be before end date.")