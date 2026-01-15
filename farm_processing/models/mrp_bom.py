# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    # Extend selection for Food Processing
    industry_type = fields.Selection(selection_add=[
        ('food_processing', 'Food Processing'),
        ('baking', 'Baking'),
        ('winemaking', 'Winemaking'),
    ])

    def _get_isl_model(self):
        res = super(MrpBom, self)._get_isl_model()
        if self.industry_type in ['food_processing', 'baking', 'winemaking']:
            return 'farm.processing.bom'
        return res

    # --- Processing Specific Fields (only if they MUST stay in base for some reason, 
    # but preferably move to farm.processing.bom) ---
    grade_distribution_ids = fields.One2many('farm.bom.grade.distribution', 'bom_id', string="Expected Grade Distribution")
    mass_balance_tolerance = fields.Float("Mass Balance Tolerance (%)", default=0.1)
    allergen_ids = fields.Many2many('farm.allergen', string="Allergens Involved")