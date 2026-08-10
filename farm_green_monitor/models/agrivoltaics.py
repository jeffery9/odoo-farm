from odoo import models, fields, api, _

class FarmGreenMonitor(models.Model):
    _name = 'farm.green.monitor'
    _description = 'Green Monitoring Station'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Station Name", required=True)
    
    # [US-SCENARIO-36] Agrivoltaics / Solar Sharing
    crop_id = fields.Many2one('product.product', string="Under-Panel Crop")
    crop_revenue_est = fields.Float("Est. Crop Revenue ($)")
    solar_revenue_est = fields.Float("Est. Solar Revenue ($)")
    total_revenue_per_acre = fields.Float("Total Revenue / Acre", compute="_compute_total_rev")
    panel_tilt_angle = fields.Float("Panel Tilt Angle", default=30.0)
    
    @api.depends('crop_revenue_est', 'solar_revenue_est')
    def _compute_total_rev(self):
        for rec in self:
            rec.total_revenue_per_acre = rec.crop_revenue_est + rec.solar_revenue_est
            
    def action_ai_optimize_tilt(self):
        """ Optimizes tilt based on DLI needs of the shade crop vs peak pricing """
        for rec in self:
            # Mock AI logic: Tilt heavily to let sun hit crop if revenue is dropping
            old_tilt = rec.panel_tilt_angle
            rec.panel_tilt_angle = 45.0
            rec.message_post(body=_("AI Tilt Optimization: Adjusted from %s to %s to balance crop DLI and peak electricity.") % (old_tilt, rec.panel_tilt_angle))

