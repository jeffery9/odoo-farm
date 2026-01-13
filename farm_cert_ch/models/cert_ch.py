from odoo import models, fields, api, _

class FarmProductCertificate(models.Model):
    _name = 'farm.product.certificate'
    _description = 'Edible Agri-Product Certificate'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'certificate_no'

    certificate_no = fields.Char("Certificate No.", default=lambda self: _('New'))
    picking_id = fields.Many2one('stock.picking', string="Source Dispatch", required=True)
    lot_id = fields.Many2one('stock.lot', string="Product Lot", required=True)
    product_id = fields.Many2one('product.product', related='lot_id.product_id', store=True)

    producer_name = fields.Char("Producer Name", default=lambda self: self.env.company.name)
    origin_location_id = fields.Many2one('stock.location', string="Origin/Farm", domain=[('is_land_parcel', '=', True)])
    production_date = fields.Date("Production Date", related='lot_id.create_date', store=True)
    
    # 承诺声明
    commitment_statement = fields.Html("Commitment Statement", default="""
        <p>本单位郑重承诺，所销售食用农产品符合农产品质量安全国家强制性标准，对产品质量安全负责。</p>
        <p>I/We hereby solemnly promise that the edible agricultural products sold comply with the national mandatory standards for agricultural product quality and safety, and are responsible for the quality and safety of the products.</p>
    """)
    
    # 检测结果
    quality_check_ids = fields.Many2many('farm.quality.check', string="Related Quality Checks")
    
    certificate_qr_code = fields.Char("Certificate QR Code", compute='_compute_qr_code', store=True)

    @api.depends('certificate_no')
    def _compute_qr_code(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        for cert in self:
            cert.certificate_qr_code = f"{base_url}/farm/cert_ch/view/{cert.certificate_no}"

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('certificate_no', _('New')) == _('New'):
                vals['certificate_no'] = self.env['ir.sequence'].next_by_code('farm.product.certificate') or _('PPC')
        return super().create(vals_list)

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    requires_cert_ch = fields.Boolean("Requires Cert. (China)", compute='_compute_requires_cert_ch', store=True)
    certificate_ch_ids = fields.One2many('farm.product.certificate', 'picking_id', string="Certificates (China)")

    @api.depends('move_ids.product_id')
    def _compute_requires_cert_ch(self):
        for picking in self:
            # 简化逻辑: 只要有农产品出库就可能需要
            picking.requires_cert_ch = any(p.categ_id.id == self.env.ref('farm_core.category_harvested').id for p in picking.move_ids.mapped('product_id'))

    def action_generate_cert_ch(self):
        """ 生成食用农产品承诺达标合格证 [US-18-03] """
        self.ensure_one()
        for move in self.move_ids.filtered(lambda m: m.state == 'done'):
            for lot in move.lot_ids:
                # 检查是否已生成
                existing_cert = self.env['farm.product.certificate'].search([
                    ('picking_id', '=', self.id),
                    ('lot_id', '=', lot.id)
                ], limit=1)
                if not existing_cert:
                    self.env['farm.product.certificate'].create({
                        'picking_id': self.id,
                        'lot_id': lot.id,
                        'producer_name': self.env.company.name, # 默认本公司
                        'origin_location_id': move.location_id.id, # 默认发货库位所在的地块
                        'quality_check_ids': lot.quality_check_ids.ids, # 关联批次的所有质检记录
                    })
        return True
