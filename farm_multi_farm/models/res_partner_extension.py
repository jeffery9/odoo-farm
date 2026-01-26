from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    """
    扩展 res.partner 以支持内部信用余额 [US-48-04]
    """
    _inherit = 'res.partner'

    internal_credit_balance = fields.Float(
        'Internal Credit Balance',
        default=0.0,
        help='Internal credit balance for cooperative transactions'
    )