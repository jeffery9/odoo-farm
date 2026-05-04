from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class StockPickingType(models.Model):
    """
    扩展 stock.picking.type 以支持"垫资分发"类型 [US-078-04]
    """
    _inherit = 'stock.picking.type'

    is_advancing_distribution = fields.Boolean(
        'Is Advancing Distribution',
        default=False,
        help='Check if this operation type is for advancing distribution to members'
    )