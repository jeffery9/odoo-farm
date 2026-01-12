from odoo import models, fields, api, _

class FarmManureBatch(models.Model):
    _name = 'farm.manure.batch'
    _description = 'Manure Batch Record'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'batch_no'

    batch_no = fields.Char("Batch No.", default=lambda self: _('New'))
    production_date = fields.Date("Production Date", default=fields.Date.today)
    quantity = fields.Float("Quantity (kg)")
    lot_source_ids = fields.Many2many('stock.lot', string="Source Animal Lots", domain=[('agricultural_type', 'in', ['animal', 'animal_group'])])
    location_source_id = fields.Many2one('stock.location', string="Source Location", domain=[('usage', '=', 'internal')]) # e.g., Barn
    
    # 处理方式
    disposal_method = fields.Selection([
        ('composting', 'Composting (堆肥)'),
        ('biogas', 'Biogas Digestion (沼气发酵)'),
        ('transfer_third_party', 'Transfer to Third Party (第三方转运)'),
        ('direct_field_use', 'Direct Field Use (直接还田)')
    ], string="Disposal Method", required=True)
    
    # 去向及接收方
    destination_location_id = fields.Many2one('stock.location', string="Destination Location", domain=[('is_land_parcel', '=', True)], invisible="disposal_method != 'direct_field_use'")
    recipient_partner_id = fields.Many2one('res.partner', string="Recipient (Third Party)", invisible="disposal_method != 'transfer_third_party'")
    
    notes = fields.Text("Notes")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('batch_no', _('New')) == _('New'):
                vals['batch_no'] = self.env['ir.sequence'].next_by_code('farm.manure.batch') or _('MNR')
        return super().create(vals_list)

class FarmManureLedger(models.Model):
    _name = 'farm.manure.ledger'
    _description = 'Monthly Manure Resource Utilization Ledger'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'ledger_no'

    ledger_no = fields.Char("Ledger No.", default=lambda self: _('New'))
    month = fields.Selection([
        ('01', 'January'), ('02', 'February'), ('03', 'March'), ('04', 'April'),
        ('05', 'May'), ('06', 'June'), ('07', 'July'), ('08', 'August'),
        ('09', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')
    ], string="Month", default=lambda self: fields.Date.today().strftime('%m'), required=True)
    year = fields.Integer("Year", default=lambda self: fields.Date.today().year, required=True)
    
    batch_ids = fields.Many2many('farm.manure.batch', string="Manure Batches Included", compute='_compute_batch_ids', store=True)
    total_quantity_disposed = fields.Float("Total Disposed Quantity (kg)", compute='_compute_ledger_stats', store=True)
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('reported', 'Reported')
    ], default='draft', tracking=True)

    @api.depends('month', 'year')
    def _compute_batch_ids(self):
        for ledger in self:
            date_start = fields.Date.from_string(f"{ledger.year}-{ledger.month}-01")
            date_end = date_start + relativedelta(months=1, days=-1)
            ledger.batch_ids = self.env['farm.manure.batch'].search([
                ('production_date', '>=', date_start),
                ('production_date', '<=', date_end)
            ])
    
    @api.depends('batch_ids.quantity')
    def _compute_ledger_stats(self):
        for ledger in self:
            ledger.total_quantity_disposed = sum(ledger.batch_ids.mapped('quantity'))

    def action_generate_moara_ledger(self):
        """ 模拟生成农业农村部畜禽粪污资源化利用台账 [US-18-05] """
        self.ensure_one()
        self.message_post(body=_("MOARA Manure Utilization Ledger generated for %s/%s.") % (self.month, self.year))
        return True

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('ledger_no', _('New')) == _('New'):
                vals['ledger_no'] = self.env['ir.sequence'].next_by_code('farm.manure.ledger') or _('MNL')
        return super().create(vals_list)
