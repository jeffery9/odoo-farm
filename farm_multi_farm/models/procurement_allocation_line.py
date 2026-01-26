from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class ProcurementAllocationLine(models.Model):
    """
    农资分配明细 [US-19-12]
    """
    _name = 'procurement.allocation.line'
    _description = 'Procurement Allocation Line'

    planning_line_id = fields.Many2one('procurement.planning.line', string='Planning Line', required=True, ondelete='cascade')
    member_id = fields.Many2one('cooperative.member', string='Member', required=True)
    quantity = fields.Float('Quantity', required=True)
    priority_score = fields.Float('Priority Score', help='Based on historical contribution or other factors')
    allocation_date = fields.Date('Allocation Date', default=fields.Date.context_today)