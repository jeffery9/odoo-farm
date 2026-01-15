# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class FarmAgriProduct(models.Model):
    _name = 'farm.agri.product'
    _description = 'Specialized Agricultural Product (ISL Layer)'
    _inherits = {'product.template': 'product_tmpl_id'}

    product_tmpl_id = fields.Many2one('product.template', string='Base Product Template', required=True, ondelete='cascade')
    
    # --- Specialized Metadata (Sunk from Base) ---
    industry_tag = fields.Selection([
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
