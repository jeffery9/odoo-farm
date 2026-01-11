from odoo import models, fields, api
import urllib.parse

class StockLot(models.Model):
    _inherit = 'stock.lot'

    def get_qr_quoted_traceability_url(self):
        self.ensure_one()
        if self.traceability_url:
            return urllib.parse.quote_plus(self.traceability_url)
        return ""

class StockLocation(models.Model):
    _inherit = 'stock.location'

    def get_qr_quoted_name(self):
        self.ensure_one()
        return urllib.parse.quote_plus(self.name)
