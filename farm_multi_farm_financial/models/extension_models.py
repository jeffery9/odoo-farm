from odoo import models, fields, api, _
from odoo.exceptions import UserError

class InternalSettlement(models.Model):
    _inherit = 'internal.settlement'

    # Governance Linkage [US-042-18]
    multi_sign_process_id = fields.Many2one('multi.sign.process', string="Required Signatures", readonly=True)

    def _check_multi_sign_status(self):
        """ Intercepts confirmation to check for required signatures """
        self.ensure_one()
        # Strategy: Threshold-based mandatory signing
        # E.g. Any settlement > 10,000 requires multi-sign
        threshold = 10000.0
        if self.amount >= threshold and not self.multi_sign_process_id:
            # Determine cooperative from debtor or creditor
            target_partner = self.to_entity_id
            farm_entity = self.env['farm.entity'].search([('company_id.partner_id', '=', target_partner.id)], limit=1)
            
            if farm_entity and farm_entity.cooperative_id:
                process = self.env['multi.sign.process'].create({
                    'name': _("High-Value Settlement Approval: %s") % self.name,
                    'process_type': 'large_purchase',
                    'cooperative_id': farm_entity.cooperative_id.id,
                    'required_signers': 3,
                    'document_reference': f"{self._name},{self.id}",
                    'description': _("Mandatory approval for settlement of %s %s") % (self.amount, self.currency_id.name)
                })
                self.multi_sign_process_id = process.id
                raise UserError(_("FINANCIAL LOCK: Settlement amount exceeds threshold. A Multi-sign Process (%s) has been initiated. Approval required before confirmation.") % process.name)

        if self.multi_sign_process_id and self.multi_sign_process_id.state != 'approved':
            raise UserError(_("GOVERNANCE LOCK: Multi-sign process %s is still in status '%s'. Please complete all signatures.") % 
                            (self.multi_sign_process_id.name, self.multi_sign_process_id.state))
        
        return super(InternalSettlement, self)._check_multi_sign_status()


class CooperativeMemberExtensionFinancial(models.Model):
    _inherit = 'cooperative.member'

    share_transaction_ids = fields.One2many('share.transaction', 'member_id', string='Share Transactions')
    dividend_line_ids = fields.One2many('dividend.line', 'member_id', string='Dividend Lines')
    credit_transaction_ids = fields.One2many('credit.transaction', 'member_id', string='Credit Transactions')
    internal_marketplace_transaction_supplier_ids = fields.One2many('internal.marketplace.transaction', 'supplier_member_id', string='Marketplace Transactions (Supplier)')
    internal_marketplace_transaction_requester_ids = fields.One2many('internal.marketplace.transaction', 'requester_member_id', string='Marketplace Transactions (Requester)')
    borrower_loan_ids = fields.One2many('internal.loan', 'borrower_member_id', string='Borrowed Loans')
    lender_loan_ids = fields.One2many('internal.loan', 'lender_member_id', string='Lent Loans')
    subsidy_line_ids = fields.One2many('subsidy.disbursement.line', 'member_id', string='Subsidy Lines')
    sign_process_ids = fields.One2many('multi.sign.line', 'signer_member_id', string='Sign Processes')

class CooperativeEntityExtensionFinancial(models.Model):
    _inherit = 'cooperative.entity'

    dividend_distribution_ids = fields.One2many('dividend.distribution', 'cooperative_id', string='Dividend Distributions')
    internal_credit_ids = fields.One2many('internal.credit', 'cooperative_id', string='Internal Credits')
    cooperative_treasury_ids = fields.One2many('cooperative.treasury', 'cooperative_id', string='Treasury Accounts')
    internal_loan_ids = fields.One2many('internal.loan', 'cooperative_id', string='Internal Loans')
    subsidy_disbursement_ids = fields.One2many('subsidy.disbursement', 'cooperative_id', string='Subsidy Disbursements')
    cooperative_decision_ids = fields.One2many('cooperative.decision', 'cooperative_id', string='Cooperative Decisions')
    multi_sign_process_ids = fields.One2many('multi.sign.process', 'cooperative_id', string='Multi-sign Processes')
