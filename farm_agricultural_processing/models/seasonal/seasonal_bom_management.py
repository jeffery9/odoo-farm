# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class AgriInterventionSeasonalBom(models.Model):
    """
    US-004-06: 季节性"版本化"配方管理 [Refactored to Agri Domain]
    - 管理季节性配方变化
    - 支持为同一产品创建不同季节的配方版本
    Refactored from farm.seasonal.bom with 100% logic retention.
    """
    _name = 'agri.intervention.seasonal.bom'
    _description = 'Seasonal Versioned Recipe Management'
    _order = 'product_tmpl_id, season_start_date'

    name = fields.Char(
        "Seasonal Recipe Name",
        required=True,
        default=lambda self: self._default_name()
    )

    product_tmpl_id = fields.Many2one(
        'product.template',
        string="Product",
        required=True,
        help="Product that this seasonal recipe is for"
    )

    bom_id = fields.Many2one(
        'mrp.bom',
        string="Base BOM",
        required=True,
        help="Base BOM to be used as template for seasonal variations"
    )

    season_name = fields.Char(
        "Season Name",
        required=True,
        help="Name of the season (e.g., Spring, Summer, Winter)"
    )

    season_description = fields.Text("Season Description")

    # Season period
    season_start_date = fields.Date(
        "Season Start Date",
        required=True,
        help="Start date of this seasonal recipe validity"
    )

    season_end_date = fields.Date(
        "Season End Date",
        required=True,
        help="End date of this seasonal recipe validity"
    )

    # Seasonal adjustments to the base BOM
    seasonal_material_ids = fields.One2many(
        'agri.intervention.seasonal.bom.material',
        'seasonal_bom_id',
        string="Seasonal Material Adjustments"
    )

    seasonal_parameter_ids = fields.One2many(
        'agri.intervention.seasonal.bom.parameter',
        'seasonal_bom_id',
        string="Seasonal Parameter Adjustments"
    )

    # Versioning
    version_number = fields.Integer("Version", default=1, required=True)
    version_name = fields.Char("Version Name", help="e.g., Summer 2024 v1.0")

    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ], string="Status", default='draft')

    # Additional seasonal-specific fields
    is_seasonal_adjustment = fields.Boolean(
        "Has Seasonal Adjustment",
        compute='_compute_has_seasonal_adjustment',
        store=True
    )

    base_yield_factor = fields.Float(
        "Base Yield Factor",
        default=1.0,
        help="Base yield factor for this seasonal recipe"
    )

    seasonal_yield_factor = fields.Float(
        "Seasonal Yield Factor",
        compute='_compute_seasonal_yield_factor',
        store=True,
        help="Yield factor adjusted for season"
    )

    @api.model
    def _default_name(self):
        return "Seasonal Recipe %s" % fields.Date.today()

    @api.constrains('season_start_date', 'season_end_date')
    def _check_season_dates(self):
        """Ensure season end date is after start date"""
        for record in self:
            if record.season_start_date and record.season_end_date:
                if record.season_start_date > record.season_end_date:
                    raise ValidationError(_("Season end date must be after start date."))

    @api.constrains('product_tmpl_id', 'season_start_date', 'season_end_date')
    def _check_overlapping_seasons(self):
        """Ensure no overlapping seasons for the same product"""
        for record in self:
            overlapping = self.search([
                ('id', '!=', record.id),
                ('product_tmpl_id', '=', record.product_tmpl_id.id),
                ('season_start_date', '<=', record.season_end_date),
                ('season_end_date', '>=', record.season_start_date),
                ('state', '=', 'active'),
            ])
            if overlapping:
                raise ValidationError(_(
                    "Seasonal recipes cannot overlap for the same product. "
                    "Overlapping with: %s" % ', '.join(overlapping.mapped('name'))
                ))

    @api.depends('seasonal_material_ids', 'seasonal_parameter_ids')
    def _compute_has_seasonal_adjustment(self):
        for record in self:
            record.is_seasonal_adjustment = bool(record.seasonal_material_ids or record.seasonal_parameter_ids)

    @api.depends('base_yield_factor')
    def _compute_seasonal_yield_factor(self):
        for record in self:
            # In a real implementation, this would factor in seasonal conditions
            record.seasonal_yield_factor = record.base_yield_factor

    def action_activate(self):
        """Activate this seasonal recipe"""
        self.ensure_one()
        self.write({'state': 'active'})
        return True

    def action_deactivate(self):
        """Deactivate this seasonal recipe"""
        self.ensure_one()
        self.write({'state': 'inactive'})
        return True

    def get_applicable_seasonal_bom(self, product_id, date=None):
        """
        Get applicable seasonal BOM for a product on a specific date
        """
        if not date:
            date = fields.Date.today()

        seasonal_bom = self.search([
            ('product_tmpl_id', '=', product_id),
            ('season_start_date', '<=', date),
            ('season_end_date', '>=', date),
            ('state', '=', 'active'),
        ], limit=1)

        return seasonal_bom

    def apply_seasonal_adjustments(self, base_bom):
        """
        Apply seasonal adjustments to a base BOM
        """
        self.ensure_one()
        # This would contain the logic to create an adjusted BOM based on seasonal factors
        # For now, we return the base BOM with seasonal info
        result = base_bom.copy()
        result.name = f"{base_bom.name} - {self.season_name} Season"
        return result

    def action_view_seasonal_materials(self):
        """Open a view to see seasonal material adjustments"""
        self.ensure_one()
        action = {
            'type': 'ir.actions.act_window',
            'name': _('Seasonal Material Adjustments'),
            'res_model': 'agri.intervention.seasonal.bom.material',
            'view_mode': 'list,form',
            'domain': [('seasonal_bom_id', '=', self.id)],
            'context': {'default_seasonal_bom_id': self.id},
        }
        return action

    def action_view_seasonal_parameters(self):
        """Open a view to see seasonal parameter adjustments"""
        self.ensure_one()
        action = {
            'type': 'ir.actions.act_window',
            'name': _('Seasonal Parameter Adjustments'),
            'res_model': 'agri.intervention.seasonal.bom.parameter',
            'view_mode': 'list,form',
            'domain': [('seasonal_bom_id', '=', self.id)],
            'context': {'default_seasonal_bom_id': self.id},
        }
        return action


class AgriInterventionSeasonalBomMaterial(models.Model):
    """
    季节性材料调整 [Refactored to Agri Domain]
    """
    _name = 'agri.intervention.seasonal.bom.material'
    _description = 'Seasonal BOM Material Adjustment'

    seasonal_bom_id = fields.Many2one(
        'agri.intervention.seasonal.bom',
        string="Seasonal BOM",
        required=True,
        ondelete='cascade'
    )

    product_id = fields.Many2one(
        'product.product',
        string="Material",
        required=True
    )

    base_qty = fields.Float("Base Quantity", required=True)
    seasonal_qty = fields.Float("Seasonal Quantity", required=True)
    qty_difference = fields.Float("Quantity Difference", compute='_compute_qty_difference', store=True, precompute=True)

    adjustment_reason = fields.Text("Adjustment Reason", help="Why this material quantity changes by season")

    @api.depends('base_qty', 'seasonal_qty')
    def _compute_qty_difference(self):
        for record in self:
            record.qty_difference = record.seasonal_qty - record.base_qty

    @api.onchange('product_id')
    def _onchange_product_id(self):
        """Set base quantity from original BOM if possible"""
        if self.seasonal_bom_id and self.product_id:
            # Try to find the base quantity from the original BOM
            base_bom_line = self.seasonal_bom_id.bom_id.bom_line_ids.filtered(
                lambda l: l.product_id == self.product_id
            )
            if base_bom_line:
                self.base_qty = base_bom_line.product_qty


class AgriInterventionSeasonalBomParameter(models.Model):
    """
    季节性参数调整 [Refactored to Agri Domain]
    """
    _name = 'agri.intervention.seasonal.bom.parameter'
    _description = 'Seasonal BOM Parameter Adjustment'

    seasonal_bom_id = fields.Many2one(
        'agri.intervention.seasonal.bom',
        string="Seasonal BOM",
        required=True,
        ondelete='cascade'
    )

    parameter_name = fields.Char("Parameter Name", required=True)
    base_value = fields.Float("Base Value", required=True)
    seasonal_value = fields.Float("Seasonal Value", required=True)
    value_difference = fields.Float("Value Difference", compute='_compute_value_difference', store=True, precompute=True)

    unit_of_measure = fields.Char("Unit of Measure")
    adjustment_reason = fields.Text("Adjustment Reason", help="Why this parameter changes by season")

    @api.depends('base_value', 'seasonal_value')
    def _compute_value_difference(self):
        for record in self:
            record.value_difference = record.seasonal_value - record.base_value