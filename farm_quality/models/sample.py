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
        ('active', 'Retained (留样中)'),
        ('used', 'Used (已检测)'),
        ('disposed', 'Disposed (已销毁)')
    ], default='active', tracking=True)

    check_ids = fields.One2many('farm.quality.check', 'sample_id', string="Quality Checks")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('farm.quality.sample') or _('SMP')
        return super().create(vals_list)

    def action_dispose(self):
        self.write({'state': 'disposed'})
        self.message_post(body=_("Sample disposed on %s") % fields.Date.today())
