from odoo import models, fields, api, _
from datetime import date

class FarmLocationCert(models.Model):
    _inherit = 'stock.location'

    certification_level = fields.Selection([
        ('conventional', 'Conventional (常规)'),
        ('organic_transition', 'Organic Transition (有机转换期)'),
        ('organic', 'Organic (有机)'),
        ('green', 'Green Food (绿色食品)'),
        ('gi', 'Geographical Indication (地理标志)')
    ], string="Certification Level", default='conventional', tracking=True)
    
    conversion_start_date = fields.Date("Conversion Start Date")
    conversion_target_days = fields.Integer("Target Conversion Days", default=1095) # 默认3年
    conversion_progress = fields.Float("Conversion Progress (%)", compute='_compute_conversion_progress')
    
    certificate_number = fields.Char("Certificate No.")
    certificate_expiry = fields.Date("Certificate Expiry")

    @api.depends('conversion_start_date', 'conversion_target_days')
    def _compute_conversion_progress(self):
        today = date.today()
        for loc in self:
            if loc.conversion_start_date and loc.conversion_target_days > 0:
                delta = (today - loc.conversion_start_date).days
                loc.conversion_progress = min(100.0, (delta / loc.conversion_target_days) * 100.0)
            else:
                loc.conversion_progress = 0.0

class FarmLotCert(models.Model):
    _inherit = 'stock.lot'

    certification_level = fields.Selection([
        ('conventional', 'Conventional (常规)'),
        ('organic_transition', 'Organic Transition (有机转换期)'),
        ('organic', 'Organic (有机)'),
        ('green', 'Green Food (绿色食品)'),
        ('gi', 'Geographical Indication (地理标志)')
    ], string="Certification Level", store=True)

    @api.onchange('location_id')
    def _onchange_location_id_certification(self):
        if self.location_id:
            self.certification_level = self.location_id.certification_level
