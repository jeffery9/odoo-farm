from odoo import models, fields, api
from odoo.exceptions import ValidationError

class AgriSustainabilityCarbonModel(models.Model):
    """
    US-060-13: 行业特定碳排放模型ISL扩展
    Industry Specific Carbon Model for implementing industry-specific carbon emission calculations
    """
    _name = 'agri.sustainability.carbon.model'
    _description = 'Agricultural Industry Specific Carbon Model'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Model Name', required=True)
    industry_type = fields.Selection([
        ('crop_farming', 'Crop Farming'),
        ('livestock', 'Livestock'),
        ('dairy', 'Dairy'),
        ('poultry', 'Poultry'),
        ('aquaculture', 'Aquaculture'),
        ('horticulture', 'Horticulture'),
        ('food_processing', 'Food Processing'),
        ('beverage', 'Beverage'),
        ('biofuel', 'Biofuel'),
        ('textile', 'Textile'),
        ('pharmaceutical', 'Pharmaceutical'),
        ('chemical', 'Chemical'),
        ('other', 'Other')
    ], string='Industry Type', required=True)
    description = fields.Text('Description')
    model_version = fields.Char('Model Version', default='1.0')
    active = fields.Boolean('Active', default=True)
    calculation_method = fields.Selection([
        ('ipcc', 'IPCC Guidelines'),
        ('ghg_protocol', 'GHG Protocol'),
        ('iso_14064', 'ISO 14064'),
        ('custom', 'Custom Methodology'),
        ('regulatory', 'Regulatory Standard')
    ], string='Calculation Method', required=True)
    scope_1_supported = fields.Boolean('Scope 1 Supported', help='Direct emissions from owned/controlled sources')
    scope_2_supported = fields.Boolean('Scope 2 Supported', help='Indirect emissions from purchased energy')
    scope_3_supported = fields.Boolean('Scope 3 Supported', help='Other indirect emissions')

    # Industry-specific parameters
    emission_factors = fields.Text('Emission Factors JSON', help='JSON formatted emission factors specific to this industry')
    carbon_intensity_threshold = fields.Float('Carbon Intensity Threshold (kgCO2e/unit)',
                                              help='Threshold for carbon intensity in this industry')
    reporting_standard = fields.Selection([
        ('gri', 'GRI Standards'),
        ('sasb', 'SASB Standards'),
        ('tcfd', 'TCFD Recommendations'),
        ('cdp', 'CDP Questionnaire'),
        ('ghgp', 'GHG Protocol'),
        ('iso_14083', 'ISO 14083'),
        ('custom', 'Custom Standard')
    ], string='Reporting Standard')
    compliance_requirements = fields.Text('Compliance Requirements')
    audit_frequency = fields.Selection([
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('annually', 'Annually')
    ], string='Audit Frequency', default='annually')

    # Calculation coefficients
    direct_emission_coefficient = fields.Float('Direct Emission Coefficient',
                                               help='Coefficient for direct emissions calculation')
    indirect_energy_coefficient = fields.Float('Indirect Energy Coefficient',
                                               help='Coefficient for indirect energy emissions')
    supply_chain_coefficient = fields.Float('Supply Chain Coefficient',
                                            help='Coefficient for scope 3 emissions from supply chain')

    # Regulatory compliance
    applicable_regulations = fields.Text('Applicable Regulations')
    verification_requirements = fields.Text('Verification Requirements')

    # Related calculation rules

    @api.constrains('carbon_intensity_threshold', 'direct_emission_coefficient',
                    'indirect_energy_coefficient', 'supply_chain_coefficient')
    def _check_positive_coefficients(self):
        """Ensure all coefficients and thresholds are non-negative"""
        for record in self:
            if record.carbon_intensity_threshold < 0:
                raise ValidationError(_("Carbon intensity threshold cannot be negative."))
            if record.direct_emission_coefficient < 0:
                raise ValidationError(_("Direct emission coefficient cannot be negative."))
            if record.indirect_energy_coefficient < 0:
                raise ValidationError(_("Indirect energy coefficient cannot be negative."))
            if record.supply_chain_coefficient < 0:
                raise ValidationError(_("Supply chain coefficient cannot be negative."))

    def action_apply_model(self, product_or_operation):
        """
        Apply this industry-specific model to a specific product or operation
        This would typically be called from other models to calculate emissions using industry-specific factors
        """
        # This would be implemented to work with other models to apply industry-specific calculations
        # For now, we'll just return a structure that other models can use
        result = {
            'emission_factors': self.emission_factors,
            'direct_coefficient': self.direct_coefficient,
            'indirect_coefficient': self.indirect_energy_coefficient,
            'scope3_coefficient': self.supply_chain_coefficient,
            'threshold': self.carbon_intensity_threshold
        }
        return result