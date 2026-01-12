from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import date

class FarmDisasterIncident(models.Model):
    _name = 'farm.disaster.incident'
    _description = 'Meteorological Disaster Incident'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Incident Ref", default=lambda self: _('New'))
    disaster_type = fields.Selection([
        ('hail', 'Hail (冰雹)'),
        ('frost', 'Frost (霜冻)'),
        ('flood', 'Flood (洪涝)'),
        ('drought', 'Drought (干旱)'),
        ('gale', 'Gale/Storm (大风/暴风)'),
        ('high_temp', 'High Temperature (高温)'),
        ('other', 'Other (其他)')
    ], string="Disaster Type", required=True)
    
    date_start = fields.Date("Start Date", default=fields.Date.today)
    date_end = fields.Date("End Date")
    
    affected_location_ids = fields.Many2many('stock.location', string="Affected Land Parcels", domain=[('is_land_parcel', '=', True)])
    intensity = fields.Selection([
        ('minor', 'Minor (轻微)'),
        ('moderate', 'Moderate (中度)'),
        ('severe', 'Severe (严重)')
    ], string="Intensity", default='minor')
    
    description = fields.Text("Description of Damage")
    
    # 与危机管理模块联动
    crisis_incident_id = fields.Many2one('farm.crisis.incident', string="Linked Crisis Incident")
    
    # 损失评估关联
    loss_assessment_ids = fields.One2many('farm.loss.assessment', 'disaster_incident_id', string="Loss Assessments")
    total_estimated_loss = fields.Monetary("Total Estimated Loss", compute='_compute_total_estimated_loss')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)

    @api.depends('loss_assessment_ids.estimated_loss_amount')
    def _compute_total_estimated_loss(self):
        for incident in self:
            incident.total_estimated_loss = sum(incident.loss_assessment_ids.mapped('estimated_loss_amount'))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('farm.disaster.incident') or _('DI')
        return super().create(vals_list)
    
    def action_create_crisis_incident(self):
        """ 创建联动危机事件 """
        self.ensure_one()
        if self.crisis_incident_id:
            raise UserError(_("A crisis incident is already linked to this disaster."))
        
        crisis_vals = {
            'name': _("Disaster Crisis: %s (%s)") % (self.disaster_type, self.name),
            'protocol_id': self.env.ref('farm_crisis.protocol_natural_disaster', raise_if_not_found=False).id, # 假设有自然灾害协议
            'date_start': self.date_start,
            'affected_location_ids': self.affected_location_ids.ids,
            'description': _("Triggered by meteorological disaster incident %s.") % self.name,
        }
        crisis = self.env['farm.crisis.incident'].create(crisis_vals)
        self.write({'crisis_incident_id': crisis.id})
        return {
            'name': _('Linked Crisis Incident'),
            'view_mode': 'form',
            'res_model': 'farm.crisis.incident',
            'res_id': crisis.id,
            'type': 'ir.actions.act_window',
            'target': 'current',
        }

class FarmLossAssessment(models.Model):
    _name = 'farm.loss.assessment'
    _description = 'Disaster Loss Assessment'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Assessment Ref", default=lambda self: _('New'))
    disaster_incident_id = fields.Many2one('farm.disaster.incident', string="Disaster Incident", required=True)
    assessment_date = fields.Date("Assessment Date", default=fields.Date.today)
    assessor_id = fields.Many2one('res.partner', string="Assessor")
    
    affected_parcel_id = fields.Many2one('stock.location', string="Affected Land Parcel", domain=[('is_land_parcel', '=', True)], required=True)
    crop_id = fields.Many2one('product.product', string="Affected Crop", domain=[('is_variety', '=', True)])
    
    estimated_loss_amount = fields.Monetary("Estimated Loss Amount", currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    
    loss_description = fields.Text("Detailed Loss Description")
    
    insurance_claim_id = fields.Many2one('account.move', string="Linked Insurance Claim") # 假设是供应商账单/退款
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted to Insurance'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], default='draft', tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('farm.loss.assessment') or _('LA')
        return super().create(vals_list)
