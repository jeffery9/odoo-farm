from odoo import http
from odoo.http import request

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
        
        # 获取直播流地址 [US-16-01]
        video_url = lot.location_id.camera_device_id.live_stream_url if lot.location_id.camera_device_id else False

        values = {
            'lot': lot,
            'task': production_task,
            'qc_checks': qc_checks,
            'video_url': video_url,
            'farm_story': lot.product_id.product_tmpl_id.description_sale or "Grown with care at our sustainable farm."
        }
        return request.render('farm_marketing.traceability_portal_template', values)
