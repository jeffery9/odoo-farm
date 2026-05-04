from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class ProcurementPlanningLine(models.Model):
    """
    农资统筹预分配明细 [US-042-12]
    """
    _name = 'procurement.planning.line'
    _description = 'Procurement Planning Line'

    planning_id = fields.Many2one('procurement.planning', string='Planning', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Product', required=True)
    total_required = fields.Float('Total Required', required=True)
    total_available = fields.Float('Total Available', default=0.0)
    total_allocated = fields.Float('Total Allocated', compute='_compute_total_allocated', store=True, precompute=True)
    remaining_quantity = fields.Float('Remaining Quantity', compute='_compute_remaining', store=True, precompute=True)

    allocation_lines = fields.One2many('procurement.allocation.line', 'planning_line_id', string='Allocation Lines')

    @api.depends('allocation_lines.quantity')
    def _compute_total_allocated(self):
        for line in self:
            line.total_allocated = sum(allocation.quantity for allocation in line.allocation_lines)

    @api.depends('total_available', 'total_allocated')
    def _compute_remaining(self):
        for line in self:
            line.remaining_quantity = line.total_available - line.total_allocated