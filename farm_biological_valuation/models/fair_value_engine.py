# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)

class AgriFairValueMixin(models.AbstractModel):
    """
    [US-014-05] 生物资产公允价值实时折算 Mixin
    提供生物资产在生长周期内的动态价值评估逻辑。
    """
    _name = 'farm.biological.valuation.mixin'
    _description = 'Biological Asset Fair Value Real-time Conversion DNA'

    # 1. 核心评估指标 (KPIs)
    current_growth_progress = fields.Float("Growth Progress (%)", help="当前生长进度，由农学模型计算")
    current_yield_potential = fields.Float("Estimated Yield (at maturity)", help="预测成熟时的产出量")
    current_market_unit_price = fields.Float("Current Market Price (per Unit)", help="当前市场公允单价")
    
    fair_value = fields.Monetary("Fair Value (Real-time)", compute='_compute_fair_value', store=True, currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string="Currency", default=lambda self: self.env.company.currency_id)

    # 2. 状态追踪
    last_valuation_date = fields.Datetime("Last Revaluation", default=fields.Datetime.now)
    valuation_method = fields.Selection([
        ('market_price', 'Market Price Method (公允价值)'),
        ('cost_accumulation', 'Cost Accumulation (成本累积)')
    ], string="Valuation Method", default='market_price')

    @api.depends('current_growth_progress', 'current_yield_potential', 'current_market_unit_price')
    def _compute_fair_value(self):
        """
        公允价值计算公式：
        Fair Value = (预测产出 * 市场单价) * 生长进度系数
        """
        for rec in self:
            if rec.valuation_method == 'market_price':
                # 核心农学折算算法
                rec.fair_value = (rec.current_yield_potential * rec.current_market_unit_price) * (rec.current_growth_progress / 100.0)
            else:
                # 成本法逻辑（需子模块根据 AML 累积计算）
                rec.fair_value = rec._get_accumulated_costs()

    def _get_accumulated_costs(self):
        """ [Hook] 成本法获取方法，由具体业务模块实现 """
        return 0.0

    def action_recalculate_fair_value(self):
        """
        [Process Engine] 主动触发价值重估，并根据波动率决定是否生成凭证。
        """
        self.ensure_one()
        old_value = self.fair_value
        
        # 1. 触发农学进度更新 (由子模块实现特定计算)
        self._update_biological_progress()
        
        # 2. 强制触发计算
        self._compute_fair_value()
        
        self.last_valuation_date = fields.Datetime.now()
        
        # 3. 审计与自动对账
        if old_value > 0 and abs(self.fair_value - old_value) / old_value > 0.05:
            self._on_fair_value_significant_change(old_value, self.fair_value)
            
        return True

    def _update_biological_progress(self):
        """ [ISL Hook] 更新生物生长进度，如积温计算、龄期增加等 """
        pass

    def _on_fair_value_significant_change(self, old_val, new_val):
        """ [ISL Hook] 当价值波动超过 5% 时的回调，通常用于生成会计凭证 """
        self.message_post(body=_("SIGNIFICANT VALUE CHANGE: %s -> %s (Variance > 5%%)") % (old_val, new_val))
