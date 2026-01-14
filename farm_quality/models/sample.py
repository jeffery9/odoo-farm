from odoo import models, fields, api, _

class FarmQualitySample(models.Model):
    _name = 'farm.quality.sample'
    _description = 'Agri Quality Sample'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Sample ID", required=True, copy=False, default=lambda self: _('New'))
    lot_id = fields.Many2one('stock.lot', string="Origin Lot", required=True)
    product_id = fields.Many2one('product.product', related='lot_id.product_id', store=True)
    
    collection_date = fields.Date("Collection Date", default=fields.Date.today)
    collected_by = fields.Many2one('res.users', string="Collected By", default=lambda self: self.env.user)
    
    storage_location = fields.Char("Storage Location", help="e.g. Lab Fridge A-01")
    expiry_date = fields.Date("Retention Expiry")
    
    state = fields.Selection([
        ('active', 'Retained'),
        ('used', 'Used'),
        ('disposed', 'Disposed')
    ], default='active', tracking=True)

    # 盲样相关字段 [US-15-06]
    blind_code = fields.Char("Blind Sample Code", copy=False, help="Anonymous reference for blind testing")
    is_blind_test = fields.Boolean("Blind Test", default=False, help="When checked, hides source details from testers")
    blind_tester_id = fields.Many2one('res.users', string="Blind Tester", help="User who should only see blind code, not source details")

    check_ids = fields.One2many('farm.quality.check', 'sample_id', string="Quality Checks")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('farm.quality.sample') or _('SMP')

            # 如果启用了盲样测试，生成盲样代码
            if vals.get('is_blind_test'):
                import uuid
                vals['blind_code'] = 'BL-' + str(uuid.uuid4())[:8].upper()

        return super().create(vals_list)

    def get_blind_sample_info(self):
        """ 获取盲样测试信息，不暴露实际来源 [US-15-06] """
        self.ensure_one()
        if self.is_blind_test:
            return {
                'blind_code': self.blind_code,
                'product_display': _('Blind Sample Product'),
                'lot_display': _('Blind Sample Batch'),
                'origin_info_hidden': True
            }
        else:
            return {
                'blind_code': None,
                'product_display': self.product_id.name,
                'lot_display': self.lot_id.name,
                'origin_info_hidden': False
            }

    def action_dispose(self):
        self.write({'state': 'disposed'})
        self.message_post(body=_("Sample disposed on %s") % fields.Date.today())
