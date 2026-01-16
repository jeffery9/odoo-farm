from odoo import models, fields

class AgriIntervention(models.Model):
    _inherit = ['mrp.production', 'farm.agricultural.intervention.mixin']
    _description = 'Agricultural Intervention (De-industrialized View)'

    # Define minimal specific fields if needed, most functionality comes from the mixin
    # The mixin contains all the agricultural-specific logic and methods
    # This approach allows the existing functionality to be preserved while
    # using the new ISL-compatible architecture


class ProcurementGroup(models.Model):
    _inherit = 'procurement.group'

    agri_task_id = fields.Many2one('project.task', string="Agri Task")