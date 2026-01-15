# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class FarmIndustryPicking(models.Model):
    _name = 'farm.industry.picking'
    _description = 'Industry-Specific Inventory Operation (ISL Layer)'
    _inherits = {'stock.picking': 'picking_id'}

    picking_id = fields.Many2one('stock.picking', string='Base Picking', required=True, ondelete='cascade')
    
    # Industry specific compliance (US-TECH-05-04 Context)
    industry_type = fields.Selection([
        ('livestock', 'Livestock Movement'),
        ('processing', 'Processing Intake/Output'),
        ('crop', 'Field Transfer')
    ], string='Industry Logistics Context')

    # Specialized Data Points
    compliance_ref = fields.Char("Transport Compliance Ref", help="Regulatory code for livestock or organic goods movement.")
    biosecurity_status = fields.Selection([
        ('pending', 'Not Inspected'),
        ('passed', 'Biosecurity Passed'),
        ('quarantine', 'Quarantine Required')
    ], string='Biosecurity Status', default='pending')
    
    sanitization_timestamp = fields.Datetime("Last Vehicle Sanitization")

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def get_formview_action(self, access_uid=None):
        """ US-TECH-06-23: Transparent redirection to Industry Specialized Picking View. """
        res = super(StockPicking, self).get_formview_action(access_uid=access_uid)
        
        # Check if an ISL record exists for this picking
        isl_record = self.env['farm.industry.picking'].search([('picking_id', '=', self.id)], limit=1)
        if isl_record:
            res.update({
                'res_model': 'farm.industry.picking',
                'res_id': isl_record.id,
            })
        return res

