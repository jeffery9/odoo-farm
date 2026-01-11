from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # 批次属性定义 [US-02]
    lot_properties_definition = fields.PropertiesDefinition('Lot Properties Definition')

    # 养分含量 [US-07]
    n_content = fields.Float("Nitrogen (N) %", help="Nitrogen percentage content")
    p_content = fields.Float("Phosphorus (P) %", help="Phosphorus percentage content")
    k_content = fields.Float("Potassium (K) %", help="Potassium percentage content")
