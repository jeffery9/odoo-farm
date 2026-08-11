from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)

class A2AArbitrator(models.Model):
    """
    Level 2+: A2A Arbitration Mechanism.
    Resolves deadlocks and disputes in negotiations based on physical evidence.
    """
    _name = 'agri.a2a.arbitrator'
    _description = 'A2A Negotiation Arbitrator'
    _inherit = ['mail.thread']

    negotiation_id = fields.Many2one('agri.a2a.negotiation', string="Linked Negotiation", required=True)
    reason = fields.Text("Dispute Reason")
    
    state = fields.Selection([
        ('pending', 'Pending Review'),
        ('investigating', 'Investigating Evidence'),
        ('resolved', 'Resolved (Settled)'),
        ('slashed', 'Resolved (Slashed)'),
        ('voided', 'Voided')
    ], default='pending', tracking=True)

    def action_investigate(self):
        """
        Runs automated evidence analysis to find a resolution.
        """
        self.ensure_one()
        self.state = 'investigating'
        
        # In 2026, the arbitrator automatically calls the EvidenceAnalyzer
        # logic on the objects linked in the negotiation's payload.
        # Placeholder for complex logic.
        return True

    def action_resolve_slashing(self, agent_to_slash_id):
        """
        Arbitrator decision: Fraud detected. Apply Slashing.
        """
        self.ensure_one()
        _logger.warning("Arbitrator resolving dispute with slashing for agent: %s", agent_to_slash_id)
        
        # 1. Trigger Slashing on the target agent (via res.partner)
        # Search for partner linked to agent_id (simple mapping for now)
        partner = self.env['res.partner'].search([('name', '=', agent_to_slash_id)], limit=1)
        if partner and hasattr(partner, 'apply_slashing'):
            partner.apply_slashing(reason=_("Arbitration Decision: Fraudulent activity detected."))
        
        # 2. Close negotiation as rejected/failed
        self.negotiation_id.write({'state': 'rejected'})
        self.state = 'slashed'
        return True

    def action_resolve_settlement(self, final_credits):
        """
        Arbitrator decision: Deadlock broken. Enforce settlement.
        """
        self.ensure_one()
        self.negotiation_id.write({
            'final_credits': final_credits,
            'state': 'accepted'
        })
        self.state = 'resolved'
        return True


class A2AResourceAuction(models.Model):
    """
    [AI-Native Resource Auction]
    Enables agents to autonomously bid virtual carbon/water credits for physical resources
    (such as robotic assets, irrigation timeslots, or processing workcenters).
    """
    _name = 'agri.a2a.resource.auction'
    _description = 'A2A Physical Resource Auction'
    _inherit = ['mail.thread']

    name = fields.Char("Auction Reference", required=True)
    resource_ref = fields.Char("Target Resource (model:id)", required=True)
    state = fields.Selection([
        ('open', 'Open for Bidding'),
        ('closed', 'Closed'),
        ('allocated', 'Resource Allocated')
    ], default='open', tracking=True)

    min_bid = fields.Float("Minimum Credit Bid", default=10.0)
    current_highest_bid = fields.Float("Highest Bid", default=0.0)
    winner_agent_id = fields.Char("Winning Agent")
    winning_bid_type = fields.Selection([
        ('carbon', 'Carbon Credit'),
        ('water', 'Water Credit')
    ], string="Credit Type", default='carbon')

    bid_line_ids = fields.One2many('agri.a2a.resource.bid', 'auction_id', string="Bids")

    def action_close_auction(self):
        """
        Closes the auction, determines the winning agent, and updates the physical asset assignment.
        """
        self.ensure_one()
        if not self.bid_line_ids:
            self.state = 'closed'
            return True

        # Find highest bid
        highest_bid_rec = max(self.bid_line_ids, key=lambda b: b.amount)
        self.write({
            'current_highest_bid': highest_bid_rec.amount,
            'winner_agent_id': highest_bid_rec.agent_id,
            'winning_bid_type': highest_bid_rec.bid_type,
            'state': 'closed'
        })

        # Dynamically lock/assign resource to the winning agent
        target_info = self.resource_ref.split(':')
        if len(target_info) == 2:
            model_name, res_id = target_info
            res_id = int(res_id)
            try:
                resource_record = self.env[model_name].browse(res_id)
                if resource_record.exists():
                    if hasattr(resource_record, 'message_post'):
                        resource_record.message_post(body=_(
                            "<b>A2A Autonomous Auction allocation</b><br/>"
                            "<b>Winner Agent:</b> %s<br/>"
                            "<b>Winning Bid:</b> %s %s Credits"
                        ) % (highest_bid_rec.agent_id, highest_bid_rec.amount, highest_bid_rec.bid_type))
            except Exception as e:
                _logger.error("Failed to dynamically allocate resource via auction: %s", str(e))

        self.state = 'allocated'
        return True


class A2AResourceBid(models.Model):
    """
    Individual bid submitted autonomously by an agent using its credit ledger.
    """
    _name = 'agri.a2a.resource.bid'
    _description = 'A2A Physical Resource Bid'

    auction_id = fields.Many2one('agri.a2a.resource.auction', string="Auction", required=True, ondelete='cascade')
    agent_id = fields.Char("Agent ID", required=True)
    amount = fields.Float("Bid Amount (Credits)", required=True)
    bid_type = fields.Selection([
        ('carbon', 'Carbon Credit'),
        ('water', 'Water Credit')
    ], default='carbon', required=True)
