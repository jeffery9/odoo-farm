# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class FarmProcessingBomExtension(models.Model):
    _name = 'farm.processing.bom'
    _inherit = 'farm.processing.bom'

    processing_type = fields.Selection([
        ('primary', 'Primary'),
        ('deep', 'Deep'),
        ('packaging', 'Packaging')
    ], string='Processing Type', default='primary')

    industry_type = fields.Selection(selection_add=[
        ('food_processing', 'Food Processing'),
    ], ondelete={'food_processing': 'set null'})

    # 预期等级分布 [US-14-08]
    grade_distribution_ids = fields.One2many('farm.bom.grade.distribution', 'bom_id', string="Expected Grade Distribution")

    # 行业标准参数 [US-14-09]
    is_parameter_required = fields.Boolean('Require Process Parameters', default=False)
    target_temp = fields.Float('Standard Temperature (℃)')
    target_ph = fields.Float("Target pH")
    target_brix = fields.Float("Target Brix")
    target_proofing_time = fields.Float("Target Proofing Time (Min)")
    standard_duration = fields.Float('Standard Duration (Minutes)')
    haccp_instructions = fields.Html("HACCP Critical Instructions")

    # US-14-16: 损耗容差管理
    max_loss_rate = fields.Float("Max Allowable Loss Rate (%)", help="Maximum allowable loss rate for this process. Exceeding this will trigger hard blocking.")

    # US-14-03: 农业副产品价值分摊 - Using mixin
    byproduct_cost_share_total = fields.Float("Byproduct Cost Share Total (%)", compute='_compute_byproduct_cost_share_total', store=True)
    finished_product_cost_share = fields.Float("Finished Product Cost Share (%)", compute='_compute_finished_product_cost_share', store=True)

    @api.depends('byproduct_ids', 'byproduct_ids.cost_share')
    def _compute_byproduct_cost_share_total(self):
        for bom in self:
            bom.byproduct_cost_share_total = sum(bom.byproduct_ids.mapped('cost_share'))

    @api.depends('byproduct_cost_share_total')
    def _compute_finished_product_cost_share(self):
        for bom in self:
            bom.finished_product_cost_share = max(0.0, 100.0 - bom.byproduct_cost_share_total)

    @api.constrains('byproduct_ids', 'byproduct_ids.cost_share')
    def _check_byproduct_cost_share_total(self):
        """ US-14-03: 确保副产品成本分摊比例不超过100% """
        for bom in self:
            if bom.byproduct_cost_share_total > 100.0:
                raise ValidationError(_("Byproduct cost share total cannot exceed 100%%. Current total is %s%%") % bom.byproduct_cost_share_total)






# Add the compute and constraint methods to farm.processing.production as well to match test expectations
class FarmProcessingProductionExtension(models.Model):
    _name = 'farm.processing.production'
    _inherit = 'farm.processing.production'

    byproduct_cost_share_total = fields.Float("Byproduct Cost Share Total (%)", compute='_compute_byproduct_cost_share_total_mo', store=True)
    finished_product_cost_share = fields.Float("Finished Product Cost Share (%)", compute='_compute_finished_product_cost_share_mo', store=True)

    # @api.depends('bom_id', 'bom_id.byproduct_cost_share_total')
    def _compute_byproduct_cost_share_total_mo(self):
        for mo in self:
            if mo.bom_id:
                mo.byproduct_cost_share_total = mo.bom_id.byproduct_cost_share_total
            else:
                mo.byproduct_cost_share_total = 0.0

    # @api.depends('bom_id', 'bom_id.finished_product_cost_share')
    def _compute_finished_product_cost_share_mo(self):
        for mo in self:
            if mo.bom_id:
                mo.finished_product_cost_share = mo.bom_id.finished_product_cost_share
            else:
                mo.finished_product_cost_share = 100.0

    @api.constrains('bom_id', 'bom_id.byproduct_cost_share_total')
    def _check_byproduct_cost_share_total_mo(self):
        """ US-14-03: 确保副产品成本分摊比例不超过100% """
        for mo in self:
            if mo.bom_id and mo.bom_id.byproduct_cost_share_total > 100.0:
                raise ValidationError(_("Byproduct cost share total cannot exceed 100%%. Current total is %s%%") % mo.bom_id.byproduct_cost_share_total)