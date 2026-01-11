from odoo import models, fields, api, _

class FarmSoilAnalysis(models.Model):
    _name = 'farm.soil.analysis'
    _description = 'Soil Analysis Report'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'analysis_date desc'

    name = fields.Char("Report Reference", required=True, default=lambda self: _('New'))
    location_id = fields.Many2one('stock.location', string="Land Parcel", domain=[('is_land_parcel', '=', True)], required=True)
    analysis_date = fields.Date("Analysis Date", default=fields.Date.today, required=True)
    laboratory_id = fields.Many2one('res.partner', string="Laboratory", domain=[('is_company', '=', True)])
    
    # 养分指标
    ph_level = fields.Float("pH Level", digits=(10, 2))
    organic_matter = fields.Float("Organic Matter (%)")
    nitrogen_content = fields.Float("Nitrogen (mg/kg)")
    phosphorus_content = fields.Float("Phosphorus (mg/kg)")
    potassium_content = fields.Float("Potassium (mg/kg)")
    
    # 微量元素
    magnesium = fields.Float("Magnesium (mg/kg)")
    calcium = fields.Float("Calcium (mg/kg)")
    
    # 结论与建议
    recommendation = fields.Text("Fertilization Recommendations")
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Validated'),
        ('cancel', 'Cancelled')
    ], string="Status", default='draft', tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('farm.soil.analysis') or _('SOIL')
        return super().create(vals_list)

    def action_validate(self):
        self.write({'state': 'done'})
