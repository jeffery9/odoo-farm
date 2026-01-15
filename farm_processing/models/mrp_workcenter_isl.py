# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class FarmIndustryWorkcenter(models.Model):
    _name = 'farm.industry.workcenter'
    _description = 'Specialized Production Facility (ISL Layer)'
    _inherits = {'mrp.workcenter': 'workcenter_id'}

    workcenter_id = fields.Many2one('mrp.workcenter', string='Base Workcenter', required=True, ondelete='cascade')
    
    # --- Specialized Facility Metadata ---
    facility_type = fields.Selection([
        ('crop_field', 'Open Field'),
        ('greenhouse', 'Greenhouse'),
        ('livestock_pen', 'Animal Pen / Barn'),
        ('fish_pond', 'Aquaculture Pond'),
        ('factory_line', 'Processing Line'),
        ('lab_bench', 'Laboratory Bench')
    ], string='Physical Facility Type', default='factory_line', required=True)

    # Spatial & Environmental Stats
    surface_area = fields.Float("Surface Area (sqm)")
    volume_capacity = fields.Float("Volume Capacity (m3)")
    has_climate_control = fields.Boolean("Climate Controlled")
    
    # IoT Integration (Sync with EPIC-TECH-03)
    main_sensor_topic = fields.Char("Primary Telemetry Topic", help="Main sensor topic associated with this facility (e.g. pond temperature).")

class MrpWorkcenter(models.Model):
    _inherit = 'mrp.workcenter'

    def get_formview_action(self, access_uid=None):
        """ US-TECH-06-23: Transparent redirection to Industry Specialized Workcenter View. """
        res = super(MrpWorkcenter, self).get_formview_action(access_uid=access_uid)
        isl_record = self.env['farm.industry.workcenter'].search([('workcenter_id', '=', self.id)], limit=1)
        if isl_record:
            res.update({
                'res_model': 'farm.industry.workcenter',
                'res_id': isl_record.id,
            })
        return res
