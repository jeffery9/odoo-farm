from odoo import fields, models, api, _

class IndustryVariety(models.Model):
    """Variety data for industry packages"""
    _name = 'farm.industry.variety'
    _description = 'Industry Package Variety Data'

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