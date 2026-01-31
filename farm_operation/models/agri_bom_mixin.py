from odoo import models, fields, api


class AgriBomMixin(models.AbstractModel):
    """
    Abstract base model for agricultural BOM functionality.
    This mixin provides shared logic across different agricultural BOM implementations.
    """
    _name = 'agri.bom.mixin'
    _description = 'Agri Agricultural BOM Shared Logic'

    # Ekylibre Mapping: Recipe Classification
    agri_activity_type = fields.Selection([
        ('feed', 'Feed Formula'),
        ('fertilizer', 'Fertilizer Mix'),
        ('planting', 'Planting Scheme'),
        ('protection', 'Protection Mix')
    ], string="Agri Activity Type", help="Classify BOM as an agricultural recipe.")

    application_stage = fields.Selection([
        ('seedling', 'Seedling/Nursery'),
        ('growing', 'Growing'),
        ('harvest', 'Harvest'),
        ('finishing', 'Finishing')
    ], string="Application Stage")

    # Fields for BOM lines (for use in the mixin context)
    def _get_agri_bom_line_defaults(self):
        """Get default values for agricultural BOM lines"""
        return {
            'dilution_ratio': 0.0,
            'feeding_ratio': 0.0,
        }


class AgriBomLineMixin(models.AbstractModel):
    """
    Abstract base model for agricultural BOM line functionality.
    """
    _name = 'agri.bom.line.mixin'
    _description = 'Agri Agricultural BOM Line Shared Logic'

    # Dilution ratio for liquid applications
    dilution_ratio = fields.Float(
        "Dilution Ratio (1:N)",
        default=0.0,
        help="If set, the component quantity will be calculated as (Finished Qty / Ratio). E.g. 1:500."
    )

    # Feeding ratio for livestock applications
    feeding_ratio = fields.Float(
        "Feeding Ratio (%)",
        default=0.0,
        help="Percentage of total biomass (Count * Avg Weight) for daily feeding."
    )

    @api.onchange('dilution_ratio', 'feeding_ratio')
    def _onchange_agricultural_ratios(self):
        """Update based on agricultural ratios"""
        # Implementation would adjust quantities based on ratios
        pass