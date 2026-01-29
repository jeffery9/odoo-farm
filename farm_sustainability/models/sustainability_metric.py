from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class SustainabilityMetric(models.Model):
    """
    可持续性指标模型 - US-101-01: 三重目标指标统一管理
    与现有ESG指标模型互补，提供更通用的可持续性指标管理
    """
    _name = 'farm.sustainability.metric'
    _description = 'Farm Sustainability Metric'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # 继承现有模块的通用特性
    _order = 'category, sequence'

    name = fields.Char('指标名称', required=True)
    code = fields.Char('指标代码', required=True, unique=True, copy=False)
    category = fields.Selection([
        ('economic', '经济'),
        ('environmental', '环境'),
        ('social', '社会'),
        ('governance', '治理'),  # 与现有ESG模型兼容
    ], '指标分类', required=True, default='economic')
    unit = fields.Char('计量单位', help='指标的计量单位，如: 吨, 万元, 百分比')
    description = fields.Text('指标描述')
    sequence = fields.Integer('排序', default=10)
    target_value = fields.Float('目标值')
    current_value = fields.Float('当前值', compute='_compute_current_value', store=True)
    progress_rate = fields.Float('达成率(%)', compute='_compute_progress_rate', store=True, digits=(6, 2))
    is_active = fields.Boolean('启用', default=True)
    calculation_method = fields.Selection([
        ('manual', '手动录入'),
        ('automatic', '自动计算'),
        ('formula', '公式计算')
    ], '计算方法', required=True, default='manual')
    formula = fields.Text('计算公式', help='当计算方法为公式计算时使用的公式')
    last_updated = fields.Datetime('最后更新时间', readonly=True)

    # 指标值历史记录 - 与现有ESG指标历史记录兼容
    value_history_ids = fields.One2many('farm.sustainability.metric.value', 'metric_id', '指标值历史')

    @api.depends('value_history_ids.value')
    def _compute_current_value(self):
        """计算当前指标值"""
        for metric in self:
            if metric.value_history_ids:
                # 获取最新的指标值记录
                latest_value = metric.value_history_ids.sorted('date', reverse=True)[:1]
                metric.current_value = latest_value.value if latest_value else 0.0
            else:
                metric.current_value = 0.0

    @api.depends('current_value', 'target_value')
    def _compute_progress_rate(self):
        """计算达成率"""
        for metric in self:
            if metric.target_value != 0:
                metric.progress_rate = (metric.current_value / metric.target_value) * 100
            else:
                metric.progress_rate = 0.0

    @api.constrains('code')
    def _check_code_unique(self):
        """检查代码唯一性"""
        for record in self:
            count = self.search_count([('code', '=', record.code)])
            if count > 1:
                raise ValidationError(_('指标代码必须唯一: %s') % record.code)

    def action_update_value(self):
        """更新指标值的向导操作"""
        return {
            'type': 'ir.actions.act_window',
            'name': _('更新指标值'),
            'res_model': 'farm.sustainability.metric.value.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_metric_id': self.id,
                'default_value': self.current_value
            }
        }

    @api.model
    def create(self, vals):
        """创建时自动添加初始值记录"""
        record = super().create(vals)
        # 可以为新指标自动创建初始值记录
        if 'current_value' in vals:
            self.env['farm.sustainability.metric.value'].create({
                'metric_id': record.id,
                'value': vals['current_value'],
                'date': fields.Datetime.now(),
                'note': '初始值设置'
            })
        return record


class SustainabilityMetricValue(models.Model):
    """
    可持续性指标值历史记录模型
    """
    _name = 'farm.sustainability.metric.value'
    _description = 'Farm Sustainability Metric Value'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc'

    metric_id = fields.Many2one('farm.sustainability.metric', '指标', required=True, ondelete='cascade')
    value = fields.Float('指标值', required=True)
    date = fields.Datetime('记录日期', required=True, default=fields.Datetime.now)
    note = fields.Text('备注')
    recorded_by = fields.Many2one('res.users', '记录人', default=lambda self: self.env.user)

    @api.model
    def create(self, vals):
        """创建时更新指标的最后更新时间"""
        record = super().create(vals)
        if record.metric_id:
            record.metric_id.last_updated = fields.Datetime.now()
        return record


class SustainabilityMetricValueWizard(models.TransientModel):
    """
    更新指标值的向导
    """
    _name = 'farm.sustainability.metric.value.wizard'
    _description = 'Farm Sustainability Metric Value Update Wizard'

    metric_id = fields.Many2one('farm.sustainability.metric', '指标', readonly=True)
    value = fields.Float('新值', required=True)
    date = fields.Datetime('日期', default=fields.Datetime.now, required=True)
    note = fields.Text('备注')

    def action_update_value(self):
        """执行更新操作"""
        if self.metric_id:
            # 创建新的指标值记录
            self.env['farm.sustainability.metric.value'].create({
                'metric_id': self.metric_id.id,
                'value': self.value,
                'date': self.date,
                'note': self.note,
                'recorded_by': self.env.user.id
            })

            # 返回到指标列表视图
            return {
                'type': 'ir.actions.act_window',
                'name': _('Sustainability Metrics'),
                'res_model': 'farm.sustainability.metric',
                'view_mode': 'tree,form',
                'target': 'current',
            }
        return {'type': 'ir.actions.act_window_close'}