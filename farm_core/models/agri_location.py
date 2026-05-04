from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)

class AgriLocation(models.Model):
    """
    Agri Domain Level: Physical Location. [US-014-2026]
    The primary physical entity representing a geographic container in the Agri domain.
    Used by all sub-sectors (Farming, Forestry, Aquaculture, etc.)
    """
    _name = 'agri.location'
    _description = 'Agricultural Physical Location'
    _inherit = [
        'agri.geospatial.mixin',     # Level 1: Spatial Grid & GIS
        'agri.sustainability.mixin', # Level 0: Environmental Context
        'agri.embedding.mixin',      # Level 2: Knowledge Grounding
        'mail.thread'
    ]

    name = fields.Char("Location ID/Name", required=True, index=True)
    location_type = fields.Selection([
        ('field', 'Open Field / Plot'),
        ('greenhouse', 'Greenhouse / CEA'),
        ('barn', 'Barn / Stable'),
        ('pond', 'Pond / Tank'),
        ('processing', 'Processing Facility'),
        ('other', 'Other Container')
    ], string="Physical Type", required=True, default='field')

    parent_id = fields.Many2one('agri.location', string="Parent Location")
    child_ids = fields.One2many('agri.location', 'parent_id', string="Sub-locations")

    active = fields.Boolean(default=True)

    def _get_embedding_content(self):
        return f"Agri Location {self.name} ({self.location_type}) at grid {self.spatial_grid_id}."
