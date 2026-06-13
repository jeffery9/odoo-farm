from odoo import models, fields, api, _

class MrpBom(models.Model):
    """
    Agricultural Recipe (BOM):
    Injecting Nutrient and View Mixins to transform industrial BOM into Bio-Recipe.
    """
    _name = 'mrp.bom'
    _inherit = [
        'mrp.bom', 
        'agri.bom.mixin',
        'agri.view.mixin',           # Level 0: UI Isolation
        'agri.nutrient.mixin',       # Level 1: Nutrient Composition
        'agri.sustainability.mixin', # Level 0: Standard
    ]

    def _get_embedding_content(self):
        self.ensure_one()
        return f"Recipe {self.code or self.product_tmpl_id.name}: N={self.nitrogen_qty}, P={self.phosphorus_qty}."

class MrpBomLine(models.Model):
    _name = 'mrp.bom.line'
    _inherit = [
        'mrp.bom.line', 
        'agri.bom.line.mixin',
        'agri.nutrient.mixin', 
    ]