from odoo import models, fields, api, _

class StockLot(models.Model):
    """
    Agricultural Lot: The carrier of the Quality Fingerprint.
    Injecting Level 0-3 Mixins to stock.lot.
    """
    _name = 'stock.lot'
    _inherit = [
        'stock.lot',
        'agri.view.mixin',           # Level 0: UI Isolation
        'agri.sustainability.mixin', # Level 0: Carbon Track
        'agri.geospatial.mixin',     # Level 1: Location Evidence
        'agri.evidence.mixin',       # Level 2: Audit
        'agri.clearing.mixin',       # Level 3: Clearing & Fingerprint
    ]

    # Level 2: Semantic content for Lot RAG search
    def _get_embedding_content(self):
        self.ensure_one()
        return f"Lot {self.name}: Product {self.product_id.display_name}. " \
               f"Sustainability Credits: {self.impact_credits}. Audit Status: {self.audit_status}."

    def action_view_quality_fingerprint(self):
        """
        Action to display the generated quality fingerprint.
        """
        self.ensure_one()
        if not self.quality_fingerprint:
            self.generate_quality_fingerprint()
        
        return {
            'name': _('Quality Fingerprint - %s') % self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'stock.lot',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }

