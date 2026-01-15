from odoo import fields, models, api, _
from odoo.exceptions import UserError

class FarmRecallWizard(models.TransientModel):
    _name = 'farm.recall.wizard'
    _description = 'Recall Simulation Wizard'

    product_id = fields.Many2one('product.product', string='Product', required=True)
    lot_id = fields.Many2one(
        'stock.lot', 
        string='Lot/Serial Number',
        domain="[('product_id', '=', product_id)]", 
        required=True
    )
    trace_direction = fields.Selection([
        ('backward', 'Backward Trace (To Raw Materials)'),
        ('forward', 'Forward Trace (To Customers)')
    ], string='Trace Direction', required=True, default='backward')

    recall_line_ids = fields.One2many('farm.recall.line', 'wizard_id', string='Trace Results', readonly=True)
    
    def action_simulate_recall(self):
        self.ensure_one()

        if not self.lot_id:
            raise UserError(_("Please select a Lot/Serial Number to simulate recall."))
        
        # Clear previous results
        self.recall_line_ids.unlink()

        # Create new results
        new_recall_lines = []
        if self.trace_direction == 'backward':
            self._create_recall_line(new_recall_lines, 0, self.lot_id.product_id, self.lot_id, move_type='output', reference="Start Lot")
            self._do_backward_trace(self.lot_id, new_recall_lines, level=1)
        elif self.trace_direction == 'forward':
            self._create_recall_line(new_recall_lines, 0, self.lot_id.product_id, self.lot_id, move_type='input', reference="Start Lot")
            self._do_forward_trace(self.lot_id, new_recall_lines, level=1)
        
        self.write({'recall_line_ids': [(0, 0, vals) for vals in new_recall_lines]})

        return {
            'name': _('Recall Simulation Results'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': self._name,
            'res_id': self.id,
            'target': 'new',
            'context': self.env.context,
            'flags': {'action_buttons': True}, # Ensure buttons are visible
        }

    def _create_recall_line(self, lines_list, level, product, lot, quantity=0.0, uom=False, move_type=False, reference=False, partner=False, date=False):
        vals = {
            'level': level,
            'product_id': product.id if product else False,
            'lot_id': lot.id if lot else False,
            'quantity': quantity,
            'uom_id': uom.id if uom else False,
            'move_type': move_type,
            'reference': reference,
            'partner_id': partner.id if partner else False,
            'date': date,
        }
        lines_list.append(vals)

    def _do_backward_trace(self, current_lot, lines_list, level):
        # Find upstream MOs where this lot was consumed
        consumed_moves = self.env['stock.move'].search([
            ('lot_ids', 'in', current_lot.id),
            ('production_id', '!=', False),
            ('state', '=', 'done'),
        ], order='date desc') # Trace recent movements first

        for move in consumed_moves:
            mo = move.production_id
            self._create_recall_line(lines_list, level, mo.product_id, mo.lot_producing_id, mo.product_qty, mo.product_uom_id, move_type='input', reference=mo.name, date=mo.date_finished)
            
            # Trace raw materials used in this MO
            for raw_move in mo.move_raw_ids:
                for raw_lot in raw_move.lot_ids:
                    # Avoid infinite loops for reprocessing scenarios by checking against current_lot's product
                    if raw_lot.id not in [line['lot_id'] for line in lines_list if line.get('lot_id')] or raw_lot.product_id != current_lot.product_id:
                        self._create_recall_line(lines_list, level + 1, raw_lot.product_id, raw_lot, raw_move.product_uom_qty, raw_move.product_uom, move_type='input', reference=raw_move.reference, partner=raw_move.picking_id.partner_id if raw_move.picking_id else False, date=raw_move.date)
                        self._do_backward_trace(raw_lot, lines_list, level + 2)
            
            # If the current lot was produced by this MO, then its parent lot is relevant
            if current_lot.id == mo.lot_producing_id.id and current_lot.parent_lot_id:
                self._create_recall_line(lines_list, level + 1, current_lot.parent_lot_id.product_id, current_lot.parent_lot_id, move_type='input', reference="Parent Lot", date=current_lot.create_date)
                self._do_backward_trace(current_lot.parent_lot_id, lines_list, level + 2)
        
        # Also check if the current lot itself is a raw material in another MO (less direct, but part of lineage)
        # This is already covered by the consumed_moves logic to some extent.
        # Check stock moves that brought this lot in (e.g., from vendor)
        incoming_moves = self.env['stock.move'].search([
            ('lot_ids', 'in', current_lot.id),
            ('location_dest_id', '=', current_lot.product_id.with_company(self.env.company).property_stock_production.id), # Moved to production input location
            ('picking_id.picking_type_id.code', '=', 'incoming'), # From vendor
            ('state', '=', 'done'),
        ], order='date desc')
        for move in incoming_moves:
            self._create_recall_line(lines_list, level + 1, current_lot.product_id, current_lot, move.product_uom_qty, move.product_uom, move_type='input', reference=move.reference, partner=move.picking_id.partner_id if move.picking_id else False, date=move.date)


    def _do_forward_trace(self, current_lot, lines_list, level):
        # Find where this lot was moved (e.g., delivered to customer, transferred to another location)
        outgoing_moves = self.env['stock.move'].search([
            ('lot_ids', 'in', current_lot.id),
            ('location_id', '=', current_lot.product_id.with_company(self.env.company).property_stock_finished.id), # Moved from finished goods
            ('state', '=', 'done'),
        ], order='date desc')

        for move in outgoing_moves:
            if move.picking_id and move.picking_id.partner_id:
                self._create_recall_line(lines_list, level, current_lot.product_id, current_lot, move.product_uom_qty, move.product_uom, move_type='output', reference=move.picking_id.name, partner=move.picking_id.partner_id, date=move.date)
            else: # Internal transfer or consumption in another MO
                self._create_recall_line(lines_list, level, current_lot.product_id, current_lot, move.product_uom_qty, move.product_uom, move_type='transfer', reference=move.name, date=move.date)
            
            # Recursively trace if the lot was part of a new production after this move
            # Check if this move is consumed in another MO
            if move.production_id: # This means current_lot was consumed in this MO
                mo = move.production_id
                self._create_recall_line(lines_list, level + 1, mo.product_id, mo.lot_producing_id, mo.product_qty, mo.product_uom_id, move_type='output', reference=mo.name, date=mo.date_finished)
                self._do_forward_trace(mo.lot_producing_id, lines_list, level + 2)
            else: # Follow the new location or new lot if transferred
                for new_lot in move.move_line_ids.mapped('lot_id'):
                    if new_lot.id != current_lot.id and new_lot.product_id == current_lot.product_id: # Avoid self-loop and ensure same product
                        self._do_forward_trace(new_lot, lines_list, level + 1)
