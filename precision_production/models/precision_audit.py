# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class PrecisionInterventionBasis(models.Model):
    _name = 'precision.intervention.basis'
    _description = 'Intervention Rationale'
    name = fields.Char("Evidence Summary", required=True)
    source_type = fields.Selection([('quality', 'Metrology'), ('iot', 'IoT'), ('ai', 'AI')], default='quality')
    parameter_name = fields.Char("Parameter")
    recipe_standard_value = fields.Float("Standard")
    actual_measured_value = fields.Float("Actual")
    deviation_delta = fields.Float("Delta", compute='_compute_delta', store=True)
    res_model = fields.Char("Related Model", index=True)
    res_id = fields.Many2oneReference("Related Record", model_field='res_model', index=True)
    create_date = fields.Datetime("Captured At", readonly=True, default=fields.Datetime.now)

    @api.depends('recipe_standard_value', 'actual_measured_value')
    def _compute_delta(self):
        for rec in self: rec.deviation_delta = rec.actual_measured_value - rec.recipe_standard_value

class PrecisionInterventionLog(models.Model):
    _name = 'precision.intervention.log'
    _description = 'Intervention Audit Log'
    _order = 'create_date desc'
    name = fields.Char("Action", required=True)
    intervention_type = fields.Selection([('manual', 'Manual'), ('active', 'Active')], default='manual')
    basis_id = fields.Many2one('precision.intervention.basis', string="Justification")
    res_model = fields.Char("Related Model", required=True, index=True)
    res_id = fields.Many2oneReference("Related Record", model_field='res_model', index=True)
    user_id = fields.Many2one('res.users', string="Operator")
    create_date = fields.Datetime("Timestamp", readonly=True, default=fields.Datetime.now)

class PrecisionGradedOutput(models.Model):
    _name = 'precision.graded.output'
    _description = 'Graded Output Worklist'
    res_model = fields.Char("Related Model", required=True, index=True)
    res_id = fields.Many2oneReference("Related Record", model_field='res_model', index=True)
    product_id = fields.Many2one('product.product', string="Product", required=True)
    grade = fields.Selection([('premium', 'Premium'), ('standard', 'Standard'), ('fail', 'Rejected')], required=True)
    quantity = fields.Float("Actual Quantity", required=True)
    move_id = fields.Many2one('stock.move', string="Linked Move")
    notes = fields.Text("Notes")
