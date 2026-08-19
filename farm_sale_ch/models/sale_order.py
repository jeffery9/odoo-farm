# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ExportCountryStandard(models.Model):
    """
    国家出口标准 [US-040-06]
    维护各国禁用农药清单和其他出口准入标准
    """
    _name = 'export.country.standard'
    _description = 'Export Country Standard'
    
    name = fields.Char('Country Name', required=True)
    code = fields.Char('Country Code', required=True, help='ISO国家代码')
    prohibited_products = fields.Many2many('product.template', 'export_country_standard_product_template_rel', 'standard_id', 'template_id',
        string='Prohibited Products/Pesticides',
        help='该国家禁止使用的农药或其他产品清单'
    )
    compliance_requirements = fields.Text('Compliance Requirements', help='其他合规要求')
    active = fields.Boolean('Active', default=True)


class StockLot(models.Model):
    """
    扩展批次模型以支持出口合规验证 [US-040-06]
    """
    _inherit = 'stock.lot'

    # 与批次相关的投入品历史
    input_history_ids = fields.Many2many('product.template', 'stock_lot_product_template_rel', 'lot_id', 'template_id',
        string='Input History',
        compute='_compute_input_history',
        help='该批次产品生产过程中使用的所有投入品'
    )

    def _compute_input_history(self):
        """计算批次的投入品历史"""
        for lot in self:
            lot.input_history_ids = [(6, 0, self._get_input_history().ids)]

    def check_export_compliance(self, country_code):
        """
        检查批次是否符合目标国家的出口标准 [US-040-06]
        """
        country_standard = self.env['export.country.standard'].search([
            ('code', '=', country_code.upper()),
            ('active', '=', True)
        ], limit=1)

        if not country_standard:
            return True, []

        violating_products = []
        input_history = self._get_input_history()

        if input_history:
            prohibited_products = country_standard.prohibited_products
            violating_products = input_history & prohibited_products

        is_compliant = len(violating_products) == 0
        violations = [product.name for product in violating_products]

        return is_compliant, violations

    def _get_input_history(self):
        """
        [SOLID Refactored] Get input history using the centralized Kinship Engine.
        Recursively traverses the lot ancestry to find all consumed agricultural inputs.
        """
        self.ensure_one()
        input_products = self.env['product.product']
        
        # 1. Gather all lots in this order
        target_lots = self.env['stock.lot']
        if self._name == 'sale.order':
            target_lots = self.order_line.mapped('lot_id')
        elif self._name == 'stock.lot':
            target_lots = self

        if not target_lots:
            return input_products

        # 2. Use Kinship Tree to find all ancestor lots
        def get_all_ancestors(lot):
            ancestors = self.env['stock.lot']
            for kinship in lot.parent_kinship_ids:
                parent = kinship.parent_lot_id
                ancestors |= parent
                ancestors |= get_all_ancestors(parent)
            return ancestors

        all_ancestor_lots = self.env['stock.lot']
        for lot in target_lots:
            all_ancestor_lots |= get_all_ancestors(lot)

        # 3. Identify lots that are "Agri Inputs"
        input_products = all_ancestor_lots.mapped('product_id').filtered(lambda p: p.is_agri_input)
        
        # 4. Also check direct material consumption in interventions
        visited_interventions = set()
        def get_intervention_inputs(lot):
            inputs = self.env['product.product']
            for kinship in lot.parent_kinship_ids:
                if kinship.intervention_id and kinship.intervention_id not in visited_interventions:
                    visited_interventions.add(kinship.intervention_id)
                    intervention = kinship.intervention_id
                    inputs |= intervention.move_raw_ids.mapped('product_id')
                inputs |= get_intervention_inputs(kinship.parent_lot_id)
            return inputs

        for lot in target_lots:
            input_products |= get_intervention_inputs(lot)

        return input_products

    def _get_related_inputs_for_product(self, product):
        """ [Deprecated] Use _get_input_history which leverages the Kinship Engine. """
        return self.env['product.product']


class SaleOrder(models.Model):
    """
    扩展销售订单以支持出口合规检查 [US-040-06]
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
        """生成合规报告 [US-040-06]"""
        country_standard = self.env['export.country.standard'].search([
            ('code', '=', country_code.upper()),
            ('active', '=', True)
        ], limit=1)

        if not country_standard:
            return {'country': country_code, 'status': 'No standard found', 'compliant': False}

        product_lot = self.order_line[0].lot_id if self.order_line else None
        if product_lot:
            is_compliant, violations = product_lot.check_export_compliance(country_code)
        else:
            is_compliant = True
            violations = []

        return {
            'order_info': {'name': self.name},
            'country': country_code,
            'status': 'Compliant' if is_compliant else 'Non-compliant',
            'compliant': is_compliant,
            'violations': violations,
        }

    def get_intervention_calendar_data(self):
        """
        [US-097-02] [SOLID Refactored]
        Uses Kinship Engine to find all interventions associated with the order's lots.
        """
        self.ensure_one()
        lots = self.order_line.mapped('lot_id')
        if not lots:
            lots = self.picking_ids.mapped('move_line_ids.lot_id')

        intervention_data = []
        visited_interventions = set()

        def collect_interventions(lot):
            for kinship in lot.parent_kinship_ids:
                if kinship.intervention_id and kinship.intervention_id not in visited_interventions:
                    inv = kinship.intervention_id
                    visited_interventions.add(inv)
                    progress_state = 'planned'
                    if inv.state == 'done': progress_state = 'completed'
                    elif inv.state in ['confirmed', 'progress', 'in_progress']: progress_state = 'in_progress'

                    intervention_data.append({
                        'id': inv.id,
                        'name': inv.name,
                        'intervention_type': getattr(inv, 'intervention_type', 'process'),
                        'state': inv.state,
                        'progress_state': progress_state,
                        'date_start': inv.date_start,
                        'date_finished': inv.date_finished,
                        'color': self._get_intervention_color(getattr(inv, 'intervention_type', 'process')),
                    })
                collect_interventions(kinship.parent_lot_id)

        for lot in lots:
            collect_interventions(lot)
        return intervention_data

    def _get_intervention_color(self, intervention_type):
        color_map = {
            'tillage': '#1f77b4', 'sowing': '#2ca02c', 'fertilizing': '#ff7f0e',
            'irrigation': '#17becf', 'protection': '#d62728', 'aerial_spraying': '#9467bd',
            'harvesting': '#8c564b', 'feeding': '#e377c2', 'medical': '#7f7f7f',
        }
        return color_map.get(intervention_type, '#000000')

    def action_confirm(self):
        """在确认销售订单时检查出口合规性及繁育代次硬拦截 [US-001-05]"""
        for order in self:
            for line in order.order_line:
                product = line.product_id
                if product.agri_generation in ['g0', 'g1', 'g2']:
                    raise ValidationError(_("Hard-block: Sales of non-commercial breeding generations prohibited."))
            
            if order.export_country_code:
                # Optimized check using kinship-based input history
                for line in order.order_line:
                    if line.lot_id:
                        is_compliant, violations = line.lot_id.check_export_compliance(order.export_country_code)
                        if not is_compliant:
                            raise ValidationError(_("Export Compliance Violation: Lot %s contains prohibited inputs for %s: %s") % 
                                                (line.lot_id.name, order.export_country_code, ', '.join(violations)))
        
        return super(SaleOrder, self).action_confirm()
