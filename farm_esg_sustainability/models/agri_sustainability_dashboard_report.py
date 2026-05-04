from odoo import models, fields, api, _
import logging
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

_logger = logging.getLogger(__name__)


class AgriSustainabilityDashboard(models.Model):
    """
    可持续发展仪表板模型 - US-101-01: 三重目标指标统一管理
    与现有ESG仪表板功能集成
    """
    _name = 'agri.sustainability.dashboard'
    _description = 'Agricultural Sustainability Dashboard'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('仪表板名称', required=True, default='可持续发展综合仪表板')
    description = fields.Text('描述')
    period_type = fields.Selection([
        ('daily', '日'),
        ('weekly', '周'),
        ('monthly', '月'),
        ('quarterly', '季度'),
        ('yearly', '年')
    ], '统计周期', default='monthly', required=True)
    start_date = fields.Date('开始日期', required=True, default=fields.Date.today)
    end_date = fields.Date('结束日期', required=True, default=lambda self: fields.Date.today())

    # 三重底线指标
    economic_score = fields.Float('经济得分', compute='_compute_scores', store=True, precompute=True)
    environmental_score = fields.Float('环境得分', compute='_compute_scores', store=True, precompute=True)
    social_score = fields.Float('社会得分', compute='_compute_scores', store=True, precompute=True)
    overall_score = fields.Float('综合得分', compute='_compute_scores', store=True, precompute=True)

    # 关键指标
    total_circular_flows = fields.Integer('循环经济流程数', compute='_compute_kpis', store=True, precompute=True)
    total_circular_value = fields.Float('循环经济总价值', compute='_compute_kpis', store=True, precompute=True)
    waste_reduced = fields.Float('减少废料量', compute='_compute_kpis', store=True, precompute=True)
    resource_saved = fields.Float('节约资源量', compute='_compute_kpis', store=True, precompute=True)

    # 集成现有碳足迹数据
    total_carbon_footprint = fields.Float('总碳足迹', compute='_compute_kpis', store=True, precompute=True)

    # 趋势指标
    economic_trend = fields.Float('经济趋势%', compute='_compute_trends', store=True, precompute=True)
    environmental_trend = fields.Float('环境趋势%', compute='_compute_trends', store=True, precompute=True)
    social_trend = fields.Float('社会趋势%', compute='_compute_trends', store=True, precompute=True)

    # 状态
    is_active = fields.Boolean('启用', default=True)
    last_calculated = fields.Datetime('最后计算时间', readonly=True)

    @api.depends('start_date', 'end_date')
    def _compute_scores(self):
        """计算三重底线得分"""
        for dashboard in self:
            # 获取该期间内的指标数据
            economic_metrics = self.env['agri.sustainability.metric'].search([
                ('category', '=', 'economic'),
                ('is_active', '=', True)
            ])

            environmental_metrics = self.env['agri.sustainability.metric'].search([
                ('category', '=', 'environmental'),
                ('is_active', '=', True)
            ])

            social_metrics = self.env['agri.sustainability.metric'].search([
                ('category', '=', 'social'),
                ('is_active', '=', True)
            ])

            # 计算各维度得分 (简单的平均达成率)
            economic_score = sum(m.progress_rate for m in economic_metrics) / len(economic_metrics) if economic_metrics else 0
            environmental_score = sum(m.progress_rate for m in environmental_metrics) / len(environmental_metrics) if environmental_metrics else 0
            social_score = sum(m.progress_rate for m in social_metrics) / len(social_metrics) if social_metrics else 0

            dashboard.economic_score = economic_score
            dashboard.environmental_score = environmental_score
            dashboard.social_score = social_score
            dashboard.overall_score = (economic_score + environmental_score + social_score) / 3 if (economic_score + environmental_score + social_score) > 0 else 0

    @api.depends('start_date', 'end_date')
    def _compute_kpis(self):
        """计算关键指标"""
        for dashboard in self:
            # 统计循环经济流程
            circular_flows = self.env['agri.sustainability.circular.flow'].search([
                ('start_date', '>=', dashboard.start_date),
                ('end_date', '<=', dashboard.end_date),
                ('status', '=', 'completed')
            ])

            dashboard.total_circular_flows = len(circular_flows)
            dashboard.total_circular_value = sum(f.economic_value for f in circular_flows)

            # 这里可以添加废料减少和资源节约的计算逻辑
            dashboard.waste_reduced = sum(f.input_quantity for f in circular_flows if f.flow_type in ['waste_to_resource', 'recycling'])
            dashboard.resource_saved = sum(f.output_quantity for f in circular_flows if f.flow_type in ['waste_to_resource', 'recycling'])

            # 集成碳足迹数据
            carbon_calculations = self.env['agri.sustainability.carbon.footprint.calculation'].search([
                ('calculation_date', '>=', dashboard.start_date),
                ('calculation_date', '<=', dashboard.end_date)
            ])
            dashboard.total_carbon_footprint = sum(c.total_carbon_footprint for c in carbon_calculations)

    @api.depends('start_date', 'end_date')
    def _compute_trends(self):
        """计算趋势"""
        for dashboard in self:
            # 获取上一期间的数据用于比较
            period_delta = {
                'daily': relativedelta(days=1),
                'weekly': relativedelta(weeks=1),
                'monthly': relativedelta(months=1),
                'quarterly': relativedelta(months=3),
                'yearly': relativedelta(years=1)
            }[dashboard.period_type]

            prev_start = dashboard.start_date - period_delta
            prev_end = dashboard.end_date - period_delta

            # 计算之前的得分用于趋势分析
            prev_economic_score = self._calculate_period_score('economic', prev_start, prev_end)
            curr_economic_score = self._calculate_period_score('economic', dashboard.start_date, dashboard.end_date)

            prev_environmental_score = self._calculate_period_score('environmental', prev_start, prev_end)
            curr_environmental_score = self._calculate_period_score('environmental', dashboard.start_date, dashboard.end_date)

            prev_social_score = self._calculate_period_score('social', prev_start, prev_end)
            curr_social_score = self._calculate_period_score('social', dashboard.start_date, dashboard.end_date)

            # 计算趋势百分比
            dashboard.economic_trend = self._calculate_trend(prev_economic_score, curr_economic_score)
            dashboard.environmental_trend = self._calculate_trend(prev_environmental_score, curr_environmental_score)
            dashboard.social_trend = self._calculate_trend(prev_social_score, curr_social_score)

    def _calculate_period_score(self, category, start_date, end_date):
        """计算指定期间和类别的得分"""
        metrics = self.env['agri.sustainability.metric'].search([
            ('category', '=', category),
            ('is_active', '=', True)
        ])
        if not metrics:
            return 0.0

        # 简化的得分计算，实际应用中可能需要基于期间内的值
        return sum(m.progress_rate for m in metrics) / len(metrics)

    def _calculate_trend(self, previous, current):
        """计算趋势百分比"""
        if previous == 0:
            return 100.0 if current > 0 else 0.0
        return ((current - previous) / previous) * 100.0

    def action_calculate_dashboard(self):
        """手动重新计算仪表板数据"""
        for dashboard in self:
            # 触发存储字段的重新计算
            dashboard.invalidate_recordset()
            dashboard._compute_scores()
            dashboard._compute_kpis()
            dashboard._compute_trends()
            dashboard.last_calculated = fields.Datetime.now()

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('计算完成'),
                'message': _('可持续发展仪表板数据已重新计算'),
                'type': 'success'
            }
        }

    def action_view_economic_metrics(self):
        """查看经济指标"""
        return {
            'type': 'ir.actions.act_window',
            'name': _('经济指标'),
            'res_model': 'agri.sustainability.metric',
            'view_mode': 'tree,form',
            'domain': [('category', '=', 'economic')],
            'context': self.env.context
        }

    def action_view_environmental_metrics(self):
        """查看环境指标"""
        return {
            'type': 'ir.actions.act_window',
            'name': _('环境指标'),
            'res_model': 'agri.sustainability.metric',
            'view_mode': 'tree,form',
            'domain': [('category', '=', 'environmental')],
            'context': self.env.context
        }

    def action_view_social_metrics(self):
        """查看社会指标"""
        return {
            'type': 'ir.actions.act_window',
            'name': _('社会指标'),
            'res_model': 'agri.sustainability.metric',
            'view_mode': 'tree,form',
            'domain': [('category', '=', 'social')],
            'context': self.env.context
        }

    def action_view_circular_flows(self):
        """查看循环经济流程"""
        return {
            'type': 'ir.actions.act_window',
            'name': _('循环经济流程'),
            'res_model': 'agri.sustainability.circular.flow',
            'view_mode': 'tree,form',
            'domain': [('status', '=', 'completed')],
            'context': self.env.context
        }

    def action_view_carbon_footprints(self):
        """查看碳足迹数据"""
        return {
            'type': 'ir.actions.act_window',
            'name': _('碳足迹数据'),
            'res_model': 'agri.sustainability.carbon.footprint.calculation',
            'view_mode': 'tree,form',
            'context': self.env.context
        }


class AgriSustainabilityReport(models.Model):
    """
    可持续发展报告模型 - 用于生成定期报告
    集成现有ESG报告功能
    """
    _name = 'agri.sustainability.report'
    _description = 'Agricultural Sustainability Report'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'report_date desc'

    name = fields.Char('报告名称', required=True)
    report_date = fields.Date('报告日期', required=True, default=fields.Date.today)
    period_start = fields.Date('期间开始', required=True)
    period_end = fields.Date('期间结束', required=True)

    # 报告内容
    executive_summary = fields.Html('执行摘要')
    economic_analysis = fields.Html('经济分析')
    environmental_analysis = fields.Html('环境分析')
    social_analysis = fields.Html('社会分析')

    # 量化数据
    economic_score = fields.Float('经济得分')
    environmental_score = fields.Float('环境得分')
    social_score = fields.Float('社会得分')
    overall_score = fields.Float('综合得分')

    # 集成碳足迹数据
    total_carbon_footprint = fields.Float('总碳足迹')

    # 循环经济成果
    circular_flows_count = fields.Integer('循环经济流程数量')
    circular_value_created = fields.Float('循环经济创造价值')
    waste_diverted = fields.Float('分流废料量')
    resource_efficiency_improvement = fields.Float('资源效率改善%')

    # 状态管理
    state = fields.Selection([
        ('draft', '草稿'),
        ('confirmed', '已确认'),
        ('published', '已发布')
    ], '状态', default='draft')

    author_id = fields.Many2one('res.users', '编制人', default=lambda self: self.env.user)
    reviewer_id = fields.Many2one('res.users', '审核人')
    approved_by = fields.Many2one('res.users', '批准人')
    approval_date = fields.Datetime('批准日期')

    # 附录和附件
    report_attachment_ids = fields.Many2many('ir.attachment', string='相关附件')

    @api.model
    def create_report(self, period_start, period_end):
        """自动生成可持续发展报告"""
        # 计算各维度得分
        economic_metrics = self.env['agri.sustainability.metric'].search([('category', '=', 'economic'), ('is_active', '=', True)])
        environmental_metrics = self.env['agri.sustainability.metric'].search([('category', '=', 'environmental'), ('is_active', '=', True)])
        social_metrics = self.env['agri.sustainability.metric'].search([('category', '=', 'social'), ('is_active', '=', True)])

        economic_score = sum(m.progress_rate for m in economic_metrics) / len(economic_metrics) if economic_metrics else 0
        environmental_score = sum(m.progress_rate for m in environmental_metrics) / len(environmental_metrics) if environmental_metrics else 0
        social_score = sum(m.progress_rate for m in social_metrics) / len(social_metrics) if social_metrics else 0

        # 统计碳足迹数据
        carbon_calculations = self.env['agri.sustainability.carbon.footprint.calculation'].search([
            ('calculation_date', '>=', period_start),
            ('calculation_date', '<=', period_end)
        ])
        total_carbon_footprint = sum(c.total_carbon_footprint for c in carbon_calculations)

        # 统计循环经济数据
        circular_flows = self.env['agri.sustainability.circular.flow'].search([
            ('start_date', '>=', period_start),
            ('end_date', '<=', period_end),
            ('status', '=', 'completed')
        ])

        # 创建报告记录
        report = self.create({
            'name': f'可持续发展报告 {period_start.strftime("%Y-%m-%d")} 至 {period_end.strftime("%Y-%m-%d")}',
            'report_date': fields.Date.today(),
            'period_start': period_start,
            'period_end': period_end,
            'economic_score': economic_score,
            'environmental_score': environmental_score,
            'social_score': social_score,
            'overall_score': (economic_score + environmental_score + social_score) / 3,
            'total_carbon_footprint': total_carbon_footprint,
            'circular_flows_count': len(circular_flows),
            'circular_value_created': sum(f.economic_value for f in circular_flows),
            'waste_diverted': sum(f.input_quantity for f in circular_flows if f.flow_type in ['waste_to_resource', 'recycling']),
            'executive_summary': self._generate_executive_summary(economic_score, environmental_score, social_score, total_carbon_footprint),
            'economic_analysis': self._generate_economic_analysis(circular_flows),
            'environmental_analysis': self._generate_environmental_analysis(circular_flows, total_carbon_footprint),
            'social_analysis': self._generate_social_analysis()
        })

        return report

    def _generate_executive_summary(self, economic_score, environmental_score, social_score, total_carbon_footprint):
        """生成执行摘要"""
        return f"""
        <p>本报告期公司在可持续发展方面取得显著进展：</p>
        <ul>
            <li>经济维度得分: {economic_score:.2f}%</li>
            <li>环境维度得分: {environmental_score:.2f}%</li>
            <li>社会维度得分: {social_score:.2f}%</li>
            <li>综合得分为: {(economic_score + environmental_score + social_score) / 3:.2f}%</li>
            <li>总碳足迹为: {total_carbon_footprint:.2f} kg CO2e</li>
        </ul>
        <p>公司在循环经济方面表现突出，实现了资源的有效利用和价值创造。</p>
        """

    def _generate_economic_analysis(self, circular_flows):
        """生成经济分析"""
        total_value = sum(f.economic_value for f in circular_flows)
        return f"""
        <p>经济维度分析：</p>
        <ul>
            <li>完成循环经济流程 {len(circular_flows)} 项</li>
            <li>创造总经济价值: {total_value:,.2f} 元</li>
            <li>平均每个流程创造价值: {total_value/len(circular_flows) if circular_flows else 0:,.2f} 元</li>
        </ul>
        """

    def _generate_environmental_analysis(self, circular_flows, total_carbon_footprint):
        """生成环境分析"""
        waste_reduced = sum(f.input_quantity for f in circular_flows if f.flow_type in ['waste_to_resource', 'recycling'])
        return f"""
        <p>环境维度分析：</p>
        <ul>
            <li>通过循环经济减少废料 {waste_reduced:,.2f} 单位</li>
            <li>实现了 {len(circular_flows)} 个资源循环利用流程</li>
            <li>总碳足迹为: {total_carbon_footprint:.2f} kg CO2e</li>
            <li>减少了环境负荷，提高了资源利用效率</li>
        </ul>
        """

    def _generate_social_analysis(self):
        """生成社会分析"""
        return """
        <p>社会维度分析：</p>
        <ul>
            <li>通过可持续发展实践提升了企业社会形象</li>
            <li>为当地社区创造了就业和经济价值</li>
            <li>推动了行业的可持续发展示范作用</li>
        </ul>
        """

    def action_confirm(self):
        """确认报告"""
        self.write({
            'state': 'confirmed',
            'reviewer_id': self.env.user.id
        })

    def action_approve(self):
        """批准报告"""
        self.write({
            'state': 'published',
            'approved_by': self.env.user.id,
            'approval_date': fields.Datetime.now()
        })

    def action_print_report(self):
        """打印报告"""
        return self.env.ref('farm_sustainability.action_sustainability_report').report_action(self)