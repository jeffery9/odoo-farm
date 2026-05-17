from odoo import fields, models


class CommonAgriculturalFields(models.AbstractModel):
    """
    Abstract model containing common field definitions for agricultural entities
    """
    _name = 'farm.core.common.fields'
    _description = 'Farm Core Common Fields'

    # Agricultural type classification
    agricultural_type = fields.Selection([
        ('land_parcel', 'Land Parcel'),
        ('animal', 'Animal'),
        ('animal_group', 'Animal Group'),
        ('equipment', 'Equipment'),
        ('input', 'Input'),
        ('output', 'Output'),
    ], string="Agricultural Type")

    # Basic identification
    identification_number = fields.Char("Identification No.")
    batch_number = fields.Char("Batch Number")

    # Growth and development
    growth_stage = fields.Selection([
        ('newborn', 'Newborn/Seedling'),
        ('growing', 'Growing'),
        ('mature', 'Mature/Adult'),
        ('harvested', 'Harvested/Culled')
    ], string="Growth Stage", default='newborn')

    # Generational tracking (G0-G3)
    generation = fields.Selection([
        ('g0', 'G0 (Breeder)'),
        ('g1', 'G1 (Foundation)'),
        ('g2', 'G2 (Registered)'),
        ('g3', 'G3 (Commercial)')
    ], string="Generation", help="Generation tracking for seeds or livestock.")

    # Nutrient content
    n_content = fields.Float("Nitrogen (N) %", help="Nitrogen percentage content")
    p_content = fields.Float("Phosphorus (P) %", help="Phosphorus percentage content")
    k_content = fields.Float("Potassium (K) %", help="Potassium percentage content")

    # Growth parameters
    growth_duration = fields.Integer("Growth Duration (Days)")
    maturity_age_days = fields.Integer("Maturity Age (Days)")

    # Quality grading
    quality_grade = fields.Selection([
        ('grade_a', 'Grade A'),
        ('grade_b', 'Grade B'),
        ('grade_c', 'Grade C'),
    ], string="Quality Grade")

    # Compliance and safety
    withdrawal_period_days = fields.Integer("Withdrawal Period (Days)")

    # Production cycle
    production_cycle = fields.Selection([
        ('annual', 'Annual'),
        ('perennial', 'Perennial'),
    ], string="Production Cycle", default='annual')

    # Dynamic properties for flexible attribute management
    properties_definition = fields.PropertiesDefinition('Properties Definition')
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    properties = fields.Properties(
        'Properties',
        definition='company_id.properties_definition'
    )