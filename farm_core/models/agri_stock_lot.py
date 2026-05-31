from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)

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

    # Kinship / Ancestry Tracking [US-TECH-DNA-05]
    parent_kinship_ids = fields.One2many('agri.lot.kinship', 'child_lot_id', string='Ancestry (Parents)', help='The lots that this lot was derived from.')
    child_kinship_ids = fields.One2many('agri.lot.kinship', 'parent_lot_id', string='Lineage (Descendants)', help='The lots that were derived from this lot.')

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

    @api.model
    def _get_dna_plugins(self):
        """
        Registry for DNA inheritance plugins.
        """
        return [
            {'name': 'nutrients', 'class': 'agri.dna.plugin.nutrient'},
            {'name': 'sustainability', 'class': 'agri.dna.plugin.sustainability'},
            {'name': 'spatial', 'class': 'agri.dna.plugin.spatial'},
            {'name': 'certification', 'class': 'agri.dna.plugin.certification'},
            {'name': 'kinship', 'class': 'agri.dna.plugin.kinship'},
        ]

    def inherit_dna_from_source(self, inputs):
        """
        [Level 1+ DNA Traceability]
        Orchestrates DNA transfer from inputs to the output lot via plugins.
        """
        self.ensure_one()
        if not inputs:
            return

        plugins = self._get_dna_plugins()
        for plugin_info in plugins:
            plugin_model = self.env.get(plugin_info['class'])
            if plugin_model:
                try:
                    plugin_model.inherit_dna(self, inputs)
                except Exception as e:
                    _logger.error(f"DNA Inheritance Plugin Error ({plugin_info['name']}): {str(e)}")

        self.generate_quality_fingerprint()
        return True