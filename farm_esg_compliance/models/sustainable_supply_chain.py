from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class AgriSustainableSupplyChain(models.Model):
    """
    US-101-04: Sustainable Supply Chain Management
    Model for managing the sustainability of the entire supply chain, ensuring partners meet triple bottom line requirements.
    """
    _name = 'agri.sustainable.supply.chain'
    _description = 'Agricultural Sustainable Supply Chain'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Supply Chain Name', required=True)
    description = fields.Text('Description')

    # Triple bottom line performance tracking
    economic_score = fields.Float('Economic Score (0-100)')
    environmental_score = fields.Float('Environmental Score (0-100)')
    social_score = fields.Float('Social Score (0-100)')
    overall_sustainability_score = fields.Float('Overall Score (0-100)', compute='_compute_overall_score', store=True)

    # Related supplier
    partner_id = fields.Many2one('res.partner', string='Supplier/Partner', required=True)
    partner_credit_score = fields.Integer('Partner Credit Score',
                                         help='Credit score from A2A protocol verification')

    # Supply chain assessment
    sustainability_assessment_date = fields.Date('Last Assessment Date')
    sustainability_assessment_result = fields.Text('Assessment Result')
    certification_ids = fields.Many2many('farm.certification', string='Sustainability Certifications')

    # Monitoring
    monitoring_frequency = fields.Selection([
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('annually', 'Annually'),
    ], string='Monitoring Frequency', default='quarterly')

    next_monitoring_date = fields.Date('Next Monitoring Date')

    # Performance metrics
    delivery_performance = fields.Float('Delivery Performance (%)')
    quality_performance = fields.Float('Quality Performance (%)')
    sustainability_compliance = fields.Float('Sustainability Compliance (%)')

    # Status
    status = fields.Selection([
        ('prospective', 'Prospective'),
        ('approved', 'Approved'),
        ('monitoring', 'In Monitoring'),
        ('suspended', 'Suspended'),
        ('deactivated', 'Deactivated'),
    ], string='Status', default='prospective')

    # Integration with procurement
    procurement_policy = fields.Text('Procurement Policy')
    dynamic_authorization_rules = fields.Text('Dynamic Authorization Rules')

    # Integration with other models
    farm_id = fields.Many2one('farm.location', string='Farm Location')
    related_product_ids = fields.Many2many('product.template', string='Related Products')

    @api.depends('economic_score', 'environmental_score', 'social_score')
    def _compute_overall_score(self):
        for record in self:
            if record.economic_score and record.environmental_score and record.social_score:
                record.overall_sustainability_score = (record.economic_score +
                                                      record.environmental_score +
                                                      record.social_score) / 3
            else:
                record.overall_sustainability_score = 0.0

    def action_assess_supplier_sustainability(self):
        """Assess the sustainability performance of the supplier"""
        for record in self:
            # This would integrate with actual supplier data and assessment tools
            # For now, we'll create a basic assessment based on available fields
            assessment = f"""
Supply Chain Sustainability Assessment for {record.partner_id.name}

Economic Assessment:
- Delivery Performance: {record.delivery_performance}%
- Quality Performance: {record.quality_performance}%
- Economic Score: {record.economic_score}/100

Environmental Assessment:
- Sustainability Compliance: {record.sustainability_compliance}%
- Environmental Score: {record.environmental_score}/100
- Certifications: {len(record.certification_ids)} active certifications

Social Assessment:
- Social Score: {record.social_score}/100
- Partner Credit Score: {record.partner_credit_score}

Overall Sustainability Score: {record.overall_sustainability_score}/100
            """
            record.sustainability_assessment_result = assessment
            record.sustainability_assessment_date = fields.Date.context_today(record)

    def action_approve_supplier(self):
        """Approve supplier after A2A protocol verification [US-101-04]"""
        for record in self:
            # 1. Verify partner credit score via A2A Algorithm
            algo = self.env['agri.sustainability.algorithms']
            record.partner_credit_score = algo.verify_a2a_agent_credit(record.partner_id.id)
            
            if record.partner_credit_score < 600:
                raise ValidationError(_("Supplier's A2A Agent Credit Score (%s) is below threshold.") % record.partner_credit_score)

            # 2. Check certifications
            if not record.certification_ids:
                raise ValidationError(_("Supplier must have at least one sustainability certification."))

            record.status = 'approved'
            record.message_post(body=_("Supplier approved after A2A protocol Agent-KYC check. Score: %s") % record.partner_credit_score)

    def action_monitor_supply_chain(self):
        """Monitor the supply chain performance"""
        for record in self:
            # Create monitoring activities
            record.next_monitoring_date = fields.Date.add(
                fields.Date.context_today(record),
                months=3 if record.monitoring_frequency == 'quarterly' else
                       1 if record.monitoring_frequency == 'monthly' else
                       7 if record.monitoring_frequency == 'weekly' else 12
            )

            # Update performance metrics (in real implementation, this would come from actual data)
            record.delivery_performance = 95.0  # Example value
            record.quality_performance = 98.0  # Example value
            record.sustainability_compliance = 92.0  # Example value

    def action_suspend_supplier(self):
        """Suspend supplier due to non-compliance"""
        self.write({'status': 'suspended'})

    def action_deactivate_supplier(self):
        """Deactivate supplier relationship"""
        self.write({'status': 'deactivated'})

    def action_update_procurement_policy(self):
        """Update procurement policy based on sustainability requirements"""
        for record in self:
            policy = f"""
Procurement Policy for {record.name}

- Only suppliers with overall sustainability score >= 70 are eligible
- Required certifications: {', '.join(cert.name for cert in record.certification_ids)}
- Monitoring frequency: {record.monitoring_frequency}
- Minimum credit score: 600
- Performance thresholds: Delivery >= 90%, Quality >= 95%, Sustainability >= 85%
            """
            record.procurement_policy = policy


class AgriSustainableSupplierEvaluation(models.Model):
    """
    Additional model for detailed supplier evaluation based on triple bottom line
    """
    _name = 'agri.sustainable.supplier.evaluation'
    _description = 'Agricultural Sustainable Supplier Evaluation'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Evaluation Name', required=True)
    evaluation_date = fields.Date('Evaluation Date', required=True, default=fields.Date.context_today)
    supply_chain_id = fields.Many2one('agri.sustainable.supply.chain', string='Supply Chain', required=True)

    # Detailed scores
    economic_criteria_score = fields.Float('Economic Criteria Score (0-100)')
    environmental_criteria_score = fields.Float('Environmental Criteria Score (0-100)')
    social_criteria_score = fields.Float('Social Criteria Score (0-100)')
    overall_evaluation_score = fields.Float('Overall Score (0-100)', compute='_compute_overall_score', store=True)

    # Evaluation details
    evaluation_details = fields.Text('Evaluation Details')
    recommendations = fields.Text('Recommendations')
    evaluation_by = fields.Many2one('res.users', string='Evaluated By', default=lambda self: self.env.user)

    # Compliance check
    is_compliant = fields.Boolean('Is Compliant', compute='_compute_compliance', store=True)

    @api.depends('economic_criteria_score', 'environmental_criteria_score', 'social_criteria_score')
    def _compute_overall_score(self):
        for record in self:
            if record.economic_criteria_score and record.environmental_criteria_score and record.social_criteria_score:
                record.overall_evaluation_score = (record.economic_criteria_score +
                                                  record.environmental_criteria_score +
                                                  record.social_criteria_score) / 3
            else:
                record.overall_evaluation_score = 0.0

    @api.depends('overall_evaluation_score')
    def _compute_compliance(self):
        for record in self:
            record.is_compliant = record.overall_evaluation_score >= 70.0  # 70% threshold for compliance

    @api.model
    def create(self, vals):
        record = super().create(vals)
        # Trigger supply chain update
        if record.supply_chain_id:
            record.supply_chain_id.action_assess_supplier_sustainability()
        return record