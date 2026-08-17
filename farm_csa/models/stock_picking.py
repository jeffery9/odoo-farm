# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        res = super(StockPicking, self).button_validate()
        
        # Hunt for active source CSA subscriptions
        for picking in self:
            if picking.origin and picking.state == 'done':
                sub = self.env['farm.csa.subscription'].search([
                    ('name', '=', picking.origin),
                    ('state', '=', 'active')
                ], limit=1)
                
                if sub:
                    # Determine delivered quantity across move lines
                    delivered_qty = sum(picking.move_ids.mapped('quantity')) or 1.0
                    
                    # 1. Guard check
                    if sub.yield_token_balance < delivered_qty:
                        raise ValidationError(_(
                            "CSA_TOKEN_EXHAUSTED: Pre-sale yield token balance is exhausted. "
                            "(提货代币已耗尽。)"
                        ))
                    
                    # 2. Debit tokens
                    sub.yield_token_balance -= delivered_qty
                    
                    # 3. Proportionate credit release
                    unit_price = sub.plan_id.price or 20.0
                    delivered_value = delivered_qty * unit_price
                    
                    if sub.use_coop_credit:
                        released_credit = min(sub.credit_held_amount, delivered_value)
                        sub.credit_held_amount -= released_credit
                        
                        # Set associated draft ledger line to confirmed
                        if sub.credit_ledger_line_id and sub.credit_ledger_line_id.state == 'draft':
                            sub.credit_ledger_line_id.action_confirm()
                            
                    sub.message_post(body=_("Delivery Picking %s validated. Debited %s tokens and released %s coop credits.") % (picking.name, delivered_qty, delivered_value))
                    
        return res
