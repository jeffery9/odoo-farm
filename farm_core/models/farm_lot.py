from odoo import models, fields, api, _

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

    # 生物资产成熟状态 [US-01-06]
    is_mature = fields.Boolean("Is Mature", compute='_compute_is_mature', store=True)
    maturity_date = fields.Date("Maturity Date", compute='_compute_maturity_date', store=True)

    @api.depends('birth_date', 'product_id.maturity_age_days')
    def _compute_maturity_date(self):
        for lot in self:
            if lot.birth_date and lot.product_id.maturity_age_days:
                from datetime import timedelta
                lot.maturity_date = lot.birth_date + timedelta(days=lot.product_id.maturity_age_days)
            else:
                lot.maturity_date = False

    @api.depends('birth_date', 'product_id.maturity_age_days', 'maturity_date')
    def _compute_is_mature(self):
        from datetime import date
        today = date.today()
        for lot in self:
            lot.is_mature = (lot.maturity_date and lot.maturity_date <= today) or False

    # 生物资产转固核算 [US-01-06]
    @api.model
    def _cron_check_maturity_and_transfer_asset(self):
        """
        检查生物资产成熟度并执行成本结转
        """
        today = fields.Date.today()
        lots_due_maturity = self.search([
            ('is_animal', '=', True),
            ('product_id.is_biological_asset', '=', True),
            ('product_id.maturity_age_days', '>', 0),
            ('maturity_date', '<=', today),
            ('biological_stage', '!=', 'mature')
        ])

        for lot in lots_due_maturity:
            lot._process_maturity_transfer()

    def _process_maturity_transfer(self):
        """
        处理生物资产成熟时的成本结转逻辑 [US-01-06]
        """
        self.ensure_one()
        if not self.product_id.is_biological_asset or not self.is_mature:
            return

        # 检查是否有成本需要结转
        if hasattr(self, 'analytic_account_id'):
            # 查找与该资产相关的WIP成本
            analytic_lines = self.env['account.analytic.line'].search([
                ('account_id', '=', self.analytic_account_id.id),
                ('lot_id', '=', self.id)
            ])

            total_wip_cost = abs(sum(analytic_lines.mapped('amount')))

            if total_wip_cost > 0:
                # 创建会计分录，将WIP成本结转到固定资产
                asset_account = self.env['account.account'].search([
                    ('code', '=like', '1602%'),  # 固定资产科目
                    ('company_id', '=', self.company_id.id)
                ], limit=1)

                wip_account = self.env['account.account'].search([
                    ('code', '=like', '1603%'),  # 消耗性生物资产科目
                    ('company_id', '=', self.company_id.id)
                ], limit=1)

                if asset_account and wip_account:
                    move_vals = {
                        'journal_id': self.env['account.journal'].search([
                            ('type', '=', 'general'),
                            ('company_id', '=', self.company_id.id)
                        ], limit=1).id,
                        'date': fields.Date.today(),
                        'ref': f'Biological Asset Maturity Transfer - {self.name}',
                        'line_ids': [
                            (0, 0, {
                                'account_id': asset_account.id,
                                'name': f'Maturity transfer for {self.name}',
                                'debit': total_wip_cost,
                                'credit': 0,
                            }),
                            (0, 0, {
                                'account_id': wip_account.id,
                                'name': f'Maturity transfer for {self.name}',
                                'debit': 0,
                                'credit': total_wip_cost,
                            })
                        ]
                    }
                    move = self.env['account.move'].create(move_vals)

                    # 记录审计日志
                    self.message_post(body=_(
                        "BIOLOGICAL ASSET MATURITY: WIP costs of %s transferred to fixed asset account. "
                        "Asset is now mature and ready for production use."
                    ) % total_wip_cost)

                    # 更新生物阶段状态
                    self.biological_stage = 'mature'

    @api.onchange('product_id')
    def _onchange_product_id_generation(self):
        if self.product_id and self.product_id.agri_generation:
            self.agri_generation = self.product_id.agri_generation
