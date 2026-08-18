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

    # 生物资产属性 [US-001-04]
    is_animal = fields.Boolean("Is Animal Asset", default=False)
    birth_date = fields.Date("Birth Date")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender")

    product_tmpl_id = fields.Many2one(
        'product.template',
        related='product_id.product_tmpl_id',
        string='Product Template',
        store=True,
        readonly=True
    )

    lot_properties = fields.Properties(
        'Properties',
        definition='product_tmpl_id.lot_properties_definition'
    )

    # Trust DNA [US-TECH-DNA-07]
    entity_audit_status = fields.Selection([
        ('compliant', 'Compliant'),
        ('warning', 'Warning'),
        ('non_compliant', 'Non-Compliant')
    ], string='Entity Audit Status', default='compliant')

    dna_integrity_score = fields.Float('DNA Integrity Score', compute='_compute_dna_integrity', store=True)

    @api.depends('certification_type', 'entity_audit_status', 'audit_status', 'parent_kinship_ids')
    def _compute_dna_integrity(self):
        for lot in self:
            score = 100.0
            if lot.certification_type != 'organic':
                score -= 20.0
            if lot.entity_audit_status != 'compliant':
                score -= 30.0
            if lot.audit_status == 'fraudulent':
                score -= 50.0
            
            # Heritage check: if parents have low integrity, child inherits some penalty
            if lot.parent_kinship_ids:
                avg_parent_score = sum(lot.parent_kinship_ids.mapped('parent_lot_id.dna_integrity_score')) / len(lot.parent_kinship_ids)
                if avg_parent_score < 80:
                    score -= (100 - avg_parent_score) * 0.5
            
            lot.dna_integrity_score = max(0.0, score)

    # [US-002-04] Quality Grading
    quality_grade = fields.Selection([
        ('grade_a', 'Grade A'),
        ('grade_b', 'Grade B'),
        ('grade_c', 'Grade C'),
        ('ungraded', 'Not Graded')
    ], string="Quality Grade", default='ungraded')

    # Visualization Trigger [US-TECH-DNA-06]
    holographic_map_trigger = fields.Boolean('Traceability Map Active', default=True)

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
            {'name': 'inbound_init', 'class': 'agri.dna.plugin.inbound'},
            {'name': 'nutrients', 'class': 'agri.dna.plugin.nutrient'},
            {'name': 'sustainability', 'class': 'agri.dna.plugin.sustainability'},
            {'name': 'spatial', 'class': 'agri.dna.plugin.spatial'},
            {'name': 'certification', 'class': 'agri.dna.plugin.certification'},
            {'name': 'kinship', 'class': 'agri.dna.plugin.kinship'},
            {'name': 'entity_trust', 'class': 'agri.dna.plugin.entity_compliance'},
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
            plugin_model_name = plugin_info['class']
            if plugin_model_name in self.env:
                plugin_model = self.env[plugin_model_name]
                try:
                    plugin_model.inherit_dna(self, inputs)
                except Exception as e:
                    _logger.error(f"DNA Inheritance Plugin Error ({plugin_info['name']}): {str(e)}")

        self.generate_quality_fingerprint()
        return True