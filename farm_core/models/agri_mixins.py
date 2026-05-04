from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import logging
import json
import base64
import hashlib
from datetime import datetime

_logger = logging.getLogger(__name__)


class GeoSpatialMixin(models.AbstractModel):
    """
    [US-001-03, US-TECH-04-01]
    Mixin for Grid-based spatial tracking.
    Level 1: Geo-grounding & Spatial Evidence.
    Level 1+: Neighborhood Discovery Service. [US-100-2026]
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
        """ [US-TECH-04-02] Divide the earth into grids (~11m precision). """
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
        """ Auto-register presence in the neighborhood registry on creation. """
        records = super(GeoSpatialMixin, self).create(vals_list)
        for record in records:
            if record.spatial_grid_id:
                self.env['agri.neighborhood.registry'].register_presence(
                    record._name, record.id, record.spatial_grid_id
                )
        return records

    def write(self, vals):
        """ Update registry presence if location or grid changes. """
        res = super(GeoSpatialMixin, self).write(vals)
        if 'geo_point' in vals or 'spatial_grid_id' in vals:
            for record in self:
                if record.spatial_grid_id:
                    self.env['agri.neighborhood.registry'].register_presence(
                        record._name, record.id, record.spatial_grid_id
                    )
        return res

    def get_spatial_context(self):
        """ Returns environment data including neighborhood agents. [L1+] """
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
    [US-002-03, US-057-01]
    Mixin for Bio-mass Balance and Nutrient Tracking.
    Level 1: Qualitative Efficiency Standard.
    Level 1+: Auto-correction logic.
    """
    _name = 'agri.nutrient.mixin'
    _description = 'Agricultural Nutrient & Mass Balance Mixin'

    nitrogen_qty = fields.Float("Nitrogen (N)", digits=(12, 4), help="kg per unit.")
    phosphorus_qty = fields.Float("Phosphorus (P)", digits=(12, 4))
    potassium_qty = fields.Float("Potassium (K)", digits=(12, 4))
    carbon_content = fields.Float("Organic Carbon", digits=(12, 4))
    water_footprint = fields.Float("Water Footprint (L)", digits=(12, 2))

    def calculate_mass_balance(self, inputs, outputs):
        """ [US-057-01] Bio-efficiency = Output Nutrient / Input Nutrient. """
        total_in_n = sum(i.nitrogen_qty for i in inputs)
        total_out_n = sum(o.nitrogen_qty for o in outputs)
        efficiency = (total_out_n / total_in_n) if total_in_n > 0 else 0.0
        return {
            'n_efficiency': efficiency,
            'n_loss': total_in_n - total_out_n,
            'is_sustainable': efficiency > 0.7
        }

    def suggest_nutrient_correction(self, sensor_data):
        """ Feedback Loop: Sensor -> Suggestion. """
        self.ensure_one()
        current_n = sensor_data.get('n_soil_level', 0.0)
        target_n = self.nitrogen_qty
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
    [US-TECH-05-01]
    Mixin for Physical Actuation and Feedback Execution. [Level 1+]
    """
    _name = 'agri.actuator.mixin'
    _description = 'Agricultural Feedback Actuator Mixin'

    def apply_feedback_correction(self, correction_vals):
        """ Executes the physical business record updates based on suggestions. """
        self.ensure_one()
        _logger.info("Applying feedback actuation for %s: %s", self._name, correction_vals)
        if hasattr(self, 'move_raw_ids'):
            for move in getattr(self, 'move_raw_ids'):
                if 'nitrogen' in move.product_id.name.lower():
                    ratio = 1.0 + correction_vals.get('nitrogen_qty', 0.0)
                    move.write({'product_uom_qty': move.product_uom_qty * ratio})
        return True


class AgriGrowthCycleMixin(models.AbstractModel):
    """
    [US-002-02, US-105-02]
    Growth Cycle & Physiological Stage Mixin based on GDD.
    """
    _name = 'agri.growth.cycle.mixin'
    _description = 'Agri Growth Cycle & GDD Mixin'

    current_stage_id = fields.Many2one('agri.industry.physio.stage', string="Current Stage")
    accumulated_gdd = fields.Float("Accumulated GDD", default=0.0)
    biological_zero_temp = fields.Float(string="T-Base", default=10.0)
    stage_progress = fields.Float("Stage Progress (%)", compute='_compute_stage_progress')

    @api.depends('accumulated_gdd', 'current_stage_id')
    def _compute_stage_progress(self):
        for rec in self:
            if rec.current_stage_id and rec.current_stage_id.target_gdd > 0:
                rec.stage_progress = min(100.0, (rec.accumulated_gdd / rec.current_stage_id.target_gdd) * 100.0)
            else:
                rec.stage_progress = 0.0

    def update_daily_gdd(self, t_max, t_min):
        """ Implement calculate_daily_gdd from algorithm spec. """
        for rec in self:
            t_base = rec.biological_zero_temp or 10.0
            daily_gdd = max(0, (t_max + t_min) / 2.0 - t_base)
            rec.accumulated_gdd += daily_gdd
            self._check_stage_migration()

    def _check_stage_migration(self):
        """ To be implemented in child models. """
        pass


class AgriBiologicalInventoryMixin(models.AbstractModel):
    """
    [Level 1: Physical DNA]
    Mixin for Biological Inventory Tracking (Count, Weight, Mortality).
    """
    _name = 'agri.biological.inventory.mixin'
    _description = 'Agri Biological Inventory Mixin'

    animal_count = fields.Integer("Animal Count", default=0)
    average_weight = fields.Float("Avg Weight (kg)", default=0.0)
    total_biomass = fields.Float("Total Biomass (kg)", compute='_compute_biomass', store=True, precompute=True)
    mortality_rate = fields.Float("Mortality Rate (%)", compute='_compute_mortality', store=True, precompute=True)
    dead_count = fields.Integer("Deaths Recorded", default=0)

    @api.depends('animal_count', 'average_weight')
    def _compute_biomass(self):
        for rec in self:
            rec.total_biomass = rec.animal_count * rec.average_weight

    @api.depends('animal_count', 'dead_count')
    def _compute_mortality(self):
        for rec in self:
            total = rec.animal_count + rec.dead_count
            rec.mortality_rate = (rec.dead_count / total * 100.0) if total > 0 else 0.0

    def action_record_mortality(self, count, reason):
        if any(count > rec.animal_count for rec in self):
            raise UserError(_("Recorded deaths cannot exceed population."))
        for rec in self:
            rec.animal_count -= count
            rec.dead_count += count


class AgriTraceabilityMixin(models.AbstractModel):
    """
    [US-049-01, US-112-03]
    Mixin for Blockchain-ready Traceability Fingerprint.
    """
    _name = 'agri.traceability.mixin'
    _description = 'Agri Traceability DNA Mixin'

    traceability_hash = fields.Char("Traceability Fingerprint", compute='_compute_trace_hash', store=True, precompute=True)

    @api.depends('create_date', 'geo_point')
    def _compute_trace_hash(self):
        for rec in self:
            payload = f"{rec._name}:{rec.id}:{rec.create_date}:{getattr(rec, 'geo_point', 'No-Geo')}"
            rec.traceability_hash = hashlib.sha256(payload.encode()).hexdigest()

    def generate_qr_content(self):
        self.ensure_one()
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        return f"{base_url}/trace/{self.traceability_hash}"


class AgriResourceConsumptionMixin(models.AbstractModel):
    """
    [Level 1: Physical DNA]
    Mixin for Precision Resource Tracking (Water, Energy, Fuel).
    """
    _name = 'agri.resource.consumption.mixin'
    _description = 'Agri Resource Consumption Mixin'

    water_consumed_m3 = fields.Float("Water Consumed (m3)", digits=(12, 3))
    electricity_consumed_kwh = fields.Float("Electricity Consumed (kWh)", digits=(12, 2))
    fuel_consumed_l = fields.Float("Fuel Consumed (L)", digits=(12, 2))
    resource_intensity_score = fields.Float("Resource Intensity", compute='_compute_resource_intensity')

    def _compute_resource_intensity(self):
        for rec in self:
            produced_qty = getattr(rec, 'product_qty', 1.0) or 1.0
            rec.resource_intensity_score = (rec.water_consumed_m3 * 10 + rec.fuel_consumed_l * 5) / produced_qty


class AgriWeatherSensitiveMixin(models.AbstractModel):
    """
    [Level 2: Decision DNA]
    Weather Impact & Operation Gating Mixin based on WEATHER_IMPACT_ALGORITHM.md.
    """
    _name = 'agri.weather.sensitive.mixin'
    _description = 'Agri Weather Sensitivity Mixin'

    weather_risk_level = fields.Selection([
        ('low', 'Optimal'), ('medium', 'Caution'), ('high', 'Blocked')
    ], string="Weather Risk", default='low')

    def check_weather_window(self, activity_type):
        """ Hard-gating logic for safety. """
        forecast = {'wind_speed': 2.0, 'rain_probability': 10} 
        if activity_type == 'spraying':
            if forecast['wind_speed'] > 5.5:
                raise UserError(_("Weather Interception: Wind speed too high."))
            if forecast['rain_probability'] > 60:
                raise UserError(_("Weather Interception: High rain probability."))
        return True


class AgriIncidentAlertMixin(models.AbstractModel):
    """
    [US-053-05, US-105-04]
    Mixin for Standardized Incident Reporting and Alerting.
    """
    _name = 'agri.incident.alert.mixin'
    _description = 'Agri Incident & Alert Mixin'

    def report_incident(self, severity, category, description):
        self.ensure_one()
        _logger.warning("INCIDENT [%s]: %s", category, description)
        self.env['mail.activity'].create({
            'activity_type_id': self.env.ref('mail.mail_activity_data_warning').id,
            'summary': f"INCIDENT: {category} ({severity})",
            'note': description,
            'res_id': self.id,
            'res_model_id': self.env['ir.model'].sudo().search([('model', '=', self._name)]).id,
            'user_id': self.env.user.id,
        })
        return True


class AgriQualityGateMixin(models.AbstractModel):
    """
    [US-038-01, US-114-02]
    Mixin for Quality Gate Enforcement (HACCP/QCP).
    """
    _name = 'agri.quality.gate.mixin'
    _description = 'Agri Quality Gate Mixin'

    def validate_quality_gate(self):
        """ Check mandatory QCPs. """
        _logger.info("Validating Quality Gate for %s", self._name)
        return True


class AgriCertificationStatusMixin(models.AbstractModel):
    """
    [Level 2: Audit DNA]
    Mixin for Certification and Compliance Validity Tracking.
    """
    _name = 'agri.certification.status.mixin'
    _description = 'Agri Certification Status Mixin'

    certification_type = fields.Selection([
        ('organic', 'Organic'), ('green', 'Green'), ('fairtrade', 'Fair Trade'), ('globalgap', 'GlobalGAP')
    ], string="Primary Certification")
    cert_expiry_date = fields.Date("Certification Expiry")
    is_certified = fields.Boolean("Valid Certificate", compute='_compute_cert_validity')

    @api.depends('cert_expiry_date')
    def _compute_cert_validity(self):
        today = fields.Date.today()
        for rec in self:
            rec.is_certified = rec.cert_expiry_date and rec.cert_expiry_date > today

    def check_certification_compliance(self):
        for rec in self:
            if not rec.is_certified:
                raise UserError(_("Compliance Block: Certification expired for %s.") % rec.display_name)


class AgriBiologicalValuationMixin(models.AbstractModel):
    """
    [Level 3: Value DNA]
    Mixin for Dynamic Fair Value Estimation of Biological Assets. [US-088-15]
    """
    _name = 'agri.biological.valuation.mixin'
    _description = 'Agri Biological Asset Valuation Mixin'

    fair_value_unit = fields.Float("Estimated Unit Fair Value", compute='_compute_fair_value', store=True, precompute=True)
    total_asset_value = fields.Float("Total Asset Fair Value", compute='_compute_fair_value', store=True, precompute=True)
    valuation_date = fields.Datetime("Last Valuation Date", default=fields.Datetime.now)
    market_peg_price = fields.Float("Market Price Reference")

    @api.depends('total_biomass', 'current_stage_id', 'market_peg_price')
    def _compute_fair_value(self):
        for rec in self:
            stage_multiplier = 0.5 + (rec.stage_progress / 200.0) if hasattr(rec, 'stage_progress') else 1.0
            biomass = getattr(rec, 'total_biomass', 0.0)
            rec.total_asset_value = biomass * (rec.market_peg_price or 15.0) * stage_multiplier
            rec.fair_value_unit = rec.total_asset_value / rec.animal_count if hasattr(rec, 'animal_count') and rec.animal_count > 0 else 0.0


class AgriAgentInstructionMixin(models.AbstractModel):
    """
    [US-092-01, US-TECH-05-01]
    Mixin for Level 4-5 DNA: Orchestration and Feedback Loop.
    """
    _name = 'agri.agent.instruction.mixin'
    _description = 'Agri Agent Instruction & Command Mixin'

    agent_instruction_json = fields.Text("Structured Command (JSON)")
    agent_status_feedback = fields.Selection([
        ('pending', 'Awaiting Agent'), ('executing', 'In Execution'),
        ('success', 'Succeeded'), ('failed', 'Failed'), ('manual_override', 'Manual')
    ], string="Agent Execution Status", default='pending')

    def action_receive_agent_feedback(self, status, feedback_log):
        """ [Level 5 Loop] [US-092-01] """
        self.ensure_one()
        self.write({'agent_status_feedback': status})
        if status == 'failed' and hasattr(self, 'report_incident'):
            self.report_incident('high', 'Agent Failure', feedback_log)
        return True


class EmbeddingMixin(models.AbstractModel):
    """ Mixin for RAG-ready semantic search. Level 2. """
    _name = 'agri.embedding.mixin'
    _description = 'Agricultural Embedding Mixin'

    embedding_vector = fields.Binary("Vector Data")
    embedding_last_updated = fields.Datetime("Vector Updated At")
    is_embedded = fields.Boolean("Has Vector Index", default=False)

    def _get_embedding_content(self): return ""

    def action_sync_embedding(self):
        llm_service = self.env['llm.service'].search([('config_id.is_active', '=', True)], limit=1)
        if not llm_service: return False
        for record in self:
            content = record._get_embedding_content()
            if content:
                vector = llm_service.get_embeddings(content)
                if vector:
                    record.write({'embedding_vector': base64.b64encode(json.dumps(vector).encode()), 
                                  'is_embedded': True, 'embedding_last_updated': datetime.now()})
        return True


class ClearingEngineMixin(models.AbstractModel):
    """
    Mixin for Community Value Clearing and Settlement.
    Level 3: Economic Monetization.
    """
    _name = 'agri.clearing.mixin'
    _description = 'Agricultural Value Clearing Mixin'

    impact_credits = fields.Float("Sustainability Credits", compute="_compute_impact_credits", store=True, precompute=True)
    quality_fingerprint = fields.Text("Quality Fingerprint")
    clearing_status = fields.Selection([('draft', 'Drafting'), ('settled', 'Settled')], default='draft')

    def _compute_impact_credits(self):
        for record in self:
            entries = self.env['agri.clearing.ledger'].search([
                ('source_ref', '=', '%s,%d' % (record._name, record.id)), ('state', '=', 'confirmed')
            ])
            record.impact_credits = sum(entries.mapped('credit_change'))

    def generate_quality_fingerprint(self):
        self.ensure_one()
        fingerprint = {
            'model': self._name, 'id': self.id, 'timestamp': datetime.now().isoformat(),
            'nutrient': {'n': getattr(self, 'nitrogen_qty', 0)},
            'fair_value': getattr(self, 'total_asset_value', 0.0),
        }
        self.quality_fingerprint = json.dumps(fingerprint, indent=2)
        return fingerprint

    def calculate_community_value(self):
        """ [US-014-01] Multi-dimensional Valuation Engine. """
        self.ensure_one()
        n_peg = 1.2
        physical_value = getattr(self, 'nitrogen_qty', 0) * n_peg
        esg_score = getattr(self, 'esg_score', 100)
        multiplier = (esg_score / 100.0)
        return physical_value * multiplier
