from odoo import models, fields, api, _
from odoo.exceptions import UserError
from .base_mixins import ComplianceMixin
from .common_fields import CommonAgriculturalFields
import logging

_logger = logging.getLogger(__name__)


class BiologicalAsset(models.Model):
    """
    Biological Asset Management - replacing the functionality from farm_lot.py
    US-01-04: Biological Asset Management
    US-01-07: Biological Asset Valuation
    """
    _name = 'farm.biological.asset'
    _description = 'Biological Asset'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'farm.core.creation.method.mixin', 'farm.core.computed.field.mixin', 'farm.core.compliance.mixin']

    name = fields.Char("Asset Name", required=True, default=lambda self: _('New'))
    lot_id = fields.Many2one('stock.lot', string="Stock Lot", required=True)

    # Inherit common agricultural fields
    agricultural_type = fields.Selection([
        ('animal', 'Animal'),
        ('plant', 'Plant'),
        ('tree', 'Tree'),
    ], string="Asset Type", default='animal')

    birth_date = fields.Date("Birth/Germination Date")
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string="Gender")

    # Parent tracking (pedigree)
    father_id = fields.Many2one('farm.biological.asset', string="Father")
    mother_id = fields.Many2one('farm.biological.asset', string="Mother")

    # Growth and maturity
    growth_stage = fields.Selection([
        ('newborn', 'Newborn/Seedling'),
        ('growing', 'Growing'),
        ('mature', 'Mature/Adult'),
        ('harvested', 'Harvested/Culled')
    ], string="Growth Stage", default='newborn', required=True)

    is_mature = fields.Boolean("Is Mature", compute='_compute_is_mature_from_age', store=True)

    # Generation tracking
    generation = fields.Selection([
        ('g0', 'G0 (Breeder)'),
        ('g1', 'G1 (Foundation)'),
        ('g2', 'G2 (Registered)'),
        ('g3', 'G3 (Commercial)')
    ], string="Generation")

    # Quality and grade
    quality_grade = fields.Selection([
        ('grade_a', 'Grade A'),
        ('grade_b', 'Grade B'),
        ('grade_c', 'Grade C'),
    ], string="Quality Grade")

    # Valuation integration
    valuation_ids = fields.One2many('farm.biological.asset.valuation', 'asset_id', string="Asset Valuations")
    current_valuation = fields.Float("Current Valuation", compute='_compute_current_valuation', store=True)

    maturity_date = fields.Date("Maturity Date", compute='_compute_maturity_date', store=True)

    @api.depends('birth_date', 'lot_id.product_id.maturity_age_days')
    def _compute_maturity_date(self):
        """Compute maturity date based on birth date and product maturity age"""
        for asset in self:
            if asset.birth_date and asset.lot_id.product_id.maturity_age_days:
                from datetime import timedelta
                asset.maturity_date = asset.birth_date + timedelta(days=asset.lot_id.product_id.maturity_age_days)
            else:
                asset.maturity_date = False

    @api.depends('birth_date', 'lot_id.product_id.maturity_age_days', 'maturity_date')
    def _compute_is_mature_from_age(self):
        """Compute if asset is mature based on actual dates"""
        from datetime import date
        today = date.today()
        for asset in self:
            asset.is_mature = (asset.maturity_date and asset.maturity_date <= today) or False

    @api.depends('valuation_ids.net_book_value')
    def _compute_current_valuation(self):
        """Compute current valuation from active valuation records"""
        for asset in self:
            active_valuation = asset.valuation_ids.filtered(lambda v: v.state == 'active')
            if active_valuation:
                asset.current_valuation = active_valuation[0].net_book_value
            else:
                # Default valuation based on growth stage if no active valuation
                stage_multipliers = {
                    'newborn': 0.2,
                    'growing': 0.6,
                    'mature': 1.0,
                    'harvested': 0.0
                }
                multiplier = stage_multipliers.get(asset.growth_stage, 1.0)
                base_value = asset.lot_id.product_id.standard_price or 0.0
                asset.current_valuation = base_value * multiplier

    def _cron_check_maturity_and_transfer_asset(self):
        """
        Check biological assets for maturity and execute cost transfer
        """
        today = fields.Date.today()
        assets_due_maturity = self.search([
            ('lot_id.is_animal', '=', True),
            ('lot_id.product_id.is_biological_asset', '=', True),
            ('lot_id.product_id.maturity_age_days', '>', 0),
            ('maturity_date', '<=', today),
            ('growth_stage', '!=', 'mature')
        ])

        for asset in assets_due_maturity:
            asset._process_maturity_transfer()

    def _process_maturity_transfer(self):
        """
        Process cost transfer when biological asset reaches maturity
        """
        self.ensure_one()
        if not self.lot_id.product_id.is_biological_asset or not self.is_mature:
            return

        # Check for WIP costs to transfer
        if hasattr(self, 'analytic_account_id'):
            analytic_lines = self.env['account.analytic.line'].search([
                ('account_id', '=', self.analytic_account_id.id),
                ('stock_lot_id', '=', self.lot_id.id)  # Adjust field name as needed
            ])

            total_wip_cost = abs(sum(analytic_lines.mapped('amount')))

            if total_wip_cost > 0:
                # Create journal entry to transfer WIP costs to fixed assets
                asset_account = self.env['account.account'].search([
                    ('code', '=like', '1602%'),  # Fixed assets account
                    ('company_id', '=', self.company_id.id)
                ], limit=1)

                wip_account = self.env['account.account'].search([
                    ('code', '=like', '1603%'),  # Consumable biological assets account
                    ('company_id', '=', self.company_id.id)
                ], limit=1)

                if asset_account and wip_account:
                    journal = self.env['account.journal'].search([
                        ('type', '=', 'general'),
                        ('company_id', '=', self.company_id.id)
                    ], limit=1)

                    if journal:
                        move_vals = {
                            'journal_id': journal.id,
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

                        # Update growth stage
                        self.growth_stage = 'mature'

                        # Create valuation record
                        self.env['farm.biological.asset.valuation'].create({
                            'asset_id': self.id,
                            'original_value': total_wip_cost,
                            'depreciation_years': max(5.0, self.lot_id.product_id.maturity_age_days / 365.0 * 2 if self.lot_id.product_id.maturity_age_days else 10.0),
                            'annual_depreciation_rate': 10.0,
                            'growth_stage_coefficient': 1.0,
                            'state': 'active'
                        })

                        # Log the transfer
                        self.message_post(body=_(
                            "BIOLOGICAL ASSET MATURITY: WIP costs of %s transferred to fixed asset account. "
                            "Asset is now mature and ready for production use."
                        ) % total_wip_cost)


class BiologicalAssetValuation(models.Model):
    """
    US-01-07: Biological Asset Valuation and Depreciation
    """
    _name = 'farm.biological.asset.valuation'
    _description = 'Biological Asset Valuation and Depreciation'
    _order = 'create_date desc'

    asset_id = fields.Many2one(
        'farm.biological.asset',
        string="Biological Asset",
        required=True
    )

    original_value = fields.Float(
        "Original Value",
        help="Original cost/value of the biological asset",
        required=True
    )

    growth_stage_coefficient = fields.Float(
        "Growth Stage Coefficient",
        help="Value coefficient based on biological growth stage",
        default=1.0
    )

    depreciation_years = fields.Float(
        "Depreciation Years",
        help="Number of years over which the asset is depreciated",
        default=10.0
    )

    annual_depreciation_rate = fields.Float(
        "Annual Depreciation Rate (%)",
        help="Annual depreciation percentage",
        default=10.0
    )

    accumulated_depreciation = fields.Float(
        "Accumulated Depreciation",
        help="Total depreciation accumulated so far",
        compute='_compute_accumulated_depreciation',
        store=True
    )

    net_book_value = fields.Float(
        "Net Book Value",
        help="Current book value after depreciation",
        compute='_compute_net_book_value',
        store=True
    )

    stage_coefficient_ids = fields.One2many(
        'farm.biological.asset.stage.coefficient',
        'valuation_id',
        string="Growth Stage Coefficients"
    )

    state = fields.Selection([
        ('active', 'Active'),
        ('disposed', 'Disposed'),
        ('depreciated', 'Fully Depreciated'),
    ], string="Status", default='active')

    def action_create_depreciation_entry(self):
        """Create depreciation journal entry for the biological asset"""
        for record in self:
            if not record.asset_id or not record.original_value:
                continue

            # Calculate current period depreciation
            depreciation_amount = record.original_value * (record.annual_depreciation_rate / 100)

            # Ensure we don't depreciate more than the original value
            if record.accumulated_depreciation + depreciation_amount > record.original_value:
                depreciation_amount = record.original_value - record.accumulated_depreciation

            if depreciation_amount <= 0:
                continue

            # Create journal entry
            journal = self.env['account.journal'].search([
                ('type', '=', 'general'),
                ('company_id', '=', self.env.company.id)
            ], limit=1)

            if not journal:
                raise UserError(_("No general journal found for depreciation entries."))

            asset_account = self.env['account.account'].search([
                ('code', '=like', '1602%'),  # Fixed assets account
                ('company_id', '=', self.env.company.id)
            ], limit=1)

            depreciation_account = self.env['account.account'].search([
                ('code', '=like', '1602%'),  # Or separate accumulated depreciation account
                ('company_id', '=', self.env.company.id)
            ], limit=1)

            if not asset_account or not depreciation_account:
                raise UserError(_("Required asset accounts not found for depreciation."))

            move_vals = {
                'journal_id': journal.id,
                'date': fields.Date.today(),
                'ref': f'Biological Asset Depreciation - {record.asset_id.name}',
                'line_ids': [
                    (0, 0, {
                        'account_id': depreciation_account.id,
                        'name': f'Depreciation for {record.asset_id.name}',
                        'debit': depreciation_amount,
                        'credit': 0,
                    }),
                    (0, 0, {
                        'account_id': asset_account.id,
                        'name': f'Depreciation for {record.asset_id.name}',
                        'debit': 0,
                        'credit': depreciation_amount,
                    })
                ]
            }

            move = self.env['account.move'].create(move_vals)

            # Update accumulated depreciation
            record.accumulated_depreciation += depreciation_amount

            # Log the depreciation
            record.asset_id.message_post(body=_(
                "DEPRECIATION ENTRY: Amount %s depreciated for biological asset %s. "
                "Accumulated depreciation: %s, Net book value: %s"
            ) % (depreciation_amount, record.asset_id.name,
                 record.accumulated_depreciation, record.net_book_value))

            # Check if fully depreciated
            if record.accumulated_depreciation >= record.original_value:
                record.state = 'depreciated'

        return True

    @api.depends('original_value', 'depreciation_years', 'annual_depreciation_rate')
    def _compute_accumulated_depreciation(self):
        """Calculate accumulated depreciation based on time passed and depreciation rate"""
        for record in self:
            if record.depreciation_years > 0:
                # Calculate based on the asset's life span and current age
                if record.asset_id and record.asset_id.birth_date:
                    from datetime import date
                    today = date.today()
                    birth_date = fields.Date.from_string(record.asset_id.birth_date)

                    if birth_date:
                        days_old = (today - birth_date).days
                        years_old = days_old / 365.0

                        # Calculate depreciation based on age and rate
                        depreciation_rate = record.annual_depreciation_rate / 100.0
                        record.accumulated_depreciation = min(
                            record.original_value,  # Never exceed original value
                            record.original_value * depreciation_rate * years_old
                        )
                    else:
                        record.accumulated_depreciation = 0.0
                else:
                    record.accumulated_depreciation = 0.0
            else:
                record.accumulated_depreciation = 0.0

    @api.depends('original_value', 'accumulated_depreciation')
    def _compute_net_book_value(self):
        """Calculate net book value after depreciation"""
        for record in self:
            record.net_book_value = record.original_value - record.accumulated_depreciation

    @api.onchange('asset_id')
    def _onchange_asset_id(self):
        """Auto-populate valuation parameters based on product settings"""
        if self.asset_id and self.asset_id.lot_id.product_id:
            product = self.asset_id.lot_id.product_id
            if product.is_biological_asset:
                # Set default depreciation years based on product maturity
                if product.maturity_age_days:
                    self.depreciation_years = max(5.0, product.maturity_age_days / 365.0 * 2)  # 2x maturity time as depreciation period
                    self.annual_depreciation_rate = 100.0 / self.depreciation_years if self.depreciation_years > 0 else 10.0


class BiologicalAssetStageCoefficient(models.Model):
    """
    US-01-07: Growth stage coefficient configuration
    """
    _name = 'farm.biological.asset.stage.coefficient'
    _description = 'Biological Asset Stage Coefficient'

    valuation_id = fields.Many2one(
        'farm.biological.asset.valuation',
        string="Valuation Record",
        required=True,
        ondelete='cascade'
    )

    biological_stage = fields.Selection([
        ('newborn', 'Newborn/Seedling'),
        ('growing', 'Growing'),
        ('mature', 'Mature/Adult'),
        ('harvested', 'Harvested/Culled')
    ], string="Biological Stage", required=True)

    coefficient = fields.Float(
        "Value Coefficient",
        help="Multiplier for asset value based on growth stage",
        default=1.0
    )

    description = fields.Char("Description")

    @api.onchange('biological_stage')
    def _onchange_biological_stage(self):
        """Set default coefficient based on growth stage"""
        if self.biological_stage == 'newborn':
            self.coefficient = 0.2  # Newborn assets valued at 20% of mature value
        elif self.biological_stage == 'growing':
            self.coefficient = 0.6  # Growing assets valued at 60% of mature value
        elif self.biological_stage == 'mature':
            self.coefficient = 1.0  # Mature assets at full value
        elif self.biological_stage == 'harvested':
            self.coefficient = 0.0  # Harvested assets have no continuing value