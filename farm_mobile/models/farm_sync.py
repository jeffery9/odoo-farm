from odoo import models, fields, api, _

class FarmSyncQueue(models.Model):
    _name = 'farm.sync.queue'
    _description = 'Offline Data Sync Queue'
    _order = 'create_date asc'

    operation_type = fields.Selection([
        ('worklog', 'Field Worklog'),
        ('feeding', 'Feeding record'),
        ('harvest', 'Harvest record')
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
                
                record.write({'status': 'done', 'error_message': False})
            except Exception as e:
                record.write({'status': 'failed', 'error_message': str(e)})
