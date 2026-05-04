from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import logging

_logger = logging.getLogger(__name__)

class StockPicking(models.Model):
    """
    扩展 stock.picking 以支持垫资分发时更新信用余额 [US-078-04] 和 FEFO 验證 [US-009-20]
    """
    _inherit = 'stock.picking'

    def _action_done(self):
        """Override to update credit balance for advancing distributions"""
        res = super()._action_done()

        # Check if this is an advancing distribution
        for picking in self:
            if picking.picking_type_id.is_advancing_distribution:
                # For each move line, calculate the value and deduct from partner's credit balance
                total_value = 0.0
                for move in picking.move_ids_without_package:
                    # Calculate the value of the distributed items
                    unit_cost = move.product_id.standard_price
                    total_value += move.quantity_done * unit_cost

                # Deduct the total value from the partner's internal credit balance
                if picking.partner_id:
                    new_balance = picking.partner_id.internal_credit_balance - total_value
                    picking.partner_id.internal_credit_balance = new_balance

                    # Log the transaction
                    picking.message_post(
                        body=f"垫资分发扣款: -{total_value}，剩余信用余额: {new_balance}"
                    )

        return res

    def check_fefo_compliance_for_move_line(self, move_line):
        """
        US-009-20: Check if the selected lot in move_line is compliant with FEFO (First Expired First Out)
        If there's an earlier expiring lot available, raise a warning.
        """
        if not move_line.lot_id or move_line.product_id.tracking not in ['lot', 'serial']:
            return True  # No tracking, no FEFO check needed

        # Find all available quants for this product at this location
        quant_domain = [
            ('product_id', '=', move_line.product_id.id),
            ('quantity', '>', 0),
            ('location_id', 'child_of', move_line.location_id.id)
        ]

        quants = self.env['stock.quant'].search(quant_domain)

        # Filter out expired lots and get the one with earliest expiration date
        today = fields.Date.today()
        non_expired_quants = []
        for quant in quants:
            if quant.lot_id.expiration_date:
                if quant.lot_id.expiration_date >= today:
                    non_expired_quants.append(quant)
            else:
                non_expired_quants.append(quant)

        if not non_expired_quants:
            return True  # No available lots

        # Find the lot with the earliest expiration date
        earliest_expiring_quant = min(
            non_expired_quants,
            key=lambda q: q.lot_id.expiration_date or fields.Date.from_string('9999-12-31')
        )

        # Check if the selected lot is NOT the one that expires soonest
        if (earliest_expiring_quant.lot_id.id != move_line.lot_id.id and
            move_line.lot_id.expiration_date and
            earliest_expiring_quant.lot_id.expiration_date):
            # Check if the earliest expiring lot has an earlier expiration date
            if earliest_expiring_quant.lot_id.expiration_date < move_line.lot_id.expiration_date:
                raise UserError(_(
                    "FEFO WARNING: There is an earlier expiring lot available!\n"
                    "Selected lot: %(selected_lot)s (exp: %(selected_date)s)\n"
                    "Recommended lot: %(recommended_lot)s (exp: %(recommended_date)s)\n"
                    "Please use the earliest expiring lot first to minimize waste.",
                    selected_lot=move_line.lot_id.name,
                    selected_date=move_line.lot_id.expiration_date,
                    recommended_lot=earliest_expiring_quant.lot_id.name,
                    recommended_date=earliest_expiring_quant.lot_id.expiration_date
                ))

        return True