# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class ProductTemplate(models.Model):
    _name = 'product.template'
    _inherit = 'product.template'
    production_drive_type = fields.Selection([
        ('material', 'Material Driven'),
        ('parameter', 'Recipe/Parameter Driven')
    ], string="Production Drive Mode", default='material')

class MrpBom(models.Model):
    _inherit = ['mrp.bom', 'mail.thread', 'mail.activity.mixin']
    _name = 'mrp.bom'

    master_recipe_version = fields.Integer("Master Recipe Version", default=1, tracking=True)
    master_recipe_phase_ids = fields.One2many('precision.master.recipe.phase', 'bom_id', string="Master Phases")
    required_workcenter_id = fields.Many2one('mrp.workcenter', string="Required Main Facility", tracking=True)
    ambient_requirement = fields.Text("Ambient Constraints", tracking=True)

    # [NEW] Batch Size Core: Everything below is defined relative to this quantity
    recipe_batch_size = fields.Float("Recipe Batch Size", default=1.0, 
                                    help="The base quantity this master recipe is designed for.")

    production_drive_type = fields.Selection([
        ('material', 'Material Driven'),
        ('parameter', 'Recipe/Parameter Driven')
    ], string="Drive Mode", compute='_compute_drive_type', store=True, readonly=False, tracking=True)

    @api.depends('product_tmpl_id.production_drive_type')
    def _compute_drive_type(self):
        for bom in self:
            if not bom.production_drive_type:
                bom.production_drive_type = bom.product_tmpl_id.production_drive_type

class PrecisionMasterRecipePhase(models.Model):
    _name = 'precision.master.recipe.phase'
    _description = 'Master Recipe Phase Template'
    _order = 'sequence'
    
    bom_id = fields.Many2one('mrp.bom', ondelete='cascade')
    name = fields.Char("Phase Name", required=True)
    sequence = fields.Integer("Sequence", default=10)
    
    master_parameter_ids = fields.One2many('precision.master.recipe.parameter', 'phase_id', string="Master Parameters")
    master_material_ids = fields.One2many('precision.master.recipe.material', 'phase_id', string="Phase Materials")
    
    duration_expected = fields.Float("Planned Duration (Hours)")
    sampling_plan = fields.Char("Sampling Plan")
    required_workcenter_id = fields.Many2one('mrp.workcenter', string="Phase Specific Equipment")
    required_role = fields.Selection([('operator', 'Operator'), ('technician', 'Technician'), ('specialist', 'Specialist')], default='operator')

class PrecisionMasterRecipeParameter(models.Model):
    _name = 'precision.master.recipe.parameter'
    _description = 'Master Recipe Parameter Template'
    bom_id = fields.Many2one('mrp.bom', ondelete='cascade')
    phase_id = fields.Many2one('precision.master.recipe.phase', ondelete='cascade')
    name = fields.Char("Parameter Name", required=True)
    target_value = fields.Float("Target Setpoint", required=True)
    
    # [NEW] Scaling Logic: e.g. Temp (False), Total Gas Volume (True)
    is_scalable = fields.Boolean("Scales with Batch Size", default=False)
    
    tolerance_percent = fields.Float("Tolerance (%)", default=5.0)
    uom_id = fields.Many2one('uom.uom', string="Unit")

class PrecisionMasterRecipeMaterial(models.Model):
    _name = 'precision.master.recipe.material'
    _description = 'Master Recipe Material Template'
    phase_id = fields.Many2one('precision.master.recipe.phase', ondelete='cascade')
    product_id = fields.Many2one('product.product', string="Material/Reagent", required=True)
    quantity = fields.Float("Qty (per Batch Size)", required=True, default=1.0)
    uom_id = fields.Many2one('uom.uom', string="Unit", related='product_id.uom_id')
