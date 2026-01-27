# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    data_storage_region = fields.Selection([
        ('china_mainland', 'China Mainland'),
        ('overseas', 'Overseas')
    ], string="Data Storage Region", config_parameter='farm_data_security.data_storage_region')
    
    is_dengbao_level3_compliant = fields.Boolean("Dengbao Level 3 Compliant", config_parameter='farm_data_security.is_dengbao_level3_compliant')

    def action_check_data_localization(self):
        """ 模拟数据本地化检查 [US-18-10] """
        self.ensure_one()
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

class FarmDataClassification(models.Model):
    """ [US-55-02] 农业数据隐私与合规保护 """
    _name = 'farm.data.classification'
    _description = 'Agricultural Data Classification'

    name = fields.Char("Classification Name", required=True)
    level = fields.Selection([
        ('public', 'Public'),
        ('internal', 'Internal'),
        ('sensitive', 'Sensitive (PII)'),
        ('critical', 'Critical (IP)')
    ], string="Sensitivity Level", required=True, default='internal')
    
    encryption_required = fields.Boolean("Encryption Required", default=False)
    retention_period_years = fields.Integer("Retention Period (Years)", default=5)
    description = fields.Text("Description")

class FarmIotDeviceRegistry(models.Model):
    """ [US-55-03] IoT 设备安全管理 """
    _name = 'farm.iot.device.registry'
    _description = 'IoT Device Security Registry'

    name = fields.Char("Device Name", required=True)
    device_uid = fields.Char("Physical UID / MAC", required=True)
    device_type = fields.Selection([
        ('sensor', 'Sensor'),
        ('actuator', 'Actuator'),
        ('controller', 'Gateway/Controller'),
        ('robot', 'Robotic Unit')
    ], string="Device Type", required=True)
    
    auth_status = fields.Selection([
        ('pending', 'Pending Authentication'),
        ('authorized', 'Authorized'),
        ('revoked', 'Revoked/Blocked')
    ], string="Authentication Status", default='pending')
    
    firmware_version = fields.Char("Firmware Version")
    last_security_audit = fields.Datetime("Last Security Audit")
    is_encrypted_comm = fields.Boolean("Encrypted Communication (TLS)", default=True)

    def action_authorize(self):
        self.ensure_one()
        self.write({
            'auth_status': 'authorized',
            'last_security_audit': fields.Datetime.now()
        })

class FarmLocation(models.Model):
    _inherit = 'stock.location'

    def unlink(self):
        """ 敏感操作审计：删除地块 [US-18-10] """
        for rec in self:
            _logger.info("Sensitive Operation Audit: User %s deleted Land Parcel %s (ID: %s)", 
                         self.env.user.name, rec.name, rec.id)
        return super().unlink()

class ResPartner(models.Model):
    _inherit = 'res.partner'

    def write(self, vals):
        """ 敏感操作审计：修改农户信息 [US-18-10] """
        if 'is_company' in vals and not vals['is_company']: # 如果是个人农户
            _logger.info("Sensitive Operation Audit: User %s modified Farmer/Partner %s (ID: %s) with changes: %s",
                         self.env.user.name, self.name, self.id, vals)
        return super().write(vals)
