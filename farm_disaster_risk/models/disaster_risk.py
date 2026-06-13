from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import date

class FarmDisasterIncident(models.Model):
    _name = 'farm.disaster.incident'
    _description = 'Meteorological Disaster Incident'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Incident Ref", default=lambda self: _('New'))
    disaster_type = fields.Selection([
        ('hail', 'Hail'),
        ('frost', 'Frost'),
        ('flood', 'Flood'),
        ('drought', 'Drought'),
        ('gale', 'Gale/Storm'),
        ('high_temp', 'High Temperature'),
        ('other', 'Other')
    ], string="Disaster Type", required=True)
    
    date_start = fields.Date("Start Date", default=fields.Date.today)
    date_end = fields.Date("End Date")
    
    affected_location_ids = fields.Many2many('farm.location', string="Affected Land Parcels", domain=[('is_land_parcel', '=', True)])
    intensity = fields.Selection([
        ('minor', 'Minor'),
        ('moderate', 'Moderate'),
        ('severe', 'Severe')
    ], string="Intensity", default='minor')
    
    description = fields.Text("Description of Damage")
    
    # 与危机管理模块联动
    #crisis_incident_id = fields.Many2one('farm.crisis.incident', string="Linked Crisis Incident")
    
    # 损失评估关联
    loss_assessment_ids = fields.One2many('farm.loss.assessment', 'disaster_incident_id', string="Loss Assessments")
    total_estimated_loss = fields.Monetary("Total Estimated Loss", compute='_compute_total_estimated_loss')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)


    # AI Integration
    ai_strategy_log = fields.Text("AI Remediation Strategy", tracking=True)
    intervention_ids = fields.Many2many('mrp.production', string="AI Generated Interventions")

    def action_request_ai_strategy(self):
        self.ensure_one()
        
        # Soft dependency check: Only run if AI modules are installed
        if 'agri.ai.llm.service' not in self.env:
            self.message_post(body=_("AI Services are not installed. Cannot generate strategy."))
            return False
            
        import json
        import logging
        _logger = logging.getLogger(__name__)

        llm_service = self.env['agri.ai.llm.service'].search([], limit=1)
        prompt = f"Disaster Type: {self.disaster_type}, Intensity: {self.intensity}, Description: {self.description}. Generate an urgent agricultural intervention strategy JSON with keys 'action_type' (one of: protection, irrigation, harvesting, aerial_spraying), 'strategy_name', and 'details'."
        
        strategy_json = "{}"
        if llm_service and not self.env.context.get('test_mock_llm'):
            try:
                # We expect the LLM to return a JSON string
                strategy_json = llm_service.call_llm(prompt)
            except Exception as e:
                _logger.warning("LLM call failed: %s", str(e))
                strategy_json = self._get_mock_strategy()
        else:
            strategy_json = self._get_mock_strategy()

        try:
            strategy_data = json.loads(strategy_json)
        except json.JSONDecodeError:
            strategy_data = {"action_type": "protection", "strategy_name": "Emergency Fallback", "details": strategy_json}

        self.ai_strategy_log = json.dumps(strategy_data, indent=2, ensure_ascii=False)

        # Automatically generate the Intervention (mrp.production)
        # Using a generic service product
        product = self.env['product.product'].search([('type', '=', 'service')], limit=1)
        if not product:
            product = self.env['product.product'].create({'name': 'Disaster Remediation Service', 'type': 'service'})
            
        intervention_type = strategy_data.get('action_type', 'protection')
        if intervention_type not in ['tillage', 'sowing', 'fertilizing', 'irrigation', 'protection', 'aerial_spraying', 'harvesting', 'feeding']:
            intervention_type = 'protection'
            
        intervention = self.env['mrp.production'].create({
            'product_id': product.id,
            'product_qty': 1.0,
            'intervention_type': intervention_type,
            'origin': self.name,
        })
        
        # Link the generated intervention
        self.write({'intervention_ids': [(4, intervention.id)]})
        
        self.message_post(body=_("Robot AI Agent generated a strategy and automatically created Intervention Order: %s") % intervention.name)
        return True

    def _get_mock_strategy(self):
        if self.disaster_type == 'frost':
            return '{"action_type": "protection", "strategy_name": "Anti-Frost Spraying", "details": "Deploy drones to spray anti-frost agents immediately."}'
        elif self.disaster_type == 'drought':
            return '{"action_type": "irrigation", "strategy_name": "Deep Irrigation", "details": "Trigger deep root irrigation across all affected parcels."}'
        return '{"action_type": "harvesting", "strategy_name": "Emergency Harvest", "details": "Harvest marketable crops immediately to minimize financial loss."}'

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
    
    affected_parcel_id = fields.Many2one('farm.location', string="Affected Land Parcel", domain=[('is_land_parcel', '=', True)], required=True)
    crop_id = fields.Many2one('product.product', string="Affected Crop", domain=[('is_variety', '=', True)])
    
    estimated_loss_amount = fields.Monetary("Estimated Loss Amount", currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    
    loss_description = fields.Text("Detailed Loss Description")
    
    insurance_claim_id = fields.Many2one('account.move', string="Linked Insurance Claim") # 退款
    
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
