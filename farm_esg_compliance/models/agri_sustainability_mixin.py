from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class AgriSustainabilityMixin(models.AbstractModel):
    """
    US-101 DNA: Agri Sustainability Mixin - Non-Functional Requirement (Plugin Style)
    This abstract model serves as the foundational DNA for ESG compliance,
    providing inheritable sustainability features for all agricultural models.
    
    Logic only executes if 'is_esg_sustainability_active' is enabled in settings.
    """
    _name = 'agri.sustainability.mixin'
    _description = 'Agri Sustainability Mixin - DNA Framework'

    # Plugin State Control
    is_sustainability_enabled = fields.Boolean(
        compute='_compute_is_sustainability_enabled',
        help="Technical field to hide/show ESG fields based on plugin state"
    )

    def _compute_is_sustainability_enabled(self):
        is_active = self.env['ir.config_parameter'].sudo().get_param('farm_esg.is_esg_sustainability_active')
        for record in self:
            record.is_sustainability_enabled = bool(is_active)

    # DNA-level fields (Preserved from original implementation)
    environmental_impact = fields.Float(
        'Environmental Score (0-100)',
        help='Environmental impact score based on resource usage, emissions, and ecological footprint',
        group_operator='avg'
    )
    social_impact = fields.Float(
        'Social Score (0-100)',
        help='Social impact score based on community benefit, labor practices, and stakeholder engagement',
        group_operator='avg'
    )
    economic_impact = fields.Float(
        'Economic Score (0-100)',
        help='Economic impact score based on profitability, cost efficiency, and economic sustainability',
        group_operator='avg'
    )
    
    overall_sustainability_score = fields.Float(
        'Overall Sustainability Score',
        compute='_compute_sustainability_dna',
        store=True,
        help='Composite sustainability score from environmental, social, and economic impacts',
        group_operator='avg'
    )

    # ESG compliance status tracking
    esg_compliance_status = fields.Selection([
        ('pending', 'Pending Assessment'),
        ('compliant', 'Compliant'),
        ('non_compliant', 'Non-Compliant'),
        ('exceeds_standards', 'Exceeds Standards'),
    ], string='ESG Compliance Status', compute='_compute_esg_compliance_status', store=True, precompute=True)

    # Sustainability certification tracking
    sustainability_certifications = fields.Many2many(
        'farm.certification',
        string='Sustainability Certifications',
        help='Sustainability certifications applicable to this record'
    )

    # Standards governance
    applicable_esg_standards = fields.Text(
        'Applicable ESG Standards',
        help='ESG standards and regulations applicable to this record'
    )

    # Sustainability notes and recommendations
    sustainability_notes = fields.Text('Sustainability Notes')
    sustainability_recommendations = fields.Text('Sustainability Recommendations')

    @api.depends('environmental_impact', 'social_impact', 'economic_impact')
    def _compute_sustainability_dna(self):
        """Plugin-aware DNA computation"""
        is_active = self.env['ir.config_parameter'].sudo().get_param('farm_esg.is_esg_sustainability_active')
        for record in self:
            if not is_active:
                record.overall_sustainability_score = 0.0
                continue
            
            scores = [s for s in [record.environmental_impact, record.social_impact, record.economic_impact] if s]
            record.overall_sustainability_score = sum(scores) / len(scores) if scores else 0.0

    @api.depends('overall_sustainability_score')
    def _compute_esg_compliance_status(self):
        """Compute ESG compliance status based on overall sustainability score"""
        for record in self:
            if record.overall_sustainability_score >= 80:
                record.esg_compliance_status = 'exceeds_standards'
            elif record.overall_sustainability_score >= 60:
                record.esg_compliance_status = 'compliant'
            elif record.overall_sustainability_score >= 30:
                record.esg_compliance_status = 'non_compliant'
            else:
                record.esg_compliance_status = 'pending'

    def action_update_sustainability_assessment(self):
        """DNA-level action to update sustainability assessment (Plugin-Aware)"""
        is_active = self.env['ir.config_parameter'].sudo().get_param('farm_esg.is_esg_sustainability_active')
        if not is_active:
            return False

        for record in self:
            assessment = f"""
Sustainability Assessment for Record: {record.display_name}
Environmental Impact: {record.environmental_impact or 0}/100
Social Impact: {record.social_impact or 0}/100
Economic Impact: {record.economic_impact or 0}/100
Overall Score: {record.overall_sustainability_score or 0}/100
Compliance Status: {dict(record._fields['esg_compliance_status'].selection).get(record.esg_compliance_status, record.esg_compliance_status)}

Last Updated: {fields.Datetime.now()}
            """
            if record.sustainability_notes:
                record.sustainability_notes += f"\n\n{assessment}"
            else:
                record.sustainability_notes = assessment

    def action_generate_sustainability_recommendations(self):
        """DNA-level action to generate recommendations (Plugin-Aware)"""
        is_active = self.env['ir.config_parameter'].sudo().get_param('farm_esg.is_esg_sustainability_active')
        if not is_active:
            return False

        for record in self:
            recommendations = []
            if record.environmental_impact and record.environmental_impact < 60:
                recommendations.append("Consider implementing resource efficiency improvements.")
            if record.social_impact and record.social_impact < 60:
                recommendations.append("Evaluate community engagement and stakeholder practices.")
            if record.economic_impact and record.economic_impact < 60:
                recommendations.append("Review cost structures and revenue optimization.")
            
            record.sustainability_recommendations = '\n'.join(recommendations) if recommendations else "No specific recommendations."

    def _validate_esg_compliance(self):
        """
        DNA-level validation
        Ensures ESG compliance is considered at the data level.
        Blocks operations if ESG thresholds are exceeded.
        """
        is_active = self.env['ir.config_parameter'].sudo().get_param('farm_esg.is_esg_sustainability_active')
        if not is_active:
            return True

        for record in self:
            if (record.environmental_impact is not None and (record.environmental_impact < 0 or record.environmental_impact > 100)):
                raise ValidationError(_("Environmental impact score must be between 0 and 100."))
            
            # Check for critical violations if thresholds are defined
            if record.overall_sustainability_score > 0 and record.overall_sustainability_score < 30:
                # Potential block based on score
                _logger.warning("Low sustainability score (%s) detected for %s", 
                               record.overall_sustainability_score, record.display_name)
        return True

    def check_operation_esg_gate(self):
        """
        [Level 0: Standard] Pre-validation gate for operations.
        Returns False if ESG criteria are not met.
        """
        if not self.env['ir.config_parameter'].sudo().get_param('farm_esg.is_esg_sustainability_active'):
            return True
            
        for record in self:
            # Logic: If overall score is too low, block the operation
            if record.overall_sustainability_score > 0 and record.overall_sustainability_score < 20:
                raise UserError(_("Operation blocked: Sustainability score (%s) is below the minimum threshold (20).") % 
                               record.overall_sustainability_score)
        return True

    @api.model
    def create(self, vals):
        record = super().create(vals)
        record._validate_esg_compliance()
        record.action_update_sustainability_assessment()
        record.action_generate_sustainability_recommendations()
        return record

    def write(self, vals):
        result = super().write(vals)
        self._validate_esg_compliance()
        esg_fields = {'environmental_impact', 'social_impact', 'economic_impact'}
        if any(field in vals for field in esg_fields):
            self.action_update_sustainability_assessment()
            self.action_generate_sustainability_recommendations()
        return result