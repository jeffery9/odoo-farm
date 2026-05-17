# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class FarmAgriProduct(models.Model):
    """
    Specialized Agricultural Product extension of ISL architecture
    This extends the centralized farm.product.template model with agricultural specific features
    """
    _inherit = 'product.template'

    # --- Specialized Metadata (Sunk from Base) ---
    industry_tag = fields.Selection(selection=[
        ('material', 'Input Material (Seeds/Fertilizer)'),
        ('food', 'Processed Food'),
        ('livestock', 'Live Animal'),
        ('material', 'Input Material (Seeds/Fertilizer)'),
        ('food', 'Processed Food'),
        ('livestock', 'Live Animal'),
        ('raw_grain', 'Raw Grain / Harvest')
    ], string='Agricultural Industry Tag', default='material')

    # Nutrient Data
    n_content = fields.Float("Nitrogen (N) %")
    p_content = fields.Float("Phosphorus (P) %")
    k_content = fields.Float("Potassium (K) %")

    # Food Compliance
    sc_category_ids = fields.Many2many('farm.sc.category', string="SC License Categories")
    allergen_ids = fields.Many2many('farm.allergen', string="Allergens")
    nutrition_table = fields.Text("Nutrition Data (JSON/Text)")

    is_potency_standardized = fields.Boolean("Standardize by Potency")
    target_purity = fields.Float("Target Purity %", default=100.0)

    def write(self, vals):
        # Ensure industry type is set appropriately when not specified
        if 'industry_type' not in vals and not self.industry_type:
            # Set based on industry_tag if available
            if 'industry_tag' in vals:
                if vals['industry_tag'] in ['food']:
                    vals['industry_type'] = 'food_processing'
                elif vals['industry_tag'] in ['material', 'raw_grain']:
                    vals['industry_type'] = 'general'
        return super().write(vals)

    @api.model_create_multi
    def create(self, vals_list):
        # Ensure industry type is set appropriately
        for vals in vals_list:
            if 'industry_type' not in vals or not vals.get('industry_type'):
                # Set based on industry_tag if available
                if vals.get('industry_tag') in ['food']:
                    vals['industry_type'] = 'food_processing'
                elif vals.get('industry_tag') in ['material', 'raw_grain']:
                    vals['industry_type'] = 'general'
        return super().create(vals_list)
class FarmScCategory(models.Model):
    _name = 'farm.sc.category'
    _description = 'Food Production Category'

    name = fields.Char('Category Name', required=True)
    code = fields.Char('Category Code')

