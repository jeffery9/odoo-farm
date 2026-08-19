# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class FarmOrchardCycle(models.Model):
    """
    [ISL Layer] Annual Nurturing Cycle for Orchard.
    Proxies mrp.production to manage perennial interventions.
    """
    _name = 'farm.orchard.cycle'
    _description = 'Annual Nurturing Cycle'
    _inherits = {'mrp.production': 'production_id'}
    _inherit = [
        'agri.intervention.mixin',
        'agri.weather.sensitive.mixin',
        'agri.agent.instruction.mixin'
    ]

    production_id = fields.Many2one('mrp.production', string='Base Order', required=True, ondelete='cascade')
    
    # Orchard Specifics [US-ORCH-03]
    intervention_scope = fields.Selection([
        ('block', 'Block Level'),
        ('tree', 'Single Tree Level')
    ], string="Scope", default='block')
    
<<<<<<< HEAD
    target_tree_ids = fields.Many2many('stock.lot', 'farm_orchard_cycle_stock_lot_rel', 'cycle_id', 'lot_id', string="Target Trees", domain=[('is_fruit_tree', '=', True)])
=======
    target_tree_ids = fields.Many2many('stock.lot', 'farm_orchard_cycle_stock_lot_nurture_rel', 'cycle_id', 'lot_id', string="Target Trees", domain=[('is_fruit_tree', '=', True)])
>>>>>>> 5351cad217860264bdd3ca8394fa45a799fce3d0

    def action_confirm(self):
        """ [Level 2 DNA] Prevent pruning/spraying during extreme frost. """
        self.check_weather_window('general')
        return super(FarmOrchardCycle, self).action_confirm()

class OrchardStockLot(models.Model):
    _name = 'stock.lot'

    """
    [ISL Layer] Digital Twin of a Single Fruit Tree or Block."""
    _inherit = ['stock.lot', 'agri.biological.inventory.mixin', 
        'agri.growth.cycle.mixin', 
        'agri.biological.valuation.mixin', 
        'agri.geospatial.mixin',
        'agri.traceability.mixin'
    ]

    # Enhanced Fields [US-ORCH-01]
    is_fruit_tree = fields.Boolean("Is Fruit Tree", default=False)
    tree_variety_id = fields.Many2one('agri.industry.variety', string="Variety DNA")
    planting_date = fields.Date("Planting Date")
    
    # Maturity Logic [US-ORCH-02]
    expected_harvest_gdd = fields.Float("Target GDD for Ripening")
    maturity_status = fields.Float("Maturity Progress (%)", compute='_compute_maturity_progress')

    @api.depends('accumulated_gdd', 'expected_harvest_gdd')
    def _compute_maturity_progress(self):
        for rec in self:
            if rec.expected_harvest_gdd > 0:
                rec.maturity_status = min(100.0, (rec.accumulated_gdd / rec.expected_harvest_gdd) * 100.0)
            else:
                rec.maturity_status = 0.0

    def action_update_valuation(self):
        """ US-ORCH-04 Dynamic valuation based on age and biomass. """
        self.ensure_one()
        # Call Level 3 DNA
        self._compute_fair_value()
        return True

class OrchardOperation(models.Model):
    """
    Orchard Operation proxy for project.task.
    Used for ad-hoc manual interventions (e.g. Pruning).
    """
    _name = 'farm.orchard.operation'
    _description = 'Orchard Manual Operation'
    _inherits = {'project.task': 'operation_id'}
    _inherit = ['mail.thread', 'mail.activity.mixin', 'agri.quality.gate.mixin']

    operation_id = fields.Many2one('project.task', required=True, ondelete='cascade')
    tree_id = fields.Many2one('stock.lot', domain=[('is_fruit_tree', '=', True)], string='Target Asset')
    
    pruning_type = fields.Selection([
        ('formative', 'Formative'),
        ('maintenance', 'Maintenance'),
        ('fruiting', 'Fruiting')
    ], string='Pruning Category')

    def action_done(self):
        """ Enforce Quality Gate before closing intervention. """
        self.validate_quality_gate()
        return self.operation_id.action_fsm_validate()

    def action_view_tree_details(self):
        return True
