# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class AgriBiodiversityIndicator(models.Model):
    """
    Agri Domain Level: Biodiversity Indicator. [US-104-2026]
    Standard observation log for ecological health across the Agri domain.
    Refactored from farm.biodiversity.indicator with 100% logic retention.
    """
    _name = 'agri.sustainability.biodiversity.indicator'
    _description = 'Biodiversity Observation Log'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'agri.sustainability.mixin', 'agri.evidence.mixin']
    _order = 'date desc'

    date = fields.Date("Observation Date", default=fields.Date.today, required=True)
    location_id = fields.Many2one('farm.location', string="Physical Container", domain=[('is_land_parcel', '=', True)])
    
    indicator_type = fields.Selection([
        ('insect', 'Insects/Pollinators'),
        ('bird', 'Birds'),
        ('plant', 'Wild Vegetation'),
        ('soil_life', 'Soil Life'),
        ('other', 'Other Biodiversity')
    ], string="Indicator Category", required=True)
    
    species_name = fields.Char("Species/Common Name", translate=True)
    count_observed = fields.Integer("Population Abundance", help="Number of individuals or density observed.")
    
    photo = fields.Binary("Photo Evidence", help="Visual proof of the observation.")
    notes = fields.Text("Contextual Notes", translate=True)

    # --- 100% Original Logic Retention (RESTORED) ---
    def action_verify_observation(self):
        """Domain logic to verify biodiversity data integrity."""
        self.ensure_one()
        # In 2026, this triggers a Level 2 physical evidence audit
        return self.perform_evidence_audit()
    # --- End of Original Logic ---

class AgriEcologicalZone(models.Model):
    """
    Agri Domain Level: Ecological Infrastructure. [US-104-2026]
    Represents non-productive ecological areas (hedges, ponds, forests).
    Refactored from farm.ecological.zone with 100% logic retention.
    """
    _name = 'agri.sustainability.ecological.zone'
    _description = 'Agricultural Ecological Infrastructure'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'agri.geospatial.mixin']

    name = fields.Char("Ecological Zone Name", required=True, translate=True)
    zone_type = fields.Selection([
        ('hedge', 'Hedge'),
        ('buffer', 'Buffer Strip'),
        ('pond', 'Ecological Pond'),
        ('forest', 'Forest Patch'),
        ('fallow', 'Fallow Land')
    ], string="Zone Category", required=True)
    
    area = fields.Float("Area (sqm)", help="Surface area of the ecological infrastructure.")
    location_id = fields.Many2one('farm.location', string="Associated Operational Parcel")
    
    active = fields.Boolean(default=True)