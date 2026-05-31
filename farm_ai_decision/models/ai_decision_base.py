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

    # Bridge to execution [US-TECH-AI-01]
    result_intervention_id = fields.Reference(
        selection=[('mrp.production', 'Intervention'), ('project.task', 'Task')],
        string='Triggered Action',
        readonly=True
    )

    def action_apply_recommendation(self):
        """
        [SOLID Refactored] Apply the AI recommendation and trigger an actual intervention.
        """
        self.ensure_one()
        self.write({'status': 'applied'})
        
        # Trigger creation of a correction intervention if logic exists
        if hasattr(self, '_create_correction_intervention'):
            intervention = self._create_correction_intervention()
            if intervention:
                self.result_intervention_id = f"{intervention._name},{intervention.id}"
                self.message_post(body=_("AI Action: Automatically created correction intervention %s") % intervention.name)

    def _create_correction_intervention(self):
        """
        Stub for specific AI models to implement their execution logic.
        Should return an intervention record.
        """
        return False

    def action_reject_recommendation(self):
        """Reject the AI recommendation"""
        self.write({'status': 'rejected'})

    def action_mark_completed(self):
        """Mark the decision as completed"""
        self.write({'status': 'completed'})
