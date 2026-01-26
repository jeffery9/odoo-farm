from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class StockPicking(models.Model):
    """
    扩展 stock.picking 以支持垫资分发时更新信用余额 [US-48-04]
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