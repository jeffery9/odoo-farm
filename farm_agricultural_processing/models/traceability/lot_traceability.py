# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class StockLotTraceabilityExtension(models.Model):
    _inherit = 'stock.lot'

    # 批次溯源 [US-14-03]
    parent_lot_id = fields.Many2one('stock.lot', string="Parent Lot/Origin", help="Trace back to the raw material lot")
    child_lot_ids = fields.One2many('stock.lot', 'parent_lot_id', string="Derived Products")

    # 性能优化：写入时预计算的全路径 [Pre-calculated Path]
    full_traceability_path = fields.Text("Full Traceability Path", readonly=True,
                                       help="Flattened upstream lot IDs for instant lookup.")

    # 分级与元数据 [US-14-05]
    quality_grade = fields.Selection([
        ('a', 'Grade A / Premium'),
        ('b', 'Grade B / Standard'),
        ('c', 'Grade C / Processing'),
        ('loss', 'Loss/Waste')
    ], string='Quality Grade')

    harvest_date = fields.Date('Harvest Date')
    plot_id = fields.Many2one('farm.land', string='Origin Plot')

    @api.model
    def create(self, vals):
        """Override create to populate full traceability path"""
        record = super().create(vals)
        record._compute_full_traceability_path()
        return record

    def write(self, vals):
        """Override write to update full traceability path when parent changes"""
        result = super().write(vals)
        if 'parent_lot_id' in vals:
            self._compute_full_traceability_path()
        return result

    def _compute_full_traceability_path(self):
        """Compute and set the full traceability path for instant lookup"""
        for record in self:
            path_ids = []
            current = record
            # Traverse up the parent chain to build the path
            while current and current.parent_lot_id:
                path_ids.append(current.parent_lot_id.id)
                current = current.parent_lot_id
            # Store as comma-separated string for quick lookup
            record.full_traceability_path = ','.join(map(str, path_ids)) if path_ids else ''

    def get_full_traceability_chain(self):
        """Get the complete traceability chain (both upstream and downstream)"""
        upstream_chain = self._get_upstream_traceability()
        downstream_chain = self._get_downstream_traceability()
        return {
            'upstream': upstream_chain,
            'downstream': downstream_chain
        }

    def _get_upstream_traceability(self):
        """Get all parent lots in the traceability chain"""
        chain = []
        current = self
        while current and current.parent_lot_id:
            chain.append(current.parent_lot_id)
            current = current.parent_lot_id
        return chain

    def _get_downstream_traceability(self):
        """Get all child lots in the traceability chain"""
        chain = []
        # Use a queue for BFS traversal
        lots_to_check = [self]
        checked_lots = set()

        while lots_to_check:
            current_lot = lots_to_check.pop(0)
            if current_lot.id not in checked_lots:
                checked_lots.add(current_lot.id)
                for child in current_lot.child_lot_ids:
                    if child.id not in checked_lots:
                        chain.append(child)
                        lots_to_check.append(child)

        return chain


class AgriProcessingLotTracking(models.Model):
    """
    Advanced Lot Tracking and Traceability - US-14-03
    """
    _name = 'agri.processing.lot.tracking'
    _description = 'Advanced Lot Tracking and Traceability'

    name = fields.Char('Traceability Record', required=True)
    source_lot_id = fields.Many2one('stock.lot', string='Source Lot', required=True)
    target_lot_id = fields.Many2one('stock.lot', string='Target Lot', required=True)

    # Traceability path information
    trace_direction = fields.Selection([
        ('upstream', 'Upstream (Source to Parent)'),
        ('downstream', 'Downstream (Source to Child)'),
    ], string='Trace Direction', required=True)

    # Process information
    production_id = fields.Many2one('farm.processing.production', string='Production Order')
    process_date = fields.Date('Process Date')

    # Quality and compliance
    transfer_quality_status = fields.Selection([
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('non_compliant', 'Non-Compliant'),
    ], string='Transfer Quality Status', default='pending')

    # Notes and audit trail
    trace_notes = fields.Text('Trace Notes')
    traced_by = fields.Many2one('res.users', string='Traced By', default=lambda self: self.env.user)
    trace_date = fields.Datetime('Trace Date', default=fields.Datetime.now)

    @api.model
    def create(self, vals):
        if 'name' not in vals or not vals['name']:
            vals['name'] = 'TRACE/' + fields.Date.to_string(fields.Date.today()) + '/' + str(self.id or 0)
        return super().create(vals)

    def action_verify_traceability(self):
        """Verify the traceability connection between lots"""
        for record in self:
            # Add verification logic here
            record.transfer_quality_status = 'verified'