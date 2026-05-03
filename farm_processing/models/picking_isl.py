# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class FarmIndustryPicking(models.Model):
    """
    Industry-Specific Inventory Operation extension of ISL architecture
    This extends the centralized farm.stock.picking model with food processing specific features
    """
    _inherit = 'farm.stock.picking'

    # Industry specific compliance (US-TECH-05-04 Context)
    # Note: industry_type is already defined in the base ISL model
    # We're adding our specific values to the selection
    industry_type = fields.Selection(selection_add=[
        ('livestock', 'Livestock Movement'),
        ('processing', 'Processing Intake/Output'),
        ('crop', 'Field Transfer')
    ], string='Industry Logistics Context', ondelete={'livestock': 'cascade', 'processing': 'cascade', 'crop': 'cascade'})

    # Specialized Data Points
    compliance_ref = fields.Char("Transport Compliance Ref", help="Regulatory code for livestock or organic goods movement.")
    biosecurity_status = fields.Selection([
        ('pending', 'Not Inspected'),
        ('passed', 'Biosecurity Passed'),
        ('quarantine', 'Quarantine Required')
    ], string='Biosecurity Status', default='pending')

    sanitization_timestamp = fields.Datetime("Last Vehicle Sanitization")

    def write(self, vals):
        # Ensure industry type is set to processing when not specified and this is a processing record
        if 'industry_type' not in vals and not self.industry_type and 'processing' in str(self._name):
            vals['industry_type'] = 'processing'
        return super().write(vals)

    @api.model_create_multi
    def create(self, vals_list):
        # Ensure industry type is set to processing when not specified
        for vals in vals_list:
            if 'industry_type' not in vals or not vals.get('industry_type'):
                vals['industry_type'] = 'processing'
        return super().create(vals_list)


class StockPicking(models.Model):
    _name = 'stock.picking'
    _inherit = 'stock.picking'

    def get_formview_action(self, access_uid=None):
        """ US-TECH-06-23: Transparent redirection to Industry Specialized Picking View. """
        # Now use the centralized ISL redirection mechanism
        res = super(StockPicking, self).get_formview_action(access_uid=access_uid)

        # Use the centralized redirection utility from farm_isl
        redirector = self.env['agri.isl.model.redirector']
        isl_record = redirector.get_isl_record('stock.picking', self.id)

        if isl_record:
            res.update({
                'res_model': 'farm.stock.picking',
                'res_id': isl_record.id,
            })
        return res