from odoo import models, fields, api, _

class AgriIntervention(models.Model):
    """
    Agricultural Intervention: The 2026 De-industrialized core model.
    Injects Level 0-3 Mixins to transform standard MRP into a community agricultural entity.
    """
    _name = 'mrp.production'
    _inherit = [
        'mrp.production',
        'farm.agricultural.intervention.mixin',
        'agri.view.mixin',           # Level 0: UI Isolation
        'agri.sustainability.mixin', # Level 0: Value Standard
        'agri.geospatial.mixin',     # Level 1: Spatial Grid
        'agri.nutrient.mixin',       # Level 1: Mass Balance
        'agri.actuator.mixin',       # Level 1+: Physical Actuation
        'agri.evidence.mixin',       # Level 2: Audit
        'agri.clearing.mixin',       # Level 3: Clearing
    ]
    _description = 'Agricultural Intervention (De-industrialized View)'

    def _get_embedding_content(self):
        self.ensure_one()
        return f"Intervention {self.name}: {self.product_id.display_name} at grid {self.spatial_grid_id}."

    @api.model_create_multi
    def create(self, vals_list):
        records = super(AgriIntervention, self).create(vals_list)
        for record in records:
            record.generate_quality_fingerprint()
        return records

    def action_confirm_intervention(self):
        self.ensure_one()
        return self.action_confirm()

    def action_complete_intervention(self):
        self.ensure_one()
        self.action_finalize_clearing()
        return True


class ProcurementGroup(models.Model):
    _inherit = 'procurement.group'

    agri_task_id = fields.Many2one('project.task', string="Agri Task")
