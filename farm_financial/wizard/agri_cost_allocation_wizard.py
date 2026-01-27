from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class AgriCostAllocationWizard(models.TransientModel):
    """
    Wizard for agricultural cost allocation
    Provides user-friendly interface for farmers to allocate standard costs
    US-65-03: User-friendly cost allocation for farmers without financial backgrounds
    """
    _name = 'agri.cost.allocation.wizard'
    _description = 'Agricultural Cost Allocation Wizard'

    # Context fields
    task_id = fields.Many2one('project.task', string='Production Task', required=True)
    land_parcel_id = fields.Many2one('stock.location', string='Land Parcel', required=True)
    area_value = fields.Float('Area Value', help='Area of the land parcel')
    area_unit = fields.Selection([
        ('mu', 'Mu (Chinese Acre)'),
        ('hectare', 'Hectare'),
        ('square_meter', 'Square Meter'),
    ], string='Area Unit', default='mu')

    # Cost allocation lines
    cost_line_ids = fields.One2many('agri.cost.allocation.line.wizard', 'wizard_id', string='Cost Allocation Lines')

    # Summary fields
    total_calculated_cost = fields.Float('Total Calculated Cost', compute='_compute_totals')
    total_applied_cost = fields.Float('Total Applied Cost', compute='_compute_totals')

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)

        # Get the active task if available
        active_ids = self.env.context.get('active_ids')
        active_model = self.env.context.get('active_model')

        if active_model == 'project.task' and active_ids:
            task = self.env['project.task'].browse(active_ids[0])
            res['task_id'] = task.id
            res['land_parcel_id'] = task.land_parcel_id.id if task.land_parcel_id else False
            # Set area_value from land parcel if available
            if task.land_parcel_id:
                res['area_value'] = task.land_parcel_id.land_area  # Assuming there's a land_area field
                res['area_unit'] = 'square_meter'  # Default to square meter, could be configured per location

        return res

    @api.depends('cost_line_ids')
    def _compute_totals(self):
        for wizard in self:
            wizard.total_calculated_cost = sum(line.total_cost for line in wizard.cost_line_ids)
            wizard.total_applied_cost = wizard.total_calculated_cost

    def action_apply_cost_allocation(self):
        """
        Apply the cost allocation to the linked task and create cost records
        """
        self.ensure_one()

        if not self.task_id:
            raise ValidationError(_("A production task must be selected to apply cost allocation."))

        # Process each cost line
        for line in self.cost_line_ids:
            if line.quantity > 0 and line.template_id:
                # Apply the cost to the task - you might want to create actual cost records here
                # This could be linked to the existing FarmCpaAnalysis or create new analytic entries

                # Create a message on the task to record the cost allocation
                self.task_id.message_post(
                    body=_("Cost allocated: %s %s units at %s per unit = %s total") % (
                        line.template_id.name,
                        line.quantity,
                        line.template_id.unit_cost,
                        line.total_cost
                    )
                )

        # Update the linked FarmCpaAnalysis if it exists
        cpa_analysis = self.env['farm.cpa.analysis'].search([
            ('activity_id', '=', self.task_id.campaign_id.id),
            ('location_id', '=', self.land_parcel_id.id)
        ], limit=1)

        if cpa_analysis:
            # Update the CPA analysis with calculated costs by category
            total_material_cost = sum(line.total_cost for line in self.cost_line_ids
                                    if line.template_id.category in ['seedling', 'fertilizer', 'pesticide', 'packaging'])
            total_labor_cost = sum(line.total_cost for line in self.cost_line_ids
                                  if line.template_id.category == 'labor')
            total_machinery_cost = sum(line.total_cost for line in self.cost_line_ids
                                      if line.template_id.category == 'machinery')
            total_indirect_cost = sum(line.total_cost for line in self.cost_line_ids
                                    if line.template_id.category in ['irrigation', 'fuel', 'other'])

            cpa_analysis.write({
                'total_material_cost': total_material_cost,
                'total_labor_cost': total_labor_cost,
                'total_machinery_cost': total_machinery_cost,
                'total_indirect_cost': total_indirect_cost,
            })
        else:
            # Create a new CPA analysis if none exists
            if self.task_id.campaign_id and self.land_parcel_id:
                self.env['farm.cpa.analysis'].create({
                    'activity_id': self.task_id.campaign_id.id,
                    'location_id': self.land_parcel_id.id,
                    'name': f'CPA-{self.task_id.campaign_id.name}-{self.land_parcel_id.name}',
                    'total_material_cost': sum(line.total_cost for line in self.cost_line_ids
                                            if line.template_id.category in ['seedling', 'fertilizer', 'pesticide', 'packaging']),
                    'total_labor_cost': sum(line.total_cost for line in self.cost_line_ids
                                          if line.template_id.category == 'labor'),
                    'total_machinery_cost': sum(line.total_cost for line in self.cost_line_ids
                                              if line.template_id.category == 'machinery'),
                    'total_indirect_cost': sum(line.total_cost for line in self.cost_line_ids
                                             if line.template_id.category in ['irrigation', 'fuel', 'other']),
                    'date_from': self.task_id.planned_date_begin,
                    'date_to': self.task_id.date_deadline,
                    'state': 'calculated',
                })

        return {
            'type': 'ir.actions.act_window_close'
        }


class AgriCostAllocationLineWizard(models.TransientModel):
    """
    Line item for the cost allocation wizard
    """
    _name = 'agri.cost.allocation.line.wizard'
    _description = 'Agricultural Cost Allocation Line Wizard'

    wizard_id = fields.Many2one('agri.cost.allocation.wizard', string='Wizard', ondelete='cascade')
    template_id = fields.Many2one('agri.cost.template', string='Cost Template', required=True)
    category = fields.Selection(related='template_id.category', string='Category')
    unit_type = fields.Selection(related='template_id.unit_type', string='Unit Type')
    unit_cost = fields.Float(related='template_id.unit_cost', string='Unit Cost')
    quantity = fields.Float('Quantity', default=1.0, help='How many units of this cost to apply')
    total_cost = fields.Float('Total Cost', compute='_compute_total_cost', store=True)

    @api.depends('unit_cost', 'quantity')
    def _compute_total_cost(self):
        for line in self:
            line.total_cost = line.unit_cost * line.quantity

    @api.onchange('template_id')
    def _onchange_template_id(self):
        """Set quantity based on land area if the unit type matches"""
        if self.template_id and self.wizard_id.area_value:
            # If template unit type matches the area unit of the wizard, initialize quantity
            if self.template_id.unit_type == 'mu' and self.wizard_id.area_unit == 'mu':
                self.quantity = self.wizard_id.area_value
            elif self.template_id.unit_type == 'hectare' and self.wizard_id.area_unit == 'hectare':
                self.quantity = self.wizard_id.area_value
            elif self.template_id.unit_type == 'square_meter' and self.wizard_id.area_unit == 'square_meter':
                self.quantity = self.wizard_id.area_value