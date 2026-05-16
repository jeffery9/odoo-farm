# -*- coding: utf-8 -*-
from odoo import models, api

class IiotDevice(models.Model):
    _inherit = 'iiot.device'

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
