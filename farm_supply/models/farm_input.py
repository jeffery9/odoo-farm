from odoo import models, fields, api, _

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_agri_input = fields.Boolean("Is Agri Input", default=False)

    is_agri_input = fields.Boolean("Is Agri Input", default=False)
    input_type = fields.Selection([
        ('seed', 'Seed/Variety'),
        ('fertilizer', 'Fertilizer'),
        ('pesticide', 'Pesticide'),
        ('feed', 'Feed'),
        ('medicine', 'Medicine'),
        ('other', 'Other Supplies')
    ], string="Input Type")
    
    is_safety_approved = fields.Boolean("Safety Approved", default=True, help="Is this input compliant with organic/safety standards?")
    active_ingredient = fields.Char("Active Ingredient", help="e.g. Glyphosate, Nitrogen content")
    
    # 养分含量 [US-01-03]
    n_content = fields.Float("Nitrogen (%)", help="Nitrogen percentage")
    p_content = fields.Float("Phosphorus (%)", help="Phosphorus percentage")
    k_content = fields.Float("Potassium (%)", help="Potassium percentage")
    
    # 安全间隔期 [US-11-03]
    withdrawal_period_days = fields.Integer("Withdrawal Period (Days)", default=0, help="Days to wait before harvest/slaughter after using this input.")
    
    # 生长周期 [US-03-01]
    growth_cycle_days = fields.Integer("Growth Cycle (Days)", default=0, help="Typical duration from start to harvest.")

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        """ 检查生长周期提前期 [US-03-01] """
        for order in self:
            for line in order.order_line:
                product = line.product_id
                if product.growth_cycle_days > 0:
                    # 假定交付日期为 commitment_date 或 request_date
                    delivery_date = order.commitment_date or order.expected_date
                    if delivery_date:
                        delivery_date = fields.Date.to_date(delivery_date)
                        min_date = fields.Date.add(fields.Date.today(), days=product.growth_cycle_days)
                        if delivery_date < min_date:
                            # 发出警告（此处使用 message_post，因为 action_confirm 通常不适合抛出 UserError 阻止确认，除非非常严重）
                            order.message_post(body=_("WARNING: Lead time insufficient for product %s. Growth cycle is %s days, but delivery is scheduled in %s days.") % (
                                product.name, product.growth_cycle_days, (delivery_date - fields.Date.today()).days
                            ))
        return super(SaleOrder, self).action_confirm()

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    # Link to joint procurement for cooperative purchases
    joint_procurement_order_id = fields.Many2one(
        'joint.procurement.order',
        string="Joint Procurement Order",
        help="Link to cooperative/consortium procurement order"
    )

    # Fields for acquisition scenarios - US-09-19 Quality-based pricing
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

    agri_task_id = fields.Many2one(
        'project.task',
        string="Origin Agri Task",
        help="The specific production task that triggered this procurement."
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
        US-09-19: Apply quality-based pricing when purchase order is confirmed.
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

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'procurement_group_id' in vals and not vals.get('agri_task_id'):
                group = self.env['procurement.group'].browse(vals['procurement_group_id'])
                if hasattr(group, 'agri_task_id') and group.agri_task_id:
                    vals['agri_task_id'] = group.agri_task_id.id
        return super().create(vals_list)

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    # Quality-based pricing fields for acquisitions - US-09-19
    quality_check_ids = fields.One2many(
        'farm.quality.check', 'purchase_order_line_id',
        string="Quality Checks"
    )
    quality_grade = fields.Selection([
        ('grade_a', 'Grade A (Premium)'),
        ('grade_b', 'Grade B (Standard)'),
        ('grade_c', 'Grade C (Economy)'),
        ('grade_d', 'Grade D (Below Standard)'),
    ], string='Quality Grade', help="Quality grade based on lab results")
    quality_factor = fields.Float('Quality Factor', help="Multiplier based on quality grade")
    quality_adjustment_amount = fields.Float(
        'Quality Adjustment Amount',
        compute='_compute_quality_adjustment',
        store=True,
        help="Adjustment amount based on quality metrics"
    )
    quality_notes = fields.Text('Quality Notes')

    is_compliance_warning = fields.Boolean("Compliance Warning", compute='_compute_compliance_warning', store=True)

    @api.depends('product_id', 'quality_grade')
    def _compute_compliance_warning(self):
        for line in self:
            if line.product_id.is_agri_input and not line.product_id.is_safety_approved:
                line.is_compliance_warning = True
            else:
                line.is_compliance_warning = False

    @api.depends('quality_grade', 'product_id', 'price_unit', 'product_qty',
                 'quality_check_ids.measure', 'quality_check_ids.appearance_score',
                 'quality_check_ids.aroma_score', 'quality_check_ids.flavor_score',
                 'quality_check_ids.texture_score')
    def _compute_quality_adjustment(self):
        """Compute quality adjustment amount based on grade and base price"""
        for line in self:
            if line.price_unit > 0:
                # Enhanced quality calculation that considers specific attributes like protein content, etc.
                factor = 1.0

                # Use quality grade if available
                if line.quality_grade:
                    grade_factors = {
                        'grade_a': 1.3,  # Premium: +30%
                        'grade_b': 1.0,  # Standard: base price
                        'grade_c': 0.85,  # Economy: -15%
                        'grade_d': 0.6,   # Below standard: -40%
                    }
                    factor = grade_factors.get(line.quality_grade, 1.0)
                else:
                    # If no grade is set, calculate based on quality check values
                    # (e.g., protein content, impurity rate, moisture content)
                    quality_checks = line.quality_check_ids
                    if quality_checks:
                        # Calculate average of sensory scores if available
                        avg_sensory = 0
                        score_count = 0
                        for check in quality_checks:
                            total_score = 0
                            if check.appearance_score:
                                total_score += check.appearance_score
                                score_count += 1
                            if check.aroma_score:
                                total_score += check.aroma_score
                                score_count += 1
                            if check.flavor_score:
                                total_score += check.flavor_score
                                score_count += 1
                            if check.texture_score:
                                total_score += check.texture_score
                                score_count += 1

                            if score_count > 0:
                                avg_sensory = total_score / score_count / 10  # Normalize to 0-1 range

                        # Calculate based on measured values (like protein content, etc.)
                        measure_values = [check.measure for check in quality_checks if check.measure]
                        if measure_values:
                            avg_measure = sum(measure_values) / len(measure_values)
                            # Use quality-based pricing rules if available
                            pricing_rules = self.env['quality.based.pricing'].search([
                                ('product_category_id', '=', line.product_id.categ_id.id)
                            ])
                            if pricing_rules:
                                # Use the first applicable rule to calculate factor
                                rule = pricing_rules[0]
                                calculated_grade = rule.calculate_quality_grade_from_value(avg_measure)

                                grade_multipliers = {
                                    'premium': 1.3,
                                    'standard': 1.0,
                                    'economy': 0.8,
                                    'reject': 0.5
                                }
                                factor = grade_multipliers.get(calculated_grade, 1.0)
                            else:
                                # Fallback: adjust based on measured value directly
                                factor = avg_measure / 100.0 if avg_measure > 0 else 1.0  # Assuming 100 is baseline
                                factor = max(factor, 0.5)  # Minimum 50% of base price
                                factor = min(factor, 1.5)  # Maximum 150% of base price
                        elif avg_sensory > 0:
                            # Use sensory scores to determine factor
                            factor = avg_sensory
                        elif line.quality_grade:
                            # Use grade factors as fallback
                            grade_factors = {
                                'grade_a': 1.3,
                                'grade_b': 1.0,
                                'grade_c': 0.85,
                                'grade_d': 0.6,
                            }
                            factor = grade_factors.get(line.quality_grade, 1.0)

                line.quality_factor = factor
                # Adjustment amount is the difference between adjusted price and base price
                adjusted_price = line.price_unit * factor
                line.quality_adjustment_amount = (adjusted_price - line.price_unit) * line.product_qty
            else:
                line.quality_factor = 1.0
                line.quality_adjustment_amount = 0.0
