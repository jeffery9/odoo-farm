from odoo import http
from odoo.http import request
from datetime import datetime

class FarmTraceabilityController(http.Controller):

    @http.route('/farm/trace/<string:lot_name>', type='http', auth='public', website=True)
    def trace_product(self, lot_name, **kwargs):
        """ 公开溯源页面：展示产品生命周期、质检结果和农场故事 """
        lot = request.env['stock.lot'].sudo().search([('name', '=', lot_name)], limit=1)
        if not lot:
            return request.render('website.404')

        # 获取关联的生产任务
        production_task = request.env['project.task'].sudo().search([
            ('biological_lot_id', '=', lot.id)
        ], limit=1)

        # 获取质检通过记录
        qc_checks = lot.quality_check_ids.filtered(lambda c: c.quality_state == 'pass')

        # 获取直播流地址 [US-039-01]
        video_url = lot.location_id.camera_device_id.live_stream_url if lot.location_id.camera_device_id else False

        # 获取干预日历数据
        intervention_data = []
        if production_task:
            interventions = request.env['agri.intervention'].sudo().search([
                ('agri_task_id', '=', production_task.id)
            ])
            for intervention in interventions:
                intervention_data.append({
                    'id': intervention.id,
                    'name': intervention.name,
                    'intervention_type': intervention.intervention_type,
                    'state': intervention.state,
                    'date_start': intervention.date_start,
                    'date_finished': intervention.date_finished,
                    'task_name': production_task.name,
                })

        values = {
            'lot': lot,
            'task': production_task,
            'qc_checks': qc_checks,
            'video_url': video_url,
            'farm_story': lot.product_id.product_tmpl_id.description_sale or "Grown with care at our sustainable farm.",
            'intervention_data': intervention_data,
        }
        return request.render('farm_marketing.traceability_portal_template', values)

    @http.route('/farm/order/<int:order_id>/calendar', type='http', auth='public', website=True)
    def order_calendar(self, order_id, **kwargs):
        """ US-097-02: 订单生产透明度 - 为渠道买家提供实时的田间作业日历视图 """
        order = request.env['sale.order'].sudo().search([('id', '=', order_id)], limit=1)
        if not order:
            return request.render('website.404')

        # 验证用户权限 - 买家只能访问自己的订单
        if request.env.user.partner_id != order.partner_id and not request.env.user.has_group('base.group_user'):
            return request.render('website.403')

        # 获取干预日历数据
        intervention_data = order.get_intervention_calendar_data()

        values = {
            'order': order,
            'intervention_data': intervention_data,
        }
        return request.render('farm_marketing.order_calendar_template', values)

    @http.route('/farm/api/order/<int:order_id>/calendar', type='json', auth='public', methods=['POST'])
    def order_calendar_api(self, order_id, **kwargs):
        """ US-097-02: AJAX API for order calendar data """
        order = request.env['sale.order'].sudo().search([('id', '=', order_id)], limit=1)
        if not order:
            return {'error': 'Order not found'}

        # 验证用户权限
        if request.env.user.partner_id != order.partner_id and not request.env.user.has_group('base.group_user'):
            return {'error': 'Access denied'}

        # 获取干预日历数据
        intervention_data = order.get_intervention_calendar_data()

        # 格式化为日历所需的JSON格式
        calendar_events = []
        for intervention in intervention_data:
            color_map = {
                'tillage': 'blue',
                'sowing': 'green',
                'fertilizing': 'orange',
                'irrigation': 'lightblue',
                'protection': 'red',
                'aerial_spraying': 'darkred',
                'harvesting': 'brown',
                'feeding': 'gray',
                'medical': 'purple',
            }

            color = color_map.get(intervention['intervention_type'], 'black')

            event = {
                'id': intervention['id'],
                'title': f"{dict(self.env['agri.intervention.mixin'].fields_get(allfields=['intervention_type'])['intervention_type']['selection']).get(intervention['intervention_type'], intervention['intervention_type'])} - {intervention['task_name']}",
                'start': intervention['date_start'].isoformat() if intervention['date_start'] else '',
                'end': intervention['date_finished'].isoformat() if intervention['date_finished'] else '',
                'color': color,
                'extendedProps': {
                    'state': intervention['state'],
                    'task_name': intervention['task_name'],
                    'intervention_type': intervention['intervention_type']
                }
            }
            calendar_events.append(event)

        return {'events': calendar_events}
