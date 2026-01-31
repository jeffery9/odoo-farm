from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class SustainabilityMixin(models.AbstractModel):
    """
    Mixin for Sustainability-First value standard.
    Level 0: Carbon & ESG Validation
    """
    _name = 'agri.sustainability.mixin'
    _description = 'Sustainability-First Metric Mixin'

    carbon_intensity = fields.Float(
        string="Carbon Footprint (kg CO2e/kg)",
        digits=(12, 4),
        help="Estimated carbon footprint per unit of output."
    )
    esg_score = fields.Integer(
        string="ESG Impact Score",
        default=100,
        help="Dynamic ESG score (0-1000) calculated by community impact."
    )
    credit_score = fields.Integer(
        string="Reputation Credit Score",
        compute="_compute_reputation_credit_score",
        store=True,
        help="Community reputation score (0-1000). Derived from confirmed transaction ledger entries."
    )
    is_eco_blocked = fields.Boolean(
        string="Sustainability Block",
        default=False,
        copy=False
    )

    @api.depends('is_eco_blocked') # Dependent on a trigger, effectively recomputed on ledger confirmation
    def _compute_reputation_credit_score(self):
        """
        [Level 3+: Transaction Pattern with Human Audit]
        Only sums ledger entries in 'confirmed' state.
        """
        for record in self:
            partner = False
            if record._name == 'res.partner':
                partner = record
            elif hasattr(record, 'partner_id') and record.partner_id:
                partner = record.partner_id
            
            if partner:
                entries = self.env['agri.clearing.ledger'].search([
                    ('partner_id', '=', partner.id),
                    ('state', '=', 'confirmed')
                ])
                record.credit_score = 500 + sum(entries.mapped('score_change'))
            else:
                record.credit_score = 500

    def pre_validate_sustainability(self, vals):
        """
        Hook to validate sustainability impact before commit.
        Environmental "negative" actions trigger system-level blocks.
        """
        carbon = vals.get('carbon_intensity') or self.carbon_intensity
        if carbon > 50.0:
            raise ValidationError(_(
                "Sustainability Redline: This operation exceeds the maximum carbon intensity "
                "threshold and has been blocked to protect community ESG standards."
            ))
        return True

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            self.pre_validate_sustainability(vals)
        return super().create(vals_list)

    def write(self, vals):
        self.pre_validate_sustainability(vals)
        return super().write(vals)


class CreationMethodMixin(models.AbstractModel):
    """
    Mixin to add common creation method that handles sequence generation
    """
    _name = 'farm.core.creation.method.mixin'
    _description = 'Farm Core Creation Method Mixin'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', '/') == '/' or vals.get('name', fields._('New')) == fields._('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code(self._name.replace('.', '_')) or '/'
        return super().create(vals_list)


class ComputedFieldMixin(models.AbstractModel):
    """
    Mixin to provide common computed field patterns
    """
    _name = 'farm.core.computed.field.mixin'
    _description = 'Farm Core Computed Field Mixin'

    @api.depends('create_date')
    def _compute_age_days(self):
        """Compute age in days from create date"""
        from datetime import datetime
        for record in self:
            if record.create_date:
                create_date = fields.Date.from_string(fields.Datetime.to_date(record.create_date))
                today = fields.Date.today()
                delta = today - create_date
                record.age_days = delta.days
            else:
                record.age_days = 0

    @api.depends('age_days')
    def _compute_is_mature(self):
        """Compute if an entity is mature based on age"""
        for record in self:
            record.is_mature = record.age_days >= getattr(record, 'maturity_threshold_days', 0)


class ComplianceMixin(models.AbstractModel):
    """
    Mixin for common compliance and safety features
    """
    _name = 'farm.core.compliance.mixin'
    _description = 'Farm Core Compliance Mixin'

    # Withdrawal period management
    withdrawal_end_datetime = fields.Datetime("Safe Period End", help="End date for withdrawal period.")
    is_safe_for_harvest = fields.Boolean("Is Safe", compute='_compute_is_safe', store=True)
    withdrawal_days_remaining = fields.Integer("Days Remaining", compute='_compute_withdrawal_days', store=True)

    @api.depends('withdrawal_end_datetime')
    def _compute_is_safe(self):
        """Compute if entity is safe for harvest"""
        now = fields.Datetime.now()
        for record in self:
            record.is_safe_for_harvest = not record.withdrawal_end_datetime or record.withdrawal_end_datetime <= now

    @api.depends('withdrawal_end_datetime')
    def _compute_withdrawal_days(self):
        """Compute remaining withdrawal days"""
        now = fields.Datetime.now()
        for record in self:
            if record.withdrawal_end_datetime and record.withdrawal_end_datetime > now:
                delta = record.withdrawal_end_datetime - now
                record.withdrawal_days_remaining = max(0, delta.days + 1)
            else:
                record.withdrawal_days_remaining = 0

    # Health/quality state management
    health_state = fields.Selection([
        ('healthy', 'Healthy'),
        ('quarantine', 'Quarantine'),
        ('disposed', 'Disposed'),
        ('locked', 'Locked')
    ], string="Health State", default='healthy', tracking=True)

    @api.onchange('quality_status')
    def _onchange_quality_status_lock(self):
        """Lock entity when quality fails"""
        for record in self:
            if hasattr(record, 'quality_status') and record.quality_status == 'failed':
                record.health_state = 'locked'
