# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class FarmProcessingProductionSCExtension(models.Model):
    """
    Extension to Processing ISL Production Model for SC License - US-14-21
    """
    _inherit = 'farm.processing.production'

    # Add SC category field to production order
    sc_category_id = fields.Many2one('farm.sc.category', string="SC Category")

    def action_confirm(self):
        """ [US-14-21] SC Range Check for industry specific requirements """
        # First call the parent method
        result = super().action_confirm()

        # Then perform SC license check
        for production in self:
            # Check SC category from production order first, fallback to BOM
            sc_category = production.sc_category_id or (production.bom_id and production.bom_id.sc_category_id)
            if sc_category:
                license = self.env['farm.sc.license'].search([
                    ('company_id', '=', production.company_id.id),
                    ('is_active', '=', True),
                    ('category_ids', 'in', sc_category.id)
                ], limit=1)
                if not license:
                    raise UserError(_("SC COMPLIANCE ERROR: Company does not have a valid SC license for category '%s'!") % sc_category.name)

        return result


class FarmProcessingBomSCExtension(models.Model):
    """
    Extension to Processing ISL BOM Model for SC Category - US-14-21
    """
    _inherit = 'farm.processing.bom'

    # Add SC category field to BOM
    sc_category_id = fields.Many2one('farm.sc.category', string="SC Category")


class AgriProcessingLicenseCheck(models.Model):
    """
    Production License Scope Verification - US-14-21
    """
    _name = 'agri.processing.license.check'
    _description = 'Production License Scope Verification'

    name = fields.Char('License Check Record', required=True)
    production_id = fields.Many2one('farm.processing.production', string='Production Order', required=True)
    license_id = fields.Many2one('farm.sc.license', string='SC License', required=True)

    # Product and category checks
    product_category = fields.Many2one('product.category', string='Product Category')
    product_type = fields.Char('Product Type Code')
    is_category_permitted = fields.Boolean('Category Permitted', compute='_compute_category_check', store=True)

    # License status checks
    license_active = fields.Boolean('License Active', related='license_id.is_active', store=True)
    license_expiry_date = fields.Date('License Expiry', related='license_id.expiry_date')

    # Compliance status
    compliance_status = fields.Selection([
        ('compliant', 'Compliant'),
        ('warning', 'Warning'),
        ('non_compliant', 'Non-Compliant'),
    ], string='Compliance Status', compute='_compute_compliance_status', store=True)

    # Violation tracking
    violations_found = fields.Text('Violations Found')
    override_authorized_by = fields.Many2one('res.users', string='Override Authorized By')
    override_reason = fields.Text('Override Reason')

    # Automatic blocking capability
    is_production_blocked = fields.Boolean('Production Blocked', default=False)

    # Audit trail
    checked_by = fields.Many2one('res.users', string='Checked By', default=lambda self: self.env.user)
    checked_date = fields.Datetime('Checked Date', default=fields.Datetime.now)

    @api.model
    def create(self, vals):
        if 'name' not in vals or not vals['name']:
            vals['name'] = 'LICENSE/' + fields.Date.to_string(fields.Date.today()) + '/' + str(self.id or 0)
        return super().create(vals)

    @api.depends('product_category', 'license_id')
    def _compute_category_check(self):
        for record in self:
            record.is_category_permitted = False
            if record.license_id and record.product_category:
                # Check if the product category is in the permitted categories
                permitted_categories = record.license_id.category_ids.mapped('name')
                record.is_category_permitted = record.product_category.name in permitted_categories

    @api.depends('is_category_permitted', 'license_active')
    def _compute_compliance_status(self):
        for record in self:
            if not record.license_active:
                record.compliance_status = 'non_compliant'
            elif not record.is_category_permitted:
                record.compliance_status = 'non_compliant'
            else:
                record.compliance_status = 'compliant'