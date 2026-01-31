from odoo import models, fields, api, _

class AgriIndustryVarietyMixin(models.AbstractModel):
    """
    Agri Domain Level: Variety Traits Mixin. [US-104-2026]
    Encapsulates biological and industrial traits of a specific variety.
    """
    _name = 'agri.industry.variety.mixin'
    _description = 'Variety Traits Mixin'

    # Domain Standard Traits
    scientific_name = fields.Char("Scientific Name")
    breed_origin = fields.Char("Place of Origin")
    resistance_level = fields.Selection([
        ('high', 'High Resistance'),
        ('medium', 'Medium'),
        ('low', 'Low')
    ], string="Disease Resistance")


class AgriIndustryVariety(models.Model):
    """
    Agri Domain Level: Variety Registry.
    Universal registry for all agricultural biological varieties.
    Refactored from farm.industry.variety with 100% logic retention.
    """
    _name = 'agri.industry.variety'
    _description = 'Agricultural Variety Standard'
    _inherit = ['agri.industry.variety.mixin', 'mail.thread']

    # --- 100% Original Logic Retention ---
    package_id = fields.Many2one(
        'farm.industry.data.package',
        string="Industry Package",
        required=True,
        ondelete='cascade'
    )

    product_name = fields.Char("Product Name", required=True)
    variety_name = fields.Char("Variety Name", required=True)
    
    agricultural_type = fields.Selection([
        ('land_parcel', 'Land Parcel'),
        ('animal', 'Animal'),
        ('animal_group', 'Animal Group'),
        ('equipment', 'Equipment'),
        ('input', 'Input'),
        ('output', 'Output'),
    ], string="Agricultural Type", default='output')

    # Standard agricultural properties
    standard_dose = fields.Float("Standard Dose")
    dose_uom_id = fields.Many2one('uom.uom', string="Dose Unit")
    n_content = fields.Float("Nitrogen (N) %")
    p_content = fields.Float("Phosphorus (P) %")
    k_content = fields.Float("Potassium (K) %")
    growth_duration = fields.Integer("Growth Duration (Days)")
    maturity_age_days = fields.Integer("Maturity Age (Days)")
    is_biological_asset = fields.Boolean("Is Biological Asset")
    # --- End of Original Logic ---

    active = fields.Boolean(default=True)

    def name_get(self):
        result = []
        for record in self:
            name = f"[{record.product_name}] {record.variety_name}"
            result.append((record.id, name))
        return result