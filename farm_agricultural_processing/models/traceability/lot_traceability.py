# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class StockLot(models.Model):
    _inherit = 'stock.lot'

    # [Refactored] Migrated to agri.lot.kinship for performance and consistency
    # Redundant parent_lot_id removed.
    
    def get_full_traceability_chain(self):
        """
        [SOLID Refactored] Use the centralized kinship model for deep traceability.
        """
        self.ensure_one()
        return {
            'upstream': self.parent_kinship_ids.mapped('parent_lot_id'),
            'downstream': self.child_kinship_ids.mapped('child_lot_id')
        }

    def _compute_full_traceability_path(self):
        """ [Deprecated] Logic migrated to agri.lot.kinship graph traversal """
        pass

class AgriProcessingLotTracking(models.Model):
    """
    Advanced Lot Tracking and Traceability - US-037-03
    Refactored to bridge with the Kinship Engine.
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

    # Process information (Using ISL naming)
    production_id = fields.Many2one('agri.isl.mrp.production', string='Intervention Order')
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
        
        record = super().create(vals)
        
        # [DNA Integration] Automatically sync with Kinship model
        self.env['agri.lot.kinship'].create_kinship(
            parent_lot=record.source_lot_id if record.trace_direction == 'downstream' else record.target_lot_id,
            child_lot=record.target_lot_id if record.trace_direction == 'downstream' else record.source_lot_id,
            derivation_type='process'
        )
        return record

    def action_verify_traceability(self):
        """Verify the traceability connection between lots"""
        for record in self:
            record.transfer_quality_status = 'verified'
