from odoo import models, fields, api, _

class FarmMarketConnector(models.Model):
    _name = 'farm.market.connector'
    _description = 'External Market Connector'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Connector Name", required=True) # e.g., Shopee, Walmart, Local Govt Portal
    connector_type = fields.Selection([
        ('ecommerce', 'E-commerce Platform'),
        ('retailer', 'Large Retailer'),
        ('government', 'Government G2B Portal'),
        ('custom', 'Custom API')
    ], string="Type", required=True)
    
    api_key = fields.Char("API Key / Token", groups="base.group_erp_manager")
    endpoint_url = fields.Char("Remote Endpoint")
    
    active = fields.Boolean(default=True)
    
    # Sync Logs
    last_sync_date = fields.Datetime("Last Synchronization")
    sync_status = fields.Selection([('ok', 'Healthy'), ('error', 'Error')], default='ok')

    def action_test_connection(self):
        """ Mock connection test to external market """
        self.ensure_one()
        self.sync_status = 'ok'
        self.last_sync_date = fields.Datetime.now()
        return True

class FarmMarketDemand(models.Model):
    _inherit = 'farm.market.demand'

    connector_id = fields.Many2one('farm.market.connector', string="Source Connector")
    external_id = fields.Char("External Reference ID")
    
    # Matching logic enhancement
    min_integrity_score = fields.Float("Min Integrity Score Required", default=80.0)
    requires_organic = fields.Boolean("Requires Organic Cert", default=False)

    def action_match_production(self):
        """
        Enhanced matching: filters lots by integrity score and certification.
        """
        for rec in self:
            domain = [
                ('product_id', '=', rec.product_id.id),
                ('state', 'not in', ['sold', 'scrap']),
                ('integrity_score', '>=', rec.min_integrity_score)
            ]
            if rec.requires_organic:
                # Assuming quality_status 'passed' implies basic compliance
                domain.append(('quality_status', '=', 'passed'))
            
            matching_lots = self.env['stock.lot'].search(domain)
            rec.matched_lot_ids = [(6, 0, matching_lots.ids)]
            if matching_lots:
                rec.state = 'matched'
            return True
