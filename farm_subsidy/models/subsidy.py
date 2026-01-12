from odoo import models, fields, api, _

class FarmSubsidyProgram(models.Model):
    _name = 'farm.subsidy.program'
    _description = 'Agricultural Subsidy Program'

    name = fields.Char("Program Name", required=True) # e.g. "2026 Organic Conversion Support"
    code = fields.Char("Policy Code")
    authority = fields.Char("Issuing Authority")
    
    subsidy_type = fields.Selection([
        ('area', 'Per Area (按面积)'),
        ('head', 'Per Head (按头数)'),
        ('project', 'Project Based (项目制)'),
        ('output', 'Per Output (按产量)')
    ], required=True, default='area')
    
    amount_per_unit = fields.Monetary("Amount per Unit")
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    
    requirements = fields.Text("Compliance Requirements")

class FarmSubsidyApplication(models.Model):
    _name = 'farm.subsidy.application'
    _description = 'Subsidy Application'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Application Ref", default=lambda self: _('New'))
    program_id = fields.Many2one('farm.subsidy.program', string="Program", required=True)
    fiscal_year = fields.Integer("Fiscal Year", default=lambda self: fields.Date.today().year)
    
    # 申报对象
    land_parcel_ids = fields.Many2many('stock.location', string="Declared Parcels", domain=[('is_land_parcel', '=', True)])
    
    declared_quantity = fields.Float("Declared Qty (Area/Head)")
    estimated_amount = fields.Monetary("Estimated Amount", compute='_compute_estimated_amount')
    currency_id = fields.Many2one('res.currency', related='program_id.currency_id')
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('paid', 'Paid')
    ], default='draft', tracking=True)

    @api.depends('declared_quantity', 'program_id.amount_per_unit')
    def _compute_estimated_amount(self):
        for app in self:
            app.estimated_amount = app.declared_quantity * app.program_id.amount_per_unit

    @api.onchange('land_parcel_ids')
    def _onchange_parcels(self):
        if self.program_id.subsidy_type == 'area':
            self.declared_quantity = sum(self.land_parcel_ids.mapped('land_area'))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('farm.subsidy.application') or _('SUB')
        return super().create(vals_list)
