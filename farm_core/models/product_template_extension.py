from odoo import fields, models, api, _

class ProductTemplate(models.Model):
    """
    Product template extensions for agricultural products - replacing functionality from product_template.py
    """
    _inherit = ['product.template', 'agri.quality.gate.mixin']

    # Agricultural-specific fields
    agricultural_type = fields.Selection([
        ('land_parcel', 'Land Parcel'),
        ('animal', 'Animal'),
        ('animal_group', 'Animal Group'),
        ('equipment', 'Equipment'),
        ('input', 'Input'),
        ('output', 'Output'),
    ], string="Agricultural Type")

    # Agricultural-specific fields
    agri_variety = fields.Char("Variety/Species", tracking=True)
    breed_certificate_no = fields.Char("Breed Registration/Certificate No.")
    breeder_id = fields.Many2one('res.partner', string="Breeder/Source Organization")

    # Genetic & Physical Traits
    genetic_traits = fields.Text("Genetic Traits", help="Key characteristics like drought resistance, high yield, etc.")
    is_transgenic = fields.Boolean("GMO / Transgenic", default=False)

    # Seasonality Matrix [US-001-02]
    best_sowing_month_start = fields.Selection([(str(i), str(i)) for i in range(1, 13)], string="Sowing Start Month")
    best_sowing_month_end = fields.Selection([(str(i), str(i)) for i in range(1, 13)], string="Sowing End Month")
    harvest_season_notes = fields.Char("Harvest Season Description")
    born_at = fields.Datetime("Born At/Started At")
    dead_at = fields.Datetime("Dead At/Terminated At")
    identification_number = fields.Char("Identification No.")
    
    # GS1 Global Identifiers [EPCIS Alignment]
    gs1_gtin = fields.Char('GS1 GTIN', help='Global Trade Item Number (8, 12, 13, or 14 digits)', size=14)

    # Growth curve data
    growth_curve_ids = fields.One2many('agri.biological.growth.curve', 'product_id', string="Growth Curve")

    def get_expected_weight(self, age_days):
        """Get expected weight based on age"""
        curve = self.growth_curve_ids.filtered(lambda c: c.age_days <= age_days).sorted('age_days', reverse=True)
        return curve[0].target_weight if curve else 0.0

    # Lot property definitions
    lot_properties_definition = fields.PropertiesDefinition('Lot Properties Definition')

    # Nutrient content
    n_content = fields.Float("Nitrogen (N) %", help="Nitrogen percentage content")
    p_content = fields.Float("Phosphorus (P) %", help="Phosphorus percentage content")
    k_content = fields.Float("Potassium (K) %", help="Potassium percentage content")

    # MTO lead time logic
    growth_duration = fields.Integer("Growth Duration (Days)", help="Standard growth period from planting to harvest.")

    # Generation tracking (G0-G3)
    agri_generation = fields.Selection([
        ('g0', 'G0 (Breeder Seed/Original)'),
        ('g1', 'G1 (Foundation Seed)'),
        ('g2', 'G2 (Registered Seed)'),
        ('g3', 'G3 (Certified/Commercial Seed)')
    ], string="Agri Generation", help="Generation tracking for seeds or livestock.")

    # Biological asset accounting
    is_biological_asset = fields.Boolean("Is Biological Asset", default=False)
    maturity_age_days = fields.Integer("Maturity Age (Days)", help="Age at which the asset is considered mature (e.g. starts producing fruit/milk).")

    # Agricultural UOM flexible conversion
    standard_dose = fields.Float("Standard Dose", help="Recommended quantity per unit of area.")
    dose_uom_id = fields.Many2one('uom.uom', string="Dose Unit", help="Unit for the dose (e.g., kg/mu, L/ha).")