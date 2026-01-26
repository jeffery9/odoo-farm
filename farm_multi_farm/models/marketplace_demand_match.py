from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class MarketplaceDemandMatch(models.Model):
    """
    市场供需匹配 [US-19-11]
    """
    _name = 'marketplace.demand.match'
    _description = 'Marketplace Demand Match'

    listing_id = fields.Many2one('internal.marketplace', string='Listing', required=True, ondelete='cascade')
    member_id = fields.Many2one('cooperative.member', string='Member', required=True)
    quantity = fields.Float('Quantity', required=True)
    priority = fields.Integer('Priority', default=1)
    match_date = fields.Date('Match Date', default=fields.Date.context_today)