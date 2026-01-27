from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class AgriCostTemplate(models.Model):
    """
    Agricultural Cost Template
    Provides pre-defined agricultural cost categories for farmers without financial backgrounds
    US-65-03: Agricultural Standard Costing
    """
    _name = 'agri.cost.template'
    _description = 'Agricultural Cost Template'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Template Name', required=True)
    code = fields.Char('Template Code', required=True, copy=False)
    category = fields.Selection([
        ('seedling', 'Seedling & Planting Material'),
        ('fertilizer', 'Fertilizer & Soil Amendment'),
        ('pesticide', 'Pesticide & Protection'),
        ('labor', 'Labor Cost'),
        ('machinery', 'Machinery & Equipment'),
        ('irrigation', 'Irrigation & Water'),
        ('fuel', 'Fuel & Energy'),
        ('packaging', 'Packaging & Storage'),
        ('other', 'Other Operational Cost'),
    ], string='Cost Category', required=True)

    # Unit-based costing
    unit_type = fields.Selection([
        ('mu', 'Per Mu (Chinese Acre)'),
        ('hectare', 'Per Hectare'),
        ('square_meter', 'Per Square Meter'),
        ('plant', 'Per Plant'),
        ('tree', 'Per Tree'),
        ('animal', 'Per Animal'),
        ('per_kg', 'Per Kg of Yield'),
        ('per_unit', 'Per Unit'),
    ], string='Unit Type', default='mu', required=True)

    unit_cost = fields.Float('Unit Cost', digits=(16, 2), required=True,
                            help='Cost per selected unit type')

    description = fields.Text('Description')
    is_active = fields.Boolean('Active', default=True)

    # For labor category
    labor_type = fields.Selection([
        ('skilled', 'Skilled Labor'),
        ('unskilled', 'Unskilled Labor'),
        ('seasonal', 'Seasonal Worker'),
        ('contractor', 'Contractor'),
    ], string='Labor Type',
       help='Specific labor classification for labor category')

    # For machinery category
    machinery_type = fields.Selection([
        ('tractor', 'Tractor'),
        ('sprayer', 'Sprayer'),
        ('harvester', 'Harvester'),
        ('irrigation', 'Irrigation Equipment'),
        ('transport', 'Transport Vehicle'),
        ('other', 'Other Machinery'),
    ], string='Machinery Type',
       help='Specific machinery classification for machinery category')

    # For fertilizer category
    fertilizer_type = fields.Selection([
        ('nitrogen', 'Nitrogen Fertilizer'),
        ('phosphorus', 'Phosphorus Fertilizer'),
        ('potassium', 'Potassium Fertilizer'),
        ('npk', 'NPK Compound'),
        ('organic', 'Organic Fertilizer'),
        ('trace', 'Trace Elements'),
    ], string='Fertilizer Type',
       help='Specific fertilizer classification for fertilizer category')

    # For pesticide category
    pesticide_type = fields.Selection([
        ('herbicide', 'Herbicide'),
        ('insecticide', 'Insecticide'),
        ('fungicide', 'Fungicide'),
        ('biological', 'Biological Control'),
        ('growth_regulator', 'Growth Regulator'),
    ], string='Pesticide Type',
       help='Specific pesticide classification for pesticide category')

    @api.model
    def create(self, vals):
        if 'code' not in vals or not vals['code']:
            vals['code'] = self.env['ir.sequence'].next_by_code('agri.cost.template') or '/'
        return super().create(vals)

    @api.constrains('category', 'labor_type', 'machinery_type', 'fertilizer_type', 'pesticide_type')
    def _check_category_consistency(self):
        """Ensure that sub-category selections are consistent with main category"""
        for template in self:
            if template.category == 'labor' and template.labor_type == False:
                raise ValidationError(_('Labor category must have a labor type specified.'))
            elif template.category == 'machinery' and template.machinery_type == False:
                raise ValidationError(_('Machinery category must have a machinery type specified.'))
            elif template.category == 'fertilizer' and template.fertilizer_type == False:
                raise ValidationError(_('Fertilizer category must have a fertilizer type specified.'))
            elif template.category == 'pesticide' and template.pesticide_type == False:
                raise ValidationError(_('Pesticide category must have a pesticide type specified.'))
            elif template.category in ['labor', 'machinery', 'fertilizer', 'pesticide']:
                # Ensure other category-specific fields are empty
                other_categories = ['labor', 'machinery', 'fertilizer', 'pesticide']
                other_categories.remove(template.category)
                for other_cat in other_categories:
                    if other_cat == 'labor' and template.labor_type:
                        if other_categories[0] != template.category:  # Reset other fields
                            template.labor_type = False
                    elif other_cat == 'machinery' and template.machinery_type:
                        template.machinery_type = False
                    elif other_cat == 'fertilizer' and template.fertilizer_type:
                        template.fertilizer_type = False
                    elif other_cat == 'pesticide' and template.pesticide_type:
                        template.pesticide_type = False


class AgriCostCalculation(models.TransientModel):
    """
    Wizard/Model for calculating costs based on templates and land area
    US-65-03: User-friendly cost calculation for farmers
    """
    _name = 'agri.cost.calculation'
    _description = 'Agricultural Cost Calculation'

    # Link to the task/parcel for context
    task_id = fields.Many2one('project.task', string='Production Task')
    land_parcel_id = fields.Many2one('stock.location', string='Land Parcel')
    area_value = fields.Float('Area Value', help='Area in selected unit (mu, ha, etc.)')
    area_unit = fields.Selection([
        ('mu', 'Mu (Chinese Acre)'),
        ('hectare', 'Hectare'),
        ('square_meter', 'Square Meter'),
    ], string='Area Unit', default='mu')

    # Cost calculation results
    total_seedling_cost = fields.Float('Total Seedling Cost', compute='_compute_total_costs')
    total_fertilizer_cost = fields.Float('Total Fertilizer Cost', compute='_compute_total_costs')
    total_pesticide_cost = fields.Float('Total Pesticide Cost', compute='_compute_total_costs')
    total_labor_cost = fields.Float('Total Labor Cost', compute='_compute_total_costs')
    total_machinery_cost = fields.Float('Total Machinery Cost', compute='_compute_total_costs')
    total_irrigation_cost = fields.Float('Total Irrigation Cost', compute='_compute_total_costs')
    total_other_cost = fields.Float('Total Other Cost', compute='_compute_total_costs')
    total_cost = fields.Float('Total Calculated Cost', compute='_compute_total_costs')

    # Line items for the calculation
    cost_line_ids = fields.One2many('agri.cost.calculation.line', 'calculation_id', string='Cost Lines')

    @api.depends('cost_line_ids', 'area_value')
    def _compute_total_costs(self):
        for calculation in self:
            seedling_cost = sum(line.total_cost for line in calculation.cost_line_ids if line.template_id.category == 'seedling')
            fertilizer_cost = sum(line.total_cost for line in calculation.cost_line_ids if line.template_id.category == 'fertilizer')
            pesticide_cost = sum(line.total_cost for line in calculation.cost_line_ids if line.template_id.category == 'pesticide')
            labor_cost = sum(line.total_cost for line in calculation.cost_line_ids if line.template_id.category == 'labor')
            machinery_cost = sum(line.total_cost for line in calculation.cost_line_ids if line.template_id.category == 'machinery')
            irrigation_cost = sum(line.total_cost for line in calculation.cost_line_ids if line.template_id.category == 'irrigation')
            other_cost = sum(line.total_cost for line in calculation.cost_line_ids if line.template_id.category == 'other')

            calculation.total_seedling_cost = seedling_cost
            calculation.total_fertilizer_cost = fertilizer_cost
            calculation.total_pesticide_cost = pesticide_cost
            calculation.total_labor_cost = labor_cost
            calculation.total_machinery_cost = machinery_cost
            calculation.total_irrigation_cost = irrigation_cost
            calculation.total_other_cost = other_cost
            calculation.total_cost = seedling_cost + fertilizer_cost + pesticide_cost + \
                                   labor_cost + machinery_cost + irrigation_cost + other_cost


class AgriCostCalculationLine(models.TransientModel):
    """
    Line item for cost calculation
    US-65-03: Individual cost calculation lines
    """
    _name = 'agri.cost.calculation.line'
    _description = 'Agricultural Cost Calculation Line'

    calculation_id = fields.Many2one('agri.cost.calculation', string='Calculation', ondelete='cascade')
    template_id = fields.Many2one('agri.cost.template', string='Cost Template', required=True)
    quantity = fields.Float('Quantity', default=1.0, help='Quantity of units to apply')
    unit_cost = fields.Float('Unit Cost', compute='_compute_unit_cost', store=True)
    total_cost = fields.Float('Total Cost', compute='_compute_total_cost', store=True)

    @api.depends('template_id')
    def _compute_unit_cost(self):
        for line in self:
            line.unit_cost = line.template_id.unit_cost if line.template_id else 0.0

    @api.depends('unit_cost', 'quantity')
    def _compute_total_cost(self):
        for line in self:
            line.total_cost = line.unit_cost * line.quantity