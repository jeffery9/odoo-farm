from odoo import models, fields, api, _
from datetime import timedelta

class CropYieldInsurancePolicy(models.Model):
    _name = 'farm.crop.yield.insurance.policy'
    _description = 'Crop Yield Insurance Policy'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Policy Number", required=True, readonly=True, default=lambda self: _('New'))

    # Policy Terms
    partner_id = fields.Many2one('res.partner', string="Policy Holder", required=True)
    product_id = fields.Many2one('product.template', string="Insured Crop", required=True)
    location_id = fields.Many2one('farm.location', string="Insured Location", required=True)
    farm_entity_id = fields.Many2one('res.partner', string="Farm Entity")

    sum_insured = fields.Monetary("Sum Insured", currency_field='currency_id')
    premium_rate = fields.Float("Premium Rate (%)", digits=(5, 2), required=True)
    premium_amount = fields.Monetary("Premium Amount", currency_field='currency_id', compute='_compute_premium', store=True, precompute=True)

    policy_start_date = fields.Date("Policy Start Date", required=True)
    policy_end_date = fields.Date("Policy End Date", required=True)
    
    # Yield Data Integration
    # Link to prediction model for more robust data
    yield_prediction_id = fields.Many2one('farm.yield.prediction', string="Yield Prediction Ref", ondelete='set null')
    predicted_yield_kg = fields.Float("Predicted Yield (kg)", related='yield_prediction_id.predicted_yield', store=True, readonly=True)

    actual_yield_kg = fields.Float("Actual Harvest Yield (kg)")
    yield_deviation_pct = fields.Float("Yield Deviation (%)", compute='_compute_yield_deviation', store=True, precompute=True)

    # Actuarial Fields - Based on US-088-16: Yield Insurance Actuarial Analysis and Claims
    base_yield_trend = fields.Float("Base Yield Trend (kg/ha)", help="Historical average yield for this crop/location")
    risk_factor = fields.Float("Risk Factor", default=1.0, help="Risk multiplier based on location and crop type")
    actuarial_probability_loss = fields.Float("Actuarial Probability of Loss", compute='_compute_actuarial_metrics', store=True, precompute=True, help="Calculated probability of yield loss based on historical data")
    actuarial_premium_rate = fields.Float("Actuarial Premium Rate (%)", compute='_compute_actuarial_metrics', store=True, precompute=True, help="Calculated premium rate based on actuarial analysis")

    # Claims Status and Link
    claim_ids = fields.One2many('farm.insurance.claim', 'policy_id', string="Claims")
    claim_status = fields.Selection([
        ('no_claim', 'No Claim'),
        ('claim_filed', 'Claim Filed'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('paid', 'Paid'),
        ('rejected', 'Rejected')
    ], string="Claim Status", compute='_compute_claim_status', store=True, precompute=True)

    # Financials
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled')
    ], default='draft', tracking=True)

    @api.depends('sum_insured', 'premium_rate', 'actuarial_premium_rate')
    def _compute_premium(self):
        for policy in self:
            # Use actuarial premium rate if available, otherwise use manual rate
            rate_to_use = policy.actuarial_premium_rate if policy.actuarial_premium_rate > 0 else policy.premium_rate
            policy.premium_amount = policy.sum_insured * (rate_to_use / 100.0)

    @api.depends('actual_yield_kg', 'predicted_yield_kg')
    def _compute_yield_deviation(self):
        for policy in self:
            if policy.predicted_yield_kg > 0:
                deviation = ((policy.actual_yield_kg - policy.predicted_yield_kg) / policy.predicted_yield_kg) * 100.0
                policy.yield_deviation_pct = deviation
            else:
                policy.yield_deviation_pct = 0.0

    @api.depends('base_yield_trend', 'risk_factor', 'partner_id', 'product_id', 'location_id')
    def _compute_actuarial_metrics(self):
        """Compute actuarial metrics based on historical data and risk factors"""
        for policy in self:
            # Calculate probability of loss based on historical yield variance
            historical_yield_variance = 0.0
            if policy.base_yield_trend > 0:
                # Use partner, product and location to fetch historical data for more accurate calculation
                # This would normally query historical yield data from the database
                # For now, we'll simulate it based on risk factor
                historical_yield_variance = (1.0 / policy.base_yield_trend) * policy.risk_factor
            else:
                # Default value if no historical data available
                historical_yield_variance = 0.1 * policy.risk_factor

            policy.actuarial_probability_loss = min(1.0, historical_yield_variance) * 100  # As percentage

            # Calculate premium rate based on probability of loss and risk factor
            base_premium_rate = 5.0  # Base rate at 5%
            risk_premium = policy.actuarial_probability_loss * 0.2  # Additional rate based on risk
            policy.actuarial_premium_rate = base_premium_rate + risk_premium

    @api.depends('claim_ids.state')
    def _compute_claim_status(self):
        for policy in self:
            if not policy.claim_ids:
                policy.claim_status = 'no_claim'
            else:
                states = policy.claim_ids.mapped('state')
                if 'rejected' in states:
                    policy.claim_status = 'rejected'
                elif 'paid' in states:
                    policy.claim_status = 'paid'
                elif 'approved' in states:
                    policy.claim_status = 'approved'
                elif 'claim_filed' in states or 'under_review' in states:
                    policy.claim_status = 'under_review'
                else:
                    policy.claim_status = 'no_claim'
                    
    def action_calculate_actuarial_data(self):
        """Calculate actuarial data based on historical patterns and location-specific risk factors"""
        for policy in self:
            # In real implementation, this would query historical yield data
            # from previous campaigns for the same crop in the same location
            # For now, we'll use a simplified approach based on crop and location
            if policy.product_id and policy.location_id:
                # Example: fetch historical average yield from similar policies or campaigns
                # This is a placeholder implementation
                avg_historical_yield = 3000.0  # kg/ha - this would come from historical data
                policy.base_yield_trend = avg_historical_yield

    def action_activate_policy(self):
        """Activate the policy, potentially trigger premium invoice generation"""
        self.write({'state': 'active'})
        # TODO: Create premium invoice when policy is activated
        pass # Placeholder

    def action_file_claim(self):
        """Initiate a claim process for this policy"""
        action = self.env.ref('farm_insurance.action_farm_insurance_claim_form')
        return action.read()[0]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('POLICY') or _('POL/%s/00001' % fields.Date.context_today(self).strftime('%Y'))
        return super().create(vals_list)

class FarmInsuranceClaim(models.Model):
    _name = 'farm.insurance.claim'
    _description = 'Crop Yield Insurance Claim'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'claim_date desc'

    name = fields.Char("Claim Reference", required=True, readonly=True, default=lambda self: _('New'))
    policy_id = fields.Many2one('farm.crop.yield.insurance.policy', string="Insurance Policy", required=True)
    
    partner_id = fields.Many2one('res.partner', related='policy_id.partner_id', string="Policy Holder", readonly=True)
    product_id = fields.Many2one('product.template', related='policy_id.product_id', string="Insured Crop", readonly=True)
    location_id = fields.Many2one('farm.location', related='policy_id.location_id', string="Insured Location", readonly=True)
    
    claim_date = fields.Date("Claim Date", default=fields.Date.today, required=True)
    reported_yield_kg = fields.Float("Reported Harvest Yield (kg)", required=True)
    
    # Assessment & Payout
    assessment_report = fields.Text("Assessment Report")
    assessed_loss_amount = fields.Monetary("Assessed Loss Amount", currency_field='currency_id')
    payout_amount = fields.Monetary("Payout Amount", currency_field='currency_id')
    
    state = fields.Selection([
        ('filed', 'Filed'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('paid', 'Paid'),
        ('rejected', 'Rejected')
    ], default='filed', tracking=True)
    
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('farm.insurance.claim') or _('CLAIM')
        return super().create(vals_list)

    def action_review_claim(self):
        self.write({'state': 'under_review'})

    def action_approve_claim(self):
        self.write({'state': 'approved'})
        # Calculate payout based on policy terms and actual loss
        self.calculate_payout()
        # Trigger payout process or invoice generation

    def calculate_payout(self):
        """Calculate the payout amount based on actuarial analysis and actual loss"""
        for claim in self:
            if claim.policy_id:
                # Calculate loss based on yield deviation
                yield_loss_pct = abs(min(0, claim.policy_id.yield_deviation_pct))  # Only negative deviations count as loss

                # Calculate payout as percentage of sum insured based on loss
                loss_ratio = yield_loss_pct / 100.0
                coverage_threshold = 0.1  # Only pay if loss exceeds 10% threshold

                if loss_ratio >= coverage_threshold:
                    # Calculate actual payout amount
                    payout_amount = claim.policy_id.sum_insured * loss_ratio

                    # Apply coverage limits (e.g., max 90% of sum insured)
                    max_coverage = claim.policy_id.sum_insured * 0.9
                    payout_amount = min(payout_amount, max_coverage)

                    claim.payout_amount = payout_amount
                    claim.assessed_loss_amount = payout_amount
                else:
                    # Loss is below threshold, no payout
                    claim.payout_amount = 0.0
                    claim.assessed_loss_amount = 0.0

    def action_reject_claim(self):
        self.write({'state': 'rejected'})

    def action_mark_as_paid(self):
        self.write({'state': 'paid'})
        # Update policy status if needed, or create payment records

class YieldPredictionModel(models.Model):
    """
    Placeholder for Yield Prediction Model configuration.
    This could store parameters for the AI model used in Biological Twin.
    """
    _name = 'farm.yield.prediction'
    _description = 'Yield Prediction Model Configuration'

    name = fields.Char("Model Name")
    product_id = fields.Many2one('product.template', string="Crop/Product")
    location_id = fields.Many2one('farm.location', string="Target Location")
    
    model_type = fields.Char("AI Model Type") # e.g., 'RandomForest', 'NeuralNetwork'
    parameters = fields.Text("Model Parameters (JSON)")
    
    predicted_yield = fields.Float("Predicted Yield (kg)", readonly=True)
    prediction_date = fields.Datetime("Prediction Date", readonly=True)
    active = fields.Boolean(default=True)

# Add necessary sequences and menu items in data files.
# Add security rules in security/ir.model.access.csv