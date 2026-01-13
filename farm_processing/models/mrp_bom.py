from odoo import models, fields, api, _

class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    processing_type = fields.Selection([
        ('primary', 'Primary'),
        ('deep', 'Deep'),
        ('packaging', 'Packaging')
    ], string='Processing Type', default='primary')

    industry_type = fields.Selection([
        ('standard', 'Standard'),
        ('baking', 'Baking (烘焙)'),
        ('winemaking', 'Winemaking (酿酒)'),
        ('food_processing', 'Food Processing (食品加工)')
    ], string="Industry Type", default='standard')

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

class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    ingredient_role = fields.Selection([
        ('main', 'Main Material (主料)'),
        ('additive', 'Additive (添加剂)'),
        ('yeast', 'Fermentation Agent (发酵剂/菌种)'),
        ('packaging', 'Packaging (包材)')
    ], string="Ingredient Role", default='main')

class FarmBomGradeDistribution(models.Model):
    _name = 'farm.bom.grade.distribution'
    _description = 'Expected Grade Distribution in BOM'

    bom_id = fields.Many2one('mrp.bom', ondelete='cascade')
    quality_grade = fields.Selection([
        ('grade_a', 'Grade A (特级/优等)'),
        ('grade_b', 'Grade B (一级/合格)'),
        ('grade_c', 'Grade C (二级/次品)'),
    ], string="Quality Grade", required=True)
    expected_percentage = fields.Float("Expected %", required=True)
