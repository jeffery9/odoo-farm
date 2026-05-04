# -*- coding: utf-8 -*-
# [US-048-02] AI Decision Cockpit Actions (Bridge between AI and Operation)
from odoo import models, fields, api, _

class AgriIntervention(models.Model):
    _name = 'mrp.production'
    _inherit = 'mrp.production'

    # AI 预警与建议计数
    ai_recommendation_count = fields.Integer("AI Recommendations", compute='_compute_ai_alerts')
    has_critical_stress = fields.Boolean("Critical Stress Alert", compute='_compute_ai_alerts')

    def _compute_ai_alerts(self):
        for rec in self:
            decisions = self.env['ai.decision.engine'].search([
                ('intervention_id', '=', rec.id),
                ('active_skill_json', '!=', '{}')
            ])
            rec.ai_recommendation_count = len(decisions)
            rec.has_critical_stress = rec.biological_stress_index > 25.0

    def action_view_ai_cockpit(self):
        """ [UX] 跳转至 AI 决策中心 """
        self.ensure_one()
        return {
            'name': _('AI Decision Cockpit'),
            'type': 'ir.actions.act_window',
            'res_model': 'ai.decision.engine',
            'view_mode': 'list,form',
            'domain': [('intervention_id', '=', self.id)],
            'context': {'default_intervention_id': self.id},
        }

    def action_approve_latest_ai_skill(self):
        """ [US-048-02] 执行最新的 AI 补救指令 """
        self.ensure_one()
        latest = self.env['ai.decision.engine'].search([
            ('intervention_id', '=', self.id),
            ('active_skill_json', '!=', '{}')
        ], order='create_date desc', limit=1)
        if latest:
            latest.action_generate_recovery_plan() # 模拟执行
            self.message_post(body=_("Approved AI recovery plan via Cockpit."))
        return True
