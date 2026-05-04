from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.tools import drop_view_if_exists
import logging

_logger = logging.getLogger(__name__)


class AgriSustainabilityCircularFlow(models.Model):
    """
    循环经济流模型 - US-101-03: 循环经济价值评估体系, US-100-04: 残次品循环利用市场
    与现有碳足迹计算模型互补，专注资源循环利用价值评估
    """
    _name = 'agri.sustainability.circular.flow'
    _description = 'Agricultural Circular Flow'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char('流程名称', required=True, copy=False)
    code = fields.Char('流程代码', required=True, copy=False)
    flow_type = fields.Selection([
        ('waste_to_resource', '废料转资源'),
        ('byproduct_to_sale', '副产品转销售'),
        ('recycling', '回收利用'),
        ('energy_recovery', '能量回收'),
        ('composting', '堆肥利用'),
        ('biogas_production', '生物气生产')
    ], '流程类型', required=True, default='waste_to_resource')
    description = fields.Text('流程描述')

    # 输入输出产品
    input_product_id = fields.Many2one('product.product', '输入产品/原料', required=True)
    output_product_id = fields.Many2one('product.product', '输出产品/资源', required=True)
    input_quantity = fields.Float('输入数量', required=True)
    output_quantity = fields.Float('输出数量', required=True)

    # 时间范围
    start_date = fields.Date('开始日期')
    end_date = fields.Date('结束日期')
    duration_days = fields.Integer('持续天数', compute='_compute_duration', store=True)

    # 价值指标
    economic_value = fields.Float('经济价值', compute='_compute_economic_value', store=True)
    environmental_impact = fields.Float('环境影响评分', compute='_compute_environmental_impact', store=True)
    social_impact = fields.Float('社会影响评分', compute='_compute_social_impact', store=True)

    # 成本效益
    processing_cost = fields.Float('加工成本')
    revenue = fields.Float('收入')
    net_benefit = fields.Float('净收益', compute='_compute_net_benefit', store=True)

    # 状态和管理
    status = fields.Selection([
        ('planned', '计划中'),
        ('active', '进行中'),
        ('completed', '已完成'),
        ('suspended', '暂停'),
        ('cancelled', '已取消')
    ], '状态', default='planned', required=True)

    responsible_person_id = fields.Many2one('res.users', '负责人')
    department_id = fields.Many2one('hr.department', '责任部门')

    # 业务关联
    related_production_id = fields.Many2one('mrp.production', '关联生产单')
    related_sale_order_id = fields.Many2one('sale.order', '关联销售订单')
    # 集成现有碳足迹计算

    # 关联到地理空间网络 (US-057-06)
    geospatial_network_id = fields.Many2one('agri.geospatial.circular.network', string='关联地理空间网络')

    # 关联到区域治理 (US-057-07)
    regional_governance_id = fields.Many2one('agri.regional.circular.governance', string='关联区域治理')

    # 关联到农场参与 (US-057-07)
    farm_participation_id = fields.Many2one('agri.farm.circular.participation', string='关联农场参与')

    # 记录信息
    created_by = fields.Many2one('res.users', '创建人', default=lambda self: self.env.user)
    create_date = fields.Datetime('创建日期', readonly=True)
    write_date = fields.Datetime('最后修改', readonly=True)

    @api.depends('start_date', 'end_date')
    def _compute_duration(self):
        """计算持续天数"""
        from datetime import date
        for flow in self:
            if flow.start_date and flow.end_date:
                duration = (flow.end_date - flow.start_date).days
                flow.duration_days = max(0, duration)  # 确保不为负数
            else:
                flow.duration_days = 0

    @api.depends('processing_cost', 'revenue')
    def _compute_net_benefit(self):
        """计算净收益"""
        for flow in self:
            flow.net_benefit = flow.revenue - flow.processing_cost

    @api.depends('output_quantity', 'output_product_id')
    def _compute_economic_value(self):
        """计算经济价值"""
        for flow in self:
            if flow.output_product_id and flow.output_quantity:
                # 使用产品的标准价格作为基础
                price = flow.output_product_id.standard_price or flow.output_product_id.lst_price
                flow.economic_value = flow.output_quantity * price
            else:
                flow.economic_value = 0.0

    @api.depends('related_production_id', 'input_product_id', 'input_quantity')
    def _compute_environmental_impact(self):
        """[US-101-03] Mass_Balance Recursive Value Flow Algorithm"""
        for flow in self:
            if flow.related_production_id:
                # Use Mass Balance Recursive Algorithm
                algo = self.env['agri.sustainability.algorithms']
                inputs = []
                for move in flow.related_production_id.move_raw_ids:
                    inputs.append({
                        'qty': move.product_uom_qty,
                        'env_score': move.product_id.environmental_impact or 50.0,
                        'soc_score': move.product_id.social_impact or 50.0,
                        'eco_score': move.product_id.economic_impact or 50.0,
                        'carbon': move.product_id.carbon_emission_factor or 0.0
                    })
                
                results = algo.calculate_recursive_mass_balance(inputs, flow.output_quantity)
                flow.environmental_impact = results.get('environmental_score', 50.0)
                flow.social_impact = results.get('social_score', 50.0)
                flow.economic_value = flow.output_quantity * (flow.output_product_id.standard_price or 1.0)
            else:
                # Fallback to simple multiplier logic
                base_score = 50.0
                type_multiplier = {'waste_to_resource': 1.2, 'biogas_production': 1.4}
                multiplier = type_multiplier.get(flow.flow_type, 1.0)
                flow.environmental_impact = min(100, base_score * multiplier)

    @api.depends('flow_type', 'output_quantity')
    def _compute_social_impact(self):
        """计算社会影响评分 (0-100)"""
        for flow in self:
            base_score = 30  # 基础分

            # 根据流程类型调整分数
            type_multiplier = {
                'waste_to_resource': 1.0,
                'byproduct_to_sale': 1.2,
                'recycling': 1.1,
                'composting': 0.9,
                'biogas_production': 1.3,
            }

            multiplier = type_multiplier.get(flow.flow_type, 1.0)

            flow.social_impact = min(100, base_score * multiplier)

    @api.constrains('input_quantity', 'output_quantity')
    def _check_positive_quantities(self):
        """检查数量为正数"""
        for flow in self:
            if flow.input_quantity <= 0:
                raise ValidationError(_('输入数量必须大于0'))
            if flow.output_quantity < 0:  # 输出数量可以为0（完全转化）
                raise ValidationError(_('输出数量不能为负数'))

    @api.constrains('start_date', 'end_date')
    def _check_date_range(self):
        """检查日期范围合理性"""
        for flow in self:
            if flow.start_date and flow.end_date and flow.start_date > flow.end_date:
                raise ValidationError(_('开始日期不能晚于结束日期'))

    def action_activate_flow(self):
        """激活流程"""
        for flow in self:
            if flow.status == 'planned':
                flow.status = 'active'

    def action_complete_flow(self):
        """完成流程"""
        for flow in self:
            if flow.status in ['planned', 'active']:
                flow.status = 'completed'

    def action_suspend_flow(self):
        """暂停流程"""
        for flow in self:
            if flow.status in ['planned', 'active']:
                flow.status = 'suspended'

    @api.model
    @api.model_create_multi
    def create(self, vals_list):
        """创建时设置默认值和业务逻辑"""
        for vals in vals_list:
            if "code" not in vals or not vals['code']:
                # Try the new sequence first, fall back to the old one for compatibility
                new_sequence = self.env['ir.sequence'].next_by_code('agri.sustainability.circular.flow')
                if new_sequence:
                    vals['code'] = new_sequence
                else:
                    vals['code'] = self.env['ir.sequence'].next_by_code('farm.sustainability.circular.flow') or '/'

        record = super().create(vals_list)

        # 如果有相关联的生产或销售订单，可在此处添加额外逻辑
        return record

    def name_get(self):
        """自定义显示名称"""
        result = []
        for record in self:
            name = f"[{record.code}] {record.name}"
            result.append((record.id, name))
        return result


class AgriSustainabilityCircularFlowAnalysis(models.Model):
    """
    循环经济流分析模型 - 用于生成分析报表
    """
    _name = 'agri.sustainability.circular.flow.analysis'
    _description = 'Agricultural Circular Flow Analysis'
    _auto = False  # 这是一个视图模型，不创建实际表

    flow_id = fields.Many2one('agri.sustainability.circular.flow', '循环经济流', readonly=True)
    flow_type = fields.Selection(related='flow_id.flow_type', string='流程类型', readonly=True)
    input_product_id = fields.Many2one(related='flow_id.input_product_id', string='输入产品', readonly=True)
    output_product_id = fields.Many2one(related='flow_id.output_product_id', string='输出产品', readonly=True)
    economic_value = fields.Float(related='flow_id.economic_value', string='经济价值', readonly=True)
    environmental_impact = fields.Float(related='flow_id.environmental_impact', string='环境影响', readonly=True)
    net_benefit = fields.Float(related='flow_id.net_benefit', string='净收益', readonly=True)
    status = fields.Selection(related='flow_id.status', string='状态', readonly=True)
    month = fields.Char('月份', readonly=True)
    year = fields.Char('年份', readonly=True)

    def init(self):
        """初始化视图"""
        drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW %s AS (
                SELECT
                    cf.id as id,
                    cf.id as flow_id,
                    cf.flow_type,
                    cf.input_product_id,
                    cf.output_product_id,
                    cf.economic_value,
                    cf.environmental_impact,
                    cf.net_benefit,
                    cf.status,
                    TO_CHAR(cf.create_date, 'YYYY-MM') as month,
                    TO_CHAR(cf.create_date, 'YYYY') as year
                FROM agri_sustainability_circular_flow cf
                WHERE cf.status = 'completed'
            )
        """ % self._table)