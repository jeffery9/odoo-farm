# -*- coding: utf-8 -*-
from odoo import models, fields, api

class FarmRecallWizard(models.TransientModel):
    """
    US-09-17: 农产品缺陷溯源与快速召回演练向导
    """
    _name = 'farm.recall.wizard'
    _description = 'Agricultural Product Recall Wizard'

    lot_id = fields.Many2one('stock.lot', string='Target Lot/Batch', required=True)
    recall_reason = fields.Selection([
        ('safety', 'Food Safety Issue (Pathogens/Contamination)'),
        ('quality', 'Quality Defect'),
        ('compliance', 'Regulatory Non-Compliance'),
        ('simulation', 'Mock Recall (Drill)')
    ], string='Recall Reason', required=True, default='simulation')
    
    action_plan = fields.Text('Action Plan')
    affected_picking_ids = fields.Many2many('stock.picking', 'farm_recall_wizard_stock_picking_rel', 'wizard_id', 'picking_id', string='Affected Deliveries', compute='_compute_affected_pickings')

    @api.depends('lot_id')
    def _compute_affected_pickings(self):
        for wiz in self:
            if wiz.lot_id:
                # Find pickings that moved this lot to customers
                moves = self.env['stock.move.line'].search([
                    ('lot_id', '=', wiz.lot_id.id),
                    ('state', '=', 'done'),
                    ('location_dest_id.usage', '=', 'customer')
                ])
                wiz.affected_picking_ids = moves.mapped('picking_id')
            else:
                wiz.affected_picking_ids = False

    def action_execute_recall(self):
        # Placeholder for executing recall logic (e.g., sending emails to customers)
        return {'type': 'ir.actions.act_window_close'}


class FarmTransformationWizard(models.TransientModel):
    """
    US-04-12: 次品降级与形态转化向导 (e.g., Grade B Apples -> Apple Jam)
    """
    _name = 'farm.transformation.wizard'
    _description = 'Agricultural Product Transformation Wizard'

    source_lot_id = fields.Many2one('stock.lot', string='Source Batch', required=True)
    source_qty = fields.Float('Quantity to Transform', required=True)
    
    target_product_id = fields.Many2one('product.product', string='Target Product', required=True)
    target_qty_expected = fields.Float('Expected Target Quantity', required=True)
    
    transformation_reason = fields.Char('Reason / Recipe')

    def action_confirm_transformation(self):
        # This would typically create a dismantling or specialized manufacturing order
        return {'type': 'ir.actions.act_window_close'}
