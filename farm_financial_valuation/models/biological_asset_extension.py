from odoo import models, api

class BiologicalAssetValuation(models.Model):
    _inherit = 'agri.biological.asset'

    def trigger_financial_revaluation(self, reason="Biological Growth"):
        """
        [US-VALUATION-02] 
        Intercepts biological growth events and automatically generates a new
        financial valuation based on the current market price and new weight.
        """
        for asset in self:
            # Find the latest valuation to get the market price
            latest_val = self.env['farm.financial.asset.valuation'].search([
                ('asset_id', '=', asset.id),
                ('valuation_method', '=', 'market_price')
            ], order='valuation_date desc', limit=1)
            
            if not latest_val:
                continue
                
            current_price = latest_val.market_price
            new_valuation_amount = asset.base_weight_kg * current_price
            
            # Create new valuation record
            new_val = self.env['farm.financial.asset.valuation'].create({
                'asset_id': asset.id,
                'valuation_method': 'market_price',
                'market_price': current_price,
                'valuation_amount': new_valuation_amount,
                'asset_type': latest_val.asset_type,
                'previous_valuation_id': latest_val.id,
                'valuation_notes': reason
            })
            
            # Generate the accounting journal entry automatically
            new_val.action_create_accounting_entries()

