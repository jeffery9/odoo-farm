from odoo import models, fields, api, _
import json
import logging

_logger = logging.getLogger(__name__)

class A2ANegotiation(models.Model):
    """
    State machine for Agent-to-Agent negotiation and bargaining. [US-62-2026]
    Level 2+: Coordination & Game Theory.
    """
    _name = 'agri.a2a.negotiation'
    _description = 'Agricultural Agent Negotiation'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Negotiation ID", required=True, default=lambda self: _('New'))
    
    sender_agent_id = fields.Char("Sender Agent", required=True)
    receiver_agent_id = fields.Char("Receiver Agent", required=True)
    
    intent_type = fields.Selection([
        ('service_request', 'Service Request (e.g. Harvest)'),
        ('trade_proposal', 'Trade Proposal'),
        ('clearing_request', 'Value Clearing Request')
    ], string="Intent", required=True)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('proposed', 'Proposed'),
        ('bargaining', 'Bargaining'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('executed', 'Executed'),
        ('cleared', 'Value Cleared')
    ], default='draft', tracking=True)

    payload_revision = fields.Integer("Revision", default=1)
    current_payload = fields.Text("Current PlanAPI Payload")
    
    # Financial/Value anchors
    proposed_credits = fields.Float("Proposed Credits")
    final_credits = fields.Float("Final Settled Credits")

    def action_propose(self, payload):
        self.ensure_one()
        self.write({
            'state': 'proposed',
            'current_payload': json.dumps(payload),
        })

    def evaluate_proposal(self, incoming_payload):
        self.ensure_one()
        carbon = incoming_payload.get('context_memory', {}).get('carbon_intensity', 100)
        if carbon > 50.0:
            return {'decision': 'reject', 'reason': 'Sustainability redline exceeded'}
        offered = incoming_payload.get('proposed_credits', 0.0)
        if offered < self.proposed_credits * 0.9:
            return {'decision': 'counter', 'price': self.proposed_credits * 0.95}
        return {'decision': 'accept'}
