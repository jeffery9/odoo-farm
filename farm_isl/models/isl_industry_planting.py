from odoo import models, fields, api, _

class ISLIndustryPlanting(models.Model):
    """
    Industry Standard Layer: Planting Sector. [US-014-2026]
    Provides a standardized interface for planting operations.
    Delegates to agri.location or agri.task via mixin injection.
    Refactored to agri namespace for domain alignment.
    """
    _name = 'agri.isl.industry.planting'
    _description = 'ISL Planting Specification'
    _inherit = ['agri.industry.planting.mixin']

    name = fields.Char("Spec Name", required=True)
    standard_id = fields.Char("Global Standard ID", help="e.g. GLOBALG.A.P. Planting Standard")
    
    # ISL specific logic
    is_organic_compatible = fields.Boolean("Organic Compatible", default=True)
    min_buffer_zone_meters = fields.Float("Min Buffer Zone (m)", default=5.0)