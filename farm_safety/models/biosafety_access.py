from odoo import models, fields, api, _

class FarmBiosafetyAccessLog(models.Model):
    """ US-35-01: Bio-safety Access Control (生物安全门禁) """
    _name = 'farm.biosafety.access.log'
    _description = 'Bio-safety Access Log'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'access_time desc'

    location_id = fields.Many2one('stock.location', string="Restricted Area", domain=[('usage', '=', 'internal')], required=True)
    person_id = fields.Many2one('res.partner', string="Person/Visitor")
    employee_id = fields.Many2one('hr.employee', string="Employee")
    
    access_time = fields.Datetime("Access Time", default=fields.Datetime.now)
    access_type = fields.Selection([
        ('entry', 'Entry'),
        ('exit', 'Exit')
    ], string="Type", required=True, default='entry')
    
    sanitization_confirmed = fields.Boolean("Sanitization Performed", default=False)
    quarantine_period_passed = fields.Boolean("Quarantine Period Passed", default=True)
    
    vehicle_plate = fields.Char("Vehicle Plate")
    purpose = fields.Text("Purpose of Entry")

    @api.model_create_multi
    def create(self, vals_list):
        logs = super().create(vals_list)
        for log in logs:
            if not log.sanitization_confirmed and log.access_type == 'entry':
                log.message_post(body=_("WARNING: Bio-safety entry without confirmed sanitization!"))
        return logs
