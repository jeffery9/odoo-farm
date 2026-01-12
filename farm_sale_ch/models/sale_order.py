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