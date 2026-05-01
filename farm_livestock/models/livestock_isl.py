# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class FarmLivestockBom(models.Model):
    _name = 'farm.livestock.bom'
    _description = 'Livestock Breeding BOM (ISL Layer)'
    _inherits = {'mrp.bom': 'bom_id'}
    _inherit = ['agri.bom.mixin']

    bom_id = fields.Many2one('mrp.bom', string='Base BOM', required=True, ondelete='cascade')

    # Livestock Specifics
    growth_days_expected = fields.Integer("Expected Growth Days")
    daily_feed_intake = fields.Float("Avg Daily Feed (kg)")

class FarmLotLivestock(models.Model):
    _name = 'farm.lot.livestock'
    _description = 'Livestock Asset Lot (ISL Layer)'
    _inherits = {'stock.lot': 'lot_id'}
    _inherit = [
        'agri.growth.cycle.mixin',
        'agri.biological.inventory.mixin',
        'agri.biological.valuation.mixin',
        'agri.certification.status.mixin'
    ]

    lot_id = fields.Many2one('stock.lot', string='Base Lot', required=True, ondelete='cascade')

    # [US-64-01] 个体动物档案管理
    birth_date = fields.Date("Birth Date")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender")
    current_weight = fields.Float("Weight (kg)")

    # [US-64-04] 生殖与繁殖管理
    breeding_status = fields.Selection([
        ('immature', 'Immature'),
        ('open', 'Open'),
        ('in_heat', 'In Heat'),
        ('pregnant', 'Pregnant'),
        ('lactating', 'Lactating'),
        ('dry', 'Dry')
    ], string="Breeding Status", default='immature')

    # [US-64-02] 智能健康监测
    health_index = fields.Float("Health Index (0-100)", default=100.0)
    last_vet_check = fields.Date("Last Veterinary Check")

    # [US-64-06] 产量与性能分析
    fcr_actual = fields.Float("Actual FCR", compute='_compute_performance_metrics')
    avg_daily_gain = fields.Float("Actual ADG (kg/day)", compute='_compute_performance_metrics')

    def _compute_performance_metrics(self):
        for rec in self:
            # Aggregate data from completed production orders
            orders = self.env['farm.livestock.production'].search([
                ('production_id.lot_producing_id', '=', rec.lot_id.id),
                ('production_id.state', '=', 'done')
            ])
            if orders:
                rec.fcr_actual = sum(orders.mapped('fcr')) / len(orders)
                # Simplified ADG calculation
                rec.avg_daily_gain = sum(orders.mapped('avg_daily_gain_recorded')) / len(orders) if hasattr(orders, 'avg_daily_gain_recorded') else 0.5
            else:
                rec.fcr_actual = 0.0
                rec.avg_daily_gain = 0.0

    @api.model_create_multi
    def create(self, vals_list):
        """ [Bridge] Initialize DNA when purchased or received. """
        records = super(FarmLotLivestock, self).create(vals_list)
        for rec in records:
            # Auto-assign initial weight from product standard if missing
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

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        """ [ISL Bridge] Enforce industry gates before picking confirmation. """
        for picking in self:
            for move in picking.move_line_ids:
                if move.lot_id:
                    # Look for livestock proxy
                    livestock_lot = self.env['farm.lot.livestock'].search([('lot_id', '=', move.lot_id.id)], limit=1)
                    if livestock_lot:
                        livestock_lot.action_check_harvest_safety()
        return super(StockPicking, self).button_validate()

class FarmLivestockProduction(models.Model):
    _name = 'farm.livestock.production'
    _description = 'Livestock Growth Order (ISL Layer)'
    _inherits = {'mrp.production': 'production_id'}
    _inherit = [
        'agri.intervention.mixin',
        'agri.quality.gate.mixin',
        'agri.odoo19.performance.security.mixin'  # Added Odoo 19 performance and security mixin
    ]

    production_id = fields.Many2one('mrp.production', string='Base Production Order', required=True, ondelete='cascade')

    # Weight Gain & Efficiency (Moved from Base)
    initial_total_weight = fields.Float("Initial Total Weight (kg)")
    final_total_weight = fields.Float("Final Total Weight (kg)")

    # Enhanced with Odoo 19 precompute for performance
    fcr = fields.Float(
        "Feed Conversion Ratio (FCR)",
        compute='_compute_fcr_isl',
        precompute=True,  # Use precompute for immediate calculation during creation
        store=True
    )

    avg_daily_gain_recorded = fields.Float("Recorded ADG (kg/day)", compute='_compute_fcr_isl')

    # Use JSON for flexible configuration
    livestock_config = fields.Json(
        "Livestock Configuration",
        default=dict,
        help="JSON-based configuration for livestock-specific parameters"
    )

    # --- Polymorphic Link (US-TECH-06-26) ---
    livestock_bom_id = fields.Many2one('farm.livestock.bom', string='Livestock Recipe', compute='_compute_livestock_bom_id')

    def _compute_livestock_bom_id(self):
        """ Automatically up-cast base bom_id to ISL livestock.bom. """
        for rec in self:
            if rec.bom_id:
                rec.livestock_bom_id = self.env['farm.livestock.bom'].search([('bom_id', '=', rec.bom_id.id)], limit=1)
            else:
                rec.livestock_bom_id = False

    @api.depends('initial_total_weight', 'final_total_weight', 'production_id.product_qty', 'production_id.date_start', 'production_id.date_finished')
    def _compute_fcr_isl(self):
        for rec in self:
            gain = rec.final_total_weight - rec.initial_total_weight
            # FCR = Total Feed / Total Weight Gain
            # Assuming product_qty is the feed amount for simplicity in this context,
            # or it's linked via analytics.
            rec.fcr = (rec.production_id.product_qty / gain) if gain > 0 else 0.0

            # ADG calculation
            if rec.production_id.date_start and rec.production_id.date_finished:
                days = (rec.production_id.date_finished - rec.production_id.date_start).days or 1
                rec.avg_daily_gain_recorded = gain / (days * (rec.production_id.product_qty or 1.0)) # per head approx
            else:
                rec.avg_daily_gain_recorded = 0.0

    def isl_post_done(self):
        """ US-TECH-06-27: Update resulting lot metadata with ISL weight data. """
        self.ensure_one()
        if self.production_id.lot_producing_id:
            lot = self.production_id.lot_producing_id
            # Search for ISL lot record
            isl_lot = self.env['farm.lot.livestock'].search([('lot_id', '=', lot.id)], limit=1)
            if isl_lot:
                isl_lot.current_weight = self.final_total_weight / (self.production_id.product_qty or 1.0)
                # Create a weight measurement event [US-64-01]
                self.env['farm.livestock.event'].create({
                    'lot_id': lot.id,
                    'event_type': 'weight',
                    'measured_weight': isl_lot.current_weight,
                    'event_date': fields.Datetime.now(),
                    'notes': _("Auto-recorded from Production Order %s") % self.production_id.name
                })