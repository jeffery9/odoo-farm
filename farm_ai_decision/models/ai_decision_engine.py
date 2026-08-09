# -*- coding: utf-8 -*-
# [US-202] AI Decision Support Engine
from odoo import models, fields, api, _
import json

class AiDecisionEngine(models.Model):
    """ AI 决策引擎：基于生物压力指数生成补救方案与采收预测 """
    _name = 'ai.decision.engine'
    _description = 'AI Decision Engine'
    _inherit = ['agri.ai.decision.base']

    intervention_id = fields.Many2one('mrp.production', string="Target Intervention", required=True)
    stress_index = fields.Float(related='intervention_id.biological_stress_index', string="Current Stress Index")
    growth_stage_id = fields.Many2one(related='intervention_id.current_growth_stage_id', string="Current Stage")
    
    # [US-046-01] 自动补救决策
    recovery_plan = fields.Text("Suggested Recovery Plan (AI)")
    active_skill_json = fields.Text("Active Skill Directive (JSON)")
    
    # [US-046-02] 采收窗口预测
    predicted_harvest_date = fields.Date("Predicted Harvest Date", compute='_compute_harvest_prediction', store=True, precompute=True)

    def _create_correction_intervention(self):
        """ Automatically execute the generated recovery plan [US-TECH-AI-01] """
        if not self.active_skill_json or self.active_skill_json == "{}":
            return False
            
        try:
            plan = json.loads(self.active_skill_json)
            action = plan.get('action')
            
            # Map AI action to intervention type
            type_map = {
                'irrigation_boost': 'irrigation',
                'nutrient_correction': 'fertilizing',
                'pest_control': 'protection'
            }
            
            intervention_type = type_map.get(action, 'protection')
            
            vals = {
                'product_id': self.intervention_id.product_id.id,
                'product_qty': 1.0,
                'intervention_type': intervention_type,
                'location_id': self.intervention_id.location_id.id,
                'origin': f"AI Recovery: {self.name}",
            }
            
            intervention = self.env['mrp.production'].create(vals)
            intervention.action_confirm()
            return intervention
        except Exception as e:
            _logger.error(f"Failed to execute AI recovery plan: {str(e)}")
            return False

    @api.depends('intervention_id.cumulative_gdd', 'intervention_id.physiology_profile_id')
    def _compute_harvest_prediction(self):
        """ 基于 GDD 累积速度与历史气象预测采收日期 """
        for rec in self:
            if rec.intervention_id and rec.intervention_id.physiology_profile_id:
                # 简化逻辑：假设平均每日 GDD 为 15
                total_needed = 1200.0  # 假设 1200 GDD 采收
                remaining = total_needed - rec.intervention_id.cumulative_gdd
                days_to_go = max(remaining / 15.0, 0)
                rec.predicted_harvest_date = fields.Date.add(fields.Date.today(), days=int(days_to_go))
            else:
                rec.predicted_harvest_date = False

    def action_generate_recovery_plan(self):
        """ 根据压力指数生成补救 JSON 指令 (Active Skill) """
        self.ensure_one()
        if self.stress_index > 30:
            plan = {
                "action": "irrigation_boost",
                "intensity": "high",
                "duration_minutes": 45,
                "reason": f"Stress index at {self.stress_index}% detected."
            }
            self.recovery_plan = _("Detected high stress. Recommend boosting irrigation by 45 minutes.")
            self.active_skill_json = json.dumps(plan, indent=4)
        else:
            self.recovery_plan = _("Plant health is stable. No urgent intervention required.")
            self.active_skill_json = "{}"
        
        self.message_post(body=_("AI Recovery Plan generated for stress level %s") % self.stress_index)
