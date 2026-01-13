from odoo import models, fields, api
import urllib.parse

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # US-14-10: GB 7718 Compliance
    ingredient_list = fields.Text("Ingredients", translate=True)
    storage_condition = fields.Char("Storage Condition", default="Store in cool and dry place", translate=True)
    shelf_life_days = fields.Integer("Shelf Life (Days)")
    food_standard_code = fields.Char("Executive Standard Code", default="GB/T ...")
    production_license_no = fields.Char("Production License No (SC)")

class StockLot(models.Model):
    _inherit = 'stock.lot'

    # US-14-10: Specific to the batch
    producer_id = fields.Many2one('res.partner', string="Producer", default=lambda self: self.env.company.partner_id)
    net_content = fields.Char("Net Content", help="e.g. 500g, 1L")

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
