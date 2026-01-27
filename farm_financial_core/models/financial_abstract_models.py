from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class FinancialAbstractModel(models.AbstractModel):
    """
    Abstract base model for financial models in farm management system
    Provides common fields and methods for all financial-related models
    """
    _name = 'farm.financial.abstract'
    _description = 'Farm Financial Abstract Model'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # Common financial fields
    name = fields.Char("Reference", required=True)
    description = fields.Text("Description")
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)

    # Financial period and date tracking
    date = fields.Date("Date", default=fields.Date.today)
    period = fields.Char("Financial Period", help="Accounting period for this financial record")
    fiscal_year = fields.Char("Fiscal Year")

    # Amount fields with common patterns
    amount = fields.Monetary("Amount", currency_field='currency_id')
    amount_base = fields.Monetary("Base Amount", currency_field='currency_id', help="Base amount before adjustments")
    amount_adjusted = fields.Monetary("Adjusted Amount", currency_field='currency_id', compute='_compute_amount_adjusted')

    # Status and tracking
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('posted', 'Posted'),
        ('cancelled', 'Cancelled'),
    ], string="Status", default='draft', required=True)

    # Cost center or project allocation
    cost_center_id = fields.Many2one('account.analytic.account', string="Cost Center")
    project_id = fields.Many2one('project.project', string="Project")

    # Audit trail
    created_by = fields.Many2one('res.users', string="Created By", default=lambda self: self.env.user)
    created_date = fields.Datetime("Created Date", default=fields.Datetime.now)
    last_modified_by = fields.Many2one('res.users', string="Last Modified By", default=lambda self: self.env.user)
    last_modified_date = fields.Datetime("Last Modified", default=fields.Datetime.now)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', '/') == '/':
                vals['name'] = self.env['ir.sequence'].next_by_code('farm.financial.abstract') or '/'
        records = super().create(vals_list)
        return records

    def write(self, vals):
        if 'last_modified_by' not in vals:
            vals['last_modified_by'] = self.env.user.id
        if 'last_modified_date' not in vals:
            vals['last_modified_date'] = fields.Datetime.now()
        return super().write(vals)

    @api.depends('amount_base')
    def _compute_amount_adjusted(self):
        """Compute adjusted amount - can be overridden by child classes"""
        for record in self:
            record.amount_adjusted = record.amount_base

    def action_confirm(self):
        """Confirm the financial record"""
        self.write({'state': 'confirmed'})
        return True

    def action_post(self):
        """Post the financial record to accounting system"""
        self.write({'state': 'posted'})
        return True

    def action_cancel(self):
        """Cancel the financial record"""
        self.write({'state': 'cancelled'})
        return True

    def action_draft(self):
        """Reset to draft state"""
        self.write({'state': 'draft'})
        return True


class FinancialUtilityMixin(models.AbstractModel):
    """
    Mixin providing common financial utilities and calculations
    """
    _name = 'farm.financial.utility.mixin'
    _description = 'Farm Financial Utility Mixin'

    def _calculate_cost_per_unit(self, total_cost, quantity):
        """Calculate cost per unit"""
        if quantity and quantity != 0:
            return total_cost / quantity
        return 0.0

    def _calculate_percentage(self, partial_amount, total_amount):
        """Calculate percentage of partial amount relative to total"""
        if total_amount and total_amount != 0:
            return (partial_amount / total_amount) * 100
        return 0.0

    def _format_currency(self, amount, currency=None):
        """Format amount with proper currency formatting"""
        if not currency:
            currency = self.env.company.currency_id
        return f"{amount:,.2f} {currency.symbol}"

    def _get_account_by_code(self, code_pattern):
        """Get account by code pattern"""
        account_obj = self.env['account.account']
        return account_obj.search([
            ('code', '=like', code_pattern),
            ('company_id', '=', self.env.company.id)
        ], limit=1)

    def _create_journal_entry(self, move_vals):
        """Utility to create journal entry with error handling"""
        try:
            journal_entry = self.env['account.move'].create(move_vals)
            journal_entry.action_post()
            return journal_entry
        except Exception as e:
            _logger.error(f"Error creating journal entry: {e}")
            raise UserError(_("Error creating journal entry: %s", str(e)))

    def _validate_amount(self, amount):
        """Validate financial amount"""
        if amount < 0:
            raise UserError(_("Amount cannot be negative"))
        return True

    def _calculate_period_dates(self, period_code):
        """Calculate start and end dates for financial period"""
        # This is a simplified version - would need more sophisticated date handling
        from datetime import datetime, timedelta

        if period_code.lower().startswith('y'):
            # Yearly period format: Y2023
            year = int(period_code[1:])
            start_date = datetime(year, 1, 1).date()
            end_date = datetime(year, 12, 31).date()
        elif period_code.lower().startswith('q'):
            # Quarterly period format: Q2023-1 (first quarter of 2023)
            parts = period_code[1:].split('-')
            year = int(parts[0])
            quarter = int(parts[1])
            month_start = (quarter - 1) * 3 + 1
            start_date = datetime(year, month_start, 1).date()
            # Calculate end of quarter
            if month_start == 10:
                end_date = datetime(year, 12, 31).date()
            else:
                end_date = datetime(year, month_start + 2, 1).date().replace(
                    day=1) - timedelta(days=1)
        else:
            # Monthly period format: M2023-01 (January 2023)
            parts = period_code[1:].split('-')
            year = int(parts[0])
            month = int(parts[1])
            start_date = datetime(year, month, 1).date()
            # Calculate end of month
            if month == 12:
                end_date = datetime(year, 12, 31).date()
            else:
                end_date = datetime(year, month + 1, 1).date() - timedelta(days=1)

        return start_date, end_date


class FinancialCostCategory(models.Model):
    """
    Cost category for organizing farm financial activities
    """
    _name = 'farm.financial.cost.category'
    _description = 'Farm Financial Cost Category'
    _order = 'sequence, name'

    name = fields.Char("Category Name", required=True)
    code = fields.Char("Category Code", required=True)
    description = fields.Text("Description")
    sequence = fields.Integer("Sequence", default=10)
    active = fields.Boolean("Active", default=True)
    type = fields.Selection([
        ('direct', 'Direct Cost'),
        ('indirect', 'Indirect Cost'),
        ('fixed', 'Fixed Cost'),
        ('variable', 'Variable Cost'),
    ], string="Cost Type", default='direct')

    parent_id = fields.Many2one('farm.financial.cost.category', string="Parent Category", ondelete='cascade')
    child_ids = fields.One2many('farm.financial.cost.category', 'parent_id', string="Child Categories")
    account_id = fields.Many2one('account.account', string="Financial Account")

    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)', 'Code must be unique!'),
    ]

    @api.constrains('parent_id')
    def _check_parent_recursion(self):
        """Prevent recursive categories"""
        level = 0
        current = self
        while current.parent_id:
            level += 1
            if level > 10:  # Prevent infinite loops
                raise UserError(_("Category hierarchy is too deep."))
            current = current.parent_id
        return True


class FinancialCostTemplate(models.Model):
    """
    Cost template for standard costing in farm operations
    """
    _name = 'farm.financial.cost.template'
    _description = 'Farm Financial Cost Template'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Template Name", required=True)
    code = fields.Char("Template Code", required=True)
    description = fields.Text("Description")
    active = fields.Boolean("Active", default=True)

    # Cost breakdown
    direct_labor_cost = fields.Monetary("Direct Labor Cost", currency_field='currency_id')
    direct_material_cost = fields.Monetary("Direct Material Cost", currency_field='currency_id')
    overhead_cost = fields.Monetary("Overhead Cost", currency_field='currency_id')
    total_cost = fields.Monetary("Total Cost", compute='_compute_total_cost', currency_field='currency_id')

    # Cost per unit
    expected_quantity = fields.Float("Expected Quantity", help="Expected output quantity for cost calculation")
    cost_per_unit = fields.Monetary("Cost per Unit", compute='_compute_cost_per_unit', currency_field='currency_id')

    # Accounting integration
    workcenter_id = fields.Many2one('mrp.workcenter', string="Work Center")
    cost_category_id = fields.Many2one('farm.financial.cost.category', string="Cost Category")

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)

    @api.depends('direct_labor_cost', 'direct_material_cost', 'overhead_cost')
    def _compute_total_cost(self):
        for template in self:
            template.total_cost = template.direct_labor_cost + template.direct_material_cost + template.overhead_cost

    @api.depends('total_cost', 'expected_quantity')
    def _compute_cost_per_unit(self):
        for template in self:
            if template.expected_quantity and template.expected_quantity != 0:
                template.cost_per_unit = template.total_cost / template.expected_quantity
            else:
                template.cost_per_unit = 0.0

    def apply_to_production(self, production_record):
        """Apply this cost template to a production record"""
        # This method would be implemented based on specific production requirements
        pass

    def _get_default_cost_values(self):
        """Get default cost values for new templates"""
        return {
            'direct_labor_cost': 0.0,
            'direct_material_cost': 0.0,
            'overhead_cost': 0.0,
        }