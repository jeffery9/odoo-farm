# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class AgriProcessingRecipeVersioning(models.Model):
    """
    Extension to Processing ISL Recipe Model for Versioning - US-037-09 [De-industrialized]
    """
    _inherit = 'agri.isl.processing.bom'

    # Recipe version specific fields
    version_number = fields.Integer('Version', default=1)
    version_description = fields.Text('Version Description')
    version_name = fields.Char("Version Name", help="e.g., Summer 2024 v1.0")

    # Confidentiality controls
    is_blind_mode_enabled = fields.Boolean('Enable Blind Mixing Mode', default=False)
    blind_input_ids = fields.One2many('agri.processing.blind.input', 'formula_recipe_id', string='Blind Inputs')

    # Change tracking
    change_reason = fields.Text('Change Reason')
    changed_by = fields.Many2one('res.users', string='Changed By', default=lambda self: self.env.user)
    changed_date = fields.Datetime('Change Date', default=fields.Datetime.now)

    # Access control
    authorized_users = fields.Many2many('res.users', 'formula_version_auth_rel', 'bom_id', 'user_id', string='Authorized Users')

    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('in_use', 'In Use'),
        ('deprecated', 'Deprecated'),
    ], string='Status')

    @api.constrains('version_number', 'id')
    def _check_version_uniqueness(self):
        for record in self:
            existing = self.search([
                ('id', '!=', record.id),
                ('version_number', '=', record.version_number),
            ])
            if existing:
                raise ValidationError(_("Version number %s already exists for this formula.") % record.version_number)


class AgriProcessingBlindInput(models.Model):
    """
    Blind Inputs for Formula Confidentiality - US-037-09 [De-industrialized]
    """
    _name = 'agri.processing.blind.input'
    _description = 'Blind Inputs for Formula Confidentiality'

    formula_recipe_id = fields.Many2one('agri.isl.processing.bom', string='Formula Recipe', ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Product', required=True)
    blind_name = fields.Char('Blind Name', help='Confidential name shown during mixing')
    sequence = fields.Integer('Sequence', default=10)
    hide_during_mixing = fields.Boolean('Hide During Mixing', default=True)
    authorized_users = fields.Many2many('res.users', 'blind_input_auth_rel', 'blind_input_id', 'user_id', string='Authorized to View')

    def name_get(self):
        result = []
        for record in self:
            if self.env.user in record.authorized_users:
                name = f"{record.product_id.name} ({record.blind_name})"
            else:
                name = record.blind_name or "Confidential Input"
            result.append((record.id, name))
        return result


class AgriProcessingFormulaAutoCorrection(models.Model):
    """
    Formula Auto-Correction System - US-037-09 [De-industrialized]
    """
    _name = 'agri.processing.formula.auto.correction'
    _description = 'Formula Auto-Correction System'

    name = fields.Char('Correction Record', required=True)
    bom_id = fields.Many2one('agri.isl.processing.bom', string='Formula', required=True)
    production_id = fields.Many2one('agri.isl.mrp.production', string='Intervention Order')

    # Original values
    original_qty = fields.Float('Original Quantity', required=True)
    original_product_id = fields.Many2one('product.product', string='Original Product', required=True)

    # Actual values
    actual_qty = fields.Float('Actual Quantity')
    actual_product_id = fields.Many2one('product.product', string='Actual Product')

    # Correction applied
    correction_qty = fields.Float('Correction Quantity')
    correction_reason = fields.Text('Correction Reason')

    # Status
    correction_status = fields.Selection([
        ('pending', 'Pending'),
        ('applied', 'Applied'),
        ('rejected', 'Rejected'),
    ], string='Status', default='pending')

    # Audit trail
    corrected_by = fields.Many2one('res.users', string='Corrected By', default=lambda self: self.env.user)
    corrected_date = fields.Datetime('Corrected Date', default=fields.Datetime.now)

    @api.model
    def create(self, vals):
        if 'name' not in vals or not vals['name']:
            vals['name'] = 'CORR/' + fields.Date.to_string(fields.Date.today()) + '/' + str(self.id or 0)
        return super().create(vals)

    def action_apply_correction(self):
        """Apply the correction to the intervention order"""
        for record in self:
            if record.production_id and record.correction_qty:
                record.correction_status = 'applied'
                _logger.info(f"Applied correction {record.name} to intervention {record.production_id.name}")

    def action_reject_correction(self):
        """Reject the correction"""
        for record in self:
            record.correction_status = 'rejected'
