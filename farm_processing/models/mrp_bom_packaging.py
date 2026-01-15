from odoo import fields, models, api, _

class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    # US-14-10: 成品包装结构定义
    packaging_line_ids = fields.One2many('farm.bom.package.line', 'bom_id', string="Finished Product Packaging")

class FarmBomPackageLine(models.Model):
    _name = 'farm.bom.package.line'
    _description = 'BOM Finished Product Packaging Line'

    bom_id = fields.Many2one('mrp.bom', string='Bill of Materials', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Product', required=True, help="The finished product this packaging applies to.")
    package_level_id = fields.Many2one('farm.package.level', string='Package Level', required=True, help="e.g., Inner Carton, Pallet")
    quantity = fields.Float(string='Quantity per Package', required=True, default=1.0, help="How many products/inner packages are in this package level.")
    child_package_level_id = fields.Many2one('farm.package.level', string='Contains Package Level', help="This package level contains packages of this type.")
    
    _sql_constraints = [
        ('quantity_positive', 'CHECK(quantity > 0)', 'Quantity per package must be positive!'),
        ('unique_packaging_per_product_level', 'unique(bom_id, product_id, package_level_id)', 'A product can only have one packaging definition per level in a BOM.')
    ]

# US-04-03: 副产品成本分摊
class MrpBomByproduct(models.Model):
    _inherit = 'mrp.bom.byproduct'

    cost_share = fields.Float("Cost Share (%)", help="Percentage of the total BOM cost allocated to this byproduct. [US-04-03]")