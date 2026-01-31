from odoo import models, fields, api, _
from .common_fields import CommonAgriculturalFields
from .base_mixins import CreationMethodMixin


class FarmActivity(models.Model):
    """
    Agricultural Activity Management.
    Domain Role: Physical manifestation of an Agri Domain activity within a specific Farm.
    US-01-01: Agricultural Activity Classification
    US-01-02: Sector-specific attributes
    Level 4: Agri-Farm Semantic Alignment [US-104-2026]
    """
    _name = 'farm.activity'
    _description = 'Agricultural Activity'
    _inherit = ['project.project', 'farm.core.creation.method.mixin']

    # Extend project.project with agricultural properties
    is_agri_activity = fields.Boolean(
        string="Is Agricultural Activity",
        default=False,
        help="Mark this project as an agricultural activity to enable specialized features."
    )

    activity_family = fields.Selection([
        ('planting', 'Planting'),
        ('livestock', 'Livestock'),
        ('aquaculture', 'Aquaculture'),
        ('agritourism', 'Agritourism'),
        ('baking', 'Baking'),
        ('winemaking', 'Winemaking'),
        ('food_processing', 'Food Processing'),
    ], string="Activity Family", help="Specify the agricultural sector.")

    production_cycle = fields.Selection([
        ('annual', 'Annual'),
        ('perennial', 'Perennial'),
    ], string="Production Cycle", default='annual')

    task_sequence_id = fields.Many2one(
        'ir.sequence',
        string="Task Sequence",
        help="Custom sequence for tasks in this project. If empty, the family default will be used."
    )

    @api.model
    def create(self, vals_list):
        """Override to handle sequence generation for agricultural activities"""
        records = super(FarmActivity, self).create(vals_list)
        for record in records:
            if record.is_agri_activity and not record.name:
                seq_code = f'farm.activity.{record.activity_family}' if record.activity_family else 'farm.activity'
                record.name = self.env['ir.sequence'].next_by_code(seq_code) or 'AGRI'
        return records


class FarmTask(models.Model):
    """
    Agricultural Task Management.
    Domain Role: The atomic execution unit of agricultural physics.
    Level 4: Agri-Farm Semantic Alignment [US-104-2026]
    """
    _name = 'farm.task'
    _description = 'Agricultural Task'
    _inherit = [
        'project.task', 
        'farm.core.creation.method.mixin',
        'agri.task.mixin' # [Semantic Refactoring] Inherit domain physics and protocols
    ]

    # Link to land parcel (Now linked via the Agri Location domain model)
    land_parcel_id = fields.Many2one('farm.location', string="Physical Container", domain=[('is_land_parcel', '=', True)])

    # Agricultural-specific fields
    activity_family = fields.Selection([
        ('planting', 'Planting'),
        ('livestock', 'Livestock'),
        ('aquaculture', 'Aquaculture'),
        ('harvesting', 'Harvesting'),
        ('processing', 'Processing'),
    ], string="Activity Family", related='project_id.activity_family', store=True)

    # Crop or livestock involved
    product_id = fields.Many2one('product.product', string="Crop/Livestock")
    variety_id = fields.Many2one('product.template', string="Variety", related='product_id.product_tmpl_id')

    # Timing
    planned_start_date = fields.Date("Planned Start Date")
    planned_end_date = fields.Date("Planned End Date")
    actual_start_date = fields.Date("Actual Start Date")
    actual_end_date = fields.Date("Actual End Date")

    # Resource requirements
    required_equipment_ids = fields.Many2many('product.product', 'farm_task_equipment_rel', 'task_id', 'equipment_id',
                                              string="Required Equipment", domain=[('categ_id.name', 'ilike', 'equipment')])
    required_material_ids = fields.Many2many('product.product', 'farm_task_material_rel', 'task_id', 'material_id',
                                             string="Required Materials")

    # Labor and costs
    required_labor_hours = fields.Float("Required Labor Hours")
    estimated_cost = fields.Float("Estimated Cost")
    actual_cost = fields.Float("Actual Cost")

    # Quality and compliance
    safety_protocol_followed = fields.Boolean("Safety Protocol Followed", default=False)
    quality_check_required = fields.Boolean("Quality Check Required", default=False)
    quality_check_done = fields.Boolean("Quality Check Done", default=False)

    @api.model_create_multi
    def create(self, vals_list):
        new_records = super(FarmTask, self).create(vals_list)
        for vals, record in zip(vals_list, new_records):
            if record.project_id and record.project_id.is_agri_activity:
                # Get sequence rule [US-01-01]
                sequence = record.project_id.task_sequence_id
                if not sequence and record.project_id.activity_family:
                    seq_code = 'farm.task.%s' % record.project_id.activity_family
                    sequence = self.env['ir.sequence'].search([('code', '=', seq_code)], limit=1)

                if sequence:
                    # Prepend sequence to task name
                    sequence_name = sequence.next_by_id() or ''
                    if sequence_name:
                        record.name = sequence_name + ' - ' + (record.name or '')
        return new_records
