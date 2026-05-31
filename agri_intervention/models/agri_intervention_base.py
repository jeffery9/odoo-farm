# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class AgriInterventionBase(models.AbstractModel):
    """
    [L0 Foundation] The Core Intervention Abstraction.
    Follows ISA-95 standards for Physical/Biological actions.
    """
    _name = 'agri.intervention.base'
    _description = 'Agricultural Intervention Base Engine'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Intervention Reference', required=True, copy=False, readonly=True, default=lambda self: _('New'))
    
    # Standard Lifecycle [ISA-95 compliant]
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed/Planned'),
        ('in_progress', 'Executing'),
        ('done', 'Completed'),
        ('cancel', 'Cancelled')
    ], string='Status', default='draft', tracking=True)

    # GS1 EPCIS Mapping [EPCIS Alignment]
    gs1_biz_step = fields.Selection([
        ('commissioning', 'Commissioning (Setup)'),
        ('processing', 'Processing (Transformation)'),
        ('harvesting', 'Harvesting'),
        ('inspecting', 'Inspecting'),
        ('packing', 'Packing'),
        ('shipping', 'Shipping'),
        ('receiving', 'Receiving'),
    ], string='GS1 Business Step', compute='_compute_gs1_biz_step', store=True)

    @api.depends('intervention_type', 'state')
    def _compute_gs1_biz_step(self):
        """ Maps agricultural types to international EPCIS business steps """
        for rec in self:
            if not hasattr(rec, 'intervention_type'):
                rec.gs1_biz_step = 'processing'
                continue
                
            mapping = {
                'harvesting': 'harvesting',
                'tillage': 'commissioning',
                'sowing': 'commissioning',
                'fertilizing': 'processing',
                'protection': 'processing',
                'aerial_spraying': 'processing',
                'feeding': 'processing',
                'medical': 'inspecting',
                'process': 'processing'
            }
            rec.gs1_biz_step = mapping.get(rec.intervention_type, 'processing')

    # Contextual Domain
    location_id = fields.Many2one('farm.location', string='Target Location', help='Where the intervention takes place')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    
    # Timing
    date_planned_start = fields.Datetime('Planned Start', tracking=True)
    date_planned_finished = fields.Datetime('Planned Finish')
    date_start = fields.Datetime('Actual Start', readonly=True)
    date_finished = fields.Datetime('Actual Finish', readonly=True)

    # Actor
    responsible_id = fields.Many2one('res.users', string='Responsible', default=lambda self: self.env.user)

    # ---------------------------------------------------------
    # Execution Orchestration (The Engine Part)
    # ---------------------------------------------------------

    def action_confirm_base(self):
        """Standard confirmation flow with plugin hooks"""
        for rec in self:
            rec._run_plugins('pre_confirm')
            rec.state = 'confirmed'
            rec._run_plugins('post_confirm')
        return True

    def action_start_base(self):
        """Standard start flow with gating hooks"""
        for rec in self:
            # Gating check: Plugins can raise UserError to block start
            rec._run_plugins('pre_start')
            rec.write({
                'state': 'in_progress',
                'date_start': fields.Datetime.now()
            })
            rec._run_plugins('post_start')
        return True

    def action_done_base(self):
        """Standard completion flow with audit hooks"""
        for rec in self:
            rec._run_plugins('pre_done')
            rec.write({
                'state': 'done',
                'date_finished': fields.Datetime.now()
            })
            rec._run_plugins('post_done')
        return True

    # ---------------------------------------------------------
    # Plugin System [DIP Principle]
    # ---------------------------------------------------------

    @api.model
    def _get_intervention_plugins(self):
        """
        Registry for intervention plugins. 
        Modules should override this to add their own plugins.
        Returns a list of dicts: [{'name': 'weather_gating', 'class': 'agri.intervention.plugin.weather'}]
        """
        return []

    def _run_plugins(self, hook_point):
        """Internal runner for plugin hooks"""
        plugins = self._get_intervention_plugins()
        for plugin_info in plugins:
            plugin_model = self.env.get(plugin_info['class'])
            if plugin_model:
                try:
                    # Plugins are called with (intervention_record, hook_point)
                    plugin_model.execute_hook(self, hook_point)
                except UserError:
                    raise
                except Exception as e:
                    _logger.error(f"Intervention Plugin Error ({plugin_info['name']}): {str(e)}")

class AgriInterventionPlugin(models.AbstractModel):
    """
    Interface for Intervention Plugins.
    """
    _name = 'agri.intervention.plugin'
    _description = 'Intervention Plugin Interface'

    @api.model
    def execute_hook(self, intervention, hook_point):
        """
        Method to be implemented by specific plugins.
        hook_point: pre_confirm, post_confirm, pre_start, post_start, pre_done, post_done
        """
        pass

class AgriDnaPlugin(models.AbstractModel):
    """
    [L1 DNA Foundation] Interface for DNA Inheritance Plugins.
    Handles the transfer of physical/biological metadata from inputs to outputs.
    """
    _name = 'agri.dna.plugin'
    _description = 'DNA Inheritance Plugin Interface'

    @api.model
    def inherit_dna(self, lot, inputs):
        """
        Lot: The target stock.lot receiving the DNA.
        Inputs: The stock.move records (raw materials) used.
        """
        pass
