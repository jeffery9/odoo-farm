# -*- coding: utf-8 -*-
# [US-039-25] [LOSSLESS] [ISA-88] Advanced UI De-industrialization Engine
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from lxml import etree

class AgriViewMixin(models.AbstractModel):
    """
    高级去工业化拦截器：全维度视图重塑。
    支持：Label, Placeholder, Help-text, Title, Button String 的实时映射。
    """
    _inherit = 'agri.view.mixin'
    _description = 'Global UI De-industrialization Injector'

    @api.model
    def _get_view(self, view_id=None, view_type='form', **options):
        """ Odoo 17+ 核心拦截点：动态重构 XML 架构 """
        arch, view = super()._get_view(view_id=view_id, view_type=view_type, **options)
        
        # 1. 获取术语映射中枢
        TermMapping = self.env['term.mapping']
        industry = self.env.context.get('industry_context', 'general')
        
        # 2. 广度优先搜索并替换所有可见文本
        # 拦截 Label, String, Placeholder, Help, Title
        for node in arch.xpath("//*[@string] | //*[@placeholder] | //*[@help]"):
            for attr in ['string', 'placeholder', 'help']:
                if node.get(attr):
                    node.set(attr, TermMapping.apply_term_mapping_to_text(node.get(attr), industry_context=industry))
        
        # 3. 拦截容器级标题 (form, tree, list, kanban, search, graph, pivot)
        for node in arch.xpath("//form | //list | //tree | //kanban | //search | //graph | //pivot"):
            if node.get('string'):
                node.set('string', TermMapping.apply_term_mapping_to_text(node.get('string'), industry_context=industry))

        # 4. [Special Injection] 社区贡献预警条
        if view_type == 'form' and self._name in ['mrp.production', 'stock.lot', 'res.partner']:
            if 'agri.clearing.ledger' in self.env:
                try:
                    todo_count = self.env['agri.clearing.ledger'].sudo().search_count([('state', '=', 'draft')])
                    if todo_count > 0:
                        alert_div = etree.Element('div', {
                            'class': 'alert alert-info text-center',
                            'role': 'alert',
                            'style': 'margin-bottom: 8px; font-weight: bold; border-left: 5px solid #28a745;'
                        })
                        alert_div.text = _("🌱 %d Agricultural Contributions awaiting verification.") % todo_count
                        header = arch.xpath("//header")
                        if header: header[0].addprevious(alert_div)
                        else: arch.insert(0, alert_div)
                except:
                    pass

        return arch, view

    @api.model
    def fields_get(self, allfields=None, attributes=None):
        """ 拦截字段定义，实时替换 Selection 标签和字段 String """
        res = super(AgriViewMixin, self).fields_get(allfields=allfields, attributes=attributes)
        if self.env.context.get('skip_agri_mapping'):
            return res

        TermMapping = self.env['term.mapping']
        industry = self.env.context.get('industry_context', 'general')

        for field_name, field_def in res.items():
            # 1. 替换字段主标签
            if 'string' in field_def:
                field_def['string'] = TermMapping.apply_term_mapping_to_text(field_def['string'], industry_context=industry)
            
            # 2. 替换 Selection 选项标签
            if 'selection' in field_def and isinstance(field_def['selection'], list):
                new_selection = []
                for key, label in field_def['selection']:
                    new_selection.append((key, TermMapping.apply_term_mapping_to_text(label, industry_context=industry)))
                field_def['selection'] = new_selection

        return res

    @api.depends_context('industry_context', 'lang')
    def _compute_display_name(self):
        """ 拦截显示名称计算，实时替换工业术语 """
        super()._compute_display_name()
        if self.env.context.get('skip_agri_mapping'):
            return

        TermMapping = self.env['term.mapping']
        industry = self.env.context.get('industry_context', 'general')

        for rec in self:
            if rec.display_name:
                rec.display_name = TermMapping.apply_term_mapping_to_text(rec.display_name, industry_context=industry)

    def translate_exception(self, exception_msg):
        """ 将制造业底层错误翻译为农学语义 """
        mapping = {
            'manufacturing order': _('agricultural intervention'),
            'bill of materials': _('cultivation recipe'),
            'work order': _('field task'),
            'insufficient stock': _('insufficient input evidence'),
            'inventory': _('resource registry'),
        }
        translated_msg = exception_msg.lower()
        for industrial, agri in mapping.items():
            translated_msg = translated_msg.replace(industrial, agri)
        return translated_msg.capitalize()

    def handle_validation_error(self, e):
        """ 挂钩模型校验错误 """
        agri_msg = self.translate_exception(str(e))
        raise ValidationError(agri_msg)
