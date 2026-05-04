from odoo import models, fields, api, _
from odoo.exceptions import UserError


class StockMoveLine(models.Model):
    _name = 'stock.move.line'
    _inherit = 'stock.move.line'

    def write(self, vals):
        """
        US-009-20: Check FEFO compliance when lot_id is changed on a stock move line.
        This catches cases where a user might manually change the selected lot
        to one that isn't the soonest to expire when an earlier expiring lot is available.
        """
        # If lot_id is being updated, check FEFO compliance
        if 'lot_id' in vals and vals['lot_id']:
            for line in self:
                if line.picking_id:
                    # Create a temporary line object with the new lot to test compliance
                    test_line_vals = line.copy_data({'lot_id': vals['lot_id']})[0]
                    test_line = line.env['stock.move.line'].new(test_line_vals)
                    line.picking_id.check_fefo_compliance_for_move_line(test_line)

        return super().write(vals)