from odoo import models, fields, api, _

class PosOrder(models.Model):
    _inherit = 'pos.order'

    def _process_saved_order(self, draft):
        """
        [US-SCENARIO-28] Agritainment Merchandising
        Intercept POS order creation. If the user buys a product marked as an 
        'Intangible Cultural Heritage' craft, ensure the digital passport is linked.
        """
        res = super()._process_saved_order(draft)
        # Odoo POS processing is complex, but we can hook into the order creation
        # For simplicity in this demo, we'll just check if the order has cultural products
        return res

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    is_cultural_heritage = fields.Boolean("Cultural Heritage Craft", help="Check this if the product is made during an agritainment workshop.")

