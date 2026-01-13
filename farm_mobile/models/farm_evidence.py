from odoo import models, fields, api, _

class FarmEvidence(models.Model):
    """
    US-24-04 & US-07-05: 通用现场取证模型
    职责：记录带 GPS 水印的现场照片，支持关联任务、地块、批次等
    """
    _name = 'farm.evidence'
    _description = 'Field Evidence'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char("Evidence Label", required=True, default=lambda self: _('Field Photo'))
    res_model = fields.Char("Related Model", index=True)
    res_id = fields.Many2one_reference("Related ID", model_field='res_model', index=True)
    
    photo = fields.Binary("Evidence Photo", attachment=True, required=True)
    
    # 自动采集的硬件数据 [US-24-01]
    gps_lat = fields.Float("Latitude", digits=(10, 7))
    gps_lng = fields.Float("Longitude", digits=(10, 7))
    taken_at = fields.Datetime("Captured Time", default=fields.Datetime.now)
    
    worker_id = fields.Many2one('hr.employee', string="Captured By", default=lambda self: self.env.user.employee_id)
    note = fields.Text("Field Notes")

    # 判定位置合规性 (如果关联了地块)
    is_on_site = fields.Boolean("Location Verified", compute='_compute_site_verification', store=True)

    @api.depends('gps_lat', 'gps_lng', 'res_model', 'res_id')
    def _compute_site_verification(self):
        """ 如果取证关联了地块或任务，自动校验拍摄位置是否在边界内 """
        for rec in self:
            if not rec.gps_lat or not rec.res_model:
                rec.is_on_site = False
                continue
            
            # 逻辑：查找关联地块
            parcel = False
            if rec.res_model == 'stock.location':
                parcel = self.env[rec.res_model].browse(rec.res_id)
            elif rec.res_model == 'mrp.production':
                mo = self.env[rec.res_model].browse(rec.res_id)
                parcel = mo.agri_task_id.land_parcel_id
            
            if parcel and parcel.gps_coordinates:
                temp_fence = self.env['farm.geofence'].new({'coordinates': parcel.gps_coordinates})
                rec.is_on_site = temp_fence.is_point_inside(rec.gps_lng, rec.gps_lat)
            else:
                rec.is_on_site = True # 无边界定义则视为默认合规
