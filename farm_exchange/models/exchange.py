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
        """ 
        US-20-02: 执行标准化数据交换
        根据协议类型调用具体的 Parser
        """
        self.ensure_one()
        if self.exchange_type == 'export':
            if self.format_type == 'daplos':
                return self._export_daplos_xml()
            elif self.format_type == 'telepac':
                return self._export_telepac_csv()
        return True

    def _export_daplos_xml(self):
        """ 
        DAPLOS (ISO 11783-10) 导出：生成符合标准的农业作业 XML
        """
        import lxml.etree as ET
        root = ET.Element("ISO11783_TaskData")
        
        # 1. 节点：地块信息
        plots = self.env['stock.location'].search([('is_land_parcel', '=', True)])
        for p in plots:
            p_node = ET.SubElement(root, "PFD", C=p.name, D=str(getattr(p, 'land_area', 0)))
            if p.gps_lat:
                ET.SubElement(p_node, "GRD", LAT=str(p.gps_lat), LON=str(p.gps_lng))
        
        xml_content = ET.tostring(root, encoding='utf-8', xml_declaration=True, pretty_print=True)
        self.write({
            'data_file': base64.b64encode(xml_content),
            'file_name': f'task_data_{self.name}.xml',
            'state': 'done'
        })
        return True

    def _export_telepac_csv(self):
        """
        TELEPAC 导出：生成符合欧盟/国际合规标准的 CSV 台账
        """
        import io
        import csv
        output = io.StringIO()
        writer = csv.writer(output, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
        # 表头
        writer.writerow(['ParcelName', 'Area', 'CertLevel', 'LastInspection'])
        
        certs = self.env['stock.location'].search([('is_land_parcel', '=', True)])
        for c in certs:
            writer.writerow([
                c.name, 
                getattr(c, 'land_area', 0), 
                getattr(c, 'certification_level', 'none'),
                fields.Date.today()
            ])
            
        self.write({
            'data_file': base64.b64encode(output.getvalue().encode()),
            'file_name': f'telepac_report_{self.name}.csv',
            'state': 'done'
        })
        return True
