from odoo import models, fields, api, _
import json
import base64

class FarmDataExchanger(models.Model):
    _name = 'farm.data.exchanger'
    _description = 'Agricultural Data Exchanger'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Exchange Reference", required=True)
    format_type = fields.Selection([
        ('daplos', 'DAPLOS (Crop Data)'),
        ('telepac', 'TELEPAC (EU Compliance)'),
        ('edi', 'Agri-EDI (Generic)')
    ], string="Data Format", default='daplos', required=True)
    
    exchange_type = fields.Selection([
        ('export', 'Export (导出)'),
        ('import', 'Import (导入)')
    ], default='export', required=True)
    
    date = fields.Datetime("Exchange Date", default=fields.Datetime.now)
    
    # 数据文件
    data_file = fields.Binary("Data File")
    file_name = fields.Char("File Name")
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Completed'),
        ('error', 'Error')
    ], default='draft', tracking=True)

    def action_perform_exchange(self):
        """ 执行数据交换逻辑 [DAPLOS/TELEPAC] """
        self.ensure_one()
        if self.format_type == 'daplos':
            return self._perform_daplos_export()
        elif self.format_type == 'telepac':
            return self._perform_telepac_export()
        
    def _perform_daplos_export(self):
        """ 模拟 DAPLOS 导出逻辑 """
        # 获取最新的产季和地块数据
        plots = self.env['stock.location'].search([('is_land_parcel', '=', True)])
        data = {
            'header': {'protocol': 'DAPLOS', 'version': '1.0'},
            'plots': [{'id': p.id, 'name': p.name, 'area': getattr(p, 'land_area', 0)} for p in plots]
        }
        
        # 转为 JSON (实际 DAPLOS 可能是复杂的 XML)
        json_data = json.dumps(data, indent=4)
        self.write({
            'data_file': base64.b64encode(json_data.encode()),
            'file_name': 'export_daplos_%s.json' % self.id,
            'state': 'done'
        })
        return True

    def _perform_telepac_export(self):
        """ 模拟 TELEPAC 导出逻辑 """
        # 获取合规性数据（有机认证等）
        certs = self.env['stock.location'].search([('certification_level', '!=', 'conventional')])
        data = {
            'compliance': 'TELEPAC',
            'records': [{'plot': c.name, 'level': c.certification_level} for c in certs]
        }
        json_data = json.dumps(data, indent=4)
        self.write({
            'data_file': base64.b64encode(json_data.encode()),
            'file_name': 'export_telepac_%s.json' % self.id,
            'state': 'done'
        })
        return True
