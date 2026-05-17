from odoo import models, fields, api, _

class DividendDistribution(models.Model):
    _inherit = 'dividend.distribution'

    def action_execute_payout(self):
        """
        [US-SCENARIO-23] Village Collective Dividend Distribution
        Automatically process the calculated dividend lines into Internal Settlements
        to execute the actual financial transfer to each household.
        """
        self.ensure_one()
        if self.state != 'calculated':
            return False
            
        settlements_created = 0
        for line in self.dividend_lines:
            if line.total_amount <= 0 or line.state == 'paid':
                continue
                
            # Create an Internal Settlement from Coop to Member
            settlement = self.env['internal.settlement'].create({
                'from_entity_id': self.cooperative_id.partner_id.id,
                'to_entity_id': line.member_id.partner_id.id,
                'settlement_type': 'general',
                'amount': line.total_amount,
                'description': f"Annual Dividend: {self.name}"
            })
            
            # Auto-confirm the settlement to generate the Accounts Payable/Receivable twin entries
            settlement.action_confirm()
            
            line.write({
                'state': 'paid',
                'paid_amount': line.total_amount,
                'paid_date': fields.Date.today()
            })
            settlements_created += 1
            
        self.state = 'distributed'
        self.message_post(body=_("Automated Payout Executed: Generated %s internal settlements and transferred funds to villagers.") % settlements_created)
        return True

