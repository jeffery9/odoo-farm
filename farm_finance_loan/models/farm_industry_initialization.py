from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class FarmIndustryInitialization(models.Model):
    """
    Management model for industry initialization data packages
    """
    _name = 'farm.industry.initialization'
    _description = 'Farm Industry Initialization'

    name = fields.Char('Package Name', required=True)
    industry_code = fields.Char('Industry Code', required=True, help='Unique code for industry type')
    description = fields.Text('Description')
    is_active = fields.Boolean('Is Active', default=True)
    version = fields.Char('Version', default='1.0')

    # Components included in this package
    has_varieties = fields.Boolean('Has Varieties', default=True)
    has_growth_stages = fields.Boolean('Has Growth Stages', default=True)
    has_agri_uom = fields.Boolean('Has Agricultural UOM', default=True)
    has_task_templates = fields.Boolean('Has Task Templates', default=True)
    has_quality_standards = fields.Boolean('Has Quality Standards', default=True)

    # Statistics
    varieties_count = fields.Integer('Varieties Count', compute='_compute_counts')
    tasks_count = fields.Integer('Task Templates Count', compute='_compute_counts')
    stages_count = fields.Integer('Growth Stages Count', compute='_compute_counts')

    def _compute_counts(self):
        """Compute statistics for the initialization package"""
        for record in self:
            record.varieties_count = 0  # Would compute actual count
            record.tasks_count = 0      # Would compute actual count
            record.stages_count = 0     # Would compute actual count