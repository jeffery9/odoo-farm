from odoo import models, fields, api, _

class AgriPurchaseOrder(models.Model):
    """
    Purchase Order: Transformed into Resource Input Covenant.
    Injects Sustainability Mixin to track supplier-side ESG and Carbon.
    """
    _name = 'purchase.order'
    _inherit = [
        'purchase.order',
        'agri.sustainability.mixin', # Level 0: Value Standard
        'agri.view.mixin',           # Level 0: UI Isolation
    ]
    _description = 'Resource Input Covenant'

    def action_verify_covenant_sustainability(self):
        """Verifies if the purchased inputs meet community standards."""
        for line in self.order_line:
            if line.carbon_intensity > 50.0:
                self.is_eco_blocked = True
                self.message_post(body=_("Covenant Blocked: Line %s exceeds carbon threshold.") % line.product_id.name)
        return True


class AgriPurchaseOrderLine(models.Model):
    """
    Purchase Order Line: Detailed physical characteristics of inputs.
    Injects Nutrient Mixin for source-level mass balance tracking.
    """
    _name = 'purchase.order.line'
    _inherit = [
        'purchase.order.line',
        'agri.nutrient.mixin',       # Level 1: Mass Balance
        'agri.sustainability.mixin', # Level 0: Value Standard
    ]
    _description = 'Covenant Line'

    @api.onchange('product_id')
    def _onchange_product_nutrient_sync(self):
        """Syncs default nutrient values from product template."""
        if self.product_id:
            self.nitrogen_qty = self.product_id.nitrogen_qty
            self.phosphorus_qty = self.product_id.phosphorus_qty
            self.potassium_qty = self.product_id.potassium_qty
            self.carbon_intensity = self.product_id.carbon_intensity
