from odoo import models, fields, api, _
import json
import logging

_logger = logging.getLogger(__name__)

class A2ANegotiation(models.Model):
    """
    State machine for Agent-to-Agent negotiation and bargaining. [US-092-2026]
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
        ('cleared', 'Value Cleared'),
        ('disputed', 'In Arbitration') # Level 2+ Arbitration
    ], default='draft', tracking=True)

    payload_revision = fields.Integer("Revision", default=1)
    current_payload = fields.Text("Current PlanAPI Payload")
    
    # Financial/Value anchors
    proposed_credits = fields.Float("Proposed Credits")
    final_credits = fields.Float("Final Settled Credits")
    
    # Backlink to Orchestrator (from mission_orchestrator logic)
    orchestrator_id = fields.Many2one('agri.mission.orchestrator', string="Mission Orchestrator")

    def action_propose(self, payload):
        self.ensure_one()
        self.write({
            'state': 'proposed',
            'current_payload': json.dumps(payload),
        })

    def evaluate_proposal(self, incoming_payload):
        """
        [Level 5 Integrated]
        Evaluates a proposal using standard game theory or specialized robotic logic.
        """
        self.ensure_one()
        
        # 1. Check for Sustainability Redline (Level 0 Global Control)
        carbon = incoming_payload.get('context_memory', {}).get('carbon_intensity', 100)
        if carbon > 50.0:
            return {'decision': 'reject', 'reason': 'Sustainability redline exceeded'}

        # 2. Delegate to specialized agents (e.g. Robots)
        if self.receiver_agent_id.startswith('robot:'):
            if 'farm.robot' in self.env:
                robot = self.env['farm.robot'].search([('agent_id', '=', self.receiver_agent_id)], limit=1)
                if robot:
                    return robot.evaluate_a2a_proposal(incoming_payload)

        # 3. Standard Bargaining Heuristics
        offered = incoming_payload.get('proposed_credits', 0.0)
        if offered < self.proposed_credits * 0.9:
            return {'decision': 'counter', 'price': self.proposed_credits * 0.95}
            
        return {'decision': 'accept'}

    def action_trigger_arbitration(self, reason):
        """
        [Level 2+ Arbitration]
        Transitions the negotiation to disputed state and creates an arbitrator record.
        """
        self.ensure_one()
        self.state = 'disputed'
        arbitrator = self.env['agri.a2a.arbitrator'].create({
            'negotiation_id': self.id,
            'reason': reason,
            'state': 'pending'
        })
        self.message_post(body=_("Negotiation entered Arbitration: %s") % reason)
        return arbitrator
