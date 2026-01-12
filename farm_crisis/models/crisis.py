from odoo import models, fields, api, _

class FarmEmergencyProtocol(models.Model):
    _name = 'farm.emergency.protocol'
    _description = 'Emergency Response Protocol (SOP)'

    name = fields.Char("Protocol Name", required=True) # e.g. "Avian Flu Response Level 1"
    crisis_type = fields.Selection([
        ('disease', 'Disease Outbreak (疫病)'),
        ('pest', 'Pest Infestation (虫害)'),
        ('contamination', 'Contamination (污染)'),
        ('disaster', 'Natural Disaster (自然灾害)'),
        ('security', 'Security Breach (安防)')
    ], required=True)
    
    steps = fields.Html("Action Steps (SOP)")
    required_asset_lockdown = fields.Boolean("Requires Asset Lockdown", default=True)
    notify_authorities = fields.Boolean("Notify Authorities")

class FarmCrisisIncident(models.Model):
    _name = 'farm.crisis.incident'
    _description = 'Crisis Incident Record'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Incident Ref", default=lambda self: _('New'))
    protocol_id = fields.Many2one('farm.emergency.protocol', string="Active Protocol", required=True)
    date_start = fields.Datetime("Detected At", default=fields.Datetime.now)
    date_end = fields.Datetime("Resolved At")
    
    affected_location_ids = fields.Many2many('stock.location', string="Affected Zones", domain=[('is_land_parcel', '=', True)])
    affected_lot_ids = fields.Many2many('stock.lot', string="Affected Assets/Batches")
    
    state = fields.Selection([
        ('draft', 'Reported'),
        ('active', 'Active Crisis'),
        ('contained', 'Contained'),
        ('resolved', 'Resolved')
    ], default='draft', tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('farm.crisis.incident') or _('INCIDENT')
        return super().create(vals_list)

    def action_activate_crisis(self):
        """ 激活危机模式：锁定资产并通知人员 """
        self.ensure_one()
        self.write({'state': 'active'})
        
        if self.protocol_id.required_asset_lockdown:
            # 锁定关联的生物资产或批次
            reason = _("CRISIS LOCKDOWN: %s") % self.name
            for lot in self.affected_lot_ids:
                if hasattr(lot, 'action_quarantine'):
                    lot.action_quarantine(reason)
            
            self.message_post(body=_("CRISIS MODE ACTIVATED: Assets have been quarantined."))

    def action_resolve(self):
        self.write({'state': 'resolved', 'date_end': fields.Datetime.now()})
