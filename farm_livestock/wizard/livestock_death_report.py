from odoo import models, fields, api

class LivestockDeathReport(models.TransientModel):
    _name = 'livestock.death.report'
    _description = 'Report Livestock Death'

    lot_id = fields.Many2one('stock.lot', string="Animal Group", required=True)
    qty = fields.Float("Quantity", default=1.0, required=True)
    reason = fields.Selection([
        ('disease', 'Disease (疾病)'),
        ('accident', 'Accident (意外)'),
        ('disaster', 'Natural Disaster (自然灾害)'),
        ('other', 'Other (其他)')
    ], string="Reason", required=True)
    notes = fields.Text("Notes")

    def action_confirm(self):
        self.lot_id.action_record_death(self.qty, self.reason, self.notes)
