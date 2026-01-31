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
    Level 1+: Neighborhood Discovery Service. [US-70-2026]
    """
    _name = 'agri.geospatial.mixin'
    _description = 'Agricultural GeoSpatial Tracking Mixin'

    geo_point = fields.Char(
        string="Geo Location (Point)",
        help="Format: LON,LAT"
    )
    geo_polygon = fields.Text(
        string="Geo Boundaries (Polygon)",
        help="Format: LON,LAT;LON,LAT..."
    )
    spatial_grid_id = fields.Char(
        string="Spatial Grid ID",
        compute="_compute_spatial_grid",
        index=True,
        store=True
    )

    @api.depends('geo_point')
    def _compute_spatial_grid(self):
        """
        Divide the earth into grids (~11m precision) for neighborhood discovery.
        """
        for record in self:
            if record.geo_point:
                try:
                    lon, lat = map(float, record.geo_point.split(','))
                    record.spatial_grid_id = f"G_{round(lon, 4)}_{round(lat, 4)}"
                except Exception:
                    record.spatial_grid_id = False
            else:
                record.spatial_grid_id = False

    @api.model_create_multi
    def create(self, vals_list):
        """
        Auto-register presence in the neighborhood registry on creation.
        """
        records = super(GeoSpatialMixin, self).create(vals_list)
        for record in records:
            if record.spatial_grid_id:
                self.env['agri.neighborhood.registry'].register_presence(
                    record._name, record.id, record.spatial_grid_id
                )
        return records

    def write(self, vals):
        """
        Update registry presence if location or grid changes.
        """
        res = super(GeoSpatialMixin, self).write(vals)
        if 'geo_point' in vals or 'spatial_grid_id' in vals:
            for record in self:
                if record.spatial_grid_id:
                    self.env['agri.neighborhood.registry'].register_presence(
                        record._name, record.id, record.spatial_grid_id
                    )
        return res

    def get_spatial_context(self):
        """
        Returns the environment data including neighborhood agents.
        Connected to Registry [L1+].
        """
        self.ensure_one()
        neighbors = self.env['agri.neighborhood.registry'].search([
            ('spatial_grid_id', '=', self.spatial_grid_id),
            ('is_active', '=', True),
            ('agent_id', '!=', f"{self._name}:{self.id}")
        ])
        return {
            'grid_id': self.spatial_grid_id,
            'point': self.geo_point,
            'neighborhood_agents': [n.agent_id for n in neighbors]
        }


class NutrientMixin(models.AbstractModel):
    """
    Mixin for Bio-mass Balance and Nutrient Tracking.
    Level 1: Qualitative Efficiency Standard.
    Level 1+: Auto-correction logic.
    """
    _name = 'agri.nutrient.mixin'
    _description = 'Agricultural Nutrient & Mass Balance Mixin'

    nitrogen_qty = fields.Float(
        string="Nitrogen (N)",
        digits=(12, 4),
        help="Nitrogen content in kg per unit."
    )
    phosphorus_qty = fields.Float(
        string="Phosphorus (P)",
        digits=(12, 4),
        help="Phosphorus content in kg per unit."
    )
    potassium_qty = fields.Float(
        string="Potassium (K)",
        digits=(12, 4),
        help="Potassium content in kg per unit."
    )
    carbon_content = fields.Float(
        string="Organic Carbon",
        digits=(12, 4)
    )
    water_footprint = fields.Float(
        string="Water Footprint (L)",
        digits=(12, 2)
    )

    def calculate_mass_balance(self, inputs, outputs):
        """
        Calculate the efficiency of nutrient conversion.
        Bio-efficiency = Output Nutrient / Input Nutrient.
        """
        total_in_n = sum(i.nitrogen_qty for i in inputs)
        total_out_n = sum(o.nitrogen_qty for o in outputs)
        
        efficiency = (total_out_n / total_in_n) if total_in_n > 0 else 0.0
        
        return {
            'n_efficiency': efficiency,
            'n_loss': total_in_n - total_out_n,
            'is_sustainable': efficiency > 0.7
        }

    def suggest_nutrient_correction(self, sensor_data):
        """
        Feedback Loop: Sensor -> Suggestion.
        sensor_data example: {'n_soil_level': 20.0, 'moisture': 0.3}
        """
        self.ensure_one()
        current_n = sensor_data.get('n_soil_level', 0.0)
        target_n = self.nitrogen_qty
        
        # If soil nitrogen is higher than 80% of target, reduce input by 20%
        if current_n > target_n * 0.8:
            return {'nitrogen_qty': -0.2}
        return {}

    @api.constrains('nitrogen_qty', 'phosphorus_qty', 'potassium_qty')
    def _check_nutrient_sanity(self):
        for record in self:
            if any(val < 0 for val in [record.nitrogen_qty, record.phosphorus_qty, record.potassium_qty]):
                raise ValidationError(_("Nutrient content cannot be negative. Matter cannot be created from nothing."))


class ActuatorMixin(models.AbstractModel):
    """
    Mixin for Physical Actuation and Feedback Execution. [Level 1+]
    Transforms logical suggestions into physical business record updates.
    """
    _name = 'agri.actuator.mixin'
    _description = 'Agricultural Feedback Actuator Mixin'

    def apply_feedback_correction(self, correction_vals):
        """
        Executes the correction. 
        Example: If correction_vals is {'nitrogen_qty': -0.2}, 
        it finds the corresponding Stock Moves and reduces quantity.
        """
        self.ensure_one()
        _logger.info("Applying feedback actuation for %s: %s", self._name, correction_vals)
        
        # Implementation depends on the base model (e.g., mrp.production)
        if hasattr(self, 'move_raw_ids'):
            for move in getattr(self, 'move_raw_ids'):
                if 'nitrogen' in move.product_id.name.lower():
                    ratio = 1.0 + correction_vals.get('nitrogen_qty', 0.0)
                    move.write({'product_uom_qty': move.product_uom_qty * ratio})
        return True


class EmbeddingMixin(models.AbstractModel):
    """
    Mixin for RAG-ready semantic search.
    Level 2: Knowledge Grounding.
    """
    _name = 'agri.embedding.mixin'
    _description = 'Agricultural Embedding Mixin'

    embedding_vector = fields.Binary(
        string="Vector Data",
        help="Serialized embedding vector."
    )
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
        llm_service = self.env['llm.service'].search([
            ('config_id.is_active', '=', True)
        ], limit=1)
        
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
        compute="_compute_impact_credits",
        store=True,
        digits=(12, 2),
        help="Monetized value derived from confirmed community ledger entries."
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

    def _compute_impact_credits(self):
        """
        [Level 3+: Transaction Pattern with Human Audit]
        Only sums confirmed ledger entries.
        """
        for record in self:
            entries = self.env['agri.clearing.ledger'].search([
                ('source_ref', '=', '%s,%d' % (record._name, record.id)),
                ('state', '=', 'confirmed')
            ])
            record.impact_credits = sum(entries.mapped('credit_change'))

    def generate_quality_fingerprint(self):
        """
        Gathers all L1/L2 data into a single, verifiable JSON bundle.
        Used as proof for inter-farm value clearing.
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

    def apply_slashing(self, reason, penalty_score=50):
        """
        Level 2+: Slashing Mechanism.
        Creates a ledger entry in 'draft' state. Recomputed only after confirmation.
        """
        self.ensure_one()
        _logger.warning("Slashing triggered for %s: %s (Penalty: -%d)", self.name, reason, penalty_score)
        
        target = False
        if hasattr(self, 'user_id') and self.user_id.partner_id:
            target = self.user_id.partner_id
        elif hasattr(self, 'partner_id') and self.partner_id:
            target = self.partner_id
            
        if target:
            # Entry is PENDING audit (draft)
            self.env['agri.clearing.ledger'].create({
                'partner_id': target.id,
                'score_change': -penalty_score,
                'source_ref': '%s,%d' % (self._name, self.id),
                'description': _("PENDING SLASHING: %s") % reason,
                'state': 'draft'
            })
            
            if hasattr(self, 'message_post'):
                self.message_post(body=_("<b>Reputation Slashing Triggered:</b> -%d credits pending community audit.") % penalty_score)
        return True

    def action_finalize_clearing(self):
        """
        Executes the final value clearing.
        Creates a ledger entry in 'draft' state for human approval.
        """
        for record in self:
            esg_score = getattr(record, 'esg_score', 100)
            carbon = getattr(record, 'carbon_intensity', 0)
            
            bonus = (esg_score / 100.0) * (10.0 / (carbon + 1.0))
            
            record.write({'clearing_status': 'calculated'})
            record.generate_quality_fingerprint()

            target = False
            if hasattr(record, 'user_id') and record.user_id.partner_id:
                target = record.user_id.partner_id
            elif hasattr(record, 'partner_id') and record.partner_id:
                target = record.partner_id

            if target:
                self.env['agri.clearing.ledger'].create({
                    'partner_id': target.id,
                    'credit_change': bonus,
                    'source_ref': '%s,%d' % (record._name, record.id),
                    'description': _("PENDING BONUS for %s") % record.display_name,
                    'state': 'draft'
                })
            
            _logger.info("Value Clearing Calculated for %s: %f credits (Awaiting Audit)", record.id, bonus)
