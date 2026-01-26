from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    """
    扩展 account.move 以支持在创建供应商账单时自动抵扣信用 [US-48-04]
    """
    _inherit = 'account.move'

    def action_post(self):
        """Override to handle credit deductions for vendor bills"""
        res = super().action_post()

        # Process only vendor bills
        for move in self:
            if move.move_type == 'in_invoice' and move.partner_id:
                # Calculate total bill amount
                total_amount = move.amount_total

                # Check if partner has sufficient internal credit balance
                partner = move.partner_id
                if partner.internal_credit_balance >= total_amount:
                    # Deduct the amount from internal credit balance
                    new_balance = partner.internal_credit_balance - total_amount
                    partner.internal_credit_balance = new_balance

                    # Add a message to the chatter
                    move.message_post(
                        body=f"已使用内部信用支付: -{total_amount}，剩余信用余额: {new_balance}"
                    )
                else:
                    # If insufficient credit, we might want to partially pay or raise an exception
                    # For now, we'll just log the situation
                    if partner.internal_credit_balance > 0:
                        remaining_amount = total_amount - partner.internal_credit_balance
                        move.message_post(
                            body=f"部分使用内部信用支付: -{partner.internal_credit_balance}，剩余待付: {remaining_amount}"
                        )
                        partner.internal_credit_balance = 0.0

        return res