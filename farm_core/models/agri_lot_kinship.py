# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class AgriLotKinship(models.Model):
    """
    [L1 DNA Foundation] Lot Kinship Record.
    Explicitly tracks the derivation of one lot from another.
    Essential for complex agricultural ancestry (Pedigree).
    """
    _name = 'agri.lot.kinship'
    _description = 'Lot Kinship / Ancestry'
    _order = 'derivation_date desc'

    parent_lot_id = fields.Many2one('stock.lot', string='Parent Lot', required=True, ondelete='cascade', index=True)
    child_lot_id = fields.Many2one('stock.lot', string='Child Lot', required=True, ondelete='cascade', index=True)
    
    intervention_id = fields.Reference(
        selection=[('mrp.production', 'Intervention'), ('project.task', 'Task')],
        string='Source Action'
    )
    
    derivation_type = fields.Selection([
        ('harvest', 'Harvesting (Plant/Animal -> Product)'),
        ('process', 'Processing (Raw -> Refined)'),
        ('split', 'Splitting (Batch -> Units)'),
        ('merge', 'Merging (Multiple -> Batch)'),
        ('breeding', 'Biological Breeding (Parent -> Offspring)'),
    ], string='Derivation Type', default='process')

    derivation_date = fields.Datetime('Derivation Date', default=fields.Datetime.now)
    
    share_percentage = fields.Float('Contribution Share (%)', default=100.0, help="Percentage of the parent lot's mass/volume that went into the child lot.")
    
    notes = fields.Text('Lineage Notes')

    _sql_constraints = [
        ('kinship_uniq', 'unique(parent_lot_id, child_lot_id, intervention_id)', 'This kinship link already exists!'),
    ]

    @api.model
    def create_kinship(self, parent_lot, child_lot, intervention=False, derivation_type='process'):
        """ Standardized way to link lots [US-038-02] """
        domain = [
            ('parent_lot_id', '=', parent_lot.id),
            ('child_lot_id', '=', child_lot.id),
        ]
        if intervention:
            ref_val = f"{intervention._name},{intervention.id}"
            domain.append(('intervention_id', '=', ref_val))
        else:
            domain.append(('intervention_id', '=', False))

        existing = self.search(domain)
        _logger.info("Kinship: Search domain %s, found %s existing", domain, len(existing))
        if not existing:
            vals = {
                'parent_lot_id': parent_lot.id,
                'child_lot_id': child_lot.id,
                'intervention_id': intervention,
                'derivation_type': derivation_type
            }
            _logger.info("Kinship: Creating new with vals %s", vals)
            existing = self.create(vals)
        return existing
