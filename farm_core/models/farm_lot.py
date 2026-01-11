from odoo import models, fields

class FarmLot(models.Model):
    _inherit = 'stock.lot'

    is_animal = fields.Boolean("Is Biological Asset", default=False)
    birth_date = fields.Date("Birth/Germination Date")
    gender = fields.Selection([
        ('male', 'Male (公)'),
        ('female', 'Female (母)'),
        ('other', 'Other (其他/无)')
    ], string="Gender")
    
    # 系谱跟踪 [US-32] 预留
    father_id = fields.Many2one('stock.lot', string="Father (父本)", domain="[('product_id', '=', product_id)]")
    mother_id = fields.Many2one('stock.lot', string="Mother (母本)", domain="[('product_id', '=', product_id)]")
    
    # 状态
    biological_stage = fields.Selection([
        ('newborn', 'Newborn/Seedling (幼龄)'),
        ('growing', 'Growing (生长)'),
        ('mature', 'Mature/Adult (成年)'),
        ('harvested', 'Harvested/Culled (已收获/淘汰)')
    ], string="Biological Stage", default='newborn')

    # 质量等级 [US-08]
    quality_grade = fields.Selection([
        ('grade_a', 'Grade A (特级/优等)'),
        ('grade_b', 'Grade B (一级/合格)'),
        ('grade_c', 'Grade C (二级/次品)'),
    ], string="Quality Grade")

    # 动态属性 [US-02]
    lot_properties = fields.Properties(
        'Properties',
        definition='product_id.lot_properties_definition'
    )
