# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class FarmHealthSchedule(models.Model):
    _name = 'farm.health.schedule'
    _description = 'Livestock Vaccination & Health Schedule'

    name = fields.Char(string='Health Action', required=True, help="e.g. FMD Vaccine, Deworming")
    product_tmpl_id = fields.Many2one('product.template', string='Species', required=True, 
                                     help="The animal species this applies to.")
    
    target_life_stage = fields.Selection([
        ('juvenile', 'Juvenile / Seedling'),
        ('growing', 'Growing / Fattening'),
        ('mature', 'Mature / Breeding')
    ], string="Trigger Life Stage", required=True)
    
    activity_summary = fields.Char(string='Activity Summary', required=True)
    activity_note = fields.Text(string='Note')
    days_offset = fields.Integer(string='Days after Stage reached', default=0)

class StockLotHealth(models.Model):
    _inherit = 'stock.lot'

    # Track health activities specifically
    health_activity_ids = fields.One2many('mail.activity', 'res_id', 
                                         domain=[('res_model', '=', 'stock.lot')], 
                                         string="Planned Health Actions")

    @api.onchange('life_stage')
    def _onchange_life_stage_health(self):
        """ US-03-03: Auto-schedule health activities when life stage changes. """
        for lot in self:
            if lot.lot_purpose == 'biological_asset' and lot.life_stage:
                schedules = self.env['farm.health.schedule'].search([
                    ('product_tmpl_id', '=', lot.product_id.product_tmpl_id.id),
                    ('target_life_stage', '=', lot.life_stage)
                ])
                for sch in schedules:
                    lot.activity_schedule(
                        activity_type_id=self.env.ref('mail.mail_activity_data_todo').id,
                        summary=sch.activity_summary,
                        note=sch.activity_note,
                        date_deadline=fields.Date.today() + timedelta(days=sch.days_offset),
                    )
