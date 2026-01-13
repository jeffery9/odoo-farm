from odoo import models, fields, api, _

class FarmSyncQueue(models.Model):
    _name = 'farm.sync.queue'
    _description = 'Offline Data Sync Queue'
    _order = 'create_date asc'

    operation_type = fields.Selection([
        ('worklog', 'Field Worklog'),
        ('feeding', 'Feeding record'),
        ('harvest', 'Harvest record'),
        ('delivery', 'Mobile Delivery')
    ], required=True)
    
    payload = fields.Text("Data Payload (JSON)", required=True)
    status = fields.Selection([
        ('pending', 'Pending Sync'),
        ('done', 'Synced'),
        ('failed', 'Error')
    ], default='pending', tracking=True)
    
    error_message = fields.Text("Error Details")
    user_id = fields.Many2one('res.users', string="Worker", default=lambda self: self.env.user)

    def action_sync(self):
        """ 批量同步逻辑 """
        import json
        for record in self.filtered(lambda r: r.status != 'done'):
            try:
                data = json.loads(record.payload)
                if record.operation_type == 'worklog':
                    self.env['farm.worklog'].create(data)
                elif record.operation_type == 'delivery':
                    # data 预期包含 picking_id 或 barcode
                    picking = self.env['stock.picking'].browse(data.get('picking_id'))
                    if picking and picking.state not in ['done', 'cancel']:
                        picking.button_validate()
                
                record.write({'status': 'done', 'error_message': False})
            except Exception as e:
                record.write({'status': 'failed', 'error_message': str(e)})

    def action_get_asset_redirect(self, barcode):
        """ 根据条码返回资产跳转信息 [US-02-03] """
        # 搜索批次
        lot = self.env['stock.lot'].search([('name', '=', barcode)], limit=1)
        if lot:
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'stock.lot',
                'res_id': lot.id,
                'view_mode': 'form',
            }
        # 搜索地块
        loc = self.env['stock.location'].search([('name', '=', barcode), ('is_land_parcel', '=', True)], limit=1)
        if loc:
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'stock.location',
                'res_id': loc.id,
                'view_mode': 'form',
            }
        return False