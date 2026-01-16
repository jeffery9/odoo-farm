from odoo import models, fields, api


class QualityManagementMixin(models.AbstractModel):
    """
    Mixin class for common quality management patterns
    """
    _name = 'farm.supply.quality.utils'
    _description = 'Farm Supply Quality Utilities'

    quality_grade = fields.Selection([
        ('grade_a', 'Grade A (Premium)'),
        ('grade_b', 'Grade B (Standard)'),
        ('grade_c', 'Grade C (Economy)'),
        ('grade_d', 'Grade D (Below Standard)'),
    ], string='Quality Grade')
    quality_factor = fields.Float('Quality Factor')
    quality_notes = fields.Text('Quality Notes')
    quality_certifications = fields.Char('Quality Certifications')

    @api.depends('quality_grade')
    def _compute_quality_factor(self):
        """Compute quality factor based on grade"""
        grade_factors = {
            'grade_a': 1.3,  # Premium
            'grade_b': 1.0,  # Standard
            'grade_c': 0.7,  # Economy
            'grade_d': 0.4,  # Below standard
        }
        for record in self:
            record.quality_factor = grade_factors.get(record.quality_grade, 1.0)