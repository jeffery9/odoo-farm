from odoo import models, fields, api, _
import random
import logging

_logger = logging.getLogger(__name__)


class ProjectTask(models.Model):
    _inherit = 'project.task'

    trust_score = fields.Float("Trust Score", digits=(10, 2), default=0.0,
                               help="Evidence-based trust score (0-100) [US-48-01]")
    trust_verification_status = fields.Selection([
        ('pending', 'Pending Verification'),
        ('verified', 'Verified'),
        ('suspicious', 'Suspicious'),
        ('fraud', 'Likely Fraud')
    ], string="Trust Status", default='pending')

    def action_calculate_trust_score(self):
        """
        US-48-01: Task Evidence Scoring Algorithm
        """
        for task in self:
            score = 100.0
            reasons = []

            # 1. GPS Verification (Spatial Evidence)
            if hasattr(task, 'land_parcel_id') and task.land_parcel_id and hasattr(task, 'operation_lng'):
                if task.operation_lng and task.operation_lat:
                    is_inside = task.land_parcel_id.is_point_in_polygon(
                        task.land_parcel_id.boundary_geojson,
                        task.operation_lng,
                        task.operation_lat
                    )
                    if not is_inside:
                        score -= 40.0
                        reasons.append("Coordinates outside land parcel.")
                else:
                    score -= 10.0
                    reasons.append("Missing GPS evidence.")

            # 2. Weather Consistency (Contextual Evidence)
            # Simulated: If task is 'spraying' and weather was 'rainy'
            # In a real system, we'd query farm.weather.log
            if task.name and "spray" in task.name.lower():
                # Mock check: random suspicion
                if random.random() < 0.05:
                    score -= 30.0
                    reasons.append("Weather inconsistency (Rain reported during spraying).")

            # 3. Time Consistency (Temporal Evidence)
            # Check if duration is physically possible
            if task.planned_hours and task.planned_hours > 24:
                score -= 15.0
                reasons.append("Duration exceeds 24h limit for single intervention.")

            task.trust_score = max(0.0, score)
            if task.trust_score > 80:
                task.trust_verification_status = 'verified'
            elif task.trust_score > 40:
                task.trust_verification_status = 'suspicious'
            else:
                task.trust_verification_status = 'fraud'


class FarmCreditScore(models.Model):
    _name = 'farm.credit.score'
    _description = 'Farm Production Credit Score'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    partner_id = fields.Many2one('res.partner', string="Farmer/Entity", required=True)
    evaluation_date = fields.Date("Evaluation Date", default=fields.Date.today)

    total_score = fields.Float("Total Credit Score", compute='_compute_credit_score', store=True)

    # Weight components [US-48-02]
    gap_compliance_rate = fields.Float("GAP Compliance (%)", help="Weight: 30%")
    yield_consistency_rate = fields.Float("Yield Consistency (%)", help="Weight: 30%")
    input_reduction_rate = fields.Float("Input Reduction (%)", help="Weight: 20%")
    avg_trust_score = fields.Float("Average Evidence Trust", help="Weight: 20%")

    @api.depends('gap_compliance_rate', 'yield_consistency_rate', 'input_reduction_rate', 'avg_trust_score')
    def _compute_credit_score(self):
        """
        US-48-02: Farm Credit Score Algorithm
        Score = [GAP (30%)] + [Yield (30%)] + [Input Red (20%)] + [Trust (20%)]
        """
        for rec in self:
            rec.total_score = (
                (rec.gap_compliance_rate * 0.3) +
                (rec.yield_consistency_rate * 0.3) +
                (rec.input_reduction_rate * 0.2) +
                (rec.avg_trust_score * 0.2)
            )

    def action_auto_evaluate(self):
        """Fetch real data to populate the rates"""
        self.ensure_one()
        # 1. Fetch avg trust score from tasks
        tasks = self.env['project.task'].search([('partner_id', '=', self.partner_id.id)])
        if tasks:
            self.avg_trust_score = sum(tasks.mapped('trust_score')) / len(tasks)

        # 2. Mock GAP and others for now
        self.gap_compliance_rate = random.uniform(70, 95)
        self.yield_consistency_rate = random.uniform(60, 90)
        self.input_reduction_rate = random.uniform(50, 85)
        self._compute_credit_score()


class ResPartner(models.Model):
    _inherit = 'res.partner'

    latest_credit_score = fields.Float("Latest Credit Score", compute='_compute_latest_credit_score')
    is_high_risk_borrower = fields.Boolean("High Risk Borrower", compute='_compute_latest_credit_score')

    def _compute_latest_credit_score(self):
        for partner in self:
            latest = self.env['farm.credit.score'].search([
                ('partner_id', '=', partner.id),
                ('state', '=', 'valid')
            ], order='evaluation_date desc', limit=1)
            partner.latest_credit_score = latest.total_score if latest else 0.0
            partner.is_high_risk_borrower = partner.latest_credit_score < 70.0 and latest


class FarmCoopSettlement(models.Model):
    _name = 'farm.coop.settlement'
    _description = 'Cooperative Member Settlement'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    partner_id = fields.Many2one('res.partner', string="Member", required=True)
    date = fields.Date("Date", default=fields.Date.today)

    # Debt: Member takes inputs (seeds, fertilizer) without cash payment
    input_debt_amount = fields.Monetary("Input Debt", currency_field='currency_id',
                                       help="Accumulated debt for inputs advanced to member.")

    # Credit: Member delivers harvest to the coop
    harvest_credit_amount = fields.Monetary("Harvest Credit", currency_field='currency_id',
                                           help="Value of harvest delivered by member.")

    net_settlement_amount = fields.Monetary("Net Payout", compute='_compute_net_amount', store=True)

    @api.depends('input_debt_amount', 'harvest_credit_amount')
    def _compute_net_amount(self):
        """US-48-04: Automated Netting Algorithm"""
        for rec in self:
            rec.net_settlement_amount = rec.harvest_credit_amount - rec.input_debt_amount

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', '/') == '/':
                vals['name'] = self.env['ir.sequence'].next_by_code('farm.coop.settlement') or _('SETL')
        return super().create(vals_list)

    def action_fetch_data(self):
        """Fetch real debts (unpaid bills) and credits (unpaid sales/intake)"""
        self.ensure_one()
        # 1. Input Debt: Search for unpaid Vendor Bills (member as vendor? no, coop as vendor)
        # Assuming member buys from coop: Outgoing invoices unpaid
        invoices = self.env['account.move'].search([
            ('partner_id', '=', self.partner_id.id),
            ('move_type', '=', 'out_invoice'),
            ('payment_state', 'not in', ('paid', 'in_payment'))
        ])
        self.input_debt_amount = sum(invoices.mapped('amount_residual'))

        # 2. Harvest Credit: Search for unpaid Purchase Bills (coop buys from member)
        bills = self.env['account.move'].search([
            ('partner_id', '=', self.partner_id.id),
            ('move_type', '=', 'in_invoice'),
            ('payment_state', 'not in', ('paid', 'in_payment'))
        ])
        self.harvest_credit_amount = sum(bills.mapped('amount_residual'))
        self._compute_net_amount()

    def action_settle(self):
        """Execute the settlement - creating a netting journal entry or payment"""
        self.ensure_one()
        # Real implementation would involve Odoo payment reconciliation
        self.write({'state': 'posted'})