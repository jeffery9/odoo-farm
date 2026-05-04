from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)

class AgriTaskMixin(models.AbstractModel):
    """
    Agri Domain Level: Task Logic. [US-014-2026]
    Universal logic for executing any agricultural activity.
    Focuses on physical facts: grid location, material balance, and evidence.
    """
    _name = 'agri.task.mixin'
    _description = 'Agricultural Universal Task Mixin'
    _inherit = [
        'agri.geospatial.mixin',     # Where is the task happening?
        'agri.nutrient.mixin',       # What mass is being converted?
        'agri.sustainability.mixin', # What is the carbon impact?
        'agri.evidence.mixin',       # What is the physical proof?
    ]

    agri_status = fields.Selection([
        ('planned', 'Planned'),
        ('active', 'Physically Active'),
        ('validating', 'Auditing Evidence'),
        ('finished', 'Physically Completed'),
        ('aborted', 'Aborted')
    ], string="Agri Execution Status", default='planned')

    def action_start_agri_execution(self):
        """Standard hook for starting physical task."""
        self.write({'agri_status': 'active'})
        return True

    def action_finalize_agri_execution(self):
        """standard hook for completing task and triggering evidence bundle."""
        self.ensure_one()
        self.perform_evidence_audit()
        self.write({'agri_status': 'finished'})
        return True
