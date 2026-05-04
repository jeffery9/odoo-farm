from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class ProcurementPlanning(models.Model):
    """
    农资统筹预分配 [US-042-12]
    """
    _name = 'procurement.planning'
    _description = 'Procurement Planning'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Planning Name', required=True)
    cooperative_id = fields.Many2one('cooperative.entity', string='Cooperative', required=True)
    planning_date = fields.Date('Planning Date', default=fields.Date.context_today, required=True)
    planning_period = fields.Selection([
        ('quarterly', 'Quarterly'),
        ('bi_annual', 'Bi-annual'),
        ('annual', 'Annual'),
    ], string='Planning Period', required=True)
    season = fields.Char('Season')
    description = fields.Text('Description')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('executed', 'Executed'),
        ('cancelled', 'Cancelled'),
    ], string='State', default='draft', required=True)

    planning_lines = fields.One2many('procurement.planning.line', 'planning_id', string='Planning Lines')

    def action_confirm(self):
        """确认计划"""
        for planning in self:
            planning.state = 'confirmed'

    def action_execute(self):
        """执行计划"""
        for planning in self:
            planning.state = 'executed'