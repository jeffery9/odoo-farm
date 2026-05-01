from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)

class AgriNeighborhoodRegistry(models.Model):
    """
    Registry for discovering nearby agents and assets within the same spatial grid. [US-70-2026]
    Level 1+: Neighborhood Discovery Service.
    """
    _name = 'agri.neighborhood.registry'
    _description = 'Agricultural Neighborhood Registry'
    _order = 'last_seen desc'

    spatial_grid_id = fields.Char("Grid ID", index=True, required=True)
    res_model = fields.Char("Entity Model", required=True)
    res_id = fields.Integer("Entity ID", required=True)
    
    agent_id = fields.Char("Agent identifier", compute="_compute_agent_id", store=True)
    last_seen = fields.Datetime("Last Seen", default=fields.Datetime.now)
    
    is_active = fields.Boolean("Is Active", default=True)

    @api.depends('res_model', 'res_id')
    def _compute_agent_id(self):
        for record in self:
            record.agent_id = f"{record.res_model}:{record.res_id}"

    # _sql_constraints = [
#         (.unique_entity_grid., 'unique(res_model, res_id, spatial_grid_id)', 
#          .An entity can only be registered once in a specific grid at a time.')
#     ]

    @api.model
    def register_presence(self, res_model, res_id, grid_id):
        existing = self.search([('res_model', '=', res_model), ('res_id', '=', res_id)])
        if existing:
            existing.write({'spatial_grid_id': grid_id, 'last_seen': fields.Datetime.now(), 'is_active': True})
        else:
            self.create({'res_model': res_model, 'res_id': res_id, 'spatial_grid_id': grid_id})

    def get_neighbors(self, grid_id, exclude_model=None, exclude_id=None):
        domain = [('spatial_grid_id', '=', grid_id), ('is_active', '=', True), ('last_seen', '>', fields.Datetime.now() - fields.Timedelta(hours=24))]
        if exclude_model and exclude_id:
            domain += ['!', ('res_model', '=', exclude_model), ('res_id', '=', exclude_id)]
        return self.search(domain)
