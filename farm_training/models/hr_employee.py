# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    skill_ids = fields.Many2many(
        'farm.training.skill',
        string='Acquired Skills',
        help='Skills acquired by the employee.'
    )
    certification_ids = fields.Many2many(
        'farm.training.certification',
        string='Certifications Held',
        help='Certifications held by the employee.',
        compute='_compute_certification_ids',
        store=True,
    )
    training_record_ids = fields.One2many(
        'farm.training.training_record',
        'employee_id',
        string='Training Records'
    )

    @api.depends('training_record_ids.certification_id', 'training_record_ids.status')
    def _compute_certification_ids(self):
        for employee in self:
            valid_certs = employee.training_record_ids.filtered(lambda r: r.status in ('valid', 'upcoming_expire')).mapped('certification_id')
            employee.certification_ids = [(6, 0, valid_certs.ids)]

    def check_qualification_for_task(self, required_skills=None, required_certifications=None):
        self.ensure_one()
        if required_skills:
            # Check if employee has all required skills
            if not all(skill in self.skill_ids for skill in required_skills):
                missing_skills = ", ".join((required_skills - self.skill_ids).mapped('name'))
                raise ValidationError(_(f"Employee {self.name} is missing required skills: {missing_skills}"))
        if required_certifications:
            # Check if employee has all valid required certifications
            valid_cert_ids = self.training_record_ids.filtered(lambda r: r.status in ('valid', 'upcoming_expire')).mapped('certification_id').ids
            if not all(cert.id in valid_cert_ids for cert in required_certifications):
                missing_certs = ", ".join((required_certifications - self.certification_ids).mapped('name'))
                raise ValidationError(_(f"Employee {self.name} does not hold all valid required certifications: {missing_certs}"))
        return True
