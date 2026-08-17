from odoo import models, fields, api

class CooperativeMember(models.Model):
    _inherit = 'cooperative.member'

    subscription_ids = fields.One2many(
        'farm.csa.subscription',
        'coop_member_id',
        string='CSA Subscriptions'
    )

    @api.depends('subscription_ids.credit_held_amount', 'subscription_ids.state', 'subscription_ids.use_coop_credit')
    def _compute_credit_usage(self):
        super()._compute_credit_usage()
        for record in self:
            csa_usage = sum(record.subscription_ids.filtered(
                lambda s: s.state == 'active' and s.use_coop_credit
            ).mapped('credit_held_amount'))
            record.credit_used += csa_usage


class AgriClearingLedger(models.Model):
    _inherit = 'agri.clearing.ledger'

    source_ref = fields.Reference(
        selection_add=[('farm.csa.subscription', 'CSA Subscription')],
        ondelete={'farm.csa.subscription': 'cascade'}
    )
