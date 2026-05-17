# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AgriLocation(models.Model):
    _inherit = 'agri.location'

    # Scenario 52: Land Banking and Pension
    is_idle_trust = fields.Boolean(string='Surrendered to Coop Land Bank', default=False, tracking=True)
    pension_beneficiary_id = fields.Many2one('res.partner', string='Pension Beneficiary (Retired Farmer)')
    pension_yield_share = fields.Float(string='Pension Share (%)', default=10.0)

    def action_surrender_to_land_bank(self):
        """Retiring farmer gives land to coop, retains pension rights."""
        for rec in self:
            rec.write({
                'is_idle_trust': True,
                'pension_beneficiary_id': rec.original_owner_id.id,
                'original_owner_id': False, # Coop takes over
            })
            rec.message_post(body="Land surrendered to Coop Land Bank. Pension rights secured.")
            
    def action_payout_land_pension(self, harvest_profit):
        """Triggered automatically during harvest settlement."""
        for rec in self.filtered('is_idle_trust'):
            pension_amount = harvest_profit * (rec.pension_yield_share / 100.0)
            if pension_amount > 0 and rec.pension_beneficiary_id:
                self.env['internal.settlement'].create({
                    'from_entity_id': self.env.company.partner_id.id,
                    'to_entity_id': rec.pension_beneficiary_id.id,
                    'amount': pension_amount,
                    'type': 'pension',
                    'state': 'done'
                })
                rec.message_post(body=f"Paid {pension_amount} as Land Pension to {rec.pension_beneficiary_id.name}.")
