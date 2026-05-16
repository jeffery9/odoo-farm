from odoo import models, fields, api, _

class AgriCarbonLedger(models.Model):
    _inherit = 'agri.carbon.ledger'

    is_tokenized = fields.Boolean("Tokenized for Trading", default=False, readonly=True)

    def action_tokenize_offset(self):
        """
        [US-ESG-02] Tokenize negative emissions (carbon sinks) into tradable assets.
        """
        for ledger in self:
            if ledger.impact_type != 'sequestration' or ledger.co2e_amount <= 0:
                continue
                
            if ledger.is_tokenized:
                continue
                
            # Convert CO2e (kg) to Tons for trading
            tons_co2e = ledger.co2e_amount / 1000.0
            
            # Create the asset in the exchange module if available
            if 'farm.exchange.asset' in self.env:
                asset = self.env['farm.exchange.asset'].create({
                    'name': f"Carbon Offset: {ledger.name}",
                    'asset_type': 'carbon_credit',
                    'quantity': tons_co2e,
                    'origin_ledger_id': ledger.id,
                    'owner_id': self.env.company.partner_id.id,
                    # Base price assumption $50/ton
                    'unit_price': 50.0 
                })
                ledger.is_tokenized = True
                ledger.message_post(body=_("Tokenized %s tons of CO2e into tradable asset: %s") % (tons_co2e, asset.name))

class FarmExchangeAsset(models.Model):
    """
    Internal Asset Marketplace for cross-farm trading.
    """
    _name = 'farm.exchange.asset'
    _description = 'Internal Tradable Asset'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Asset Name", required=True)
    asset_type = fields.Selection([
        ('carbon_credit', 'Carbon Offset Credit'),
        ('water_right', 'Water Right'),
        ('quota', 'Production Quota')
    ], string="Asset Type", required=True)
    
    quantity = fields.Float("Available Quantity", required=True)
    unit_price = fields.Float("Unit Price ($)", required=True)
    
    origin_ledger_id = fields.Many2one('agri.carbon.ledger', string="Origin Carbon Ledger", readonly=True)
    owner_id = fields.Many2one('res.partner', string="Current Owner", required=True)
    
    state = fields.Selection([
        ('available', 'Listed / Available'),
        ('sold', 'Sold / Retired')
    ], default='available', tracking=True)

    def action_purchase(self, buyer_partner_id):
        """
        [US-ESG-03] Execute internal trade between entities.
        """
        self.ensure_one()
        if self.state != 'available':
            return False
            
        total_amount = self.quantity * self.unit_price
        
        # Attempt to create internal settlement if Multi-Farm is installed
        if 'internal.settlement' in self.env:
            settlement = self.env['internal.settlement'].create({
                'from_entity_id': buyer_partner_id.id,
                'to_entity_id': self.owner_id.id,
                'settlement_type': 'general',
                'amount': total_amount,
                'description': f"Purchase of {self.quantity} Carbon Credits: {self.name}"
            })
            settlement.action_confirm()
            self.message_post(body=_("Asset sold to %s. Settlement %s auto-generated.") % (buyer_partner_id.name, settlement.name))
        
        self.state = 'sold'
        self.owner_id = buyer_partner_id.id
        return True

