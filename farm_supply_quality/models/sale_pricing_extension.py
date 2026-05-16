from odoo import models, fields, api, _

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    agri_lot_id = fields.Many2one('stock.lot', string="Specific Agri Lot")
    quality_premium_applied = fields.Boolean("Quality Premium Applied", default=False)

    @api.onchange('agri_lot_id', 'product_id')
    def _onchange_agri_lot_pricing(self):
        """
        [US-COMMERCE-01] Dynamic Quality-Based Pricing
        If a specific lot is selected and it has a 'premium' quality grade,
        automatically apply a 30% price surcharge to reward high quality.
        """
        if not self.agri_lot_id:
            if self.quality_premium_applied:
                # Reset if lot removed
                self.price_unit = self.product_id.list_price
                self.quality_premium_applied = False
            return

        # Read the quality grade from the lot
        # Assume 'quality_grade' exists on stock.lot from farm_core/farm_isl
        if hasattr(self.agri_lot_id, 'quality_grade'):
            if self.agri_lot_id.quality_grade == 'premium' and not self.quality_premium_applied:
                self.price_unit = self.price_unit * 1.30 # 30% Premium
                self.quality_premium_applied = True
                
                # Optional: Add a note to the description
                if self.name:
                    self.name += "\n* Includes 30% Premium Surcharge for Top-Grade Quality."
            elif self.agri_lot_id.quality_grade != 'premium' and self.quality_premium_applied:
                # Revert if changed to a non-premium lot
                self.price_unit = self.product_id.list_price
                self.quality_premium_applied = False
