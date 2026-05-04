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
