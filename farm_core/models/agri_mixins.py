from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging
import json
import base64

_logger = logging.getLogger(__name__)


class GeoSpatialMixin(models.AbstractModel):
    """
    Mixin for Grid-based spatial tracking.
    Level 1: Geo-grounding & Spatial Evidence.
    """
    _name = 'agri.geospatial.mixin'
    _description = 'Agricultural GeoSpatial Tracking Mixin'

    geo_point = fields.Char(string="Geo Location (Point)", help="Format: LON,LAT")
    geo_polygon = fields.Text(string="Geo Boundaries (Polygon)", help="Format: LON,LAT;LON,LAT...")
    spatial_grid_id = fields.Char(string="Spatial Grid ID", compute="_compute_spatial_grid", store=True)

    @api.depends('geo_point')
    def _compute_spatial_grid(self):
        for record in self:
            if record.geo_point:
                try:
                    lon, lat = map(float, record.geo_point.split(','))
                    record.spatial_grid_id = f"G_{round(lon, 4)}_{round(lat, 4)}"
                except:
                    record.spatial_grid_id = False
            else:
                record.spatial_grid_id = False

    def get_spatial_context(self):
        self.ensure_one()
        return {
            'grid_id': self.spatial_grid_id,
            'point': self.geo_point,
            'neighborhood_agents': []
        }


class NutrientMixin(models.AbstractModel):
    """
    Mixin for Bio-mass Balance and Nutrient Tracking.
    Level 1: Qualitative Efficiency Standard.
    """
    _name = 'agri.nutrient.mixin'
    _description = 'Agricultural Nutrient & Mass Balance Mixin'

    nitrogen_qty = fields.Float("Nitrogen (N)", digits=(12, 4))
    phosphorus_qty = fields.Float("Phosphorus (P)", digits=(12, 4))
    potassium_qty = fields.Float("Potassium (K)", digits=(12, 4))
    carbon_content = fields.Float("Organic Carbon", digits=(12, 4))
    water_footprint = fields.Float("Water Footprint (L)", digits=(12, 2))

    def calculate_mass_balance(self, inputs, outputs):
        total_in_n = sum(i.nitrogen_qty for i in inputs)
        total_out_n = sum(o.nitrogen_qty for o in outputs)
        efficiency = (total_out_n / total_in_n) if total_in_n > 0 else 0.0
        return {
            'n_efficiency': efficiency,
            'n_loss': total_in_n - total_out_n,
            'is_sustainable': efficiency > 0.7
        }

    @api.constrains('nitrogen_qty', 'phosphorus_qty', 'potassium_qty')
    def _check_nutrient_sanity(self):
        for record in self:
            if any(val < 0 for val in [record.nitrogen_qty, record.phosphorus_qty, record.potassium_qty]):
                raise ValidationError(_("Nutrient content cannot be negative. Matter cannot be created from nothing."))


class EmbeddingMixin(models.AbstractModel):
    """
    Mixin for RAG-ready semantic search.
    Level 2: Knowledge Grounding.
    """
    _name = 'agri.embedding.mixin'
    _description = 'Agricultural Embedding Mixin'

    embedding_vector = fields.Binary("Vector Data", help="Serialized embedding vector.")
    embedding_last_updated = fields.Datetime("Vector Updated At")
    is_embedded = fields.Boolean("Has Vector Index", default=False)

    def _get_embedding_content(self):
        """
        To be overridden by specific models to define what text to vectorize.
        """
        return ""

    def action_sync_embedding(self):
        """
        Trigger the embedding generation via llm_service. [US-59-08]
        """
        llm_service = self.env['llm.service'].search([('config_id.is_active', '=', True)], limit=1)
        if not llm_service:
            _logger.warning("No active LLM service found for embedding.")
            return False

        for record in self:
            content = record._get_embedding_content()
            if not content:
                continue
            
            _logger.info("Syncing embedding for %s:%s", record._name, record.id)
            vector = llm_service.get_embeddings(content)
            if vector:
                # Store vector as base64 encoded JSON for portability
                record.write({
                    'embedding_vector': base64.b64encode(json.dumps(vector).encode()),
                    'is_embedded': True,
                    'embedding_last_updated': fields.Datetime.now()
                })
        return True


class ClearingEngineMixin(models.AbstractModel):
    """
    Mixin for Community Value Clearing and Settlement.
    Level 3: Economic Monetization of Sustainable Value.
    """
    _name = 'agri.clearing.mixin'
    _description = 'Agricultural Value Clearing Mixin'

    impact_credits = fields.Float(
        string="Sustainability Credits",
        digits=(12, 2),
        help="Monetized value of environmental/community impact."
    )
    quality_fingerprint = fields.Text(
        string="Quality Fingerprint",
        help="Immutable proof bundle of GIS, nutrients, and audit scores."
    )
    clearing_status = fields.Selection([
        ('draft', 'Drafting'),
        ('calculated', 'Value Calculated'),
        ('settled', 'Settled'),
        ('disputed', 'Disputed')
    ], default='draft', string="Clearing Status")

    def generate_quality_fingerprint(self):
        """
        Gathers all L1/L2 data into a single, verifiable JSON bundle.
        """
        self.ensure_one()
        fingerprint = {
            'model': self._name,
            'id': self.id,
            'timestamp': fields.Datetime.now().isoformat(),
            'spatial': self.get_spatial_context() if hasattr(self, 'get_spatial_context') else {},
            'nutrient': {
                'n': getattr(self, 'nitrogen_qty', 0),
                'p': getattr(self, 'phosphorus_qty', 0),
                'k': getattr(self, 'potassium_qty', 0),
            } if hasattr(self, 'nitrogen_qty') else {},
            'audit_confidence': getattr(self, 'audit_confidence', 0.0),
        }
        self.quality_fingerprint = json.dumps(fingerprint, indent=2)
        return fingerprint

    def action_finalize_clearing(self):
        """
        Executes the final value clearing.
        """
        for record in self:
            esg_score = getattr(record, 'esg_score', 100)
            carbon = getattr(record, 'carbon_intensity', 0)
            
            bonus = (esg_score / 100.0) * (10.0 / (carbon + 1.0))
            record.impact_credits = bonus
            record.generate_quality_fingerprint()
            record.clearing_status = 'calculated'
            
            _logger.info("Value Clearing Finalized for %s: %f credits", record.id, bonus)
