# -*- coding: utf-8 -*-
from odoo import models, api, fields

class IiotDevice(models.Model):
    _inherit = 'iiot.device'

    # Logical Mapping [ISA-95 L3/L4]
    location_id = fields.Many2one(
        'farm.location', 
        string='Logical Location', 
        help='Functional position in ISA-95 hierarchy'
    )
    
    site_id = fields.Many2one(
        'farm.location', 
        string='Site', 
        compute='_compute_site_id', 
        store=True,
        help='The farm/site this device belongs to'
    )

    @api.depends('location_id')
    def _compute_site_id(self):
        for device in self:
            if device.location_id:
                # Climb up the hierarchy to find the 'site' level
                parent = device.location_id
                while parent and parent.isa95_level != 'site' and parent.parent_id:
                    parent = parent.parent_id
                device.site_id = parent if parent and parent.isa95_level == 'site' else False
            else:
                device.site_id = False

    @api.model
    def _get_business_models(self):
        """
        Consolidated business model references injected by the Farm IoT Management Center.
        This centralized approach prevents the base agri_iot module from depending on
        business applications (mrp, stock, maintenance).
        """
        res = super()._get_business_models()
        res.extend([
            ('maintenance.equipment', 'Maintenance Equipment'),
            ('project.task', 'Project Task'),
            ('mrp.workcenter', 'Work Center'),
            ('stock.location', 'Stock Location'),
            ('product.product', 'Product'),
        ])
        return res
