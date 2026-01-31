from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)

class AgriSoilAnalysisMixin(models.AbstractModel):
    """
    Agri Domain Level: Soil Health Mixin. [US-01-09, US-104-2026]
    Universal soil physics: pH, Organic Matter, NPK, and Heavy Metals.
    """
    _name = 'agri.soil.analysis.mixin'
    _description = 'Agricultural Soil Health Mixin'

    # Universal Nutrient Indicators
    ph_level = fields.Float("pH Level", digits=(10, 2))
    organic_matter = fields.Float("Organic Matter (%)")
    nitrogen_content = fields.Float("Nitrogen (mg/kg)")
    phosphorus_content = fields.Float("Phosphorus (mg/kg)")
    potassium_content = fields.Float("Potassium (mg/kg)")

    # Universal Heavy Metals (Environmental Sovereignty)
    lead_content = fields.Float("Lead (Pb) (mg/kg)")
    cadmium_content = fields.Float("Cadmium (Cd) (mg/kg)")
    mercury_content = fields.Float("Mercury (Hg) (mg/kg)")
    arsenic_content = fields.Float("Arsenic (As) (mg/kg)")
    chromium_content = fields.Float("Chromium (Cr) (mg/kg)")
    copper_content = fields.Float("Copper (Cu) (mg/kg)")
    zinc_content = fields.Float("Zinc (Zn) (mg/kg)")
    nickel_content = fields.Float("Nickel (Ni) (mg/kg)")

    # Trace Elements
    magnesium = fields.Float("Magnesium (mg/kg)")
    calcium = fields.Float("Calcium (mg/kg)")

class AgriSoilAnalysis(models.Model):
    """
    Agri Domain Level: Soil Analysis Registry.
    Universal record of a soil physical/chemical test.
    """
    _name = 'agri.soil.analysis'
    _description = 'Agricultural Soil Analysis Standard'
    _inherit = [
        'agri.soil.analysis.mixin',
        'agri.sustainability.mixin', # Level 0: Redlines
        'agri.evidence.mixin',       # Level 2: Physical Proof
        'mail.thread'
    ]

    name = fields.Char("Analysis Identity", required=True, index=True)
    analysis_date = fields.Date("Analysis Date", default=fields.Date.today, required=True)
    
    # Grid Linkage
    spatial_grid_id = fields.Char("Target Grid ID", help="The 11m grid where the sample was taken.")
