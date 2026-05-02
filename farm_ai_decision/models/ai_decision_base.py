# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import logging
import json
from datetime import datetime, timedelta
import random

_logger = logging.getLogger(__name__)

class AgriAiDecisionBase(models.Model):
    """
    Base model for AI decision support
    """
    _name = 'agri.ai.decision.base'
    _description = 'AI Decision Support Base Model'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'agri.ai.base.mixin']

    name = fields.Char('Name', required=True)
    decision_date = fields.Datetime('Decision Date', default=fields.Datetime.now)
    recommendation = fields.Html('Recommendation')
    status = fields.Selection([
        ('draft', 'Draft'),
        ('recommended', 'Recommended'),
        ('applied', 'Applied'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
    ], default='draft', string='Status')
    model_type = fields.Char('Model Type', help="Type of AI model used for decision")
    input_data = fields.Text('Input Data', help="JSON data used for decision making")
    output_data = fields.Text("Output Data", help="JSON result data from the model")
    decision_reasoning = fields.Html('Decision Reasoning', help="Explanation of AI decision process")
    confidence_score = fields.Float("Confidence Score (%)", default=85.0)
    priority = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ], string='Priority', default='medium')

    def action_apply_recommendation(self):
        """Apply the AI recommendation"""
        self.write({'status': 'applied'})

    def action_reject_recommendation(self):
        """Reject the AI recommendation"""
        self.write({'status': 'rejected'})

    def action_mark_completed(self):
        """Mark the decision as completed"""
        self.write({'status': 'completed'})
