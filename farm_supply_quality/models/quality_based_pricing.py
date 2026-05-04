from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class QualityBasedPricing(models.Model):
    """
    质量挂钩的采购分级定价 [US-009-11 & US-009-19]
    Quality-based pricing for procurement scenarios based on quality metrics
    """
    _name = 'quality.based.pricing'
    _description = 'Quality-Based Pricing Rules'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Pricing Rule Name', required=True)
    product_category_id = fields.Many2one('product.category', string='Product Category')
    quality_attribute = fields.Char('Quality Attribute', required=True,
                                  help='e.g., protein_content, moisture_content, impurities_rate, sugar_content, fat_content')
    base_price = fields.Float('Base Price', required=True)
    min_value = fields.Float('Minimum Value for Premium')
    max_value = fields.Float('Maximum Value for Premium')
    premium_rate = fields.Float('Premium Rate (%)',
                               help='Percentage to add to base price for each unit above threshold')
    discount_rate = fields.Float('Discount Rate (%)',
                                help='Percentage to subtract from base price for each unit below threshold')
    active = fields.Boolean('Active', default=True)

    # Link to purchase orders for acquisition scenarios (US-009-19)
    purchase_order_id = fields.Many2one(
        'purchase.order',
        string="Purchase Order",
        help="Specific purchase order this rule applies to"
    )

    # Quality attribute ranges for acquisition grading
    quality_min_threshold = fields.Float(
        'Minimum Quality Threshold',
        help='Minimum value for this quality grading'
    )
    quality_max_threshold = fields.Float(
        'Maximum Quality Threshold',
        help='Maximum value for this quality grading'
    )
    quality_grade_label = fields.Selection([
        ('premium', 'Premium'),
        ('standard', 'Standard'),
        ('economy', 'Economy'),
        ('reject', 'Reject'),
    ], string='Quality Grade Label')

    # US-009-19 specific fields for acquisition pricing
    protein_content_coefficient = fields.Float('Protein Content Coefficient',
                                             help='Coefficient to apply per percentage point of protein content')
    moisture_content_coefficient = fields.Float('Moisture Content Coefficient',
                                              help='Coefficient to apply per percentage point of moisture content (usually negative)')
    impurities_rate_coefficient = fields.Float('Impurities Rate Coefficient',
                                             help='Coefficient to apply per percentage point of impurities (usually negative)')
    quality_measure_unit = fields.Char('Quality Measure Unit',
                                     help='Unit of measure for quality attribute (e.g., %, g/kg, etc.)')
    min_quality_for_acceptance = fields.Float('Minimum Quality for Acceptance',
                                            help='Minimum quality value required for acceptance')
    pricing_formula = fields.Text('Pricing Formula',
                                help='Custom formula for complex pricing calculations')

    def calculate_adjusted_price(self, quality_value, base_unit_price):
        """Calculate adjusted price based on quality attribute value"""
        if not self.active or quality_value is None:
            return base_unit_price

        if quality_value >= self.max_value:
            # Apply premium - for every unit above max_value, add premium
            excess = quality_value - self.max_value
            premium_factor = 1 + (excess * self.premium_rate / 100)
            return base_unit_price * premium_factor
        elif quality_value <= self.min_value:
            # Apply discount - for every unit below min_value, subtract discount
            deficit = self.min_value - quality_value
            discount_factor = 1 - (deficit * self.discount_rate / 100)
            # Ensure price doesn't go below zero
            return max(base_unit_price * discount_factor, 0)
        else:
            # Within normal range
            return base_unit_price

    def calculate_quality_grade_from_value(self, quality_value):
        """
        Calculate quality grade based on quality value using thresholds
        """
        if quality_value >= self.quality_max_threshold:
            return 'premium'
        elif quality_value >= self.quality_min_threshold:
            return 'standard'
        elif quality_value >= self.min_quality_for_acceptance:
            return 'economy'
        else:
            return 'reject'

    def calculate_acquisition_price(self, quality_check_results):
        """
        US-009-19: Calculate acquisition price based on multiple quality metrics
        quality_check_results: dict with quality metrics like {'protein_content': 15.5, 'moisture_content': 12.0, 'impurities_rate': 2.5}
        """
        base_price = self.base_price
        adjusted_price = base_price

        # Apply protein content adjustment
        if 'protein_content' in quality_check_results and self.protein_content_coefficient:
            protein_value = quality_check_results['protein_content']
            protein_adjustment = protein_value * self.protein_content_coefficient
            adjusted_price += protein_adjustment

        # Apply moisture content adjustment (usually negative impact)
        if 'moisture_content' in quality_check_results and self.moisture_content_coefficient:
            moisture_value = quality_check_results['moisture_content']
            moisture_adjustment = moisture_value * self.moisture_content_coefficient
            adjusted_price += moisture_adjustment

        # Apply impurities rate adjustment (usually negative impact)
        if 'impurities_rate' in quality_check_results and self.impurities_rate_coefficient:
            impurities_value = quality_check_results['impurities_rate']
            impurities_adjustment = impurities_value * self.impurities_rate_coefficient
            adjusted_price += impurities_adjustment

        # Apply the min quality for acceptance check
        min_metric = min(quality_check_results.values()) if quality_check_results else 0
        if min_metric < self.min_quality_for_acceptance:
            # Apply significant discount or rejection
            adjusted_price = base_price * 0.5  # 50% discount for below acceptance quality

        return max(adjusted_price, 0)  # Ensure non-negative price


class PurchaseOrderLine(models.Model):
    """
    Extension of purchase order line to support quality-based pricing [US-009-19]
    """
    _inherit = 'purchase.order.line'
    quality_adjustment_amount = fields.Float("Quality Adjustment Amount", compute="_compute_quality_adjustment", store=True, precompute=True)
    
    @api.depends("price_subtotal")
    def _compute_quality_adjustment(self):
        for line in self:
            line.quality_adjustment_amount = 0.0

    # Quality metrics fields for acquisition pricing
    quality_protein_content = fields.Float('Protein Content (%)',
                                         help='Protein content percentage for quality-based pricing')
    quality_moisture_content = fields.Float('Moisture Content (%)',
                                          help='Moisture content percentage for quality-based pricing')
    quality_impurities_rate = fields.Float('Impurities Rate (%)',
                                         help='Impurities rate for quality-based pricing')
    quality_grade = fields.Selection([
        ('premium', 'Premium'),
        ('standard', 'Standard'),
        ('economy', 'Economy'),
        ('reject', 'Reject'),
    ], string='Quality Grade', compute='_compute_quality_grade', store=True, precompute=True)

    # Quality-adjusted pricing fields
    base_unit_price = fields.Float('Base Unit Price',
                                 help='Base price before quality adjustments')
    quality_adjusted_unit_price = fields.Float('Quality Adjusted Unit Price',
                                             compute='_compute_quality_adjusted_price', store=True, precompute=True)
    quality_pricing_rule_id = fields.Many2one('quality.based.pricing', string='Quality Pricing Rule')

    @api.depends('quality_protein_content', 'quality_moisture_content', 'quality_impurities_rate')
    def _compute_quality_grade(self):
        """Compute quality grade based on quality metrics"""
        for line in self:
            if line.quality_pricing_rule_id:
                # Use the primary quality attribute from the rule to determine grade
                primary_quality = line._get_primary_quality_value()
                line.quality_grade = line.quality_pricing_rule_id.calculate_quality_grade_from_value(primary_quality)
            else:
                line.quality_grade = False

    def _get_primary_quality_value(self):
        """Get the primary quality value to determine grade"""
        # This could be configurable based on the product type
        # For now, we'll use protein content as the primary metric if available
        if self.quality_protein_content:
            return self.quality_protein_content
        elif self.quality_moisture_content:
            return self.quality_moisture_content
        elif self.quality_impurities_rate:
            return self.quality_impurities_rate
        return 0

    @api.depends('base_unit_price', 'quality_pricing_rule_id', 'quality_protein_content',
                 'quality_moisture_content', 'quality_impurities_rate')
    def _compute_quality_adjusted_price(self):
        """Compute quality adjusted price based on quality metrics"""
        for line in self:
            if line.quality_pricing_rule_id:
                # Get quality check results
                quality_results = {
                    'protein_content': line.quality_protein_content or 0,
                    'moisture_content': line.quality_moisture_content or 0,
                    'impurities_rate': line.quality_impurities_rate or 0,
                }

                # Calculate acquisition price using the quality-based pricing rule
                adjusted_price = line.quality_pricing_rule_id.calculate_acquisition_price(quality_results)
                line.quality_adjusted_unit_price = adjusted_price
            else:
                # If no rule, use base price
                line.quality_adjusted_unit_price = line.base_unit_price or line.price_unit

    @api.onchange('quality_pricing_rule_id', 'quality_protein_content',
                  'quality_moisture_content', 'quality_impurities_rate')
    def onchange_quality_metrics(self):
        """Update price when quality metrics change"""
        if self.quality_pricing_rule_id:
            # Update the computed fields
            quality_results = {
                'protein_content': self.quality_protein_content or 0,
                'moisture_content': self.quality_moisture_content or 0,
                'impurities_rate': self.quality_impurities_rate or 0,
            }
            self.quality_adjusted_unit_price = self.quality_pricing_rule_id.calculate_acquisition_price(quality_results)

    def action_apply_quality_pricing(self):
        """Apply quality-based pricing to this line"""
        for line in self:
            if line.quality_pricing_rule_id:
                # Apply the quality adjusted price to the actual purchase price
                line.price_unit = line.quality_adjusted_unit_price
                line.order_id.message_post(
                    body=f"Applied quality-based pricing to line: {line.product_id.name}. "
                         f"Adjusted price: {line.quality_adjusted_unit_price} from base: {line.base_unit_price}"
                )


class PurchaseOrder(models.Model):
    """
    Extension of purchase order to support quality-based acquisition pricing [US-009-19]
    """
    _inherit = 'purchase.order'

    # Fields for acquisition scenarios - US-009-19 Quality-based pricing
    quality_based_pricing_enabled = fields.Boolean(
        "Quality-Based Pricing Enabled",
        help="Enable quality-based pricing adjustments for this order"
    )
    acquisition_pricing_rules = fields.One2many(
        'quality.based.pricing', 'purchase_order_id',
        string="Acquisition Pricing Rules"
    )
    total_pricing_adjustments = fields.Float(
        "Total Quality Adjustments",
        compute='_compute_total_pricing_adjustments',
        store=True,
        help="Total adjustments based on quality metrics"
    )

    @api.depends('order_line.price_subtotal', 'order_line.quality_adjustment_amount')
    def _compute_total_pricing_adjustments(self):
        """Compute total quality-based pricing adjustments for the purchase order"""
        for order in self:
            # Calculate the sum of all quality adjustments for all order lines
            total = sum(line.quality_adjustment_amount for line in order.order_line)
            order.total_pricing_adjustments = total

    def action_apply_quality_based_pricing(self):
        """
        US-009-19: Apply quality-based pricing when purchase order is confirmed.
        This method automatically calculates pricing based on quality check results
        """
        for order in self:
            for line in order.order_line:
                # Process quality checks associated with this line
                for quality_check in line.quality_check_ids:
                    if quality_check.quality_state == 'pass' and quality_check.measure:
                        # Use the quality-based pricing rules to calculate adjustments
                        pricing_rules = self.env['quality.based.pricing'].search([
                            ('product_category_id', '=', line.product_id.categ_id.id)
                        ])
                        if pricing_rules:
                            rule = pricing_rules[0]  # Use first applicable rule
                            adjusted_price = rule.calculate_adjusted_price(quality_check.measure, line.price_unit)

                            # Update the line's price and quality grade
                            line.price_unit = adjusted_price

                            # Calculate the quality grade based on the measurement
                            calculated_grade = rule.calculate_quality_grade_from_value(quality_check.measure)
                            grade_mapping = {
                                'premium': 'grade_a',
                                'standard': 'grade_b',
                                'economy': 'grade_c',
                                'reject': 'grade_d'
                            }
                            line.quality_grade = grade_mapping.get(calculated_grade)

            # Update the total adjustments
            order._compute_total_pricing_adjustments()

    def action_apply_quality_pricing_to_all_lines(self):
        """Apply quality-based pricing to all order lines"""
        for order in self:
            for line in order.order_line:
                line.action_apply_quality_pricing()

            order.message_post(body="Applied quality-based pricing to all order lines.")