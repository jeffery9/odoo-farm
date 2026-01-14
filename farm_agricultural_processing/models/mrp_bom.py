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
        ('baking', 'Baking'),
        ('winemaking', 'Winemaking'),
        ('food_processing', 'Food Processing')
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

    # US-14-16: 损耗容差管理
    max_loss_rate = fields.Float("Max Allowable Loss Rate (%)", help="Maximum allowable loss rate for this process. Exceeding this will trigger hard blocking.")

class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    ingredient_role = fields.Selection([
        ('main', 'Main Material'),
        ('additive', 'Additive'),
        ('yeast', 'Fermentation Agent'),
        ('packaging', 'Packaging')
    ], string="Ingredient Role", default='main')

class FarmBomGradeDistribution(models.Model):
    _name = 'farm.bom.grade.distribution'
    _description = 'Expected Grade Distribution in BOM'

    bom_id = fields.Many2one('mrp.bom', ondelete='cascade')
    quality_grade = fields.Selection([
        ('grade_a', 'Grade A'),
        ('grade_b', 'Grade B'),
        ('grade_c', 'Grade C'),
    ], string="Quality Grade", required=True)
    expected_percentage = fields.Float("Expected %", required=True)
