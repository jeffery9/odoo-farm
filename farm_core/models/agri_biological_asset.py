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
        'agri.sustainability.mixin', # Level 0: Impact
        'agri.evidence.mixin',       # Level 2: Evidence
        'mail.thread'
    ]

    name = fields.Char("Standard Identity", required=True, index=True)
    active = fields.Boolean(default=True)

    parent_asset_id = fields.Many2one('agri.biological.asset', string="Domain Parent")
    sub_asset_ids = fields.One2many('agri.biological.asset', 'parent_asset_id', string="Biological Offspring")
