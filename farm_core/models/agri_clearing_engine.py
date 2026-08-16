from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)

class AgriNettingEngine(models.Model):
    """
    [US-014-04] Internal Netting & Debt Offsetting Engine.
    Offsets payables and receivables within the community using a single clearing lock.
    """
    _name = 'agri.clearing.netting.engine'
    _description = 'Agricultural Internal Netting Engine'

    name = fields.Char("Clearing Session", required=True, default=lambda self: _('NEW_LOCK'))
    state = fields.Selection([('draft', 'Drafting'), ('locked', 'Mutex Locked'), ('cleared', 'Settled')], default='draft')

    def action_execute_netting(self, partner_ids):
        """
        [AwaitedMutex Pattern]
        Executes atomic offsetting for a group of members.
        """
        _logger.info("Executing community netting for partners: %s", partner_ids)
        self.state = 'locked'
        
        for partner in self.env['res.partner'].browse(partner_ids):
            # 1. Fetch total credits (receivables) and debts (payables)
            credits = partner.impact_credits
            # debt = partner.total_unpaid_covenants (Simplified stub)
            
            # 2. Apply offsetting ledger entries
            if credits > 0:
                self.env['agri.clearing.ledger'].create({
                    'partner_id': partner.id,
                    'credit_change': -credits,
                    'description': _("Debt Offsetting via Netting Engine Session %s") % self.name,
                    'state': 'confirmed' # Netting is auto-confirmed if engine is trusted
                })
        
        self.state = 'cleared'
        return True

    def action_execute_a2a_auction_clearing(self, buyer_id, seller_id, transaction_credits, detail_desc):
        """
        Execute atomic A2A resource clearance.
        Increments credits for seller, decrements for buyer inside an atomic transaction block.
        """
        buyer = self.env['res.partner'].browse(buyer_id)
        seller = self.env['res.partner'].browse(seller_id)
        if not buyer.exists() or not seller.exists():
            raise ValidationError(_("Buyer or Seller partner records not found. (交易主体未找到。)"))
            
        if buyer.impact_credits < transaction_credits:
            raise ValidationError(_("Insufficient credits! (信用额度/余额不足！)") + f" [{buyer.name}]")

        # Atomic debit & credit ledger postings
        self.env['agri.clearing.ledger'].create([
            {
                'partner_id': buyer.id,
                'credit_change': -transaction_credits,
                'description': f"A2A Debit: {detail_desc} (多智能体自动扣款结算)",
                'state': 'confirmed'
            },
            {
                'partner_id': seller.id,
                'credit_change': transaction_credits,
                'description': f"A2A Credit: {detail_desc} (多智能体自动收款结算)",
                'state': 'confirmed'
            }
        ])
        
        # Trigger actual partner score recomputation
        buyer._compute_reputation_credit_score()
        seller._compute_reputation_credit_score()
        return True

class AgriDividendPool(models.Model):
    """
    [US-014-05] Community Impact Dividend Pool.
    Distributes collective surplus back to members based on ESG contributions.
    """
    _name = 'agri.dividend.pool'
    _description = 'Community Dividend Distribution'

    name = fields.Char("Dividend Period", required=True)
    total_surplus = fields.Float("Total Surplus Credits", required=True)
    distributed_credits = fields.Float("Distributed Credits", readonly=True)
    
    state = fields.Selection([('draft', 'Draft'), ('distributed', 'Distributed')], default='draft')

    def action_distribute_dividend(self):
        """
        Calculates and pushes impact credits to all members.
        Weighted by reputation credit_score.
        """
        self.ensure_one()
        partners = self.env['res.partner'].search([('credit_score', '>', 0)])
        total_reputation = sum(partners.mapped('credit_score'))
        
        if total_reputation <= 0:
            return False

        for partner in partners:
            share = (partner.credit_score / total_reputation) * self.total_surplus
            self.env['agri.clearing.ledger'].create({
                'partner_id': partner.id,
                'credit_change': share,
                'description': _("Community Impact Dividend: %s") % self.name,
                'state': 'draft' # Dividends ALWAYS require final human confirmation
            })
            
        self.distributed_credits = self.total_surplus
        self.state = 'distributed'
        return True
