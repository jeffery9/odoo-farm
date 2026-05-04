from odoo import models, fields, api, _
from datetime import datetime, timedelta
import logging

_logger = logging.getLogger(__name__)


class MarketPrice(models.Model):
    """
    Market Price Integration - External commodity price feeds
    US-040-11: Biological Asset Fair Value Real-time Accounting
    """
    _name = 'farm.market.price'
    _description = 'Market Price Reference'
    _order = 'product_id, date desc'

    name = fields.Char("Price Reference", required=True, default=lambda self: _('New'))
    product_id = fields.Many2one('product.template', string="Commodity", required=True)
    date = fields.Date("Price Date", default=fields.Date.today, required=True)
    unit_price = fields.Float("Unit Price", digits=(12, 4), required=True, help="Price per unit of measure")
    unit_of_measure = fields.Many2one('uom.uom', string="Price UOM", help="Unit of measure for the price")
    source = fields.Char("Source", help="Source of the price data (e.g., Commodity Exchange, Futures)")

    # Futures-specific fields
    futures_contract = fields.Char("Futures Contract", help="Specific futures contract identifier (e.g., CBOT Corn Dec26)")
    futures_price = fields.Float("Futures Price", digits=(12, 4), help="Price from futures market if applicable")

    # Price volatility indicators
    price_volatility = fields.Float("Volatility Index", help="Price volatility indicator")
    confidence_level = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ], string="Data Confidence", default='high')

    @api.model
    def create(self, vals_list):
        if isinstance(vals_list, dict):
            vals_list = [vals_list]

        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                # Generate name as PRODUCT-YYYYMMDD
                product = self.env['product.template'].browse(vals.get('product_id', False))
                d = vals.get('date', fields.Date.today())
                if isinstance(d, str):
                    d = fields.Date.to_date(d)
                date_str = d.strftime('%Y%m%d')
                vals['name'] = f"{product.name or 'COMMODITY'}-{date_str}"

        return super().create(vals_list)

    @api.model
    def get_current_price(self, product_id, date=None):
        """
        Get current market price for a product on a specific date or today
        """
        if not date:
            date = fields.Date.today()

        price_record = self.search([
            ('product_id', '=', product_id),
            ('date', '<=', date)
        ], order='date desc', limit=1)

        return price_record.unit_price if price_record else 0.0

    def _cron_update_market_prices(self):
        """
        Scheduled job to update market prices from external sources
        """
        _logger.info("Starting market price update job")
        # In a real implementation, this would connect to commodity exchanges
        # or other pricing services to update prices automatically
        pass


class ProductTemplateMarketPrice(models.Model):
    """Extension to product template to include market price information"""
    _inherit = 'product.template'

    # Market price fields
    market_price = fields.Float("Market Price", digits=(12, 4), compute='_compute_market_price', store=True, precompute=True)
    market_price_date = fields.Date("Market Price Date", compute='_compute_market_price', store=True, precompute=True)
    market_price_uom = fields.Many2one('uom.uom', "Market Price UOM", help="Unit of measure for market price")

    # Expected yield for valuation calculation
    expected_yield_per_unit = fields.Float("Expected Yield per Unit", help="Expected yield per biological unit (e.g., per head, per plant)")

    @api.depends('market_price_date')
    def _compute_market_price(self):
        """Compute current market price based on latest market data"""
        for product in self:
            latest_price = self.env['farm.market.price'].search([
                ('product_id', '=', product.id)
            ], order='date desc', limit=1)

            if latest_price:
                product.market_price = latest_price.unit_price
                product.market_price_date = latest_price.date
            else:
                product.market_price = 0.0
                product.market_price_date = False