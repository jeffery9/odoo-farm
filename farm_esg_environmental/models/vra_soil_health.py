from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class AgriVRASoilHealthMonitor(models.Model):
    """
    US-080-03: VRA Soil Health Models
    Soil health VRA models with health metrics integration and precision agriculture
    """
    _name = 'agri.vra.soil.health.monitor'
    _description = 'VRA Soil Health Monitoring and Analytics'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Soil Health Assessment', required=True, copy=False)
    assessment_date = fields.Date('Assessment Date', default=fields.Date.context_today)

    # Location and sampling information
    location_id = fields.Many2one('farm.location', string='Location', required=True)
    sampling_method = fields.Selection([
        ('grid', 'Grid Sampling'),
        ('zone', 'Zone Sampling'),
        ('gps', 'GPS Directed Sampling'),
        ('random', 'Random Sampling'),
    ], string='Sampling Method', default='grid')

    # Soil health parameters
    organic_matter_content = fields.Float('Organic Matter Content (%)')
    ph_level = fields.Float('pH Level')
    nitrogen_level = fields.Float('Nitrogen Level (ppm)')
    phosphorus_level = fields.Float('Phosphorus Level (ppm)')
    potassium_level = fields.Float('Potassium Level (ppm)')
    cation_exchange_capacity = fields.Float('CEC (cmol/kg)')
    base_saturation_calcium = fields.Float('Base Saturation - Calcium (%)')
    base_saturation_magnesium = fields.Float('Base Saturation - Magnesium (%)')
    base_saturation_potassium = fields.Float('Base Saturation - Potassium (%)')
    base_saturation_sodium = fields.Float('Base Saturation - Sodium (%)')
    total_salinity = fields.Float('Total Salinity (dS/m)')
    soil_texture = fields.Selection([
        ('clay', 'Clay'),
        ('clay_loam', 'Clay Loam'),
        ('loam', 'Loam'),
        ('silty_loam', 'Silty Loam'),
        ('sandy_loam', 'Sandy Loam'),
        ('sandy', 'Sandy'),
        ('silt', 'Silt'),
    ], string='Soil Texture')
    soil_compaction_level = fields.Float('Soil Compaction Level (MPa)')

    # VRA application history and impact
    previous_fertilizer_application = fields.Text('Previous Fertilizer Applications')
    previous_pesticide_application = fields.Text('Previous Pesticide Applications')
    crop_rotation_history = fields.Text('Crop Rotation History')

    # Soil health metrics
    soil_health_score = fields.Float('Soil Health Score (0-100)', compute='_compute_soil_health_score', store=True, precompute=True)
    soil_health_category = fields.Selection([
        ('excellent', 'Excellent (90-100)'),
        ('good', 'Good (70-89)'),
        ('fair', 'Fair (50-69)'),
        ('poor', 'Poor (30-49)'),
        ('very_poor', 'Very Poor (0-29)'),
    ], string='Soil Health Category', compute='_compute_soil_health_category', store=True, precompute=True)

    # VRA prescription integration
    related_prescription_ids = fields.Many2many('agri.intervention.vra.prescription', relation='agri_soil_health_rx_rel',
                                              string='Related VRA Prescriptions')
    next_vra_recommendations = fields.Text('Recommended VRA Applications', compute='_compute_vra_recommendations')

    # Environmental impact
    erosion_risk_level = fields.Selection([
        ('low', 'Low Risk'),
        ('medium', 'Medium Risk'),
        ('high', 'High Risk'),
        ('very_high', 'Very High Risk'),
    ], string='Erosion Risk Level', compute='_compute_erosion_risk', store=True, precompute=True)

    # Recommendations
    improvement_recommendations = fields.Text('Improvement Recommendations')
    recommended_practices = fields.Text('Recommended Best Practices')

    # Monitoring and tracking
    assessment_frequency = fields.Selection([
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('annually', 'Annually'),
    ], string='Assessment Frequency', default='quarterly')

    next_assessment_date = fields.Date('Next Assessment Date',
                                     compute='_compute_next_assessment_date', store=True, precompute=True)

    # Soil sampling details
    sampling_depth = fields.Float('Sampling Depth (cm)', default=20.0)
    sampling_points = fields.Integer('Number of Sampling Points')
    sampling_area = fields.Float('Sampling Area (ha)')

    # Additional soil parameters
    microbial_activity = fields.Float('Microbial Activity Index')
    enzyme_activity = fields.Float('Enzyme Activity Level')
    soil_respiration_rate = fields.Float('Soil Respiration Rate (mg CO2/kg/hr)')
    water_holding_capacity = fields.Float('Water Holding Capacity (mm/m)')

    @api.depends('organic_matter_content', 'ph_level', 'nitrogen_level', 'phosphorus_level',
                 'potassium_level', 'cation_exchange_capacity', 'total_salinity', 'soil_compaction_level')
    def _compute_soil_health_score(self):
        """Compute overall soil health score based on multiple parameters"""
        for record in self:
            score = 0.0

            # Organic matter content (weight: 20%)
            if record.organic_matter_content is not None:
                if record.organic_matter_content >= 4:
                    score += 20  # Excellent
                elif record.organic_matter_content >= 2.5:
                    score += 15  # Good
                elif record.organic_matter_content >= 1.5:
                    score += 10  # Fair
                elif record.organic_matter_content >= 1:
                    score += 5   # Poor
                else:
                    score += 0   # Very poor

            # pH level (weight: 15%)
            if record.ph_level is not None:
                if 6.0 <= record.ph_level <= 7.5:
                    score += 15  # Optimal range
                elif 5.5 <= record.ph_level <= 8.0:
                    score += 10  # Good range
                elif 5.0 <= record.ph_level <= 8.5:
                    score += 5   # Acceptable range
                else:
                    score += 0   # Outside range

            # Nitrogen level (weight: 10%)
            if record.nitrogen_level is not None:
                if 20 <= record.nitrogen_level <= 50:
                    score += 10  # Optimal
                elif 10 <= record.nitrogen_level <= 80:
                    score += 7   # Good
                elif 5 <= record.nitrogen_level <= 120:
                    score += 4   # Fair
                else:
                    score += 0   # Too low or high

            # Phosphorus level (weight: 10%)
            if record.phosphorus_level is not None:
                if 15 <= record.phosphorus_level <= 50:
                    score += 10  # Optimal
                elif 10 <= record.phosphorus_level <= 80:
                    score += 7   # Good
                elif 5 <= record.phosphorus_level <= 100:
                    score += 4   # Fair
                else:
                    score += 0   # Too low or high

            # Potassium level (weight: 10%)
            if record.potassium_level is not None:
                if 120 <= record.potassium_level <= 200:
                    score += 10  # Optimal
                elif 100 <= record.potassium_level <= 300:
                    score += 7   # Good
                elif 80 <= record.potassium_level <= 400:
                    score += 4   # Fair
                else:
                    score += 0   # Too low or high

            # CEC (weight: 10%)
            if record.cation_exchange_capacity is not None:
                if record.cation_exchange_capacity >= 20:
                    score += 10  # Excellent
                elif record.cation_exchange_capacity >= 10:
                    score += 7   # Good
                elif record.cation_exchange_capacity >= 5:
                    score += 4   # Fair
                else:
                    score += 0   # Poor

            # Salinity (weight: 10%)
            if record.total_salinity is not None:
                if record.total_salinity <= 2:
                    score += 10  # Excellent
                elif record.total_salinity <= 4:
                    score += 7   # Good
                elif record.total_salinity <= 8:
                    score += 4   # Fair
                else:
                    score += 0   # High salinity

            # Compaction (weight: 15%)
            if record.soil_compaction_level is not None:
                if record.soil_compaction_level <= 2.0:
                    score += 15  # No compaction
                elif record.soil_compaction_level <= 3.0:
                    score += 10  # Light compaction
                elif record.soil_compaction_level <= 4.0:
                    score += 5   # Moderate compaction
                else:
                    score += 0   # Severe compaction

            record.soil_health_score = min(100, max(0, score))

    @api.depends('soil_health_score')
    def _compute_soil_health_category(self):
        """Determine soil health category based on score"""
        for record in self:
            if record.soil_health_score >= 90:
                record.soil_health_category = 'excellent'
            elif record.soil_health_score >= 70:
                record.soil_health_category = 'good'
            elif record.soil_health_score >= 50:
                record.soil_health_category = 'fair'
            elif record.soil_health_score >= 30:
                record.soil_health_category = 'poor'
            else:
                record.soil_health_category = 'very_poor'

    @api.depends('soil_health_score', 'soil_compaction_level', 'total_salinity')
    def _compute_erosion_risk(self):
        """Compute erosion risk based on soil health parameters"""
        for record in self:
            # Erosion risk is inversely related to soil health
            if record.soil_health_score is not None:
                if record.soil_health_score >= 80:
                    risk = 'low'
                elif record.soil_health_score >= 60:
                    risk = 'medium'
                elif record.soil_health_score >= 40:
                    risk = 'high'
                else:
                    risk = 'very_high'

                # Adjust risk based on specific factors
                if record.soil_compaction_level and record.soil_compaction_level > 3.5:
                    # Severe compaction increases erosion risk
                    if risk == 'low':
                        risk = 'medium'
                    elif risk == 'medium':
                        risk = 'high'
                    elif risk == 'high':
                        risk = 'very_high'

                if record.total_salinity and record.total_salinity > 6.0:
                    # High salinity increases erosion risk
                    if risk == 'low':
                        risk = 'medium'
                    elif risk == 'medium':
                        risk = 'high'
                    else:
                        risk = risk  # Keep same or higher risk

                record.erosion_risk_level = risk

    @api.depends('assessment_date', 'assessment_frequency')
    def _compute_next_assessment_date(self):
        """Compute next assessment date based on frequency"""
        for record in self:
            if record.assessment_date and record.assessment_frequency:
                if record.assessment_frequency == 'monthly':
                    record.next_assessment_date = fields.Date.add(record.assessment_date, months=1)
                elif record.assessment_frequency == 'quarterly':
                    record.next_assessment_date = fields.Date.add(record.assessment_date, months=3)
                elif record.assessment_frequency == 'annually':
                    record.next_assessment_date = fields.Date.add(record.assessment_date, years=1)
            else:
                record.next_assessment_date = False

    def _compute_vra_recommendations(self):
        """Generate VRA recommendations based on soil health assessment"""
        for record in self:
            recommendations = []

            # Nitrogen recommendations
            if record.nitrogen_level is not None:
                if record.nitrogen_level < 10:
                    recommendations.append("Apply nitrogen fertilizer: High requirement (150-200 kg/ha)")
                elif record.nitrogen_level < 20:
                    recommendations.append("Apply nitrogen fertilizer: Medium requirement (80-120 kg/ha)")
                elif record.nitrogen_level > 80:
                    recommendations.append("Reduce nitrogen application: High levels detected")

            # Phosphorus recommendations
            if record.phosphorus_level is not None:
                if record.phosphorus_level < 5:
                    recommendations.append("Apply phosphorus fertilizer: High requirement")
                elif record.phosphorus_level < 10:
                    recommendations.append("Apply phosphorus fertilizer: Medium requirement")
                elif record.phosphorus_level > 80:
                    recommendations.append("Reduce phosphorus application: High levels detected")

            # Potassium recommendations
            if record.potassium_level is not None:
                if record.potassium_level < 80:
                    recommendations.append("Apply potassium fertilizer: Requirement detected")
                elif record.potassium_level > 350:
                    recommendations.append("Reduce potassium application: High levels detected")

            # pH recommendations
            if record.ph_level is not None:
                if record.ph_level < 5.5:
                    recommendations.append("Apply lime to raise pH")
                elif record.ph_level > 7.5:
                    recommendations.append("Consider sulfur application to lower pH")

            # Organic matter recommendations
            if record.organic_matter_content is not None:
                if record.organic_matter_content < 2:
                    recommendations.append("Increase organic matter through compost or cover crops")

            # Compaction recommendations
            if record.soil_compaction_level is not None:
                if record.soil_compaction_level > 3.0:
                    recommendations.append("Perform subsoiling to address compaction issues")

            record.next_vra_recommendations = "\n".join(recommendations) if recommendations else "Soil parameters are within optimal ranges. No specific VRA adjustments needed."

    @api.constrains('organic_matter_content', 'ph_level', 'nitrogen_level', 'phosphorus_level',
                    'potassium_level', 'cation_exchange_capacity', 'total_salinity', 'soil_compaction_level',
                    'microbial_activity', 'enzyme_activity', 'soil_respiration_rate', 'water_holding_capacity')
    def _check_positive_values(self):
        """Validate that soil parameters have reasonable values"""
        for record in self:
            if record.organic_matter_content is not None and record.organic_matter_content < 0:
                raise ValidationError(_("Organic matter content cannot be negative."))
            if record.ph_level is not None and (record.ph_level < 0 or record.ph_level > 14):
                raise ValidationError(_("pH level must be between 0 and 14."))
            if record.nitrogen_level is not None and record.nitrogen_level < 0:
                raise ValidationError(_("Nitrogen level cannot be negative."))
            if record.phosphorus_level is not None and record.phosphorus_level < 0:
                raise ValidationError(_("Phosphorus level cannot be negative."))
            if record.potassium_level is not None and record.potassium_level < 0:
                raise ValidationError(_("Potassium level cannot be negative."))
            if record.cation_exchange_capacity is not None and record.cation_exchange_capacity < 0:
                raise ValidationError(_("CEC cannot be negative."))
            if record.total_salinity is not None and record.total_salinity < 0:
                raise ValidationError(_("Salinity cannot be negative."))
            if record.soil_compaction_level is not None and record.soil_compaction_level < 0:
                raise ValidationError(_("Soil compaction level cannot be negative."))

    def action_update_soil_health_assessment(self):
        """Recalculate soil health metrics and recommendations"""
        for record in self:
            # Trigger recomputation of all computed fields
            record._compute_soil_health_score()
            record._compute_soil_health_category()
            record._compute_erosion_risk()
            record._compute_vra_recommendations()
            record.message_post(body=_("Soil health assessment updated. Current score: %.2f") % record.soil_health_score)

    def action_generate_soil_health_report(self):
        """Generate detailed soil health report"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('VRA Soil Health Report'),
            'res_model': 'agri.vra.soil.health.monitor',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
            'context': self.env.context,
        }

    def action_create_improvement_plan(self):
        """Create a soil improvement plan based on assessment"""
        for record in self:
            plan = f"""
            Soil Health Improvement Plan for {record.location_id.name if record.location_id else 'Unknown Location'}

            Current Status:
            - Soil Health Score: {record.soil_health_score or 0:.2f} ({record.soil_health_category or 'N/A'})
            - Erosion Risk: {record.erosion_risk_level or 'N/A'}

            Priority Actions:
            1. Address Critical Deficiencies:
               {record.improvement_recommendations or 'No critical deficiencies identified'}

            2. Recommended Practices:
               {record.recommended_practices or 'No specific practices recommended'}

            3. VRA Applications:
               {record.next_vra_recommendations or 'No VRA adjustments needed'}

            4. Monitoring Schedule:
               Next Assessment: {record.next_assessment_date or 'Not scheduled'}

            Implementation Timeline:
            - Immediate (0-30 days): Address urgent issues
            - Short-term (1-6 months): Implement primary recommendations
            - Long-term (6-12 months): Monitor and adjust based on results
            """
            record.improvement_recommendations = plan
            record.message_post(body=_("Soil health improvement plan created."))

    def action_schedule_next_assessment(self):
        """Schedule the next soil health assessment"""
        for record in self:
            if record.assessment_frequency:
                record.next_assessment_date = fields.Date.add(
                    fields.Date.context_today(record),
                    months={'monthly': 1, 'quarterly': 3, 'annually': 12}
                    [record.assessment_frequency]
                )
                record.message_post(body=_("Next soil health assessment scheduled for %s") % record.next_assessment_date)