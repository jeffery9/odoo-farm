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

class StockLot(models.Model):
    _inherit = 'stock.lot'

    is_crisis_locked = fields.Boolean("Locked by Crisis", compute='_compute_crisis_lock', search='_search_crisis_locked')

    def _compute_crisis_lock(self):
        """ 检查该批次是否处于活动状态的危机区域中 """
        for lot in self:
            active_crisis = self.env['farm.crisis.incident'].search([
                ('state', '=', 'active'),
                '|',
                ('affected_lot_ids', 'in', lot.id),
                ('affected_location_ids', 'parent_of', lot.location_id.id)
            ])
            lot.is_crisis_locked = bool(active_crisis)

    def _search_crisis_locked(self, operator, value):
        """ 支持对锁定状态的搜索和过滤 """
        active_crisis = self.env['farm.crisis.incident'].search([('state', '=', 'active')])
        lot_ids = active_crisis.mapped('affected_lot_ids').ids
        location_ids = active_crisis.mapped('affected_location_ids').ids
        
        # 找到处于这些位置的所有子位置下的批次
        all_affected_locations = self.env['stock.location'].search([('id', 'child_of', location_ids)])
        
        return ['|', ('id', 'in', lot_ids), ('location_id', 'in', all_affected_locations.ids)]

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        """ 确认销售订单前，强行校验是否包含锁定批次 """
        for order in self:
            for line in order.order_line:
                if line.lot_id and line.lot_id.is_crisis_locked:
                    raise UserError(_("SALE BLOCK: Lot '%s' is under CRISIS LOCKDOWN and cannot be sold.") % line.lot_id.name)
        return super(SaleOrder, self).action_confirm()
