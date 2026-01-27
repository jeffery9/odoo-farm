from odoo import models, fields, api, _
from odoo.exceptions import UserError
from .base_mixins import ComplianceMixin
from .common_fields import CommonAgriculturalFields
import logging

_logger = logging.getLogger(__name__)


class BiologicalAsset(models.Model):
    """
    Biological Asset Management - Core agricultural asset tracking functionality
    US-01-04: Biological Asset Management
    NOTE: Financial valuation functionality has been moved to farm_finance_advanced module
    """
    _name = 'farm.biological.asset'
    _description = 'Biological Asset'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'farm.core.creation.method.mixin', 'farm.core.computed.field.mixin', 'farm.core.compliance.mixin']

    name = fields.Char("Asset Name", required=True, default=lambda self: _('New'))
    lot_id = fields.Many2one('stock.lot', string="Stock Lot", required=True)

    # Inherit common agricultural fields
    agricultural_type = fields.Selection([
        ('animal', 'Animal'),
        ('plant', 'Plant'),
        ('tree', 'Tree'),
    ], string="Asset Type", default='animal')

    birth_date = fields.Date("Birth/Germination Date")
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string="Gender")

    # Parent tracking (pedigree)
    father_id = fields.Many2one('farm.biological.asset', string="Father")
    mother_id = fields.Many2one('farm.biological.asset', string="Mother")

    # Growth and maturity
    growth_stage = fields.Selection([
        ('newborn', 'Newborn/Seedling'),
        ('growing', 'Growing'),
        ('mature', 'Mature/Adult'),
        ('harvested', 'Harvested/Culled')
    ], string="Growth Stage", default='newborn', required=True)

    is_mature = fields.Boolean("Is Mature", compute='_compute_is_mature_from_age', store=True)

    # Generation tracking
    generation = fields.Selection([
        ('g0', 'G0 (Breeder)'),
        ('g1', 'G1 (Foundation)'),
        ('g2', 'G2 (Registered)'),
        ('g3', 'G3 (Commercial)')
    ], string="Generation")

    # Quality and grade
    quality_grade = fields.Selection([
        ('grade_a', 'Grade A'),
        ('grade_b', 'Grade B'),
        ('grade_c', 'Grade C'),
    ], string="Quality Grade")

    # Basic valuation reference (financial valuation now in farm_finance_advanced module)
    current_valuation = fields.Float("Current Valuation", compute='_compute_current_valuation', store=True)

    maturity_date = fields.Date("Maturity Date", compute='_compute_maturity_date', store=True)

    @api.depends('birth_date', 'lot_id.product_id.maturity_age_days')
    def _compute_maturity_date(self):
        """Compute maturity date based on birth date and product maturity age"""
        for asset in self:
            if asset.birth_date and asset.lot_id.product_id.maturity_age_days:
                from datetime import timedelta
                asset.maturity_date = asset.birth_date + timedelta(days=asset.lot_id.product_id.maturity_age_days)
            else:
                asset.maturity_date = False

    @api.depends('birth_date', 'lot_id.product_id.maturity_age_days', 'maturity_date')
    def _compute_is_mature_from_age(self):
        """Compute if asset is mature based on actual dates"""
        from datetime import date
        today = date.today()
        for asset in self:
            asset.is_mature = (asset.maturity_date and asset.maturity_date <= today) or False

    @api.depends('current_valuation')  # Simplified - now references valuation from finance module
    def _compute_current_valuation(self):
        """Compute current valuation - now references finance module for complex calculations"""
        for asset in self:
            # For core functionality, use simple growth-stage-based valuation
            # Complex financial valuation is handled in farm_finance_advanced
            stage_multipliers = {
                'newborn': 0.2,
                'growing': 0.6,
                'mature': 1.0,
                'harvested': 0.0
            }
            multiplier = stage_multipliers.get(asset.growth_stage, 1.0)
            base_value = asset.lot_id.product_id.standard_price or 0.0
            asset.current_valuation = base_value * multiplier