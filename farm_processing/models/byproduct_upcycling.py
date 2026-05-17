from odoo import models, fields, api, _

class MrpProduction(models.Model):
    _inherit = 'mrp.production'
    
    # [US-SCENARIO-37] By-Product Upcycling
    def button_mark_done(self):
        res = super().button_mark_done()
        
        # Trigger secondary MO for specific by-products
        for mo in self:
            # We mock the presence of wet peels in the move_byproduct_ids
            # In a real BOM, this is configured. We trigger an action here.
            if 'Orange' in mo.product_id.name:
                self.env['mrp.production'].create({
                    'product_id': self.env['product.product'].search([('name', 'ilike', 'Pectin')], limit=1).id or mo.product_id.id,
                    'product_qty': mo.product_qty * 0.6, # 60% is peels
                    'origin': f"Upcycled from {mo.name}"
                })
                mo.message_post(body=_("By-product Upcycling: Automatically spawned secondary MO to extract Pectin from wet peels."))
                
        return res

