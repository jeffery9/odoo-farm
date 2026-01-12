from odoo import models, fields, api, _

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    data_storage_region = fields.Selection([
        ('china_mainland', 'China Mainland (中国大陆)'),
        ('overseas', 'Overseas (境外)')
    ], string="Data Storage Region", config_parameter='farm_data_security.data_storage_region')
    
    is_dengbao_level3_compliant = fields.Boolean("Dengbao Level 3 Compliant (等保三级)", config_parameter='farm_data_security.is_dengbao_level3_compliant')

    def action_check_data_localization(self):
        """ 模拟数据本地化检查 [US-74] """
        self.ensure_one()
        # 实际应检查 Odoo 实例的部署区域、数据库位置等
        if self.data_storage_region == 'china_mainland':
            message = _("Data localization check passed: Configured for China Mainland deployment.")
        else:
            message = _("WARNING: Data is configured for Overseas storage. May not meet China localization requirements.")
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Data Localization Check'),
                'message': message,
                'type': 'info',
            }
        }

class FarmLocation(models.Model):
    _inherit = 'stock.location'

    def unlink(self):
        """ 敏感操作审计：删除地块 [US-74] """
        for rec in self:
            _logger.info("Sensitive Operation Audit: User %s deleted Land Parcel %s (ID: %s)", 
                         self.env.user.name, rec.name, rec.id)
        return super().unlink()

class ResPartner(models.Model):
    _inherit = 'res.partner'

    def write(self, vals):
        """ 敏感操作审计：修改农户信息 [US-74] """
        if 'is_company' in vals and not vals['is_company']: # 如果是个人农户
            _logger.info("Sensitive Operation Audit: User %s modified Farmer/Partner %s (ID: %s) with changes: %s",
                         self.env.user.name, self.name, self.id, vals)
        return super().write(vals)

# 导入 logging
import logging
_logger = logging.getLogger(__name__)
