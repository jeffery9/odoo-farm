from odoo import models, fields, api

class MrpWorkorderExtension(models.Model):
    _name = 'mrp.workorder'
    _inherit = 'mrp.workorder'

    def action_trigger_precision_skill(self):
        return True

    active_execution_phase_id = fields.Many2one('precision.recipe.phase', string="Active Phase")
