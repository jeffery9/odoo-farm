from odoo import models, fields, api, _

class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    # [US-SCENARIO-40] Dynamic FEFO Smart Logistics
    ripeness_index = fields.Float("Average Ripeness Index (0-100)", compute="_compute_ripeness")
    routing_strategy = fields.Selection([
        ('local', 'Local Hub (Fast Ripening)'),
        ('export', 'Export Route (Hardy)'),
        ('standard', 'Standard')
    ], default='standard')
    
    def _compute_ripeness(self):
        for picking in self:
            # Mock ripeness from Biological Twin
            picking.ripeness_index = 80.0 if picking.partner_id.name == 'FastMarket' else 40.0
            
    def action_fefo_routing(self):
        for picking in self:
            if picking.ripeness_index > 75.0:
                picking.routing_strategy = 'local'
                picking.message_post(body=_("FEFO Triggered: High ripeness index. Re-routing to Local Hub."))
            elif picking.ripeness_index < 50.0:
                picking.routing_strategy = 'export'
                picking.message_post(body=_("FEFO Triggered: Low ripeness index. Cleared for 14-day Export Route."))

