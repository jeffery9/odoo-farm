from odoo import models, fields, api

class FarmEquipmentLog(models.Model):
    _inherit = 'farm.equipment.log'

    carbon_ledger_id = fields.Many2one('agri.carbon.ledger', string="Linked Carbon Ledger")

    @api.model_create_multi
    def create(self, vals_list):
        logs = super().create(vals_list)
        for log in logs:
            if log.fuel_consumed > 0 and log.equipment_id.fuel_type:
                log._generate_carbon_ledger_entry()
        return logs

    def write(self, vals):
        res = super().write(vals)
        if 'fuel_consumed' in vals:
            for log in self:
                if log.carbon_ledger_id:
                    # Recompute if updated
                    log._update_carbon_ledger_entry()
                elif log.fuel_consumed > 0:
                    log._generate_carbon_ledger_entry()
        return res

    def _generate_carbon_ledger_entry(self):
        """
        [US-ESG-01] Scope 1 Carbon Tracking
        Convert fuel consumption into carbon footprint.
        """
        self.ensure_one()
        # Find the carbon factor for this fuel type.
        # Assuming product name maps to fuel type or we find by category 'energy'
        # For a robust system, the equipment's fuel type should map to a product.template or factor directly.
        # Let's search for a factor that mentions 'diesel' if fuel type is diesel.
        
        fuel_keyword = self.equipment_id.fuel_type.capitalize() if self.equipment_id.fuel_type else 'Diesel'
        
        factor = self.env['agri.carbon.factor'].search([
            ('category', '=', 'energy'),
            '|', ('name', 'ilike', fuel_keyword), ('product_id.name', 'ilike', fuel_keyword)
        ], limit=1)

        if not factor:
            # Silent fail for the demo if no factor is configured
            return

        co2e = self.fuel_consumed * factor.emission_factor

        ledger = self.env['agri.carbon.ledger'].create({
            'name': f"Fuel Emission: {self.equipment_id.name}",
            'date': self.date,
            'scope': 'scope1', # Direct emission from owned asset
            'impact_type': 'emission',
            'co2e_amount': co2e,
            'source_factor_id': factor.id,
            'origin': f'Equipment Log: {self.id}',
        })
        
        self.carbon_ledger_id = ledger.id

    def _update_carbon_ledger_entry(self):
        self.ensure_one()
        if self.carbon_ledger_id and self.carbon_ledger_id.source_factor_id:
            new_co2e = self.fuel_consumed * self.carbon_ledger_id.source_factor_id.emission_factor
            self.carbon_ledger_id.write({'co2e_amount': new_co2e})

