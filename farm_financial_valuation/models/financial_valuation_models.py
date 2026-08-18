from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime, date, timedelta
import logging

_logger = logging.getLogger(__name__)


class FinancialAssetValuation(models.Model):
    """
    Financial Asset Valuation - specialized financial valuation models
    Extends the core biological asset valuation with additional financial instruments
    """
    _name = 'farm.financial.asset.valuation'
    _description = 'Financial Asset Valuation'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'asset_id, valuation_date desc'

    name = fields.Char("Valuation Reference", required=True, default=lambda self: _('New'))
    asset_id = fields.Many2one('agri.biological.asset', string="Financial Asset", required=True)
    valuation_date = fields.Date("Valuation Date", default=fields.Date.today, required=True)

    # Valuation Method Selection
    valuation_method = fields.Selection([
        ('market_price', 'Fair Value - Market Price'),
        ('cost_model', 'Cost Model'),
        ('income_approach', 'Income Approach'),
        ('comparable_sales', 'Comparable Sales Approach'),
        ('hybrid', 'Hybrid Model')
    ], string="Valuation Method", default='market_price', required=True)

    # Asset Classification
    asset_type = fields.Selection([
        ('biological', 'Biological Asset'),
        ('machinery', 'Machinery & Equipment'),
        ('land', 'Land & Property'),
        ('livestock', 'Livestock'),
        ('crop', 'Crop Inventory'),
        ('investment', 'Investment Assets'),
    ], string="Asset Type", default='biological', required=True)

    # Market Value Parameters
    market_price = fields.Float("Market Price (per unit)", digits=(12, 4))
    market_price_source = fields.Char("Market Price Source", help="Source of the market price data")
    market_adjustment_factor = fields.Float("Market Adjustment Factor", default=1.0,
                                           help="Factor to adjust market prices for condition, location, etc.")
    fair_value = fields.Float("Fair Value", compute='_compute_fair_value', store=True, precompute=True,
                             help="Calculated fair value based on selected method")

    # Cost Parameters
    original_cost = fields.Float("Original Cost")
    accumulated_depreciation = fields.Float("Accumulated Depreciation", default=0.0)
    net_book_value = fields.Float("Net Book Value", compute='_compute_net_book_value', store=True, precompute=True)

    # Income Approach Parameters
    projected_cash_flows = fields.Text("Projected Cash Flows (JSON)")
    discount_rate = fields.Float("Discount Rate (%)", default=5.0)
    useful_life_years = fields.Float("Remaining Useful Life (Years)")

    # Comparable Sales Parameters
    comparable_asset_ids = fields.Many2many('farm.financial.asset.valuation', relation='farm_financial_asset_valuation_comparable_rel', column1='valuation_id', column2='comparable_id', string="Comparable Assets")
    adjustment_factors = fields.Text("Adjustment Factors for Comparables")

    # Valuation Result
    valuation_amount = fields.Float("Valuation Amount", compute='_compute_valuation_amount', store=True, precompute=True, readonly=False)
    valuation_variance = fields.Float("Variance from Previous", compute='_compute_variance', store=True, precompute=True)
    confidence_level = fields.Float("Confidence Level (%)", default=85.0,
                                   help="Confidence in the valuation estimate")

    # Professional Valuation
    valuer_id = fields.Many2one('res.partner', string="Professional Valuer",
                               domain=[('is_company', '=', False), ('function', 'ilike', 'valuator')])
    valuation_report_reference = fields.Char("Valuation Report Reference")

    # Regulatory Compliance
    compliance_requirements = fields.Text("Compliance Requirements")
    valuation_notes = fields.Text("Valuation Notes")

    # [Anji Model] Ecological Linkage [US-TECH-VAL-03]
    gep_score = fields.Float("Ecological GEP", related='asset_id.location_id.gep_score')
    gep_premium_factor = fields.Float("GEP Premium Factor", compute='_compute_gep_premium', store=True)

    @api.depends('gep_score', 'asset_type')
    def _compute_gep_premium(self):
        """
        [US-ANJI-02] Ecological Value Monetization.
        If asset is 'land', apply a premium factor based on GEP score.
        GEP > 80 = +20% value, GEP > 60 = +10% value.
        """
        for record in self:
            if record.asset_type == 'land' and record.gep_score:
                if record.gep_score >= 80.0:
                    record.gep_premium_factor = 1.20
                elif record.gep_score >= 60.0:
                    record.gep_premium_factor = 1.10
                else:
                    record.gep_premium_factor = 1.0
            else:
                record.gep_premium_factor = 1.0

    # Previous valuation for comparison
    previous_valuation_id = fields.Many2one('farm.financial.asset.valuation', string="Previous Valuation")

    @api.depends('valuation_method', 'market_price', 'original_cost', 'accumulated_depreciation',
                 'market_adjustment_factor', 'discount_rate', 'projected_cash_flows', 'gep_premium_factor')
    def _compute_valuation_amount(self):
        """Compute valuation amount based on selected method and ecological premium"""
        for record in self:
            base_amount = 0.0
            if record.valuation_method == 'market_price':
                base_amount = record.market_price * record.market_adjustment_factor
            elif record.valuation_method == 'cost_model':
                base_amount = record.original_cost - record.accumulated_depreciation
            elif record.valuation_method == 'income_approach':
                if record.projected_cash_flows and record.discount_rate > 0:
                    base_amount = record.original_cost * (1 + record.discount_rate/100)
                else:
                    base_amount = record.original_cost - record.accumulated_depreciation
            elif record.valuation_method == 'comparable_sales':
                if record.comparable_asset_ids:
                    avg_comparable_value = sum(record.comparable_asset_ids.mapped('valuation_amount')) / len(record.comparable_asset_ids)
                    base_amount = avg_comparable_value * record.market_adjustment_factor
                else:
                    base_amount = record.market_price if record.market_price else record.original_cost - record.accumulated_depreciation
            else:  # hybrid
                market_val = record.market_price * record.market_adjustment_factor if record.market_price else 0
                cost_val = record.original_cost - record.accumulated_depreciation if record.original_cost else 0
                base_amount = (market_val + cost_val) / 2
            
            # Apply Ecological GEP Premium
            record.valuation_amount = base_amount * record.gep_premium_factor
            _logger.info("Valuation Compute Amount: base=%s, factor=%s -> result=%s", 
                         base_amount, record.gep_premium_factor, record.valuation_amount)

    @api.depends('original_cost', 'accumulated_depreciation')
    def _compute_net_book_value(self):
        """Compute net book value"""
        for record in self:
            record.net_book_value = record.original_cost - record.accumulated_depreciation

    @api.depends('market_price', 'market_adjustment_factor')
    def _compute_fair_value(self):
        """Compute fair value for market price method"""
        for record in self:
            if record.valuation_method == 'market_price':
                record.fair_value = record.market_price * record.market_adjustment_factor
            else:
                record.fair_value = record.valuation_amount

    @api.depends('valuation_amount', 'previous_valuation_id.valuation_amount')
    def _compute_variance(self):
        """Compute variance from previous valuation"""
        for record in self:
            if record.previous_valuation_id:
                previous_val = record.previous_valuation_id.valuation_amount
                if previous_val != 0:
                    record.valuation_variance = ((record.valuation_amount - previous_val) / previous_val) * 100
                else:
                    record.valuation_variance = 0.0
            else:
                record.valuation_variance = 0.0

    @api.model
    def _get_valuation_plugins(self):
        """ Registry for valuation plugins """
        return [
            {'name': 'fair_value', 'class': 'agri.valuation.plugin.fair_value'},
            {'name': 'growth_progress', 'class': 'agri.valuation.plugin.growth'},
            {'name': 'gep_premium', 'class': 'agri.valuation.plugin.gep'},
        ]

    def action_calculate_valuation(self):
        """
        [SOLID Refactored] Calculates valuation by orchestrating multiple plugins.
        """
        for record in self:
            final_amount = 0.0
            accumulated_notes = []
            multiplier = 1.0
            
            plugins = record._get_valuation_plugins()
            valuation_context = {
                'market_price': record.market_price,
                'market_adjustment_factor': record.market_adjustment_factor,
                'valuation_method': record.valuation_method,
            }
            for plugin_info in plugins:
                try:
                    plugin_model = self.env[plugin_info['class']]
                    _logger.info("Valuation Plugin Found: %s", plugin_info['class'])
                    res = plugin_model.calculate_value(record.asset_id, context=valuation_context)
                    _logger.info("Valuation Plugin Result: %s", res)
                    if res:
                        if 'amount' in res:
                            final_amount = res['amount'] # Take base amount
                        if 'multiplier' in res:
                            multiplier *= res['multiplier'] # Apply multipliers
                        if 'notes' in res:
                            accumulated_notes.append(res['notes'])
                except KeyError:
                    _logger.warning("Valuation Plugin Not Found: %s", plugin_info['class'])
                except Exception as e:
                    _logger.error("Valuation Plugin Error (%s): %s", plugin_info['name'], str(e))
            
            record.write({
                'valuation_amount': final_amount * multiplier,
                'valuation_notes': "\n".join(accumulated_notes)
            })
            _logger.info("Valuation Orchestrator Final: %s (Amount: %s)", record.name, record.valuation_amount)
            
            # Legacy compute triggers for UI consistency
            record._compute_net_book_value()
            record._compute_fair_value()
            record._compute_variance()
        return True

    def action_create_accounting_entries(self):
        """Create accounting entries for revaluation"""
        account_move = self.env['account.move']
        account_obj = self.env['account.account']

        for record in self:
            _logger.info("Valuation Journal Entry: Checking record %s (Variance: %s)", record.name, record.valuation_variance)
            if not record.valuation_variance or abs(record.valuation_variance) < 0.01:
                continue  # Skip if no significant change

            # Get required accounts
            asset_account = account_obj.search([
                ('code', '=like', '16%'),  # Fixed assets account
                ('company_ids', 'in', self.env.company.ids)
            ], limit=1)

            if not asset_account:
                asset_account = account_obj.search([
                    ('name', 'ilike', 'asset'),
                    ('company_ids', 'in', self.env.company.ids)
                ], limit=1)

            if not asset_account:
                raise UserError(_("No suitable asset account found for valuation entries."))

            # Create journal entry based on whether it's a gain or loss
            journal = self.env['account.journal'].search([
                ('type', '=', 'general'),
                ('company_id', '=', self.env.company.id)
            ], limit=1)

            if not journal:
                raise UserError(_("No general journal found."))

            reval_account = account_obj.search([
                ('code', '=like', '48%'),  # Revaluation reserve account
                ('company_ids', 'in', self.env.company.ids)
            ], limit=1)

            if not reval_account:
                reval_account = account_obj.search([
                    ('name', 'ilike', 'revaluation'),
                    ('company_ids', 'in', self.env.company.ids)
                ], limit=1)

            if not reval_account:
                # If no revaluation account found, use retained earnings (41xx)
                reval_account = account_obj.search([
                    ('code', '=like', '41%'),
                    ('company_id', '=', self.env.company.id)
                ], limit=1)

            if not reval_account:
                raise UserError(_("No revaluation reserve account found."))

            # Determine if gain or loss
            amount = abs(record.valuation_variance)
            if record.valuation_variance > 0:
                # Gain - debit asset account, credit revaluation account
                debit_account = asset_account
                credit_account = reval_account
            else:
                # Loss - debit revaluation account, credit asset account
                debit_account = reval_account
                credit_account = asset_account

            move_vals = {
                'journal_id': journal.id,
                'date': record.valuation_date,
                'ref': f'Asset Revaluation - {record.asset_id.name} - {record.name}',
                'line_ids': [
                    (0, 0, {
                        'account_id': debit_account.id,
                        'name': f'Asset revaluation for {record.asset_id.name}',
                        'debit': amount,
                        'credit': 0,
                        'partner_id': self.env.company.partner_id.id,
                    }),
                    (0, 0, {
                        'account_id': credit_account.id,
                        'name': f'Asset revaluation for {record.asset_id.name}',
                        'debit': 0,
                        'credit': amount,
                        'partner_id': self.env.company.partner_id.id,
                    })
                ]
            }

            move = account_move.create(move_vals)
            move.action_post()

            # Add message to the asset
            record.asset_id.message_post(body=_(
                "ASSET REVALUATION: Amount %s recorded for %s. "
                "Journal entry %s created. Previous: %s, New: %s"
            ) % (amount, record.asset_id.name, move.name,
                 record.previous_valuation_id.valuation_amount if record.previous_valuation_id else 0,
                 record.valuation_amount))

    @api.model_create_multi
    def create(self, vals_list):
        """Generate unique valuation reference on creation"""
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                asset = self.env['agri.biological.asset'].browse(vals.get('asset_id', False))
                date_str = vals.get('valuation_date', fields.Date.today()).strftime('%Y%m%d')
                vals['name'] = f"FV-{asset.name or 'ASSET'}-{date_str}-{len([v for v in vals_list if 'name' in v]) + 1}"
        return super().create(vals_list)


class FinancialValuationTemplate(models.Model):
    """
    Valuation template for standardizing valuation approaches across assets
    """
    _name = 'farm.financial.valuation.template'
    _description = 'Financial Valuation Template'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Template Name", required=True)
    code = fields.Char("Template Code", required=True, copy=False)
    active = fields.Boolean("Active", default=True)

    # Valuation method configuration
    default_valuation_method = fields.Selection([
        ('market_price', 'Fair Value - Market Price'),
        ('cost_model', 'Cost Model'),
        ('income_approach', 'Income Approach'),
        ('comparable_sales', 'Comparable Sales Approach'),
        ('hybrid', 'Hybrid Model')
    ], string="Default Valuation Method", required=True)

    # Asset type for which this template applies
    applicable_asset_types = fields.Many2many('farm.financial.asset.valuation', 'farm_financial_valua_farm_financial_asset_6af42eab_rel', 'template_id', 'valuation_id',
                                             compute='_compute_applicable_asset_types',
                                             string="Applicable Asset Types")

    # Default parameters based on asset type
    default_market_adjustment = fields.Float("Default Market Adjustment Factor", default=1.0)
    default_discount_rate = fields.Float("Default Discount Rate (%)", default=5.0)
    default_confidence_level = fields.Float("Default Confidence Level (%)", default=85.0)

    # Professional requirements
    requires_professional_valuation = fields.Boolean("Requires Professional Valuation", default=False)
    recommended_valuer_ids = fields.Many2many('res.partner',
                                             'valuation_template_valuer_rel',
                                             'template_id', 'valuer_id',
                                             string="Recommended Valuers",
                                             domain=[('is_company', '=', False), ('function', 'ilike', 'valuator')])

    # Compliance settings
    compliance_requirements = fields.Text("Compliance Requirements Template")
    standard_notes = fields.Text("Standard Valuation Notes")

    _code_unique = models.Constraint(
        'UNIQUE(code)',
        'Template code must be unique!'
    )

    @api.depends('default_valuation_method')
    def _compute_applicable_asset_types(self):
        """Compute which asset types this template applies to"""
        for template in self:
            # This would be populated based on business logic
            template.applicable_asset_types = False  # Computed field, populated by business logic

    def apply_to_asset(self, asset_id):
        """Apply this template to a specific asset for valuation"""
        # Create a new valuation record using template defaults
        vals = {
            'asset_id': asset_id,
            'valuation_method': self.default_valuation_method,
            'market_adjustment_factor': self.default_market_adjustment,
            'discount_rate': self.default_discount_rate,
            'confidence_level': self.default_confidence_level,
            'compliance_requirements': self.compliance_requirements,
            'valuation_notes': self.standard_notes,
        }

        valuation = self.env['farm.financial.asset.valuation'].create(vals)
        return valuation


class FinancialAsset(models.Model):
    """
    Enhanced financial asset model with valuation integration
    """
    _inherit = 'agri.biological.asset'  # This extends the core biological asset model

    # Financial valuation integration
    current_financial_valuation = fields.Float("Current Financial Valuation",
                                              compute='_compute_current_financial_valuation',
                                              store=True)
    last_valuation_date = fields.Date("Last Valuation Date",
                                     compute='_compute_current_financial_valuation',
                                     store=True)
    valuation_history_ids = fields.One2many('farm.financial.asset.valuation', 'asset_id',
                                          string="Valuation History")
    financial_valuation_status = fields.Selection([
        ('current', 'Current'),
        ('overdue', 'Overdue for Revaluation'),
        ('exempt', 'Exempt from Regular Valuation'),
    ], string="Valuation Status", compute='_compute_valuation_status', store=True, precompute=True)

    @api.depends('valuation_history_ids.valuation_amount', 'valuation_history_ids.valuation_date')
    def _compute_current_financial_valuation(self):
        """Compute current financial valuation based on latest valuation"""
        for asset in self:
            latest_valuation = self.env['farm.financial.asset.valuation'].search([
                ('asset_id', '=', asset.id)
            ], order='valuation_date desc', limit=1)

            asset.current_financial_valuation = latest_valuation.valuation_amount if latest_valuation else 0.0
            asset.last_valuation_date = latest_valuation.valuation_date if latest_valuation else False

    @api.depends('last_valuation_date')
    def _compute_valuation_status(self):
        """Compute valuation status based on last valuation date"""
        today = fields.Date.today()
        for asset in self:
            if not asset.last_valuation_date:
                asset.financial_valuation_status = 'overdue'
            else:
                # Assuming annual valuation requirement (would be configurable)
                from datetime import timedelta
                if (today - asset.last_valuation_date) > timedelta(days=365):
                    asset.financial_valuation_status = 'overdue'
                else:
                    asset.financial_valuation_status = 'current'

    def action_request_financial_valuation(self):
        """Request a new financial valuation for this asset"""
        for asset in self:
            # Create a new valuation record with default values
            self.env['farm.financial.asset.valuation'].create({
                'asset_id': asset.id,
                'valuation_date': fields.Date.today(),
                'valuation_method': 'market_price',  # Default method
            })

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Financial Valuation'),
                'message': _('Financial valuation request created for selected assets'),
                'type': 'success',
                'sticky': False,
            }
        }