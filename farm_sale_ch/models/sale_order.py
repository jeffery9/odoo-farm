from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ExportCountryStandard(models.Model):
    """
    国家出口标准 [US-17-06]
    维护各国禁用农药清单和其他出口准入标准
    """
    _name = 'export.country.standard'
    _description = 'Export Country Standard'
    
    name = fields.Char('Country Name', required=True)
    code = fields.Char('Country Code', required=True, help='ISO国家代码')
    prohibited_products = fields.Many2many(
        'product.template', 
        string='Prohibited Products/Pesticides',
        help='该国家禁止使用的农药或其他产品清单'
    )
    compliance_requirements = fields.Text('Compliance Requirements', help='其他合规要求')
    active = fields.Boolean('Active', default=True)


class StockLot(models.Model):
    """
    扩展批次模型以支持出口合规验证 [US-17-06]
    """
    _inherit = 'stock.lot'

    # 与批次相关的投入品历史
    input_history_ids = fields.Many2many(
        'product.template',
        string='Input History',
        compute='_compute_input_history',
        help='该批次产品生产过程中使用的所有投入品'
    )

    def _compute_input_history(self):
        """计算批次的投入品历史"""
        for lot in self:
            # 这里需要根据实际的生产/农事记录来确定投入品历史
            # 简化实现：暂时设为空
            lot.input_history_ids = [(5, 0, 0)]  # 清空关联

    def check_export_compliance(self, country_code):
        """
        检查批次是否符合目标国家的出口标准 [US-17-06]

        :param country_code: 目标国家代码
        :return: (is_compliant, violations) 是否合规及违规详情
        """
        country_standard = self.env['export.country.standard'].search([
            ('code', '=', country_code.upper()),
            ('active', '=', True)
        ], limit=1)

        if not country_standard:
            return True, []

        # 获取该批次使用过的投入品
        violating_products = []
        if self.input_history_ids:
            prohibited_products = country_standard.prohibited_products
            violating_products = self.input_history_ids & prohibited_products

        is_compliant = len(violating_products) == 0
        violations = [product.name for product in violating_products]

        return is_compliant, violations


class SaleOrder(models.Model):
    """
    扩展销售订单以支持出口合规检查 [US-17-06]
    """
    _inherit = 'sale.order'

    export_country_code = fields.Char(
        'Export Country Code',
        help='如果此订单是出口订单，请输入目标国家代码'
    )
    export_compliance_status = fields.Selection([
        ('unknown', 'Unknown'),
        ('compliant', 'Compliant'),
        ('non_compliant', 'Non-Compliant')
    ], string='Export Compliance Status', default='unknown', readonly=True)

    def generate_compliance_report(self, country_code):
        """
        生成合规报告 [US-17-06]

        :param country_code: 目标国家代码
        :return: 合规报告内容
        """
        country_standard = self.env['export.country.standard'].search([
            ('code', '=', country_code.upper()),
            ('active', '=', True)
        ], limit=1)

        if not country_standard:
            return {
                'country': country_code,
                'status': 'No standard found',
                'details': 'No export standard found for this country.',
                'compliant': False,
                'violations': [],
                'recommendations': []
            }

        # 对于销售订单，我们需要检查关联的产品批次的合规性
        # 这里简化处理，假设订单中有一个产品
        product_lot = self.order_line[0].product_id if self.order_line else None
        if product_lot:
            is_compliant, violations = product_lot.check_export_compliance(country_code)
        else:
            is_compliant = True
            violations = []

        report = {
            'order_info': {
                'name': self.name,
                'product': self.order_line[0].product_id.name if self.order_line else 'N/A',
                'order_date': self.date_order,
            },
            'country': country_code,
            'standard': country_standard.name,
            'status': 'Compliant' if is_compliant else 'Non-compliant',
            'details': country_standard.compliance_requirements,
            'compliant': is_compliant,
            'violations': violations,
            'recommendations': self._get_compliance_recommendations(country_standard, violations) if not is_compliant else []
        }

        return report

    def _get_compliance_recommendations(self, standard, violations):
        """
        获取合规建议 [US-17-06]

        :param standard: 国家标准记录
        :param violations: 违规列表
        :return: 合规建议列表
        """
        recommendations = []

        if violations:
            recommendations.append(f"Remove the following prohibited products: {', '.join(violations)}")

        if standard.compliance_requirements:
            recommendations.append(f"Follow these requirements: {standard.compliance_requirements}")

        recommendations.append("Consider using alternative inputs that comply with the destination country's regulations.")

        return recommendations

    def auto_check_compliance_before_sale(self):
        """
        销售前自动检查合规性 [US-17-06]
        """
        for order in self:
            if order.export_country_code:
                is_compliant, violations = order.check_export_compliance(order.export_country_code)

                if not is_compliant:
                    order.export_compliance_status = 'non_compliant'
                    # 记录合规检查失败的详细信息
                    compliance_log = self.env['export.compliance.log'].create({
                        'order_id': order.id,
                        'country_code': order.export_country_code,
                        'violations': ', '.join(violations),
                        'checked_on': fields.Datetime.now(),
                        'result': 'failed'
                    })
                else:
                    order.export_compliance_status = 'compliant'
                    # 记录合规检查成功的详细信息
                    compliance_log = self.env['export.compliance.log'].create({
                        'order_id': order.id,
                        'country_code': order.export_country_code,
                        'result': 'passed'
                    })

    def generate_certificate_of_compliance(self):
        """
        生成合规证书 [US-17-06]
        """
        for order in self:
            if order.export_compliance_status == 'compliant':
                certificate_data = {
                    'order_id': order.id,
                    'product_name': order.order_line[0].product_id.name if order.order_line else '',
                    'destination_country': order.export_country_code,
                    'certificate_number': self._generate_certificate_number(),
                    'issue_date': fields.Date.today(),
                    'valid_until': fields.Date.add(fields.Date.today(), months=1),  # 有效期1个月
                    'inspector': self.env.user.name,
                    'compliance_details': order.generate_compliance_report(order.export_country_code)
                }

                certificate = self.env['export.certificate'].create(certificate_data)
                return certificate
        return None

    def _generate_certificate_number(self):
        """
        生成证书编号 [US-17-06]
        """
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        random_part = str(hash(timestamp))[-6:]  # 取哈希值的后6位作为随机部分
        return f"CERT-{timestamp}-{random_part}"

    def action_confirm(self):
        """在确认销售订单时检查出口合规性"""
        for order in self:
            if order.export_country_code:
                # 检查订单中所有产品的合规性
                non_compliant_lines = []
                
                for line in order.order_line:
                    if line.product_id.tracking != 'none':
                        # 如果产品需要批次追踪，则检查每个批次
                        for move in line.move_ids:
                            for lot in move.move_line_ids.lot_ids:
                                is_compliant, violations = lot.check_export_compliance(order.export_country_code)
                                if not is_compliant:
                                    non_compliant_lines.append({
                                        'product': line.product_id.display_name,
                                        'violations': violations
                                    })
                    else:
                        # 如果产品不需要批次追踪，检查产品本身的历史
                        # 这里需要更复杂的逻辑来确定产品的投入品历史
                        pass
                
                if non_compliant_lines:
                    violation_details = "\n".join([
                        f"- {item['product']}: {', '.join(item['violations'])}" 
                        for item in non_compliant_lines
                    ])
                    
                    raise ValidationError(_(
                        "Export compliance check failed for the following products:\n%s\n\n"
                        "Please review the prohibited substances for destination country: %s") % 
                        (violation_details, order.export_country_code))
                else:
                    order.export_compliance_status = 'compliant'
        
        return super().action_confirm()


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_id', 'order_id.export_country_code')
    def _onchange_product_export_compliance(self):
        """当选择产品或出口国家时，检查合规性"""
        if self.order_id.export_country_code and self.product_id:
            # 这里可以添加实时合规性检查的逻辑
            pass