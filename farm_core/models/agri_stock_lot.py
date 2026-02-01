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
        'agri.traceability.mixin',   # [NEW] Level 1: Traceability Fingerprint
        'agri.geospatial.mixin',     # Level 1: Location Evidence
        'agri.nutrient.mixin',       # Level 1: Mass Balance DNA
        'agri.certification.status.mixin', # [NEW] Level 2: Compliance Validity
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

    def inherit_dna_from_source(self, inputs):
        """
        [Level 1+ DNA Traceability]
        Aggregates nutrients and sustainability metrics from input movements.
        """
        self.ensure_one()
        total_qty = sum(i.product_uom_qty for i in inputs)
        if total_qty <= 0:
            return

        # 1. Mass Balance Accumulation
        self.nitrogen_qty = sum(i.nitrogen_qty for i in inputs)
        self.phosphorus_qty = sum(i.phosphorus_qty for i in inputs)
        self.potassium_qty = sum(i.potassium_qty for i in inputs)
        self.water_footprint = sum(i.water_footprint for i in inputs)

        # 2. Weighted Average Sustainability (Carbon Intensity)
        weighted_carbon = sum(i.carbon_intensity * i.product_uom_qty for i in inputs)
        self.carbon_intensity = weighted_carbon / total_qty

        # 3. Spatial Context Inheritance
        # Lots often take the location of the latest intervention
        if inputs:
            self.geo_point = inputs[0].production_id.geo_point
            
        self.generate_quality_fingerprint()
        return True