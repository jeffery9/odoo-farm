from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # 批次属性定义 [US-02]
    lot_properties_definition = fields.PropertiesDefinition('Lot Properties Definition')
