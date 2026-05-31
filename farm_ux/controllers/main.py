from odoo import http
from odoo.http import request
try:
    from odoo.addons.web.controllers.home import Home
except ImportError:
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


class TraceabilityController(http.Controller):
    """
    [US-TECH-DNA-06] Holographic Traceability Controller.
    Fetches recursive kinship data and accumulated DNA for visualization.
    """

    @http.route('/agri/traceability/lot/<int:lot_id>/graph', type='json', auth='user')
    def get_lot_traceability_graph(self, lot_id):
        """
        Recursively fetches parent lots and their metadata to build a pedigree graph.
        """
        Lot = request.env['stock.lot']
        target_lot = Lot.browse(lot_id)
        if not target_lot.exists():
            return {'error': 'Lot not found'}

        # Graph structure: { nodes: [], edges: [] }
        graph = {
            'nodes': [],
            'edges': [],
            'root_id': lot_id
        }
        
        visited_ids = set()

        def build_recursive_graph(current_lot, depth=0):
            if current_lot.id in visited_ids or depth > 5: # Limit depth to 5
                return
            visited_ids.add(current_lot.id)

            # Node data (The "Holographic" metadata)
            node_data = {
                'id': current_lot.id,
                'name': current_lot.name,
                'product': current_lot.product_id.name,
                'certification': getattr(current_lot, 'certification_type', 'commodity'),
                'dna': {
                    'nitrogen': getattr(current_lot, 'nitrogen_qty', 0),
                    'phosphorus': getattr(current_lot, 'phosphorus_qty', 0),
                    'potassium': getattr(current_lot, 'potassium_qty', 0),
                    'carbon': getattr(current_lot, 'carbon_intensity', 0),
                    'water': getattr(current_lot, 'water_footprint', 0),
                },
                'depth': depth
            }
            graph['nodes'].append(node_data)

            # Recurse into parents
            for kinship in current_lot.parent_kinship_ids:
                parent = kinship.parent_lot_id
                graph['edges'].append({
                    'from': parent.id,
                    'to': current_lot.id,
                    'type': kinship.derivation_type,
                    'date': kinship.derivation_date.isoformat() if kinship.derivation_date else False
                })
                build_recursive_graph(parent, depth + 1)

        build_recursive_graph(target_lot)
        return graph


class AgriculturalTermHome(Home):
    """扩展 Home 控制器以支持农业术语"""

    def _set_lang(self, lang_code):
        """扩展语言设置以应用术语映射"""
        result = super(AgriculturalTermHome, self)._set_lang(lang_code)
        # 在这里可以应用术语映射逻辑
        return result