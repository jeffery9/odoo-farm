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
        ('composting', 'Composting'),
        ('biogas', 'Biogas Digestion'),
        ('transfer_third_party', 'Transfer to Third Party'),
        ('direct_field_use', 'Direct Field Use')
    ], string="Disposal Method", required=True)
    
    # 去向及接收方
    destination_location_id = fields.Many2one('stock.location', string="Destination Location", domain=[('is_land_parcel', '=', True)], invisible="disposal_method != 'direct_field_use'")
    recipient_partner_id = fields.Many2one('res.partner', string="Recipient (Third Party)", invisible="disposal_method != 'transfer_third_party'")
    
    fertilizer_product_id = fields.Many2one('product.product', string="Converted Fertilizer Product", domain=[('input_type', '=', 'fertilizer')])
    
    # US-27-01: Quality Check Linkage
    quality_check_id = fields.Many2one('farm.quality.check', string="Quality Check (Maturity)", domain=[('quality_state', '=', 'pass')])
    
    # Nutrient Return [US-27-01, US-27-02]
    pure_n_qty = fields.Float("Pure Nitrogen (kg)", compute='_compute_nutrients', store=True)
    pure_p_qty = fields.Float("Pure Phosphorus (kg)", compute='_compute_nutrients', store=True)
    pure_k_qty = fields.Float("Pure Potassium (kg)", compute='_compute_nutrients', store=True)

    @api.depends('quantity', 'fertilizer_product_id.n_content', 'fertilizer_product_id.p_content', 'fertilizer_product_id.k_content')
    def _compute_nutrients(self):
        for batch in self:
            prod = batch.fertilizer_product_id
            if prod:
                batch.pure_n_qty = batch.quantity * (prod.n_content / 100.0)
                batch.pure_p_qty = batch.quantity * (prod.p_content / 100.0)
                batch.pure_k_qty = batch.quantity * (prod.k_content / 100.0)
            else:
                batch.pure_n_qty = batch.pure_p_qty = batch.pure_k_qty = 0.0

    notes = fields.Text("Notes")

    def action_convert_to_fertilizer(self):
        """ US-27-02: Convert manure to fertilizer via Manufacturing Order """
        self.ensure_one()
        if not self.fertilizer_product_id:
            raise UserError(_("Please select a Converted Fertilizer Product first!"))
        
        if not self.quality_check_id or self.quality_check_id.quality_state != 'pass':
            raise UserError(_("SAFETY BLOCK: A passed quality check (Compost Maturity) is required before conversion!"))
            
        # Create a Manufacturing Order (Intervention)
        mo = self.env['mrp.production'].create({
            'product_id': self.fertilizer_product_id.id,
            'product_qty': self.quantity,
            'product_uom_id': self.fertilizer_product_id.uom_id.id,
            'location_src_id': self.location_source_id.id,
            'location_dest_id': self.location_source_id.id,
            'intervention_type': 'fertilizing', # Or a custom 'conversion' type if defined
            'origin': self.batch_no,
        })
        
        # In a real scenario, we would also add the raw manure product to the MO
        # For this prototype, we'll mark it as confirmed
        mo.action_confirm()
        
        self.message_post(body=_("Manufacturing Order %s created for manure conversion.") % mo.name)
        
        return {
            'name': _('Conversion MO'),
            'type': 'ir.actions.act_window',
            'res_model': 'mrp.production',
            'res_id': mo.id,
            'view_mode': 'form',
            'target': 'current',
        }

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
