from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)

class AgriBiologicalAssetMixin(models.AbstractModel):
    """
    Agri Domain Level: Biological Traits Mixin. [US-014-2026]
    Universal biological facts: pedigree, growth stages, and DNA markers.
    """
    _name = 'agri.biological.asset.mixin'
    _description = 'Agricultural Biological Traits Mixin'

    # Domain Standard Traits
    agricultural_type = fields.Selection([
        ('animal', 'Animal'),
        ('plant', 'Plant'),
        ('tree', 'Tree'),
        ('fungi', 'Fungi'),
        ('microbe', 'Microbial')
    ], string="Biological Domain", default='animal', required=True)

    birth_date = fields.Date("Birth/Germination Date")
    maturity_date = fields.Date("Target Maturity Date")
    is_mature = fields.Boolean("Physiological Maturity", default=False)

    # Universal Growth Stages (BBCH Alignment)
    growth_stage_id = fields.Many2one('agri.industry.physio.stage', string="Current Physio Stage")
    
    # Genetic & Quality Fingerprint

    base_weight_kg = fields.Float("Base Weight (kg)", default=0.0, tracking=True)
    fcr_ratio = fields.Float("Feed Conversion Ratio (FCR)", default=2.5, help="Kg of feed required to produce 1 Kg of asset weight.")
    dna_marker = fields.Char("Genetic Marker / DNA ID")
    quality_grade = fields.Selection([
        ('premium', 'Premium / S Grade'),
        ('standard', 'Standard / A Grade'),
        ('utility', 'Utility / B Grade'),
    ], string="Domain Quality Grade")

class AgriBiologicalAsset(models.Model):
    """
    Agri Domain Level: Biological Asset Registry.
    The universal physical entity representing a living asset in the Agri domain.
    """
    _name = 'agri.biological.asset'
    _description = 'Agricultural Biological Asset Standard'
    _inherit = [
        'agri.biological.asset.mixin',
        'agri.growth.cycle.mixin',    # Level 1: Growth
        'agri.biological.inventory.mixin', # Level 1: Inventory
        'agri.sustainability.mixin', # Level 0: Impact
        'agri.evidence.mixin',       # Level 2: Evidence
        'mail.thread'
    ]

    # Yield & Production Targets
    target_yield = fields.Float("Target Yield", default=0.0)
    actual_yield = fields.Float("Actual Yield", default=0.0)

    name = fields.Char("Standard Identity", required=True, index=True)
    active = fields.Boolean(default=True)

    owner_id = fields.Many2one('res.partner', string="Legal Owner")

    parent_asset_id = fields.Many2one('agri.biological.asset', string="Domain Parent")
    sub_asset_ids = fields.One2many('agri.biological.asset', 'parent_asset_id', string="Biological Offspring")

    tracking_carrier_ids = fields.One2many(
        'stock.matter.tracking',
        'biological_asset_id',
        string='Active Carrier Containers',
        help="The physical tracking carriers carrying this biological asset."
    )

    current_weight = fields.Float(
        string='Current Weight (kg)',
        compute='_compute_carrier_physical_properties',
        store=False,
        help="Dynamic weight resolved from active tracking carriers."
    )

    life_stage = fields.Selection([
        ('juvenile', 'Juvenile / Seedling'),
        ('growing', 'Growing / Fattening'),
        ('mature', 'Mature / Breeding'),
        ('harvested', 'Harvested / Culled')
    ], string='Life Stage', compute='_compute_carrier_physical_properties', store=False)

    last_gps_lat = fields.Float('Last Latitude', compute='_compute_carrier_physical_properties', store=False)
    last_gps_lng = fields.Float('Last Longitude', compute='_compute_carrier_physical_properties', store=False)

    @api.depends('tracking_carrier_ids', 'tracking_carrier_ids.current_weight', 'tracking_carrier_ids.life_stage', 'tracking_carrier_ids.last_gps_lat', 'tracking_carrier_ids.last_gps_lng')
    def _compute_carrier_physical_properties(self):
        for asset in self:
            carriers = asset.tracking_carrier_ids.filtered(lambda c: c.vessel_phase != 'dirty')
            if carriers:
                primary = carriers[0]
                asset.current_weight = primary.current_weight
                asset.life_stage = primary.life_stage
                asset.last_gps_lat = primary.last_gps_lat
                asset.last_gps_lng = primary.last_gps_lng
            else:
                asset.current_weight = 0.0
                asset.life_stage = 'juvenile'
                asset.last_gps_lat = 0.0
                asset.last_gps_lng = 0.0
