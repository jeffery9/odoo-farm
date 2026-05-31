# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class AgriBiodiversityIndicator(models.Model):
    """
    Agri Domain Level: Biodiversity Indicator. [US-014-2026]
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
    Agri Domain Level: Ecological Infrastructure. [US-014-2026]
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


class FarmLocation(models.Model):
    """
    [Anji Model Integration] Ecological Value Extension.
    Calculates Gross Ecosystem Product (GEP) for land parcels.
    """
    _name = 'farm.location'
    _inherit = 'farm.location'

    gep_score = fields.Float("Ecological GEP Score", compute='_compute_gep_score', store=True, group_operator="avg")
    biodiversity_index = fields.Float("Biodiversity Index", compute='_compute_gep_score', store=True)
    eco_zone_coverage = fields.Float("Eco-infrastructure Coverage (%)", compute='_compute_gep_score', store=True)

    @api.depends('calculated_area_ha', 'land_area')
    def _compute_gep_score(self):
        """
        [US-ANJI-01] GEP Calculation Algorithm.
        GEP = (Biodiversity Factor * 0.6) + (Eco Zone Factor * 0.4)
        """
        for parcel in self:
            # 1. Biodiversity Component
            observations = self.env['agri.sustainability.biodiversity.indicator'].search([
                ('location_id', '=', parcel.id)
            ])
            # Count species abundance and variety
            total_abundance = sum(observations.mapped('count_observed'))
            variety_count = len(set(observations.mapped('indicator_type')))
            bio_factor = (total_abundance * 0.5) + (variety_count * 10.0)
            parcel.biodiversity_index = min(100.0, bio_factor)

            # 2. Eco-Infrastructure Component
            zones = self.env['agri.sustainability.ecological.zone'].search([
                ('location_id', '=', parcel.id)
            ])
            total_eco_area = sum(zones.mapped('area')) # in sqm
            parcel_area_sqm = parcel.land_area or (parcel.calculated_area_ha * 10000.0)
            
            coverage = (total_eco_area / parcel_area_sqm * 100.0) if parcel_area_sqm > 0 else 0.0
            parcel.eco_zone_coverage = min(100.0, coverage)

            # 3. Final GEP Score (0-100 normalized)
            parcel.gep_score = (parcel.biodiversity_index * 0.6) + (parcel.eco_zone_coverage * 0.4)
            
            if parcel.gep_score > 80:
                parcel.message_post(body=_("Ecological Excellence: GEP Score %s reached.") % round(parcel.gep_score, 2))
