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
    last_prohibited_substance_date = fields.Date("Last Prohibited Substance Date", 
                                               help="Automatically updated when a non-organic input is used.")
    conversion_target_days = fields.Integer("Target Conversion Days", default=1095) # 默认3年
    conversion_progress = fields.Float("Conversion Progress (%)", compute='_compute_conversion_progress', store=True)
    
    @api.depends('conversion_start_date', 'last_prohibited_substance_date', 'conversion_target_days')
    def _compute_conversion_progress(self):
        today = date.today()
        for loc in self:
            # 转换起始点取“申报开始日期”和“最后一次违规施用日期”中的较晚者
            start_point = loc.conversion_start_date
            if loc.last_prohibited_substance_date:
                if not start_point or loc.last_prohibited_substance_date > start_point:
                    start_point = loc.last_prohibited_substance_date
            
            if start_point and loc.conversion_target_days > 0:
                delta = (today - start_point).days
                loc.conversion_progress = max(0.0, min(100.0, (delta / loc.conversion_target_days) * 100.0))
                
                # 如果进度达到100%，自动升级状态
                if loc.conversion_progress == 100.0 and loc.certification_level == 'organic_transition':
                    loc.certification_level = 'organic'
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
