# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging
import json

_logger = logging.getLogger(__name__)

class FarmFermentationVessel(models.Model):
    """
    [ISL Layer] Fermentation Pit (窖池) or Aging Jar (陶坛).
    Proxies mrp.workcenter to manage microbial habitat assets.
    """
    _name = 'farm.fermentation.vessel'
    _description = 'Fermentation Pit/Vessel'
    _inherits = {'mrp.workcenter': 'workcenter_id'}
    _inherit = ['agri.geospatial.mixin']

    workcenter_id = fields.Many2one('mrp.workcenter', required=True, ondelete='cascade')

    vessel_type = fields.Selection([
        ('mud_pit', 'Mud Pit (窖池)'),
        ('stone_pit', 'Stone Pit'),
        ('jar', 'Ceramic Jar (陶坛)'),
        ('vat', 'Fermentation Vat (酱缸)')
    ], string="Vessel Type", required=True)
    
    start_service_year = fields.Integer("Enable Year")
    microbial_health_index = fields.Float("Microbial Health (0-100)", default=100.0)

class FarmFermentationOrder(models.Model):
    """
    [ISL Layer] Fermentation Cycle Order.
    Proxies mrp.production to monitor biological activity.
    """
    _name = 'farm.fermentation.order'
    _description = 'Fermentation Job'
    _inherits = {'mrp.production': 'production_id'}
    _inherit = [
        'farm.agri.production.mixin',
        'agri.agent.instruction.mixin',
        'agri.incident.alert.mixin'
    ]

    production_id = fields.Many2one('mrp.production', string='Base Order', required=True, ondelete='cascade')

    # [US-120-02] Real-time Dynamics
    internal_temperature = fields.Float("Pit Temperature (℃)")
    acidity_level = fields.Float("Current Acidity (pH)")

    def handle_pit_telemetry(self, data):
        """ [Authoring-Style] Defensive logic for biological runaway. """
        self.ensure_one()
        temp = data.get('temperature')
        if temp and temp > 45.0: # High heat risk for koji
            self.report_incident('critical', 'Fermentation Thermal Stress', 
                                _("Pit %s internal temp critical: %s C") % (self.name, temp))
            self.apply_cooling_skill()
        return True

    def apply_cooling_skill(self):
        """ Level 4 DNA: Command ventilation or fanning. """
        self.ensure_one()
        payload = {'action': 'activate_cooling', 'target_temp': 35.0}
        self.agent_instruction_json = json.dumps(payload, indent=2)
        self.agent_status_feedback = 'executing'

class FarmLotBrew(models.Model):
    """
    [ISL Layer] Fermented Asset (Vinegar/Soy/Baijiu).
    """
    _name = 'farm.lot.brew'
    _description = 'Brewed Batch'
    _inherits = {'stock.lot': 'lot_id'}
    _inherit = ['agri.traceability.mixin', 'agri.biological.valuation.mixin']

    lot_id = fields.Many2one('stock.lot', string='Base Lot', required=True, ondelete='cascade')

    # [US-120-04] Vintage Valuation
    vintage_start_date = fields.Date("Aging Start")
    is_aged_product = fields.Boolean("Aged Product", default=False)

    @api.depends('vintage_start_date')
    def _compute_fair_value(self):
        """ Dynamic revaluation based on vintage age. """
        res = super(FarmLotBrew, self)._compute_fair_value()
        for rec in self:
            if rec.vintage_start_date:
                days = (fields.Date.today() - rec.vintage_start_date).days
                years = days / 365.0
                # Premium: 10% value increase per year compounded
                rec.total_asset_value *= (1.10 ** years)
        return res
