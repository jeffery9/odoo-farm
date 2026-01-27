from odoo import models, fields, api, _
from datetime import datetime, timedelta
import logging

_logger = logging.getLogger(__name__)


class BiologicalAssetFairValuation(models.Model):
    """
    Biological Asset Fair Value Real-time Accounting
    US-17-11: Biological Asset Fair Value Real-time Accounting
    """
    _name = 'farm.biological.asset.fair.valuation'
    _description = 'Biological Asset Fair Value Valuation'
    _order = 'asset_id, valuation_date desc'

    name = fields.Char("Valuation Reference", required=True, default=lambda self: _('New'))
    asset_id = fields.Many2one('farm.biological.asset', string="Biological Asset", required=True)
    valuation_date = fields.Date("Valuation Date", default=fields.Date.today, required=True)

    # Growth Progress
    current_growth_progress = fields.Float("Current Growth Progress %", help="Current physiological progress as percentage (0-100)")
    target_yield = fields.Float("Target Yield", help="Expected final yield at maturity")
    current_yield_potential = fields.Float("Current Yield Potential",
                                          compute='_compute_current_yield_potential',
                                          store=True,
                                          help="Current yield potential based on growth progress")

    # Market Price Integration
    market_price = fields.Float("Market Price (per unit)", digits=(12, 4),
                               compute='_compute_market_price',
                               store=True,
                               help="Current market price from external sources")
    market_price_source = fields.Char("Market Price Source", help="Source of the market price data")

    # Fair Value Calculation
    fair_value = fields.Float("Fair Value",
                             compute='_compute_fair_value',
                             store=True,
                             help="Calculated fair value = (current_yield_potential * market_price)")
    valuation_method = fields.Selection([
        ('market_price', 'Market Price'),
        ('cost_model', 'Cost Model'),
        ('hybrid', 'Hybrid Model')
    ], string="Valuation Method", default='market_price')

    # Revaluation
    previous_valuation = fields.Float("Previous Valuation", help="Previous fair value for comparison")
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

    # Accounting Integration
    journal_entry_id = fields.Many2one('account.move', "Journal Entry", help="Link to created journal entry")
    is_accounting_entry_created = fields.Boolean("Accounting Entry Created", default=False)

    # OPE (Operational Performance Efficiency) Integration
    ope_score = fields.Float("OPE Score", help="Operational Performance Efficiency score linked to valuation")
    efficiency_multiplier = fields.Float("Efficiency Multiplier", default=1.0,
                                        help="Multiplier based on asset efficiency metrics")

    @api.model_create_multi
    def create(self, vals_list):
        records = []
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                # Generate unique valuation reference
                asset = self.env['farm.biological.asset'].browse(vals.get('asset_id', False))
                date_str = vals.get('valuation_date', fields.Date.today()).strftime('%Y%m%d')
                vals['name'] = f"VAL-{asset.name or 'ASSET'}-{date_str}-{len(records)+1}"

            # Calculate growth progress if not provided
            if not vals.get('current_growth_progress') and vals.get('asset_id'):
                asset = self.env['farm.biological.asset'].browse(vals['asset_id'])
                vals['current_growth_progress'] = self._calculate_growth_progress(asset)

            record = super().create(vals)
            records.append(record)

        return records[0] if len(records) == 1 else records

    @api.depends('asset_id', 'valuation_date')
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
            if record.asset_id and record.asset_id.lot_id and record.asset_id.lot_id.product_id:
                market_price_model = self.env['farm.market.price']
                price = market_price_model.get_current_price(
                    record.asset_id.lot_id.product_id.id,
                    record.valuation_date
                )
                record.market_price = price
                # Also get source info
                latest_price = market_price_model.search([
                    ('product_id', '=', record.asset_id.lot_id.product_id.id),
                    ('date', '<=', record.valuation_date)
                ], order='date desc', limit=1)
                record.market_price_source = latest_price.source if latest_price else "Internal Estimate"
            else:
                record.market_price = 0.0
                record.market_price_source = "No Product Data"

    @api.depends('current_yield_potential', 'market_price', 'efficiency_multiplier')
    def _compute_fair_value(self):
        """Compute fair value: Value = Current Yield Potential * Market Price * Efficiency"""
        for record in self:
            record.fair_value = record.current_yield_potential * record.market_price * record.efficiency_multiplier

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
        US-17-11: Automatic generation of "biological asset revaluation" accounting entries
        """
        account_move = self.env['account.move']
        account_obj = self.env['account.account']
        journal_obj = self.env['account.journal']

        for record in self:
            if record.is_accounting_entry_created:
                continue  # Skip if entry already created

            if abs(record.revaluation_amount) < 0.01:  # Skip if negligible
                continue

            # Get required accounts - for biological assets we typically use:
            # - Biological Assets account (1611 in Chinese accounting standards)
            # - Revaluation Reserve account (4801)
            bio_asset_account = account_obj.search([
                ('code', '=like', '1611%'),  # Biological Assets account
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

            # Create journal entry
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
        assets = self.env['farm.biological.asset'].search([
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


class BiologicalAssetExtension(models.Model):
    """Extension to biological asset model to include fair value integration"""
    _inherit = 'farm.biological.asset'

    # Fair value fields
    current_fair_value = fields.Float("Current Fair Value",
                                     compute='_compute_current_fair_value',
                                     store=True,
                                     help="Current fair value based on market conditions")
    fair_value_date = fields.Date("Fair Value Date",
                                 compute='_compute_current_fair_value',
                                 store=True,
                                 help="Date of last fair value calculation")

    # One2many field to fair valuations
    fair_valuation_ids = fields.One2many('farm.biological.asset.fair.valuation', 'asset_id', string="Fair Valuations")

    # Integration with OPE metrics (Operational Performance Efficiency)
    ope_integration = fields.Float("OPE Integration Score",
                                  help="Integration with OPE metrics for valuation")

    @api.depends('fair_valuation_ids.fair_value')
    def _compute_current_fair_value(self):
        """Compute current fair value based on latest fair valuation"""
        for asset in self:
            latest_fair_val = self.env['farm.biological.asset.fair.valuation'].search([
                ('asset_id', '=', asset.id)
            ], order='valuation_date desc', limit=1)

            asset.current_fair_value = latest_fair_val.fair_value if latest_fair_val else 0.0
            asset.fair_value_date = latest_fair_val.valuation_date if latest_fair_val else False

    def action_run_fair_valuation(self):
        """Manual action to run fair valuation for selected assets"""
        for asset in self:
            # Create a new fair valuation
            self.env['farm.biological.asset.fair.valuation'].create({
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