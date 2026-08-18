# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    # Extend selection for Food Processing
    industry_type = fields.Selection(selection_add=[
        ('food_processing', 'Food Processing'),
    ], ondelete={'food_processing': 'set null'})
    
    expected_yield_rate = fields.Float("Expected Yield Rate")
    process_description = fields.Text("Process Description")
    target_temp = fields.Float("Target Temp")
    target_ph = fields.Float("Target pH")
    target_brix = fields.Float("Target Brix")
    target_proofing_time = fields.Float("Target Proofing Time")
    standard_duration = fields.Float("Standard Duration")
    haccp_instructions = fields.Html("HACCP Instructions")
    processing_type = fields.Selection([
        ('primary', 'Primary'),
        ('deep', 'Deep'),
        ('packaging', 'Packaging')
    ], string='Processing Type')
    dilution_ratio = fields.Float("Dilution Ratio")
    sc_category_id = fields.Many2one('farm.sc.category', string='SC License Category')

    def _get_isl_model(self):
        res = super(MrpBom, self)._get_isl_model()
        if self.industry_type in ['food_processing', 'baking', 'winemaking']:
            return 'agri.isl.processing.bom'
        return res

    # --- Processing Specific Fields ---
    grade_distribution_ids = fields.One2many('farm.bom.grade.distribution', 'bom_id', string="Expected Grade Distribution")
    mass_balance_tolerance = fields.Float("Mass Balance Tolerance (%)", default=0.1)
    allergen_ids = fields.Many2many('farm.allergen', 'mrp_bom_farm_allergen_rel', 'bom_id', 'allergen_id', string="Allergens Involved")

class FarmMrpBomExtension(models.Model):
    _inherit = 'mrp.bom'

    is_parameter_required = fields.Boolean("Parameter Required")
    target_temp = fields.Float("Target Temp")
    target_ph = fields.Float("Target pH")
    target_brix = fields.Float("Target Brix")
    target_proofing_time = fields.Float("Target Proofing Time")

class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    ingredient_role = fields.Selection([
        ('raw', 'Raw Material'),
        ('additive', 'Additive'),
        ('packaging', 'Packaging')
    ], string='Ingredient Role')

class FarmBomGradeDistribution(models.Model):
    _name = 'farm.bom.grade.distribution'
    _description = 'Expected Grade Distribution in BOM'

    bom_id = fields.Many2one('mrp.bom', ondelete='cascade')
    quality_grade = fields.Selection([
        ('grade_a', 'Grade A'),
        ('grade_b', 'Grade B'),
        ('grade_c', 'Grade C'),
    ], string='Quality Grade', required=True)
    expected_percentage = fields.Float('Expected %', required=True)
