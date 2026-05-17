from odoo import models, fields, api, _

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    eco_points_awarded = fields.Integer("Eco-Points Awarded", readonly=True, copy=False)
    carbon_savings_co2e = fields.Float("Carbon Savings (kg CO2e)", readonly=True, copy=False)

    def action_confirm(self):
        res = super().action_confirm()
        for order in self:
            order._award_eco_points_for_ugly_produce()
        return res

    def _award_eco_points_for_ugly_produce(self):
        """
        [US-SCENARIO-46] Gamified Ugly Produce & Eco-Loyalty
        Award eco-points to consumers who buy sub-standard (ugly) produce,
        saving it from becoming food waste. Calculate carbon savings.
        """
        points = 0
        carbon_savings = 0.0
        
        # Determine if they bought an "Ugly Produce Blind Box"
        for line in self.order_line:
            # We assume a tag or a specific product type, let's use a keyword for the demo
            if 'ugly' in line.product_id.name.lower() or 'blind box' in line.product_id.name.lower():
                # 1 kg of saved food ~ 2.5 kg CO2e saved (preventing landfill methane)
                qty_saved = line.product_uom_qty
                carbon_savings += qty_saved * 2.5
                points += int(qty_saved * 10) # 10 points per kg

        if points > 0:
            self.eco_points_awarded = points
            self.carbon_savings_co2e = carbon_savings
            
            # Award points via loyalty system
            program = self.env['loyalty.program'].search([('program_type', '=', 'loyalty')], limit=1)
            if not program:
                program = self.env['loyalty.program'].create({
                    'name': 'Eco-Warrior Rewards',
                    'program_type': 'loyalty',
                    'applies_on': 'both',
                })
                
            card = self.env['loyalty.card'].search([
                ('partner_id', '=', self.partner_id.id),
                ('program_id', '=', program.id)
            ], limit=1)
            
            if not card:
                card = self.env['loyalty.card'].create({
                    'partner_id': self.partner_id.id,
                    'program_id': program.id,
                    'points': 0
                })
                
            card.points += points
            
            self.message_post(body=_("Eco-Loyalty: Awarded %s points to customer for saving %.2f kg of food. Calculated carbon offset: %.2f kg CO2e.") % (
                points, qty_saved, carbon_savings
            ))
            
            # Record carbon saving into ESG if available
            if 'agri.carbon.ledger' in self.env:
                # Find or create a generic factor for Food Waste Prevention
                factor = self.env['agri.carbon.factor'].search([('name', '=', 'Food Waste Prevention')], limit=1)
                if not factor:
                    factor = self.env['agri.carbon.factor'].create({
                        'name': 'Food Waste Prevention',
                        'category': 'other',
                        'emission_factor': -2.5, # Negative emission = sink
                        'uom_id': line.product_uom.id
                    })
                
                self.env['agri.carbon.ledger'].create({
                    'name': f"Consumer Action: {self.name}",
                    'scope': 'scope3',
                    'impact_type': 'sequestration',
                    'co2e_amount': carbon_savings,
                    'source_factor_id': factor.id,
                    'origin': self.name
                })
