from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class FarmAgritourismOperation(models.Model):
    """
    Agritourism operation model for managing activities, visitor experiences, and resource planning
    """
    _name = 'farm.agritourism.operation'
    _description = 'Farm Agritourism Operation'
    _inherit = 'project.task'  # Inherit from project.task to leverage existing task functionality

    # Agritourism Activity Information
    activity_type = fields.Selection([
        ('picking', 'Picking Activity'),
        ('family_event', 'Family Event'),
        ('adoption', 'Plot/Animal Adoption'),
        ('educational', 'Educational Tour'),
        ('seasonal_festival', 'Seasonal Festival'),
        ('farm_to_table', 'Farm-to-Table Experience'),
        ('workshop', 'Workshop/Course'),
    ], string='Activity Type', required=True)
    activity_code = fields.Char('Activity Code', compute='_compute_activity_code', store=True)

    # Visitor Management
    visitor_count = fields.Integer('Planned Visitor Count')
    actual_visitor_count = fields.Integer('Actual Visitor Count')
    visitor_age_distribution = fields.Text('Visitor Age Distribution')
    visitor_special_needs = fields.Text('Special Needs/Requirements')

    # Resource and Calendar Management
    resource_usage_ids = fields.One2many('farm.resource.usage', 'agritourism_operation_id', string='Resource Usage')
    activity_date = fields.Date('Activity Date', required=True)
    activity_start_time = fields.Float('Start Time')
    activity_end_time = fields.Float('End Time')
    requires_reservation = fields.Boolean('Requires Reservation', default=True)

    # Safety and Compliance
    safety_measures = fields.Text('Safety Measures')
    emergency_contact = fields.Char('Emergency Contact')
    insurance_coverage = fields.Char('Insurance Coverage Information')
    risk_assessment_completed = fields.Boolean('Risk Assessment Completed')

    # Member and Loyalty Program Integration
    member_discount_applied = fields.Boolean('Member Discount Applied')
    membership_tier = fields.Selection([
        ('basic', 'Basic'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
        ('platinum', 'Platinum'),
    ], string='Membership Tier')
    loyalty_points_earned = fields.Integer('Loyalty Points Earned')

    # Experience Quality Management
    experience_quality_score = fields.Float('Experience Quality Score (1-5)', digits=(2, 1))
    guest_feedback = fields.Text('Guest Feedback')
    improvement_suggestions = fields.Text('Improvement Suggestions')

    # Seasonal and Weather Considerations
    weather_suitable = fields.Boolean('Weather Suitable', compute='_compute_weather_suitable', store=True)
    weather_impact_notes = fields.Text('Weather Impact Notes')
    backup_plan = fields.Text('Backup Plan for Inclement Weather')

    # Agritourism specific stages
    agritourism_stage = fields.Selection([
        ('planning', 'Planning'),
        ('resource_calendar_setup', 'Resource & Calendar Setup'),
        ('activity_promotion', 'Activity Promotion'),
        ('booking_management', 'Booking Management'),
        ('visitor_preparation', 'Visitor Preparation'),
        ('activity_execution', 'Activity Execution'),
        ('on_site_service', 'On-site Service'),
        ('product_sales', 'Product Sales'),
        ('feedback_collection', 'Feedback Collection'),
        ('activity_evaluation', 'Activity Evaluation'),
        ('optimization', 'Optimization'),
    ], string='Agritourism Stage', default='planning')

    # Experience Sales Integration
    related_sale_orders = fields.Many2many('sale.order', string='Related Sale Orders')
    merchandise_sales = fields.Float('Merchandise Sales (¥)', compute='_compute_revenue', store=True)
    food_beverage_sales = fields.Float('Food & Beverage Sales (¥)', compute='_compute_revenue', store=True)
    total_revenue = fields.Float('Total Revenue (¥)', compute='_compute_revenue', store=True)

    @api.depends('name', 'activity_type')
    def _compute_activity_code(self):
        """Compute activity code based on activity type and date"""
        for record in self:
            if record.activity_type and record.activity_date:
                type_code = record.activity_type[:3].upper()
                date_str = fields.Date.from_string(record.activity_date).strftime('%Y%m%d')
                record.activity_code = f"AT-{type_code}-{date_str}-{record.id:04d}"
            else:
                record.activity_code = "AT-NEW-0000"

    @api.depends('activity_date')  # In a real system, would integrate with weather API
    def _compute_weather_suitable(self):
        """Compute if weather is suitable for activity (placeholder)"""
        for record in self:
            record.weather_suitable = True  # Default to True, would be computed from actual weather data

    @api.depends('merchandise_sales', 'food_beverage_sales')
    def _compute_revenue(self):
        """Compute revenue from various sources"""
        for record in self:
            # This would be calculated from related sales orders and point-of-sale transactions
            record.merchandise_sales = record.merchandise_sales or 0.0
            record.food_beverage_sales = record.food_beverage_sales or 0.0
            record.total_revenue = record.merchandise_sales + record.food_beverage_sales

    def action_update_visitor_count(self, count):
        """Update actual visitor count"""
        self.ensure_one()
        self.write({'actual_visitor_count': count})
        self.message_post(body=_("Visitor count updated to: %s") % count)
        return True

    def action_record_feedback(self, quality_score, feedback, suggestions=None):
        """Record guest feedback and experience quality"""
        self.ensure_one()
        self.write({
            'experience_quality_score': quality_score,
            'guest_feedback': feedback,
            'improvement_suggestions': suggestions
        })

        body = _("FEEDBACK RECORDED: Quality score %s/5. Feedback: %s %s") % (
            quality_score, feedback, f"Suggestions: {suggestions}" if suggestions else "")
        self.message_post(body=body)
        return True

    def action_schedule_activity(self, activity_date, start_time, end_time, visitor_count):
        """Schedule the agritourism activity"""
        self.ensure_one()
        self.write({
            'activity_date': activity_date,
            'activity_start_time': start_time,
            'activity_end_time': end_time,
            'visitor_count': visitor_count
        })

        body = _("ACTIVITY SCHEDULED: %s from %.2f to %.2f. Expected visitors: %s") % (
            activity_date, start_time, end_time, visitor_count)
        self.message_post(body=body)
        return True

    def action_complete_activity(self):
        """Mark activity as completed and collect feedback"""
        self.ensure_one()
        self.write({'agritourism_stage': 'feedback_collection'})
        self.message_post(body=_("Activity completed. Ready for feedback collection."))
        return True

    def action_calculate_loyalty_points(self, base_points=10):
        """Calculate and award loyalty points"""
        self.ensure_one()
        # Calculate points based on activity type, visitor count, and spending
        points = base_points
        if self.activity_type in ['seasonal_festival', 'farm_to_table']:
            points *= 2  # Bonus for premium activities
        if self.actual_visitor_count > 10:
            points += 5  # Bonus for group activities

        self.write({'loyalty_points_earned': points})
        self.message_post(body=_("Loyalty points awarded: %s points") % points)
        return points


class FarmResourceUsage(models.Model):
    """
    Track resource usage for agritourism activities
    """
    _name = 'farm.resource.usage'
    _description = 'Farm Resource Usage for Agritourism'

    agritourism_operation_id = fields.Many2one('farm.agritourism.operation', string='Agritourism Operation', required=True)
    resource_id = fields.Many2one('farm.resource', string='Resource', required=True)
    usage_start_time = fields.Float('Usage Start Time')
    usage_end_time = fields.Float('Usage End Time')
    assigned_staff = fields.Many2one('hr.employee', string='Assigned Staff')
    usage_notes = fields.Text('Usage Notes')