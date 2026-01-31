# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime, date, timedelta
import logging

_logger = logging.getLogger(__name__)


class AgriValuationBiologicalAsset(models.Model):
    """
    Consolidated Biological Asset Valuation [Refactored to Agri Domain]
    Combines fair value accounting with cost/depreciation accounting
    Refactored from farm.biological.asset.valuation with 100% logic retention.
    """
    _name = 'agri.valuation.biological.asset'
    _description = 'Consolidated Biological Asset Valuation'
    _order = 'asset_id, valuation_date desc'

    name = fields.Char("Valuation Reference", required=True, default=lambda self: _('New'))
    asset_id = fields.Many2one('agri.biological.asset', string="Biological Asset", required=True)
    valuation_date = fields.Date("Valuation Date", default=fields.Date.today, required=True)

    # Valuation Method Selection
    valuation_method = fields.Selection([
        ('market_price', 'Fair Value - Market Price'),
        ('cost_model', 'Cost Model'),
        ('hybrid', 'Hybrid Model')
    ], string="Valuation Method", default='market_price', required=True)

    # Growth Progress (for both methods)
    current_growth_progress = fields.Float("Current Growth Progress %",
                                          help="Current physiological progress as percentage (0-100)")
    target_yield = fields.Float("Target Yield",
                               help="Expected final yield at maturity")

    # Fair Value Specific Fields
    current_yield_potential = fields.Float("Current Yield Potential",
                                          compute='_compute_current_yield_potential',
                                          store=True,
                                          help="Current yield potential based on growth progress")
    market_price = fields.Float("Market Price (per unit)", digits=(12, 4),
                               compute='_compute_market_price',
                               store=True,
                               help="Current market price from external sources")
    market_price_source = fields.Char("Market Price Source",
                                     help="Source of the market price data")
    fair_value = fields.Float("Fair Value",
                             compute='_compute_fair_value',
                             store=True,
                             help="Calculated fair value = (current_yield_potential * market_price)")

    # Cost Model Specific Fields
    original_value = fields.Float(
        "Original Value",
        help="Original cost/value of the biological asset"
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
        compute='_compute_accumulated_depreciation',
        store=True
    )
    net_book_value = fields.Float(
        "Net Book Value",
        help="Current book value after depreciation",
        compute='_compute_net_book_value',
        store=True
    )

    # Revaluation fields (for fair value method)
    previous_valuation = fields.Float("Previous Valuation",
                                     help="Previous fair value for comparison")
    revaluation_amount = fields.Float("Revaluation Amount",
                                     compute='_compute_revaluation_amount',
                                     store=True,
                                     help="Difference between current and previous valuation")
    revaluation_type = fields.Selection([
        ('gain', 'Revaluation Gain'),
        ('loss', 'Revaluation Loss')
    ], string="Revaluation Type",
       compute='_compute_revaluation_type',
       store=True)

    # Growth Stage Coefficient (for both methods)
    growth_stage_coefficient = fields.Float(
        "Growth Stage Coefficient",
        help="Value coefficient based on biological growth stage",
        default=1.0
    )
    stage_coefficient_ids = fields.One2many(
        'agri.valuation.stage.coefficient',
        'valuation_id',
        string="Growth Stage Coefficients"
    )

    # Accounting Integration
    journal_entry_id = fields.Many2one('account.move', "Journal Entry",
                                     help="Link to created journal entry")
    is_accounting_entry_created = fields.Boolean("Accounting Entry Created",
                                                default=False)

    # OPE (Operational Performance Efficiency) Integration
    ope_score = fields.Float("OPE Score",
                            help="Operational Performance Efficiency score linked to valuation")
    efficiency_multiplier = fields.Float("Efficiency Multiplier", default=1.0,
                                        help="Multiplier based on asset efficiency metrics")

    # State
    state = fields.Selection([
        ('active', 'Active'),
        ('disposed', 'Disposed'),
        ('depreciated', 'Fully Depreciated'),
    ], string="Status", default='active')

    # --- 100% ORIGINAL LOGIC AND COMMENTS RESTORED ---

    @api.model_create_multi
    def create(self, vals_list):
        records = []
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                # Generate unique valuation reference
                asset = self.env['agri.biological.asset'].browse(vals.get('asset_id', False))
                date_str = vals.get('valuation_date', fields.Date.today()).strftime('%Y%m%d')
                vals['name'] = f"VAL-{asset.name or 'ASSET'}-{date_str}-{len(records)+1}"

            # Calculate growth progress if not provided
            if not vals.get('current_growth_progress') and vals.get('asset_id'):
                asset = self.env['agri.biological.asset'].browse(vals['asset_id'])
                vals['current_growth_progress'] = self._calculate_growth_progress(asset)

            record = super(AgriValuationBiologicalAsset, self).create(vals)
            records.append(record)

        return records[0] if len(records) == 1 else records

    @api.depends('asset_id', 'valuation_date', 'current_growth_progress', 'growth_stage_coefficient')
    def _compute_current_yield_potential(self):
        """Compute current yield potential based on growth progress"""
        for record in self:
            if record.asset_id and record.current_growth_progress and record.target_yield:
                record.current_yield_potential = record.target_yield * (record.current_growth_progress / 100.0)
            else:
                # Calculate based on biological asset growth stage if no explicit target
                if record.asset_id:
                    stage_multipliers = {
                        'newborn': 0.1,  # 10% of target
                        'growing': 0.5,  # 50% of target
                        'mature': 1.0,   # 100% of target
                        'harvested': 0.0
                    }
                    multiplier = stage_multipliers.get(record.asset_id.growth_stage, 0.5)

                    # Calculate target yield from product info or default
                    if record.asset_id.lot_id and record.asset_id.lot_id.product_id:
                        product = record.asset_id.lot_id.product_id
                        if hasattr(product, 'expected_yield_per_unit') and product.expected_yield_per_unit:
                            target = product.expected_yield_per_unit
                        else:
                            target = 1000.0  # Default target
                    else:
                        target = 1000.0  # Default target

                    record.current_yield_potential = target * multiplier * (record.current_growth_progress / 100.0) if record.current_growth_progress else target * multiplier
                else:
                    record.current_yield_potential = 0.0

    @api.depends('asset_id', 'valuation_date')
    def _compute_market_price(self):
        """Compute market price from external sources"""
        for record in self:
            # Try to get market price from existing farm_valuation module
            market_price_model = self.env['farm.market.price']
            if market_price_model:
                price = market_price_model.search([
                    ('product_id', '=', record.asset_id.lot_id.product_id.id if record.asset_id.lot_id.product_id else False),
                    ('date', '<=', record.valuation_date)
                ], order='date desc', limit=1)
                record.market_price = price.price if price else 0.0
                record.market_price_source = price.source if price else "Internal Estimate"
            else:
                record.market_price = 0.0
                record.market_price_source = "No Product Data"

    @api.depends('current_yield_potential', 'market_price', 'efficiency_multiplier', 'valuation_method')
    def _compute_fair_value(self):
        """Compute fair value: Value = Current Yield Potential * Market Price * Efficiency"""
        for record in self:
            if record.valuation_method == 'market_price':
                record.fair_value = record.current_yield_potential * record.market_price * record.efficiency_multiplier
            else:
                # For cost model, fair value is based on book value
                record.fair_value = record.net_book_value

    @api.depends('original_value', 'depreciation_years', 'annual_depreciation_rate')
    def _compute_accumulated_depreciation(self):
        """Calculate accumulated depreciation based on time passed and depreciation rate"""
        for record in self:
            if record.depreciation_years > 0:
                # Calculate based on the asset's life span and current age
                if record.asset_id and record.asset_id.birth_date:
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

    @api.depends('original_value', 'accumulated_depreciation', 'growth_stage_coefficient')
    def _compute_net_book_value(self):
        """Calculate net book value after depreciation"""
        for record in self:
            base_book_value = record.original_value - record.accumulated_depreciation
            # Apply growth stage coefficient
            record.net_book_value = base_book_value * record.growth_stage_coefficient

    @api.depends('fair_value', 'previous_valuation')
    def _compute_revaluation_amount(self):
        """Compute revaluation amount as difference from previous valuation"""
        for record in self:
            record.revaluation_amount = record.fair_value - record.previous_valuation

    @api.depends('revaluation_amount')
    def _compute_revaluation_type(self):
        """Determine if revaluation is gain or loss"""
        for record in self:
            if record.revaluation_amount > 0:
                record.revaluation_type = 'gain'
            elif record.revaluation_amount < 0:
                record.revaluation_type = 'loss'
            else:
                record.revaluation_type = False  # No change

    def _calculate_growth_progress(self, asset):
        """Calculate growth progress percentage for an asset"""
        if not asset.birth_date:
            return 0.0

        # Estimate progress based on time since birth vs expected maturity
        if asset.maturity_date:
            birth_date = fields.Date.from_string(asset.birth_date)
            maturity_date = fields.Date.from_string(asset.maturity_date) if asset.maturity_date else fields.Date.today()

            if maturity_date > birth_date:
                total_days = (maturity_date - birth_date).days
                if total_days > 0:
                    current_days = (fields.Date.today() - birth_date).days
                    progress = min(100.0, (current_days / total_days) * 100.0)
                    return progress
            else:
                return 100.0  # Already past maturity
        else:
            # If no maturity date, estimate based on growth stage
            stage_progress = {
                'newborn': 25.0,
                'growing': 60.0,
                'mature': 100.0,
                'harvested': 0.0
            }
            return stage_progress.get(asset.growth_stage, 50.0)

    def action_create_revaluation_entry(self):
        """
        Create accounting entry for revaluation of biological assets
        Handles both fair value and cost model revaluations
        """
        account_move = self.env['account.move']
        account_obj = self.env['account.account']
        journal_obj = self.env['account.journal']

        for record in self:
            if record.is_accounting_entry_created:
                continue  # Skip if entry already created

            if abs(record.revaluation_amount) < 0.01:  # Skip if negligible
                continue

            # Get required accounts
            bio_asset_account = account_obj.search([
                ('code', '=like', '1611%'),  # Biological Assets account (Chinese standards)
                ('company_id', '=', self.env.company.id)
            ], limit=1)

            if not bio_asset_account:
                # Try alternative account codes
                bio_asset_account = account_obj.search([
                    ('name', 'ilike', 'biological asset'),
                    ('company_id', '=', self.env.company.id)
                ], limit=1)

            if not bio_asset_account:
                bio_asset_account = account_obj.search([
                    ('company_id', '=', self.env.company.id)
                ], limit=1)  # Fallback to first available account

            # Revaluation reserve account
            reval_reserve_account = account_obj.search([
                ('code', '=like', '4801%'),  # Revaluation Reserve
                ('company_id', '=', self.env.company.id)
            ], limit=1)

            if not reval_reserve_account:
                # Try to find asset revaluation account
                reval_reserve_account = account_obj.search([
                    ('name', 'ilike', 'revaluation reserve'),
                    ('company_id', '=', self.env.company.id)
                ], limit=1)

            if not bio_asset_account or not reval_reserve_account:
                _logger.warning(f"Cannot create revaluation entry for {record.name}: required accounts not found")
                continue

            # Determine journal
            journal = journal_obj.search([
                ('type', '=', 'general'),
                ('company_id', '=', self.env.company.id)
            ], limit=1)

            if not journal:
                _logger.warning(f"Cannot create revaluation entry for {record.name}: no general journal found")
                continue

            # Create journal entry based on valuation method
            if record.valuation_method == 'market_price':
                # Fair value revaluation - gain or loss
                debit_account = bio_asset_account if record.revaluation_amount > 0 else reval_reserve_account
                credit_account = reval_reserve_account if record.revaluation_amount > 0 else bio_asset_account

                move_vals = {
                    'journal_id': journal.id,
                    'date': record.valuation_date,
                    'ref': f'Biological Asset Revaluation - {record.asset_id.name}',
                    'line_ids': [
                        (0, 0, {
                            'account_id': debit_account.id,
                            'name': f'Revaluation of {record.asset_id.name} - {record.name}',
                            'debit': abs(record.revaluation_amount) if record.revaluation_amount > 0 else 0,
                            'credit': 0,
                            'partner_id': self.env.company.partner_id.id,
                        }),
                        (0, 0, {
                            'account_id': credit_account.id,
                            'name': f'Revaluation of {record.asset_id.name} - {record.name}',
                            'debit': 0,
                            'credit': abs(record.revaluation_amount) if record.revaluation_amount < 0 else 0,
                            'partner_id': self.env.company.partner_id.id,
                        })
                    ]
                }
            else:
                # Cost model depreciation
                depreciation_account = account_obj.search([
                    ('name', 'ilike', 'depreciation'),
                    ('company_id', '=', self.env.company.id)
                ], limit=1)

                if not depreciation_account:
                    # Create or find accumulated depreciation account
                    depreciation_account = account_obj.search([
                        ('code', '=like', '1603%'),  # Accumulated depreciation
                        ('company_id', '=', self.env.company.id)
                    ], limit=1)

                if not depreciation_account:
                    _logger.warning(f"Cannot create depreciation entry for {record.name}: depreciation account not found")
                    continue

                move_vals = {
                    'journal_id': journal.id,
                    'date': record.valuation_date,
                    'ref': f'Biological Asset Depreciation - {record.asset_id.name}',
                    'line_ids': [
                        (0, 0, {
                            'account_id': depreciation_account.id,
                            'name': f'Depreciation for {record.asset_id.name}',
                            'debit': abs(record.revaluation_amount),
                            'credit': 0,
                        }),
                        (0, 0, {
                            'account_id': bio_asset_account.id,
                            'name': f'Depreciation for {record.asset_id.name}',
                            'debit': 0,
                            'credit': abs(record.revaluation_amount),
                        })
                    ]
                }

            move = account_move.create(move_vals)
            record.journal_entry_id = move.id
            record.is_accounting_entry_created = True

            # Post the entry
            try:
                move.action_post()
            except Exception as e:
                _logger.error(f"Error posting revaluation entry for {record.name}: {e}")
                # Still mark as created but note the error
                record.message_post(body=f"Revaluation entry created but failed to post: {e}")

            # Add message to the biological asset
            record.asset_id.message_post(body=_(
                "REVALUATION ENTRY: Asset revalued from %s to %s (change: %s). "
                "Journal entry %s created for %s %s."
            ) % (
                record.previous_valuation,
                record.fair_value,
                record.revaluation_amount,
                move.name or 'N/A',
                abs(record.revaluation_amount),
                'Gain' if record.revaluation_amount > 0 else 'Loss'
            ))

    def _cron_run_monthly_revaluation(self):
        """
        Scheduled job to run monthly biological asset revaluations
        """
        _logger.info("Starting monthly biological asset revaluation")

        # Get all active biological assets
        assets = self.env['agri.biological.asset'].search([
            ('growth_stage', 'in', ['growing', 'mature'])
        ])

        for asset in assets:
            # Create a new fair valuation record for each asset
            current_valuation = self.create({
                'asset_id': asset.id,
                'valuation_date': fields.Date.today(),
                'valuation_method': 'market_price',
            })

            # Update previous valuation for next calculation
            if hasattr(asset, 'current_valuation') and asset.current_valuation:
                current_valuation.previous_valuation = asset.current_valuation

            # Create accounting entry if significant change
            if abs(current_valuation.revaluation_amount) > 1.0:  # Only if change > 1
                current_valuation.action_create_revaluation_entry()

        _logger.info("Monthly biological asset revaluation completed")


class AgriValuationStageCoefficient(models.Model):
    """
    Growth stage coefficient configuration for valuation [Refactored to Agri Domain]
    """
    _name = 'agri.valuation.stage.coefficient'
    _description = 'Biological Asset Valuation Stage Coefficient'

    valuation_id = fields.Many2one(
        'agri.valuation.biological.asset',
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


class BiologicalAssetExtension(models.Model):
    """Extension to biological asset model to include consolidated valuation integration"""
    _inherit = 'agri.biological.asset'

    # Fair value and cost accounting fields
    current_fair_value = fields.Float("Current Fair Value",
                                     compute='_compute_current_fair_value',
                                     store=True,
                                     help="Current fair value based on market conditions")
    current_net_book_value = fields.Float("Current Net Book Value",
                                         compute='_compute_current_net_book_value',
                                         store=True,
                                         help="Current net book value after depreciation")
    fair_value_date = fields.Date("Fair Value Date",
                                 compute='_compute_current_fair_value',
                                 store=True,
                                 help="Date of last fair value calculation")

    # One2many field to consolidated valuations
    valuation_ids = fields.One2many('agri.valuation.biological.asset', 'asset_id', string="Asset Valuations")

    # Integration with OPE metrics (Operational Performance Efficiency)
    ope_integration = fields.Float("OPE Integration Score",
                                  help="Integration with OPE metrics for valuation")

    @api.depends('valuation_ids.fair_value')
    def _compute_current_fair_value(self):
        """Compute current fair value based on latest fair valuation"""
        for asset in self:
            latest_fair_val = self.env['agri.valuation.biological.asset'].search([
                ('asset_id', '=', asset.id),
                ('valuation_method', '=', 'market_price')
            ], order='valuation_date desc', limit=1)

            asset.current_fair_value = latest_fair_val.fair_value if latest_fair_val else 0.0
            asset.fair_value_date = latest_fair_val.valuation_date if latest_fair_val else False

    @api.depends('valuation_ids.net_book_value')
    def _compute_current_net_book_value(self):
        """Compute current net book value based on latest cost model valuation"""
        for asset in self:
            latest_net_book_val = self.env['agri.valuation.biological.asset'].search([
                ('asset_id', '=', asset.id)
            ], order='valuation_date desc', limit=1)

            asset.current_net_book_value = latest_net_book_val.net_book_value if latest_net_book_val else 0.0

    def action_run_fair_valuation(self):
        """Manual action to run fair valuation for selected assets"""
        for asset in self:
            # Create a new fair valuation with market price method
            self.env['agri.valuation.biological.asset'].create({
                'asset_id': asset.id,
                'valuation_date': fields.Date.today(),
                'valuation_method': 'market_price',
            })

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Fair Valuation'),
                'message': _('Fair valuation process initiated for selected assets'),
                'type': 'success',
                'sticky': False,
            }
        }

    def action_run_cost_valuation(self):
        """Manual action to run cost-based valuation for selected assets"""
        for asset in self:
            # Create a new cost valuation
            self.env['agri.valuation.biological.asset'].create({
                'asset_id': asset.id,
                'valuation_date': fields.Date.today(),
                'valuation_method': 'cost_model',
                'original_value': asset.lot_id.product_id.standard_price if asset.lot_id.product_id else 0.0,
            })

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Cost Valuation'),
                'message': _('Cost-based valuation process initiated for selected assets'),
                'type': 'success',
                'sticky': False,
            }
        }