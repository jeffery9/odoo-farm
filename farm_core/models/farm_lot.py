from odoo import models, fields, api

class FarmLot(models.Model):
    _inherit = 'stock.lot'

    is_animal = fields.Boolean("Is Biological Asset", default=False)
    birth_date = fields.Date("Birth/Germination Date")
    gender = fields.Selection([
        ('male', 'Male (公)'),
        ('female', 'Female (母)'),
        ('other', 'Other (其他/无)')
    ], string="Gender")
    
    # 系谱跟踪 [US-32] 预留
    father_id = fields.Many2one('stock.lot', string="Father (父本)", domain="[('product_id', '=', product_id)]")
    mother_id = fields.Many2one('stock.lot', string="Mother (母本)", domain="[('product_id', '=', product_id)]")
    
    # 状态
    biological_stage = fields.Selection([
        ('newborn', 'Newborn/Seedling (幼龄)'),
        ('growing', 'Growing (生长)'),
        ('mature', 'Mature/Adult (成年)'),
        ('harvested', 'Harvested/Culled (已收获/淘汰)')
    ], string="Biological Stage", default='newborn')

    # 质量等级 [US-08]
    quality_grade = fields.Selection([
        ('grade_a', 'Grade A (特级/优等)'),
        ('grade_b', 'Grade B (一级/合格)'),
        ('grade_c', 'Grade C (二级/次品)'),
    ], string="Quality Grade")

    # 安全合规 [US-35]
    withdrawal_end_datetime = fields.Datetime("Safe to Harvest After", help="Withdrawal period end date.")
    is_safe_to_harvest = fields.Boolean("Is Safe to Harvest", compute='_compute_is_safe')
    withdrawal_days_left = fields.Integer("Withdrawal Countdown", compute='_compute_withdrawal_days')
    
    # 隔离管理 [US-34]
    state = fields.Selection([
        ('healthy', 'Healthy (正常)'),
        ('quarantine', 'Quarantined (隔离)'),
        ('disposed', 'Disposed (已处置)')
    ], string="Health State", default='healthy', tracking=True)

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

    # 动态属性 [US-02]
    lot_properties = fields.Properties(
        'Properties',
        definition='product_id.lot_properties_definition'
    )
