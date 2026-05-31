# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class FarmLivestockRecipe(models.Model):
    """
    Livestock Breeding Recipe (ISL Layer) [De-industrialized]
    """
    _name = 'agri.isl.livestock.recipe'
    _description = 'Livestock Breeding Recipe'
    _inherits = {'mrp.bom': 'recipe_id'}
    _inherit = ['agri.bom.mixin']

    recipe_id = fields.Many2one('mrp.bom', string='Base Recipe', required=True, ondelete='cascade')

    # Livestock Specifics
    growth_days_expected = fields.Integer("Expected Growth Days")
    daily_feed_intake = fields.Float("Avg Daily Feed (kg)")

class FarmLotLivestock(models.Model):
    """
    Livestock Asset Lot (ISL Layer) [De-industrialized]
    """
    _name = 'agri.isl.lot.livestock'
    _description = 'Livestock Asset Lot'
    _inherits = {'stock.lot': 'lot_id'}
    _inherit = [
        'agri.growth.cycle.mixin',
        'agri.biological.inventory.mixin',
        'agri.biological.valuation.mixin',
        'agri.certification.status.mixin'
    ]

    lot_id = fields.Many2one('stock.lot', string='Base Lot', required=True, ondelete='cascade')

    # [US-094-01] 个体动物档案管理
    birth_date = fields.Date("Birth Date")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender")
    current_weight = fields.Float("Weight (kg)")

    # [US-094-04] 生殖与繁殖管理
    breeding_status = fields.Selection([
        ('immature', 'Immature'),
        ('open', 'Open'),
        ('in_heat', 'In Heat'),
        ('pregnant', 'Pregnant'),
        ('lactating', 'Lactating'),
        ('dry', 'Dry')
    ], string="Breeding Status", default='immature')

    # [US-094-02] 智能健康监测
    health_index = fields.Float("Health Index (0-100)", default=100.0)
    last_vet_check = fields.Date("Last Veterinary Check")

    # [US-094-06] 产量与性能分析
    fcr_actual = fields.Float("Actual FCR", compute='_compute_performance_metrics')
    avg_daily_gain = fields.Float("Actual ADG (kg/day)", compute='_compute_performance_metrics')

    def _compute_performance_metrics(self):
        for rec in self:
            # Aggregate data from completed tasks
            orders = self.env['agri.isl.livestock.task'].search([
                ('intervention_id.lot_producing_id', '=', rec.lot_id.id),
                ('intervention_id.state', '=', 'done')
            ])
            if orders:
                rec.fcr_actual = sum(orders.mapped('fcr')) / len(orders)
                rec.avg_daily_gain = sum(orders.mapped('avg_daily_gain_recorded')) / len(orders) if hasattr(orders, 'avg_daily_gain_recorded') else 0.5
            else:
                rec.fcr_actual = 0.0
                rec.avg_daily_gain = 0.0

    @api.model_create_multi
    def create(self, vals_list):
        """ [Bridge] Initialize DNA when purchased or received. """
        records = super(FarmLotLivestock, self).create(vals_list)
        for rec in records:
            if not rec.average_weight:
                rec.average_weight = rec.product_id.weight or 0.0
            rec.animal_count = rec.product_qty or 1
        return records

    def action_check_harvest_safety(self):
        """ [DNA Gate] Enforce PHI check. """
        today = fields.Date.today()
        if self.withdrawal_end_date and self.withdrawal_end_date > today:
            raise UserError(_("BIOSECURITY BLOCK: Livestock Lot %s is in PHI until %s.") %
                           (self.lot_id.name, self.withdrawal_end_date))
        return True

class FarmLivestockTask(models.Model):
    """
    Livestock Growth Task (ISL Layer) [De-industrialized]
    """
    _name = 'agri.isl.livestock.task'
    _description = 'Livestock Growth Task'
    _inherits = {'mrp.production': 'intervention_id'}
    _inherit = [
        'agri.intervention.mixin',
        'agri.quality.gate.mixin',
        'agri.odoo19.performance.security.mixin'
    ]

    intervention_id = fields.Many2one('mrp.production', string='Base Intervention', required=True, ondelete='cascade')

    # Weight Gain & Efficiency
    initial_total_weight = fields.Float("Initial Total Weight (kg)")
    final_total_weight = fields.Float("Final Total Weight (kg)")

    fcr = fields.Float(
        "Feed Conversion Ratio (FCR)",
        compute='_compute_fcr_isl',
        precompute=True,
        store=True
    )

    avg_daily_gain_recorded = fields.Float("Recorded ADG (kg/day)", compute="_compute_fcr_isl", precompute=True, store=True)

    livestock_config = fields.Json(
        "Livestock Configuration",
        default=dict,
        help="JSON-based configuration for livestock-specific parameters"
    )

    # --- Polymorphic Link ---
    livestock_recipe_id = fields.Many2one('agri.isl.livestock.recipe', string='Livestock Recipe', compute='_compute_livestock_recipe_id')

    def _compute_livestock_recipe_id(self):
        """ Automatically up-cast base recipe_id to ISL livestock.recipe. """
        for rec in self:
            if rec.recipe_id:
                rec.livestock_recipe_id = self.env['agri.isl.livestock.recipe'].search([('recipe_id', '=', rec.recipe_id.id)], limit=1)
            else:
                rec.livestock_recipe_id = False

    @api.depends('initial_total_weight', 'final_total_weight', 'intervention_id.product_qty', 'intervention_id.date_start', 'intervention_id.date_finished')
    def _compute_fcr_isl(self):
        for rec in self:
            gain = rec.final_total_weight - rec.initial_total_weight
            rec.fcr = (rec.intervention_id.product_qty / gain) if gain > 0 else 0.0

            if rec.intervention_id.date_start and rec.intervention_id.date_finished:
                days = (rec.intervention_id.date_finished - rec.intervention_id.date_start).days or 1
                rec.avg_daily_gain_recorded = gain / (days * (rec.intervention_id.product_qty or 1.0))
            else:
                rec.avg_daily_gain_recorded = 0.0

    def isl_post_done(self):
        """ US-TECH-06-27: Update resulting lot metadata with ISL weight data. """
        self.ensure_one()
        if self.intervention_id.lot_producing_id:
            lot = self.intervention_id.lot_producing_id
            isl_lot = self.env['agri.isl.lot.livestock'].search([('lot_id', '=', lot.id)], limit=1)
            if isl_lot:
                isl_lot.current_weight = self.final_total_weight / (self.intervention_id.product_qty or 1.0)
                self.env['farm.livestock.event'].create({
                    'lot_id': lot.id,
                    'event_type': 'weight',
                    'measured_weight': isl_lot.current_weight,
                    'event_date': fields.Datetime.now(),
                    'notes': _("Auto-recorded from Intervention %s") % self.intervention_id.name
                })
