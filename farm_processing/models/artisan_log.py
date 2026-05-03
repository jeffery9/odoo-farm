from odoo import models, fields, api, _

class FarmProcessingArtisanLog(models.Model):
    _name = 'farm.processing.artisan.log'
    _description = 'Artisan-Level Processing Precision Log'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    production_id = fields.Many2one('mrp.production', string="Production Batch", required=True)
    workorder_id = fields.Many2one('mrp.workorder', string="Work Step")
    
    # 匠心参数 [US-65-02]
    parameter_name = fields.Char("Artisan Parameter", required=True, 
                               help="e.g. Cutting Angle, Fermentation Temp Stability")
    target_value = fields.Float("Target Value (Precise)")
    actual_value = fields.Float("Actual Value")
    tolerance = fields.Float("Allowed Tolerance (+/-)", default=0.1)
    
    measured_by = fields.Many2one('res.users', string="Artisan/Master", default=lambda self: self.env.user)
    
    deviation = fields.Float("Deviation", compute='_compute_deviation', store=True)
    quality_grade = fields.Selection([
        ('perfect', 'Masterpiece (Perfect)'),
        ('standard', 'Standard'),
        ('subpar', 'Subpar')
    ], compute='_compute_quality_grade', store=True)

    @api.depends('target_value', 'actual_value', 'tolerance')
    def _compute_deviation(self):
        for rec in self:
            rec.deviation = abs(rec.actual_value - rec.target_value)

    @api.depends('deviation', 'tolerance')
    def _compute_quality_grade(self):
        for rec in self:
            if rec.deviation <= (rec.tolerance * 0.5):
                rec.quality_grade = 'perfect'
            elif rec.deviation <= rec.tolerance:
                rec.quality_grade = 'standard'
            else:
                rec.quality_grade = 'subpar'

class MrpProduction(models.Model):
    _name = 'mrp.production'
    _inherit = 'mrp.production'

    artisan_log_ids = fields.One2many('farm.processing.artisan.log', 'production_id', string="Artisan Precision Logs")
    is_artisan_batch = fields.Boolean("Artisan/Premium Batch", default=False)
