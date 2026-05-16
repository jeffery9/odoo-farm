from odoo import models, fields, api, _
import json

class StockLotPassport(models.Model):
    _inherit = 'stock.lot'

    traceability_passport_json = fields.Text("Traceability Passport Data", compute="_compute_passport_data")

    def _compute_passport_data(self):
        """
        [US-MKT-01] Generates a rich JSON payload for consumer-facing QR Codes.
        Aggregates data across the L0-L3 layers:
        - Interventions (farm_operation)
        - IoT Data (farm_iot)
        - Carbon Footprint (farm_esg)
        """
        for lot in self:
            passport = {
                "lot_number": lot.name,
                "product": lot.product_id.name,
                "harvest_date": False,
                "carbon_footprint_co2e": 0.0,
                "interventions_count": 0,
                "drone_flights": 0,
                "quality_grade": getattr(lot, 'quality_grade', 'Unrated'),
                "marketing_story": lot.product_id.description_sale or "Farm fresh product."
            }

            # 1. Trace Origins (Interventions)
            if 'mrp.production' in self.env:
                interventions = self.env['mrp.production'].search([('lot_producing_id', '=', lot.id)])
                passport["interventions_count"] = len(interventions)
                
                harvest = interventions.filtered(lambda i: i.intervention_type == 'harvesting')
                if harvest and harvest[0].date_finished:
                    passport["harvest_date"] = harvest[0].date_finished.strftime('%Y-%m-%d')
                    
                # Count drone flights (aerial spraying)
                drones = interventions.filtered(lambda i: i.intervention_type == 'aerial_spraying')
                passport["drone_flights"] = len(drones)

            # 2. Trace Carbon Footprint
            if 'agri.carbon.ledger' in self.env:
                # Find ledgers linked to this lot
                ledgers = self.env['agri.carbon.ledger'].search([('lot_id', '=', lot.id)])
                # Sum the carbon sinks (sequestration) minus emissions
                for ledger in ledgers:
                    if ledger.impact_type == 'sequestration':
                        passport["carbon_footprint_co2e"] -= ledger.co2e_amount
                    else:
                        passport["carbon_footprint_co2e"] += ledger.co2e_amount

            # 3. Compile JSON
            lot.traceability_passport_json = json.dumps(passport, indent=2)

