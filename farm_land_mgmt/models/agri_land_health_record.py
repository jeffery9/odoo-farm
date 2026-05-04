from odoo import models, fields, api, _
from datetime import datetime, timedelta

class AgriLandHealthRecord(models.Model):
    """
    US-001-09: 土地健康与轮作档案 (Land Health & Crop Rotation Records)
    Model to track land health metrics and soil analysis
    """
    _name = 'agri.land.health.record'
    _description = 'Agricultural Land Health Record'
    _order = 'analysis_date desc'

    name = fields.Char('Health Record', required=True)
    land_parcel_id = fields.Many2one('farm.location', string='Land Parcel', required=True)
    analysis_date = fields.Date('Analysis Date', default=fields.Date.context_today, required=True)
    n_level = fields.Float('Nitrogen Level (N)')
    p_level = fields.Float('Phosphorus Level (P)')
    k_level = fields.Float('Potassium Level (K)')
    ph_level = fields.Float('pH Level')
    organic_matter = fields.Float('Organic Matter (%)')
    soil_texture = fields.Char('Soil Texture')
    moisture_level = fields.Float('Moisture Level (%)')
    compaction_level = fields.Float('Compaction Level (Bar)')
    salinity_level = fields.Float('Salinity Level (dS/m)')
    soil_temperature = fields.Float('Soil Temperature (°C)')
    pest_disease_incidence = fields.Text('Pest/Disease Incidence')
    soil_health_score = fields.Float('Soil Health Score (0-100)', compute='_compute_soil_health_score', store=True)
    health_status = fields.Selection([
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
        ('critical', 'Critical')
    ], string='Health Status', compute='_compute_health_status', store=True)
    recommendations = fields.Text('Recommendations')
    next_analysis_date = fields.Date('Next Analysis Date')

    @api.depends('n_level', 'p_level', 'k_level', 'ph_level', 'organic_matter', 'moisture_level')
    def _compute_soil_health_score(self):
        """Compute soil health score based on various parameters"""
        for record in self:
            score = 0.0

            # Nitrogen level (optimal range 20-40 mg/kg)
            if 20 <= record.n_level <= 40:
                score += 15
            elif 10 <= record.n_level <= 60:
                score += 10
            elif 5 <= record.n_level <= 80:
                score += 5

            # Phosphorus level (optimal range 15-25 mg/kg)
            if 15 <= record.p_level <= 25:
                score += 15
            elif 10 <= record.p_level <= 30:
                score += 10
            elif 5 <= record.p_level <= 40:
                score += 5

            # Potassium level (optimal range 100-200 mg/kg)
            if 100 <= record.k_level <= 200:
                score += 15
            elif 50 <= record.k_level <= 300:
                score += 10
            elif 25 <= record.k_level <= 400:
                score += 5

            # pH level (optimal range 6.0-7.0)
            if 6.0 <= record.ph_level <= 7.0:
                score += 15
            elif 5.5 <= record.ph_level <= 7.5:
                score += 10
            elif 5.0 <= record.ph_level <= 8.0:
                score += 5

            # Organic matter (optimal range 3-6%)
            if 3 <= record.organic_matter <= 6:
                score += 15
            elif 2 <= record.organic_matter <= 8:
                score += 10
            elif 1 <= record.organic_matter <= 10:
                score += 5

            # Moisture level (optimal range 20-30%)
            if 20 <= record.moisture_level <= 30:
                score += 10
            elif 15 <= record.moisture_level <= 35:
                score += 5

            # Cap the score at 100
            record.soil_health_score = min(100.0, score)

    @api.depends('soil_health_score')
    def _compute_health_status(self):
        """Compute health status based on soil health score"""
        for record in self:
            if record.soil_health_score >= 80:
                record.health_status = 'excellent'
            elif record.soil_health_score >= 60:
                record.health_status = 'good'
            elif record.soil_health_score >= 40:
                record.health_status = 'fair'
            elif record.soil_health_score >= 20:
                record.health_status = 'poor'
            else:
                record.health_status = 'critical'

    @api.model
    def schedule_next_analysis(self):
        """Schedule the next analysis date based on current analysis"""
        for record in self:
            # Default to 6 months from current analysis
            next_date = fields.Date.from_string(record.analysis_date) + timedelta(days=180)
            record.next_analysis_date = next_date