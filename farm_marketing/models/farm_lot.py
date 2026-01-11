from odoo import models, fields, api

class FarmLotMarketing(models.Model):
    _inherit = 'stock.lot'

    traceability_url = fields.Char("Traceability URL", compute='_compute_traceability_url')

    def _compute_traceability_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        for lot in self:
            lot.traceability_url = f"{base_url}/farm/trace/{lot.name}"
