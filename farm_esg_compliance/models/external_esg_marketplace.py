from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class AgriESGMarketplace(models.Model):
    """
    US-097-02: 外部ESG市场平台 (External ESG Marketplace Platform)
    Platform for trading ESG-related products and services
    """
    _name = 'agri.esg.marketplace'
    _description = 'External ESG Marketplace Platform'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Marketplace Name', required=True)
    code = fields.Char('Marketplace Code', required=True, copy=False, default=lambda self: self._generate_code())
    description = fields.Text('Description')

    # Marketplace type
    market_type = fields.Selection([
        ('carbon_credits', 'Carbon Credits Trading'),
        ('bio_energy', 'Bio-energy Products'),
        ('renewable_energy', 'Renewable Energy Certificates'),
        ('sustainable_products', 'Sustainable Agricultural Products'),
        ('waste_resources', 'Waste Resource Trading'),
        ('water_rights', 'Water Rights Trading'),
    ], string='Marketplace Type', required=True)

    # Operational information
    is_active = fields.Boolean('Is Active', default=True)
    operator_partner_id = fields.Many2one('res.partner', string='Market Operator', required=True)
    launch_date = fields.Date('Launch Date')
    supported_regions = fields.Many2many('res.country', 'agri_esg_marketplace_res_country_rel', 'marketplace_id', 'country_id', string='Supported Regions')
    supported_languages = fields.Many2many('res.lang', 'agri_esg_marketplace_res_lang_rel', 'marketplace_id', 'lang_id', string='Supported Languages')

    # Technical specifications
    platform_url = fields.Char('Platform URL')
    api_endpoint = fields.Char('API Endpoint')
    integration_type = fields.Selection([
        ('direct_api', 'Direct API Integration'),
        ('standard_exchange', 'Standard Exchange Protocol'),
        ('blockchain', 'Blockchain-based'),
        ('hybrid', 'Hybrid System'),
    ], string='Integration Type', default='direct_api')

    # Compliance and standards
    compliance_standards = fields.Many2many('farm.compliance.audit.standard', 'esg_market_std_rel', 'market_id', 'std_id', string='Compliance Standards')
    certification_requirement = fields.Text('Certification Requirement')
    audit_frequency = fields.Selection([
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('annual', 'Annual'),
    ], string='Audit Frequency', default='annual')

    # Fee structure
    listing_fee = fields.Float('Listing Fee ($)', help='Fee for listing products/services')
    transaction_fee_percent = fields.Float('Transaction Fee (%)', help='Percentage fee on transactions')
    withdrawal_fee = fields.Float('Withdrawal Fee ($)', help='Fee for fund withdrawal')

    # Trading statistics
    total_trades = fields.Integer('Total Trades', compute='_compute_trade_stats', store=True, precompute=True)
    total_volume = fields.Float('Total Trading Volume ($)', compute='_compute_trade_stats', store=True, precompute=True)
    total_products_listed = fields.Integer('Total Products Listed', compute='_compute_product_stats', store=True, precompute=True)

    # Security and access
    access_level = fields.Selection([
        ('public', 'Public'),
        ('registered', 'Registered Users Only'),
        ('certified', 'Certified Partners Only'),
        ('private', 'Private Network'),
    ], string='Access Level', required=True, default='registered')

    security_certificate = fields.Char('Security Certificate')
    data_encryption = fields.Boolean('Data Encryption', default=True)

    @api.model
    def _generate_code(self):
        """Generate a unique marketplace code"""
        return self.env['ir.sequence'].next_by_code('agri.esg.marketplace') or 'MKT-NEW'

    @api.constrains('transaction_fee_percent')
    def _check_fee_percent(self):
        for record in self:
            if record.transaction_fee_percent < 0 or record.transaction_fee_percent > 100:
                raise ValidationError(_("Transaction fee percentage must be between 0 and 100."))

    def _compute_trade_stats(self):
        """Compute trading statistics"""
        for record in self:
            # In real implementation, this would aggregate from trade records
            # For now, we'll compute from related trade records
            trade_records = self.env['agri.esg.marketplace.trade'].search([
                ('marketplace_id', '=', record.id),
                ('trade_status', '=', 'completed')
            ])
            record.total_trades = len(trade_records)
            record.total_volume = sum(trade_records.mapped('total_amount'))

    def _compute_product_stats(self):
        """Compute product statistics"""
        for record in self:
            # Count products listed in this marketplace
            product_records = self.env['agri.bio.energy.product'].search([
                ('is_listed_in_marketplace', '=', True),
                ('marketplace_category', '=', dict(
                    self.env['agri.bio.energy.product']._fields['marketplace_category'].selection
                ).get(record.market_type, '').lower().replace(' ', '_'))
            ])
            record.total_products_listed = len(product_records)

    def action_activate_marketplace(self):
        """Activate the marketplace"""
        for record in self:
            record.is_active = True
            record.message_post(body=_("Marketplace activated."))

    def action_deactivate_marketplace(self):
        """Deactivate the marketplace"""
        for record in self:
            record.is_active = False
            record.message_post(body=_("Marketplace deactivated."))

    def action_sync_with_external_platform(self):
        """Synchronize with external marketplace platform"""
        for record in self:
            record.message_post(body=_("Synchronization with external platform initiated."))


class AgriESGMarketplaceTrade(models.Model):
    """
    US-097-03: ESG市场交易记录 (ESG Marketplace Trade Records)
    Records of trades in the ESG marketplace
    """
    _name = 'agri.esg.marketplace.trade'
    _description = 'ESG Marketplace Trade Records'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Trade Reference', required=True, copy=False, default=lambda self: self._generate_trade_ref())
    trade_date = fields.Datetime('Trade Date', default=fields.Datetime.now)

    # Marketplace link
    marketplace_id = fields.Many2one('agri.esg.marketplace', string='Marketplace', required=True)
    trade_type = fields.Selection([
        ('buy', 'Buy'),
        ('sell', 'Sell'),
        ('trade', 'Trade'),
        ('auction', 'Auction'),
        ('tender', 'Tender'),
    ], string='Trade Type', required=True)

    # Product/Service details
    product_id = fields.Many2one('agri.bio.energy.product', string='Product')
    product_name = fields.Char('Product Name', related='product_id.name', store=True)
    product_category = fields.Selection(related='product_id.marketplace_category', string='Product Category', store=True)
    quantity = fields.Float('Quantity', required=True)
    unit_price = fields.Float('Unit Price ($)', required=True)
    total_amount = fields.Float('Total Amount ($)', compute='_compute_total_amount', store=True, precompute=True)

    # Trading parties
    buyer_partner_id = fields.Many2one('res.partner', string='Buyer', required=True)
    seller_partner_id = fields.Many2one('res.partner', string='Seller', required=True)
    broker_partner_id = fields.Many2one('res.partner', string='Broker/Intermediary')

    # Compliance and verification
    compliance_verification = fields.Selection([
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    ], string='Compliance Verification', default='pending')
    verification_date = fields.Datetime('Verification Date')
    verification_notes = fields.Text('Verification Notes')

    # Trade status
    trade_status = fields.Selection([
        ('draft', 'Draft'),
        ('pending_payment', 'Pending Payment'),
        ('payment_confirmed', 'Payment Confirmed'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('disputed', 'Disputed'),
    ], string='Trade Status', default='draft')

    # Delivery and logistics
    delivery_date = fields.Date('Expected Delivery Date')
    actual_delivery_date = fields.Date('Actual Delivery Date')
    delivery_location_id = fields.Many2one('farm.location', string='Delivery Location')
    shipping_method = fields.Selection([
        ('ground', 'Ground Transport'),
        ('sea', 'Sea Freight'),
        ('air', 'Air Freight'),
        ('rail', 'Rail Transport'),
        ('combined', 'Combined Transport'),
    ], string='Shipping Method')

    # Documentation
    trade_contract = fields.Binary('Trade Contract', attachment=True)
    contract_name = fields.Char('Contract Name')
    invoice_reference = fields.Char('Invoice Reference')
    delivery_receipt = fields.Binary('Delivery Receipt', attachment=True)
    receipt_name = fields.Char('Receipt Name')

    # ESG impact metrics
    co2_reduction_impact = fields.Float('CO2 Reduction Impact (tCO2e)',
                                       help='Environmental impact of this trade')
    sustainability_score_change = fields.Float('Sustainability Score Change',
                                              help='Change in sustainability score due to this trade')

    # Payment and fees
    payment_method = fields.Selection([
        ('wire_transfer', 'Wire Transfer'),
        ('escrow', 'Escrow Service'),
        ('cryptocurrency', 'Cryptocurrency'),
        ('carbon_credit', 'Carbon Credit'),
        ('other', 'Other'),
    ], string='Payment Method', default='wire_transfer')
    marketplace_fee = fields.Float('Marketplace Fee ($)', compute='_compute_marketplace_fee', store=True, precompute=True)
    net_amount = fields.Float('Net Amount ($)', compute='_compute_net_amount', store=True, precompute=True)

    @api.model
    def _generate_trade_ref(self):
        """Generate a unique trade reference"""
        return self.env['ir.sequence'].next_by_code('agri.esg.marketplace.trade') or 'TRD-NEW'

    @api.constrains('quantity', 'unit_price')
    def _check_positive_values(self):
        for record in self:
            if record.quantity <= 0:
                raise ValidationError(_("Quantity must be positive."))
            if record.unit_price < 0:
                raise ValidationError(_("Unit price cannot be negative."))

    @api.depends('quantity', 'unit_price')
    def _compute_total_amount(self):
        for record in self:
            record.total_amount = (record.quantity or 0) * (record.unit_price or 0)

    @api.depends('total_amount', 'marketplace_id.transaction_fee_percent')
    def _compute_marketplace_fee(self):
        for record in self:
            fee_percent = record.marketplace_id.transaction_fee_percent or 0
            record.marketplace_fee = (record.total_amount or 0) * (fee_percent / 100)

    @api.depends('total_amount', 'marketplace_fee')
    def _compute_net_amount(self):
        for record in self:
            record.net_amount = (record.total_amount or 0) - (record.marketplace_fee or 0)

    def action_confirm_payment(self):
        """Confirm payment for the trade"""
        for record in self:
            record.trade_status = 'payment_confirmed'
            record.message_post(body=_("Payment confirmed for trade."))

    def action_mark_delivered(self):
        """Mark the trade as delivered"""
        for record in self:
            record.trade_status = 'delivered'
            record.actual_delivery_date = fields.Date.context_today(record)
            record.message_post(body=_("Trade marked as delivered."))

    def action_complete_trade(self):
        """Complete the trade transaction"""
        for record in self:
            record.trade_status = 'completed'
            record.message_post(body=_("Trade completed successfully."))

    def action_verify_compliance(self):
        """Verify compliance of the trade"""
        for record in self:
            record.compliance_verification = 'verified'
            record.verification_date = fields.Datetime.now()
            record.message_post(body=_("Trade compliance verified."))

    def action_cancel_trade(self):
        """Cancel the trade"""
        for record in self:
            record.trade_status = 'cancelled'
            record.message_post(body=_("Trade cancelled."))


class AgriWasteResourceTrade(models.Model):
    """
    US-097-04: 废料资源交易 (Waste Resource Trading)
    Trading of agricultural waste materials and by-products
    """
    _name = 'agri.waste.resource.trade'
    _description = 'Agricultural Waste Resource Trading'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Waste Resource Trade', required=True, copy=False, default=lambda self: self._generate_trade_code())
    trade_reference = fields.Char('Trade Reference')

    # Waste resource details
    waste_type = fields.Selection([
        ('crop_residue', 'Crop Residue'),
        ('animal_waste', 'Animal Waste'),
        ('food_processing', 'Food Processing Waste'),
        ('biomass', 'Biomass Waste'),
        ('organic_waste', 'Organic Waste'),
        ('agro_industrial', 'Agro-industrial Waste'),
    ], string='Waste Type', required=True)

    waste_category = fields.Selection([
        ('biodegradable', 'Biodegradable'),
        ('recyclable', 'Recyclable'),
        ('energy_source', 'Energy Source'),
        ('fertilizer_base', 'Fertilizer Base'),
        ('other', 'Other'),
    ], string='Waste Category', required=True)

    # Physical properties
    quantity = fields.Float('Quantity', required=True)
    quantity_uom = fields.Many2one('uom.uom', string='Quantity Unit', required=True)
    weight_kg = fields.Float('Weight (kg)', help='Calculated weight in kg')
    moisture_content = fields.Float('Moisture Content (%)', help='Percentage of moisture in the waste')
    energy_content = fields.Float('Energy Content (MJ/kg)', help='Energy content per kg')

    # Quality specifications
    quality_grade = fields.Selection([
        ('premium', 'Premium'),
        ('standard', 'Standard'),
        ('basic', 'Basic'),
        ('low_grade', 'Low Grade'),
    ], string='Quality Grade', default='standard')

    quality_certifications = fields.Many2many('farm.certification.process', 'waste_trade_qual_cert_rel', 'trade_id', 'cert_id', string='Quality Certifications')
    contamination_level = fields.Float('Contamination Level (%)', help='Level of contamination in the waste')

    # Trading information
    source_location_id = fields.Many2one('farm.location', string='Source Location', required=True)
    source_partner_id = fields.Many2one('res.partner', string='Source Partner', required=True)
    destination_partner_id = fields.Many2one('res.partner', string='Destination Partner', required=True)
    destination_location_id = fields.Many2one('farm.location', string='Destination Location')

    # Valuation
    unit_price = fields.Float('Unit Price ($/unit)', required=True)
    total_value = fields.Float('Total Value ($)', compute='_compute_total_value', store=True, precompute=True)
    market_price_reference = fields.Char('Market Price Reference', help='Reference for the market price')

    # Environmental impact
    co2_reduction_potential = fields.Float('CO2 Reduction Potential (tCO2e)',
                                          help='Potential CO2 reduction if waste is properly utilized')
    sustainability_score = fields.Float('Sustainability Score (0-100)',
                                       compute='_compute_sustainability_score', store=True, precompute=True)

    # Trading terms
    trade_date = fields.Date('Trade Date', default=fields.Date.context_today)
    expected_collection_date = fields.Date('Expected Collection Date')
    actual_collection_date = fields.Date('Actual Collection Date')
    payment_terms = fields.Char('Payment Terms')

    # Compliance
    compliance_status = fields.Selection([
        ('pending', 'Pending Review'),
        ('verified', 'Verified'),
        ('non_compliant', 'Non-Compliant'),
    ], string='Compliance Status', default='pending')
    required_certifications = fields.Many2many('farm.certification.process', 'waste_trade_req_cert_rel', 'trade_id', 'cert_id', string='Required Certifications')

    # Documentation
    trade_agreement = fields.Binary('Trade Agreement', attachment=True)
    agreement_name = fields.Char('Agreement Name')
    collection_receipt = fields.Binary('Collection Receipt', attachment=True)
    receipt_name = fields.Char('Receipt Name')

    # Status tracking
    status = fields.Selection([
        ('draft', 'Draft'),
        ('listed', 'Listed for Trade'),
        ('contracted', 'Contracted'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft')

    @api.model
    def _generate_trade_code(self):
        """Generate a unique waste resource trade code"""
        return self.env['ir.sequence'].next_by_code('agri.waste.resource.trade') or 'WRT-NEW'

    @api.constrains('quantity', 'unit_price', 'moisture_content', 'contamination_level')
    def _check_positive_values(self):
        for record in self:
            if record.quantity <= 0:
                raise ValidationError(_("Quantity must be positive."))
            if record.unit_price < 0:
                raise ValidationError(_("Unit price cannot be negative."))
            if record.moisture_content < 0 or record.moisture_content > 100:
                raise ValidationError(_("Moisture content must be between 0 and 100%."))
            if record.contamination_level < 0 or record.contamination_level > 100:
                raise ValidationError(_("Contamination level must be between 0 and 100%."))

    @api.depends('quantity', 'unit_price')
    def _compute_total_value(self):
        for record in self:
            record.total_value = (record.quantity or 0) * (record.unit_price or 0)

    @api.depends('quality_grade', 'contamination_level', 'moisture_content')
    def _compute_sustainability_score(self):
        """Compute sustainability score based on various factors"""
        for record in self:
            score = 0.0
            # Quality grade contributes to score
            grade_factor = {'premium': 40, 'standard': 30, 'basic': 20, 'low_grade': 10}
            score += grade_factor.get(record.quality_grade, 0)

            # Adjust for contamination (lower is better)
            contamination_impact = (100 - (record.contamination_level or 0)) * 0.3
            score += contamination_impact

            # Adjust for moisture content (appropriate level depending on use)
            # Assuming ideal moisture content is between 10-30% for most applications
            if record.moisture_content is not None:
                if 10 <= record.moisture_content <= 30:
                    score += 15  # Bonus for ideal moisture
                elif 0 <= record.moisture_content <= 50:
                    score += 10  # Standard acceptable range
                else:
                    score += 5   # Minimum for other ranges

            # Certifications add to score
            pass

            record.sustainability_score = min(100, max(0, score))

    def action_list_for_trade(self):
        """List the waste resource for trading"""
        for record in self:
            record.status = 'listed'
            record.message_post(body=_("Waste resource listed for trade."))

    def action_contract_waste_resource(self):
        """Contract the waste resource with a buyer"""
        for record in self:
            record.status = 'contracted'
            record.message_post(body=_("Waste resource contracted with buyer."))

    def action_mark_delivered(self):
        """Mark the waste resource as delivered"""
        for record in self:
            record.status = 'delivered'
            record.actual_collection_date = fields.Date.context_today(record)
            record.message_post(body=_("Waste resource delivered to destination."))

    def action_complete_trade(self):
        """Complete the waste resource trade"""
        for record in self:
            record.status = 'completed'
            record.message_post(body=_("Waste resource trade completed successfully."))

    def action_verify_compliance(self):
        """Verify compliance of the waste resource trade"""
        for record in self:
            record.compliance_status = 'verified'
            record.message_post(body=_("Waste resource trade compliance verified."))