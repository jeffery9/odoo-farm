from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import datetime


class ExportComplianceLog(models.Model):
    """
    出口合规检查日志 [US-17-06]
    """
    _name = 'export.compliance.log'
    _description = 'Export Compliance Check Log'
    _order = 'checked_on desc'

    order_id = fields.Many2one('sale.order', string='Sale Order', required=True)
    country_code = fields.Char('Country Code', required=True)
    violations = fields.Char('Violations', help='Compliance violations found')
    checked_on = fields.Datetime('Checked On', required=True, default=fields.Datetime.now)
    result = fields.Selection([
        ('passed', 'Passed'),
        ('failed', 'Failed')
    ], string='Result', required=True)
    notes = fields.Text('Notes', help='Additional notes about the compliance check')
    checked_by = fields.Many2one('res.users', string='Checked By', default=lambda self: self.env.user)


class ExportCertificate(models.Model):
    """
    出口合规证书 [US-17-06]
    """
    _name = 'export.certificate'
    _description = 'Export Compliance Certificate'
    _rec_name = 'certificate_number'

    order_id = fields.Many2one('sale.order', string='Sale Order', required=True)
    product_name = fields.Char('Product Name', required=True)
    destination_country = fields.Char('Destination Country', required=True)
    certificate_number = fields.Char('Certificate Number', required=True, copy=False)
    issue_date = fields.Date('Issue Date', required=True, default=fields.Date.today)
    valid_until = fields.Date('Valid Until', required=True)
    inspector = fields.Char('Inspector', required=True)
    compliance_details = fields.Text('Compliance Details', help='Detailed compliance information')
    is_active = fields.Boolean('Is Active', default=True)
    attachment = fields.Binary('Certificate Attachment', help='Certificate file')
    attachment_name = fields.Char('Attachment Name')
    
    @api.constrains('valid_until')
    def _check_valid_until(self):
        """检查有效期 [US-17-06]"""
        for cert in self:
            if cert.valid_until and cert.valid_until < cert.issue_date:
                raise ValidationError(_("Valid until date must be after issue date."))

    def action_generate_certificate_document(self):
        """生成证书文档 [US-17-06]"""
        for cert in self:
            # 这里应该实现证书文档的实际生成逻辑
            # 例如使用PDF生成库创建正式的证书文档
            document_content = self._create_certificate_document(cert)
            cert.attachment = document_content
            cert.attachment_name = f"certificate_{cert.certificate_number}.pdf"

    def _create_certificate_document(self, certificate):
        """创建证书文档内容 [US-17-06]"""
        # 创建证书文档的逻辑
        # 这里应该使用PDF库生成正式的证书文档
        import base64
        from datetime import datetime

        # 创建证书内容
        certificate_content = f"""EXPORT COMPLIANCE CERTIFICATE

Certificate Number: {certificate.certificate_number}
Issue Date: {certificate.issue_date}
Valid Until: {certificate.valid_until}

Product: {certificate.product_name}
Destination Country: {certificate.destination_country}
Inspector: {certificate.inspector}

Compliance Details:
{certificate.compliance_details}

Issued by: Farm Management System
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """.encode('utf-8')

        # 使用base64编码内容
        certificate_pdf_content = base64.b64encode(certificate_content)
        return certificate_pdf_content

    @api.model
    def check_certificate_validity(self, certificate_number):
        """检查证书有效性 [US-17-06]"""
        certificate = self.search([('certificate_number', '=', certificate_number)], limit=1)
        if certificate:
            # 检查是否激活
            if not certificate.is_active:
                return {'valid': False, 'message': 'Certificate has been deactivated', 'certificate': certificate.read()}

            # 检查是否过期
            if certificate.valid_until and certificate.valid_until < fields.Date.today():
                return {'valid': False, 'message': 'Certificate has expired', 'certificate': certificate.read()}

            # 检查是否在有效期内
            if certificate.issue_date and certificate.issue_date > fields.Date.today():
                return {'valid': False, 'message': 'Certificate is not yet valid', 'certificate': certificate.read()}

            # 返回有效证书信息
            return {
                'valid': True,
                'certificate': certificate.read(),
                'message': 'Certificate is valid',
                'issue_date': certificate.issue_date,
                'valid_until': certificate.valid_until,
                'product_name': certificate.product_name,
                'destination_country': certificate.destination_country
            }
        return {'valid': False, 'message': 'Certificate not found', 'certificate_number': certificate_number}


class ExportCountryStandard(models.Model):
    """
    扩展国家出口标准模型，添加更多功能 [US-17-06]
    """
    _inherit = 'export.country.standard'

    # 添加更多字段以支持批量导入和自定义规则
    import_date = fields.Datetime('Import Date', help='Date when this standard was imported')
    imported_by = fields.Many2one('res.users', string='Imported By', help='User who imported this standard')
    custom_rules = fields.Text('Custom Rules', help='Custom compliance rules for this country')
    last_updated = fields.Datetime('Last Updated', help='Last time this standard was updated')
    update_frequency = fields.Selection([
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('annually', 'Annually')
    ], string='Update Frequency', default='annually', help='How often this standard should be reviewed')
    contact_person = fields.Char('Contact Person', help='Contact person for this country\'s regulations')
    official_source = fields.Char('Official Source', help='Official source for this country\'s regulations')
    next_review_date = fields.Date('Next Review Date', help='When to next review this standard')

    @api.model
    def batch_import_standards(self, standards_data):
        """批量导入标准 [US-17-06]"""
        created_standards = []
        for standard_data in standards_data:
            standard = self.create({
                'name': standard_data.get('name'),
                'code': standard_data.get('code'),
                'prohibited_products': standard_data.get('prohibited_products', []),
                'compliance_requirements': standard_data.get('compliance_requirements'),
                'import_date': fields.Datetime.now(),
                'imported_by': self.env.user.id,
                'custom_rules': standard_data.get('custom_rules'),
                'official_source': standard_data.get('official_source'),
                'update_frequency': standard_data.get('update_frequency', 'annually'),
                'contact_person': standard_data.get('contact_person'),
                'next_review_date': standard_data.get('next_review_date')
            })
            created_standards.append(standard)
        return created_standards

    def update_standard(self):
        """更新标准 [US-17-06]"""
        for standard in self:
            standard.last_updated = fields.Datetime.now()
            # 这里可以添加实际的标准更新逻辑
            # 例如从官方源获取最新信息

    def schedule_next_review(self):
        """安排下次审查 [US-17-06]"""
        for standard in self:
            if standard.update_frequency == 'daily':
                next_review = fields.Date.add(fields.Date.today(), days=1)
            elif standard.update_frequency == 'weekly':
                next_review = fields.Date.add(fields.Date.today(), weeks=1)
            elif standard.update_frequency == 'monthly':
                next_review = fields.Date.add(fields.Date.today(), months=1)
            elif standard.update_frequency == 'quarterly':
                next_review = fields.Date.add(fields.Date.today(), months=3)
            else:  # annually
                next_review = fields.Date.add(fields.Date.today(), years=1)
            
            standard.next_review_date = next_review