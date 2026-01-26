from odoo import models, fields, api
from odoo.exceptions import ValidationError

class IndustryCalculationRule(models.Model):
    """
    Calculation rules for industry-specific carbon models
    """
    _name = 'farm.sustainability.industry.calculation.rule'
    _description = 'Industry Calculation Rule'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    model_id = fields.Many2one('farm.sustainability.industry.carbon.model', 'Industry Model', required=True, ondelete='cascade')
    rule_name = fields.Char('Rule Name', required=True)
    rule_description = fields.Text('Rule Description')
    rule_type = fields.Selection([
        ('emission_factor', 'Emission Factor'),
        ('activity_data', 'Activity Data'),
        ('calculation', 'Calculation Method'),
        ('threshold', 'Threshold Rule'),
        ('compliance', 'Compliance Rule'),
        ('reporting', 'Reporting Rule')
    ], string='Rule Type', required=True)
    parameter_name = fields.Char('Parameter Name', help='Name of the parameter this rule applies to')
    formula = fields.Text('Formula', help='Mathematical formula for the calculation')
    applicable_conditions = fields.Text('Applicable Conditions', help='Conditions under which this rule applies')
    default_value = fields.Float('Default Value')
    min_value = fields.Float('Minimum Value')
    max_value = fields.Float('Maximum Value')
    units = fields.Char('Units', help='Units of measurement for this rule')
    source_documentation = fields.Text('Source Documentation', help='Documentation source for this rule')
    active = fields.Boolean('Active', default=True)

    @api.constrains('min_value', 'max_value', 'default_value')
    def _check_value_ranges(self):
        """Ensure min <= default <= max"""
        for record in self:
            if record.min_value and record.max_value and record.min_value > record.max_value:
                raise ValidationError("Minimum value cannot be greater than maximum value.")
            if record.default_value and record.min_value and record.default_value < record.min_value:
                raise ValidationError("Default value cannot be less than minimum value.")
            if record.default_value and record.max_value and record.default_value > record.max_value:
                raise ValidationError("Default value cannot be greater than maximum value.")