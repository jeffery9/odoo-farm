from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import Home
import json


class TermMappingController(http.Controller):
    """术语映射控制器 - 处理前端术语替换"""

    @http.route('/api/term_mapping', type='json', auth='user', methods=['POST'])
    def get_term_mappings(self, **kwargs):
        """获取当前用户的术语映射"""
        term_mappings = request.env['term.mapping'].search([('is_active', '=', True)])
        return {
            'mappings': [{
                'source_term': mapping.source_term,
                'target_term': mapping.target_term,
                'language_code': mapping.language_code,
                'industry_context': mapping.industry_context
            } for mapping in term_mappings]
        }

    def apply_term_mapping_to_view_data(self, data):
        """将术语映射应用到视图数据"""
        if not isinstance(data, dict):
            return data

        term_mappings = request.env['term.mapping'].search([('is_active', '=', True)])
        if not term_mappings:
            return data

        # 递归处理字典中的所有字符串值
        def replace_terms_in_dict(obj):
            if isinstance(obj, str):
                for mapping in term_mappings:
                    obj = obj.replace(mapping.source_term, mapping.target_term)
            elif isinstance(obj, dict):
                for key, value in obj.items():
                    obj[key] = replace_terms_in_dict(value)
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    obj[i] = replace_terms_in_dict(item)
            return obj

        return replace_terms_in_dict(data)


class AgriculturalTermHome(Home):
    """扩展 Home 控制器以支持农业术语"""

    def _set_lang(self, lang_code):
        """扩展语言设置以应用术语映射"""
        result = super(AgriculturalTermHome, self)._set_lang(lang_code)
        # 在这里可以应用术语映射逻辑
        return result