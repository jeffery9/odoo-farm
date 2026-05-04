# -*- coding: utf-8 -*-
# [US-045-04] [ISA-88]
from odoo import models, fields, api
import math

class AgriScienceMixin(models.AbstractModel):
    """ 农学科学内核 Mixin：提供 GDD 计算与生长曲线模拟 """
    _name = 'farm.agri.science.mixin'
    _description = 'Agri-Science Calculation Kernel'

    physiology_profile_id = fields.Many2one('agri.physiology.profile', string="Physiology Profile")
    cumulative_gdd = fields.Float("Cumulative GDD", default=0.0)
    current_growth_stage_id = fields.Many2one('agri.growth.stage', string="Current Stage", compute='_compute_biological_clock', store=True)
    
    # [US-045-05] 资源利用效率
    rue_actual = fields.Float("Radiation Use Efficiency (RUE)", compute='_compute_efficiencies')
    wue_actual = fields.Float("Water Use Efficiency (WUE)", compute='_compute_efficiencies')
    biological_stress_index = fields.Float("Stress Index (0-100)", default=0.0)

    @api.depends('cumulative_gdd', 'physiology_profile_id')
    def _compute_biological_clock(self):
        """ 根据累积 GDD 自动判定生理发育阶段 """
        for rec in self:
            if rec.physiology_profile_id and rec.cumulative_gdd:
                stage = self.env['agri.growth.stage'].search([
                    ('profile_id', '=', rec.physiology_profile_id.id),
                    ('gdd_threshold', '<=', rec.cumulative_gdd)
                ], order='gdd_threshold desc', limit=1)
                rec.current_growth_stage_id = stage
            else:
                rec.current_growth_stage_id = False

    def calculate_gdd_increment(self, t_max, t_min):
        """ 
        计算当日 GDD 增量 (Standard Method)
        GDD = max((Tmax + Tmin)/2 - Tbase, 0)
        """
        self.ensure_one()
        if not self.physiology_profile_id: return 0.0
        t_base = self.physiology_profile_id.temp_base
        t_avg = (t_max + t_min) / 2.0
        return max(t_avg - t_base, 0.0)

    def get_logistic_biomass_prediction(self, gdd=None):
        """ 
        逻辑斯蒂生长预测：W(GDD) = L / (1 + exp(-k * (GDD - GDD0)))
        """
        self.ensure_one()
        prof = self.physiology_profile_id
        if not prof: return 0.0
        gdd = gdd or self.cumulative_gdd
        try:
            return prof.logistic_l / (1 + math.exp(-prof.logistic_k * (gdd - prof.logistic_gdd0)))
        except OverflowError:
            return prof.logistic_l if (gdd - prof.logistic_gdd0) > 0 else 0.0
