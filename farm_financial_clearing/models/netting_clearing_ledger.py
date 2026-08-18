# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class AgriClearingLedger(models.Model):
    _inherit = 'agri.clearing.ledger'

    amount_to_clear = fields.Float("Amount to Clear", required=True, default=0.0)

    def action_post_netting_clearing(self):
        self.ensure_one()
        partner = self.partner_id
        # Atomic balance check
        if partner.impact_credits < self.amount_to_clear:
            raise UserError(_("Credit verification failed: Transaction amount exceeds active cooperative credit balance!"))
        
        # Subtract balance atomically
        partner.write({'impact_credits': partner.impact_credits - self.amount_to_clear})
        self.write({'state': 'confirmed'})
        return True
