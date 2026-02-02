# -*- coding: utf-8 -*-
# [US-201-01] [ISA-88]
from odoo import models, fields, api, _

class AgriPhysiologyProfile(models.Model):
    """ 品种生理指纹模型：定义作物的基点温度与生长参数 """
    _name = 'agri.physiology.profile'
    _description = 'Crop Physiology Fingerprint'

    name = fields.Char("Variety Name", required=True)
    product_id = fields.Many2one('product.product', string="Associated Seed Product")
    
    # [US-201-02] 基点温度定义 (Cardinal Temperatures)
    temp_base = fields.Float("Base Temperature (T-base)", help="Growth stops below this temp", default=10.0)
    temp_opt = fields.Float("Optimum Temperature (T-opt)", default=25.0)
    temp_max = fields.Float("Maximum Temperature (T-max)", help="Growth stops above this temp", default=35.0)

    # [US-201-03] 逻辑斯蒂生长参数 (Logistic Growth Parameters)
    logistic_l = fields.Float("Max Biomass (L)", default=100.0)
    logistic_k = fields.Float("Growth Rate (k)", default=0.1)
    logistic_gdd0 = fields.Float("Inflexion GDD (GDD0)", default=500.0)

    # [US-78-13] 品种响应曲线参数 (Nutrient Response Parameters - Mitscherlich Equation)
    # Yield = A * (1 - exp(-c * (Nutrient + b)))
    response_max_yield = fields.Float("Potential Max Yield (A)", default=800.0, help="Theoretical max yield for this variety under ideal conditions.")
    response_efficiency_c = fields.Float("Nutrient Efficiency Coefficient (c)", default=0.003, help="Curvature of the response curve (Mitscherlich c).")

    stage_ids = fields.One2many('agri.growth.stage', 'profile_id', string="Physiological Stages")

class AgriGrowthStage(models.Model):
    """ 生理发育阶段模型：通过 GDD 定义生长进度 """
    _name = 'agri.growth.stage'
    _description = 'Crop Growth Stage'
    _order = 'gdd_threshold asc'

    name = fields.Char("Stage Name", required=True)
    profile_id = fields.Many2one('agri.physiology.profile', ondelete='cascade')
    gdd_threshold = fields.Float("GDD Threshold (Cumulative)", required=True)
    stage_code = fields.Char("Stage Code (e.g. VE, V1, R1)")
    description = fields.Text("Description")
