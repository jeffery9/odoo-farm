from odoo import models, fields, api, _

class AgriIndustryPlantingMixin(models.AbstractModel):
    """
    Agri Domain Level: Planting Physics. [US-002-01, US-014-2026]
    Defines the biological and physical standards for the planting sector.
    """
    _name = 'agri.industry.planting.mixin'
    _description = 'Agricultural Planting Standard Mixin'

    # Sector specific physics
    phenology_stage_id = fields.Many2one('agri.industry.physio.stage', string="Phenology Stage")
    seeding_depth = fields.Float("Target Seeding Depth (cm)")
    target_plant_density = fields.Float("Target Plant Density (plants/ha)")
    
    # Soil conditions integration
    optimal_moisture_range = fields.Char("Optimal Moisture Range (%)", help="e.g. 20-30")

    def validate_planting_evidence(self):
        """Domain logic to validate if planting was done correctly."""
        # Stub for sensor-based validation
        return True
