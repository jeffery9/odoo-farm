from odoo import models, fields

class CooperativeMemberExtensionFinancial(models.Model):
    _name = 'cooperative.member'
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
    _name = 'cooperative.entity'
    _inherit = 'cooperative.entity'

    dividend_distribution_ids = fields.One2many('dividend.distribution', 'cooperative_id', string='Dividend Distributions')
    internal_credit_ids = fields.One2many('internal.credit', 'cooperative_id', string='Internal Credits')
    cooperative_treasury_ids = fields.One2many('cooperative.treasury', 'cooperative_id', string='Treasury Accounts')
    internal_loan_ids = fields.One2many('internal.loan', 'cooperative_id', string='Internal Loans')
    subsidy_disbursement_ids = fields.One2many('subsidy.disbursement', 'cooperative_id', string='Subsidy Disbursements')
    cooperative_decision_ids = fields.One2many('cooperative.decision', 'cooperative_id', string='Cooperative Decisions')
    multi_sign_process_ids = fields.One2many('multi.sign.process', 'cooperative_id', string='Multi-sign Processes')
