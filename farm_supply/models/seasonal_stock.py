from odoo import models, fields, api, _
from datetime import date

class FarmSeasonalStockRule(models.Model):
    """
    US-09-04: 农忙季节性安全库存计划
    """
    _name = 'farm.seasonal.stock.rule'
    _description = 'Seasonal Safety Stock Rule'

    product_id = fields.Many2one('product.product', string="Agricultural Input", 
                                domain=[('is_agri_input', '=', True)], required=True)
    location_id = fields.Many2one('stock.location', string="Storage Location", 
                                 domain=[('usage', '=', 'internal')], required=True)
    
    month = fields.Selection([
        ('1', 'January'), ('2', 'February'), ('3', 'March'), ('4', 'April'),
        ('5', 'May'), ('6', 'June'), ('7', 'July'), ('8', 'August'),
        ('9', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')
    ], string="Month", required=True)
    
    min_qty = fields.Float("Min Quantity (Safety Water)", required=True)
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('product_location_month_unique', 'unique(product_id, location_id, month)', 
         'A seasonal rule for this product, location and month already exists!')
    ]

    def _cron_check_seasonal_shortage(self):
        """ 定时任务：检查当前月份的安全库存水位 """
        current_month = str(date.today().month)
        rules = self.search([('month', '=', current_month), ('active', '=', True)])
        
        for rule in rules:
            # 获取当前库存
            quants = self.env['stock.quant'].search([
                ('product_id', '=', rule.product_id.id),
                ('location_id', '=', rule.location_id.id)
            ])
            available_qty = sum(quants.mapped('quantity'))
            
            if available_qty < rule.min_qty:
                # 触发采购预警
                self.env['mail.activity'].create({
                    'res_model_id': self.env.ref('product.model_product_product').id,
                    'res_id': rule.product_id.id,
                    'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                    'summary': _('SEASONAL SHORTAGE: %s is below safety level (%s < %s)') % (
                        rule.product_id.name, available_qty, rule.min_qty
                    ),
                    'note': _('Please prepare for the upcoming farming peak season.'),
                    'user_id': self.env.user.id,
                })
