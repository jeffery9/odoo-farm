from odoo import models, fields, api, _

class FarmEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    # 农机购置补贴信息 [US-18-07]
    is_subsidized_machinery = fields.Boolean("Eligible for Subsidy", default=False)
    subsidy_category = fields.Char("Subsidy Category (补贴机具分类)") # e.g. "耕整地机械-拖拉机"
    subsidy_model_no = fields.Char("Subsidy Model No. (补贴机具型号)")
    subsidy_grade_params = fields.Char("Subsidy Grading Parameters (分档参数)")
    estimated_subsidy_amount = fields.Monetary("Estimated Subsidy Amount", currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    
    # 用于补贴申报材料
    invoice_attachment_ids = fields.Many2many('ir.attachment', 'machinery_invoice_rel', 'equipment_id', 'attachment_id', string="Invoice Attachments")
    photo_attachment_ids = fields.Many2many('ir.attachment', 'machinery_photo_rel', 'equipment_id', 'attachment_id', string="Machinery Photos")
    
    def action_match_subsidy_catalog(self):
        """ 模拟匹配国家农机购置补贴目录 [US-18-07] """
        self.ensure_one()
        _logger.info("Simulating matching subsidy catalog for equipment %s", self.name)
        # 实际这里会通过外部API或本地数据库匹配
        self.is_subsidized_machinery = True
        self.subsidy_category = "耕整地机械-拖拉机"
        self.subsidy_model_no = self.model
        self.subsidy_grade_params = "200马力以上"
        self.estimated_subsidy_amount = 50000.0 # 模拟补贴金额
        self.message_post(body=_("Subsidy catalog matched for %s. Estimated subsidy: %s %s.") % (self.name, self.estimated_subsidy_amount, self.currency_id.symbol))
        return True

class FarmMachinerySubsidyApplication(models.Model):
    _name = 'farm.machinery.subsidy.application'
    _description = 'Agricultural Machinery Subsidy Application'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Application Ref", default=lambda self: _('New'))
    equipment_id = fields.Many2one('maintenance.equipment', string="Machinery", required=True)
    applicant_id = fields.Many2one('res.partner', string="Applicant", default=lambda self: self.env.company.partner_id)
    application_date = fields.Date("Application Date", default=fields.Date.today)
    
    estimated_subsidy = fields.Monetary("Estimated Subsidy", related='equipment_id.estimated_subsidy_amount')
    currency_id = fields.Many2one('res.currency', related='equipment_id.currency_id')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('paid', 'Paid'),
        ('rejected', 'Rejected')
    ], default='draft', tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('farm.machinery.subsidy.application') or _('AMS')
        return super().create(vals_list)
