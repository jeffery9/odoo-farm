from odoo import models, fields, api, _

class FarmEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    # 农机购置补贴信息 [US-18-07]
    is_subsidized_machinery = fields.Boolean("Eligible for Subsidy", default=False)
    subsidy_category = fields.Char("Subsidy Category") # e.g. "耕整地机械-拖拉机"
    subsidy_model_no = fields.Char("Subsidy Model No.")
    subsidy_grade_params = fields.Char("Subsidy Grading Parameters")
    estimated_subsidy_amount = fields.Monetary("Estimated Subsidy Amount", currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    
    # 用于补贴申报材料
    invoice_attachment_ids = fields.Many2many('ir.attachment', 'machinery_invoice_rel', 'equipment_id', 'attachment_id', string="Invoice Attachments")
    photo_attachment_ids = fields.Many2many('ir.attachment', 'machinery_photo_rel', 'equipment_id', 'attachment_id', string="Machinery Photos")
    
    def action_match_subsidy_catalog(self):
        """ 
        US-18-07: 匹配国家农机购置补贴目录
        实现基于铭牌编号的自动参数填充逻辑
        """
        self.ensure_one()
        # 模拟外部补贴目录数据库
        MOCK_CATALOG = {
            'DF-2004': {'category': '耕整地机械-轮式拖拉机', 'grade': '200马力及以上', 'subsidy': 42000.0},
            'LZ-1002': {'category': '收割机械-联合收割机', 'grade': '喂入量10kg/s以上', 'subsidy': 85000.0},
        }
        
        # 尝试匹配型号
        match = MOCK_CATALOG.get(self.model)
        if match:
            self.write({
                'is_subsidized_machinery': True,
                'subsidy_category': match['category'],
                'subsidy_model_no': self.model,
                'subsidy_grade_params': match['grade'],
                'estimated_subsidy_amount': match['subsidy'],
            })
            self.message_post(body=_("Subsidy Catalog Matched: %s. Estimated Subsidy: %s.") % (match['category'], match['subsidy']))
        else:
            self.message_post(body=_("No matching entry found in National Subsidy Catalog for model %s.") % self.model)
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
