# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta

class FarmTrainingSkill(models.Model):
    _name = 'farm.training.skill'
    _description = 'Farm Training Skill'

    name = fields.Char(string='Skill Name', required=True)
    description = fields.Text(string='Description')

class FarmTrainingCertification(models.Model):
    _name = 'farm.training.certification'
    _description = 'Farm Training Certification'

    name = fields.Char(string='Certification Name', required=True)
    description = fields.Text(string='Description')
    validity_period = fields.Integer(string='Validity Period (Years)', help='Number of years the certification is valid.')
    required_skills_ids = fields.Many2many(
        'farm.training.skill',
        string='Required Skills',
        help='Skills that are typically associated with this certification.'
    )

class FarmTrainingTrainingRecord(models.Model):
    _name = 'farm.training.training_record'
    _description = 'Farm Training Record'
    _rec_name = 'display_name'

    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    certification_id = fields.Many2one('farm.training.certification', string='Certification', required=True)
    training_date = fields.Date(string='Training Date', default=fields.Date.today(), required=True)
    expiration_date = fields.Date(string='Expiration Date', compute='_compute_expiration_date', store=True)
    status = fields.Selection([
        ('valid', 'Valid'),
        ('expired', 'Expired'),
        ('upcoming_expire', 'Expiring Soon'),
        ('pending', 'Pending'),
        ('revoked', 'Revoked'),
    ], string='Status', compute='_compute_status', store=True)
    trainer_id = fields.Many2one('res.partner', string='Trainer/Issued By')
    notes = fields.Text(string='Notes')
    display_name = fields.Char(compute='_compute_display_name', store=True)

    @api.depends('employee_id', 'certification_id')
    def _compute_display_name(self):
        for record in self:
            record.display_name = f"{record.employee_id.name} - {record.certification_id.name}"

    @api.depends('training_date', 'certification_id.validity_period')
    def _compute_expiration_date(self):
        for record in self:
            if record.training_date and record.certification_id and record.certification_id.validity_period:
                record.expiration_date = record.training_date + relativedelta(years=record.certification_id.validity_period)
            else:
                record.expiration_date = False

    @api.depends('expiration_date')
    def _compute_status(self):
        today = fields.Date.today()
        for record in self:
            if not record.expiration_date:
                record.status = 'pending'
            elif record.expiration_date < today:
                record.status = 'expired'
            elif record.expiration_date - relativedelta(months=3) < today: # Expiring within 3 months
                record.status = 'upcoming_expire'
            else:
                record.status = 'valid'

    @api.constrains('training_date', 'expiration_date')
    def _check_dates(self):
        for record in self:
            if record.training_date and record.expiration_date and record.training_date > record.expiration_date:
                raise ValidationError(_("Training date cannot be after expiration date."))

