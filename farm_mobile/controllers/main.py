from odoo import http
from odoo.http import request

class FarmMobileController(http.Controller):

    @http.route('/agri/scan/<string:model>/<int:res_id>', type='http', auth='user')
    def agri_scan_redirect(self, model, res_id, **kwargs):
        """ 扫码重定向逻辑 [US-02-03] """
        if model == 'location':
            # 跳转至该地块关联的未完成任务
            task = request.env['project.task'].sudo().search([
                ('land_parcel_id', '=', res_id),
                ('is_closed', '=', False)
            ], limit=1)
            if task:
                return request.redirect('/web#id=%s&model=project.task&view_type=form' % task.id)
            return request.redirect('/web#id=%s&model=stock.location&view_type=form' % res_id)
            
        elif model == 'lot':
            # 跳转至批次详情页
            return request.redirect('/web#id=%s&model=stock.lot&view_type=form' % res_id)
            
        return request.redirect('/web')