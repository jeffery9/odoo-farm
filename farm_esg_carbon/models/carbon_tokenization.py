from odoo import models, fields, api, _

class AgriCarbonLedger(models.Model):
    _inherit = 'agri.carbon.ledger'

    is_tokenized = fields.Boolean("Tokenized for Trading", default=False, readonly=True)

    def action_tokenize_offset(self):
        """
        [US-ESG-02] Tokenize verified negative emissions into tradable assets.
        """
        for ledger in self:
            if ledger.impact_type != 'sequestration' or ledger.co2e_amount <= 0:
                continue
                
            # Only tokenize if verified via evidence audit (L2)
            if hasattr(ledger, 'audit_status') and ledger.audit_status != 'verified':
                from odoo.exceptions import UserError
                raise UserError(_("Ledger %s must be 'Verified' by physical evidence before tokenization.") % ledger.name)

            if ledger.is_tokenized:
                continue
                
            # Convert CO2e (kg) to Tons for trading (GS1 Standard Unit)
            tons_co2e = ledger.co2e_amount / 1000.0
            
            if 'farm.exchange.asset' in self.env:
                asset = self.env['farm.exchange.asset'].create({
                    'name': f"CERT-C-{fields.Date.today().year}-{ledger.id}",
                    'asset_type': 'carbon_credit',
                    'quantity': tons_co2e,
                    'origin_ledger_id': ledger.id,
                    'owner_id': self.env.company.partner_id.id,
                    'unit_price': 50.0 
                })
                ledger.is_tokenized = True
                ledger.message_post(body=_("Verified Tokenization: %s tons of CO2e converted to %s") % (tons_co2e, asset.name))

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
        [US-ESG-03] [SOLID Hardened] Execute internal trade between entities.
        Ensures atomic settlement and owner transfer.
        """
        self.ensure_one()
        if self.state != 'available':
            from odoo.exceptions import UserError
            raise UserError(_("Asset %s is no longer available for purchase.") % self.name)
            
        if buyer_partner_id == self.owner_id:
            from odoo.exceptions import UserError
            raise UserError(_("You cannot purchase your own carbon credits."))

        total_amount = self.quantity * self.unit_price
        
        # 1. Atomic Internal Settlement [Link to farm_multi_farm]
        if 'internal.settlement' in self.env:
            settlement = self.env['internal.settlement'].create({
                'from_entity_id': self.env['farm.entity'].search([('company_id.partner_id', '=', buyer_partner_id.id)], limit=1).id,
                'to_entity_id': self.env['farm.entity'].search([('company_id.partner_id', '=', self.owner_id.id)], limit=1).id,
                'settlement_type': 'general',
                'amount': total_amount,
                'description': f"Carbon Credit Trade: {self.name}",
                'res_model': self._name,
                'res_id': self.id
            })
            if hasattr(settlement, 'action_confirm'):
                settlement.action_confirm()
            
            # 2. Transfer Ownership & Retire
            self.write({
                'state': 'sold',
                'owner_id': buyer_partner_id.id,
            })
            
            self.message_post(body=_(
                "Transaction Complete: %s purchased by %s. "
                "Settlement %s confirmed."
            ) % (self.name, buyer_partner_id.name, settlement.name))
            
            return True
        return False

