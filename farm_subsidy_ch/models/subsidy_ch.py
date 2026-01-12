from odoo import models, fields, api, _

class FarmSubsidyApplication(models.Model):
    _inherit = 'farm.subsidy.application'

    # 中国耕地地力保护与种粮补贴 [US-05-04]
    crop_type_china = fields.Selection([
        ('early_rice', '早稻'),
        ('wheat', '小麦'),
        ('corn', '玉米'),
        ('soybean', '大豆'),
        ('other', '其他')
    ], string="Crop Type (China)")
    
    declared_area_mu = fields.Float("Declared Area (亩)", compute='_compute_declared_area_mu', store=True)

    @api.depends('land_parcel_ids.land_area')
    def _compute_declared_area_mu(self):
        # 假设 land_area 存储为平方米，1亩 = 666.67平方米
        sqm_per_mu = 666.67
        for app in self:
            total_sqm = sum(app.land_parcel_ids.mapped('land_area'))
            app.declared_area_mu = total_sqm / sqm_per_mu if sqm_per_mu else 0.0

    def action_generate_moara_report(self):
        """ 模拟生成农业农村部补贴申报表 [US-05-04] """
        self.ensure_one()
        _logger.info("Generating MOARA subsidy report for application %s", self.name)
        # 实际这里会调用 QWeb 报告或生成特定格式文件
        self.message_post(body=_("MOARA subsidy report generation simulated for application %s.") % self.name)
        return True
