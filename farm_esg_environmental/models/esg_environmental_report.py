from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ESGEnvironmentalReport(models.Model):
    """
    US-30-XX: ESG Environmental Report
    ESG Environmental reporting that extends base ESG functionality with environmental data
    """
    _name = 'esg.environmental.report'
    _description = 'ESG Environmental Report'
    _inherit = ['esg.performance.report']  # Inherit from base ESG performance report

    # Environmental-specific fields
    carbon_footprint_tco2e = fields.Float('Carbon Footprint (tCO2e)', help='Total carbon footprint in tons CO2 equivalent')
    water_stress_score = fields.Float('Water Stress Score (0-100)', help='Water stress score for the area')
    biodiversity_risk_score = fields.Float('Biodiversity Risk Score (0-100)', help='Risk score for biodiversity impact')

    # Environmental assessment references (extending the base assessment_ids field)
