from odoo import models, fields, api

class FarmLot(models.Model):
    _inherit = 'stock.lot'

    is_animal = fields.Boolean("Is Biological Asset", default=False)
    birth_date = fields.Date("Birth/Germination Date")
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string="Gender")
    
    # 系谱跟踪 [US-10-02] 预留
    father_id = fields.Many2one('stock.lot', string="Father", domain="[('product_id', '=', product_id)]")
    mother_id = fields.Many2one('stock.lot', string="Mother", domain="[('product_id', '=', product_id)]")
    
    # 状态
    biological_stage = fields.Selection([
        ('newborn', 'Newborn/Seedling'),
        ('growing', 'Growing'),
        ('mature', 'Mature/Adult'),
        ('harvested', 'Harvested/Culled')
    ], string="Biological Stage", default='newborn')

    # 质量等级 [US-02-04]
    quality_grade = fields.Selection([
        ('grade_a', 'Grade A'),
        ('grade_b', 'Grade B'),
        ('grade_c', 'Grade C'),
    ], string="Quality Grade")

    # 安全合规 [US-11-03]
    withdrawal_end_datetime = fields.Datetime("Safe to Harvest After", help="Withdrawal period end date.")
    is_safe_to_harvest = fields.Boolean("Is Safe to Harvest", compute='_compute_is_safe')
    withdrawal_days_left = fields.Integer("Withdrawal Countdown", compute='_compute_withdrawal_days')
    
    # 隔离管理 [US-11-02]
    state = fields.Selection([
        ('healthy', 'Healthy'),
        ('quarantine', 'Quarantined'),
        ('disposed', 'Disposed'),
        ('locked', 'Quality Locked')
    ], string="Health State", default='healthy', tracking=True)

    @api.depends('quality_status')
    def _onchange_quality_status(self):
        for lot in self:
            if lot.quality_status == 'failed':
                lot.state = 'locked'

    @api.depends('withdrawal_end_datetime')
    def _compute_is_safe(self):
        now = fields.Datetime.now()
        for lot in self:
            lot.is_safe_to_harvest = not lot.withdrawal_end_datetime or lot.withdrawal_end_datetime <= now

    @api.depends('withdrawal_end_datetime')
    def _compute_withdrawal_days(self):
        now = fields.Datetime.now()
        for lot in self:
            if lot.withdrawal_end_datetime and lot.withdrawal_end_datetime > now:
                delta = lot.withdrawal_end_datetime - now
                lot.withdrawal_days_left = delta.days + 1
            else:
                lot.withdrawal_days_left = 0

    # 动态属性 [US-01-02]
    lot_properties = fields.Properties(
        'Properties',
        definition='product_id.lot_properties_definition'
    )

    # 繁育代次追踪 (G0-G3) [US-01-05]
    agri_generation = fields.Selection([
        ('g0', 'G0 (Breeder Seed/Original)'),
        ('g1', 'G1 (Foundation Seed)'),
        ('g2', 'G2 (Registered Seed)'),
        ('g3', 'G3 (Certified/Commercial Seed)')
    ], string="Agri Generation", help="Generation tracking for this specific lot.", default='g3')

    @api.onchange('product_id')
    def _onchange_product_id_generation(self):
        if self.product_id and self.product_id.agri_generation:
            self.agri_generation = self.product_id.agri_generation
