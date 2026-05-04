from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class FarmSupplyRiskMonitor(models.Model):
    _name = 'farm.supply.risk.monitor'
    _description = 'Supply Chain Risk Monitoring'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Risk Event", required=True)
    risk_category = fields.Selection([
        ('logistics', 'Transport Disruption'),
        ('quality', 'Batch Quality Recall'),
        ('supplier', 'Supplier Default'),
        ('weather', 'Climate Impact'),
        ('market', 'Market Price Volatility'),
        ('demand', 'Demand Fluctuation'),
        ('inventory', 'Inventory Shortage'),
        ('production', 'Production Disruption'),
    ], string="Risk Type", required=True)

    risk_level = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ], string="Risk Level", required=True, default='medium')

    probability = fields.Float("Probability %", help="Estimated probability of this risk occurring")
    impact_score = fields.Float("Impact Score", help="Quantitative impact score (1-10 scale)")
    risk_score = fields.Float("Risk Score", compute='_compute_risk_score', store=True, precompute=True)

    affected_node_ids = fields.Many2many('farm.supply.chain.node', string="Affected Nodes")
    affected_products = fields.Many2many('product.product', string="Affected Products")

    detection_date = fields.Datetime("Detection Date", default=fields.Datetime.now)
    mitigation_plan = fields.Text("Emergency Response Plan")
    mitigation_owner_id = fields.Many2one('res.users', string="Mitigation Owner")

    state = fields.Selection([
        ('identified', 'Risk Identified'),
        ('assessed', 'Risk Assessed'),
        ('active', 'Active Impact'),
        ('mitigated', 'Mitigated'),
        ('closed', 'Resolved'),
    ], default='identified', tracking=True)

    # Timeline
    expected_occurrence_date = fields.Date("Expected Occurrence Date")
    actual_occurrence_date = fields.Date("Actual Occurrence Date")
    mitigation_target_date = fields.Date("Target Mitigation Date")

    @api.depends('probability', 'impact_score')
    def _compute_risk_score(self):
        """Calculate risk score as probability * impact"""
        for record in self:
            if record.probability and record.impact_score:
                record.risk_score = (record.probability / 100) * record.impact_score
            else:
                record.risk_score = 0.0

    @api.onchange('risk_category')
    def onchange_risk_category(self):
        """Set default values based on risk category"""
        if self.risk_category == 'weather':
            self.risk_level = 'high'
            self.probability = 30.0
            self.impact_score = 8.0
        elif self.risk_category == 'supplier':
            self.risk_level = 'medium'
            self.probability = 15.0
            self.impact_score = 6.0
        elif self.risk_category == 'logistics':
            self.risk_level = 'medium'
            self.probability = 20.0
            self.impact_score = 7.0

    @api.constrains('probability')
    def _check_probability_range(self):
        for record in self:
            if record.probability < 0 or record.probability > 100:
                raise ValidationError(_("Probability must be between 0 and 100."))

    def action_assess_risk(self):
        """Assess the identified risk"""
        self.write({
            'state': 'assessed',
            'detection_date': fields.Datetime.now()
        })

    def action_trigger_alert(self):
        """US-084-03: Real-time Risk Alerting"""
        self.ensure_one()
        for node in self.affected_node_ids:
            node.message_post(body=_("RISK ALERT: '%s' impact detected on this node. Risk level: %s, Score: %.2f") % (
                self.name, self.risk_level, self.risk_score))

        # Send notifications to mitigation owner
        if self.mitigation_owner_id:
            self.message_post(
                body=_("Risk alert sent to mitigation owner: %s") % self.mitigation_owner_id.name,
                partner_ids=[self.mitigation_owner_id.partner_id.id]
            )

    def action_activate_risk(self):
        """Mark risk as active (has occurred)"""
        self.write({
            'state': 'active',
            'actual_occurrence_date': fields.Date.today()
        })

    def action_mitigate_risk(self):
        """Mark risk as mitigated"""
        self.write({
            'state': 'mitigated',
            'mitigation_target_date': fields.Date.today()
        })

    def action_close_risk(self):
        """Close the risk record"""
        self.write({
            'state': 'closed'
        })


class SupplyChainRiskDashboard(models.Model):
    """
    Supply Chain Risk Dashboard [US-084-03]
    """
    _name = 'supply.chain.risk.dashboard'
    _description = 'Supply Chain Risk Dashboard'
    currency_id = fields.Many2one("res.currency", string="Currency", default=lambda self: self.env.company.currency_id)

    name = fields.Char('Dashboard Name', required=True)
    refresh_date = fields.Datetime('Last Refresh', default=fields.Datetime.now)

    # KPIs
    total_risks = fields.Integer('Total Risks', compute='_compute_risk_kpis')
    active_risks = fields.Integer('Active Risks', compute='_compute_risk_kpis')
    high_risks = fields.Integer('High/Critical Risks', compute='_compute_risk_kpis')
    avg_risk_score = fields.Float('Average Risk Score', compute='_compute_risk_kpis')

    # Affected values
    affected_inventory_value = fields.Monetary('Affected Inventory Value', compute='_compute_impact')
    affected_order_value = fields.Monetary('Affected Order Value', compute='_compute_impact')

    # Visualization data
    risk_by_category = fields.Text('Risk by Category', compute='_compute_visualization_data')
    risk_timeline = fields.Text('Risk Timeline', compute='_compute_visualization_data')

    @api.depends('refresh_date')
    def _compute_risk_kpis(self):
        for dashboard in self:
            all_risks = self.env['farm.supply.risk.monitor'].search([])
            dashboard.total_risks = len(all_risks)
            dashboard.active_risks = len(all_risks.filtered(lambda r: r.state == 'active'))
            dashboard.high_risks = len(all_risks.filtered(lambda r: r.risk_level in ['high', 'critical']))
            dashboard.avg_risk_score = sum(r.risk_score for r in all_risks) / len(all_risks) if all_risks else 0.0

    @api.depends('refresh_date')
    def _compute_impact(self):
        for dashboard in self:
            active_risks = self.env['farm.supply.risk.monitor'].search([('state', '=', 'active')])
            # Calculate affected inventory based on affected products
            affected_products = active_risks.mapped('affected_products')
            dashboard.affected_inventory_value = sum(
                prod.qty_available * prod.standard_price for prod in affected_products
            )
            # Calculate affected order value
            affected_order_lines = self.env['sale.order.line'].search([
                ('product_id', 'in', affected_products.ids)
            ])
            dashboard.affected_order_value = sum(line.price_subtotal for line in affected_order_lines)

    @api.depends('refresh_date')
    def _compute_visualization_data(self):
        for dashboard in self:
            # Risk by category for visualization
            risks = self.env['farm.supply.risk.monitor'].search([])
            category_counts = {}
            for risk in risks:
                category = risk.risk_category or 'unknown'
                category_counts[category] = category_counts.get(category, 0) + 1
            dashboard.risk_by_category = str(category_counts)

            # Basic timeline data
            import json
            from datetime import datetime, timedelta
            dates = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]
            dashboard.risk_timeline = json.dumps({
                'labels': dates,
                'data': [len(risks.filtered(lambda r, d=dates[6-i]: str(r.detection_date or r.create_date)[:10] == d))
                        for i in range(7)]
            })