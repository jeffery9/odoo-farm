from odoo import models, fields, _


class CooperativeMemberExtension(models.Model):
    """
    扩展合作社会员模型以关联新的功能 [US-042-06 through US-042-22]
    """
    _inherit = 'cooperative.member'

    # US-042-06 fields - already in base model
    # US-042-07 fields - already in base model
    # US-042-14 fields - already in base model
    # US-042-15 fields - already in base model

    # Add One2many relationships for new models
    share_transaction_ids = fields.One2many('share.transaction', 'member_id', string='Share Transactions')
    dividend_line_ids = fields.One2many('dividend.line', 'member_id', string='Dividend Lines')
    credit_transaction_ids = fields.One2many('credit.transaction', 'member_id', string='Credit Transactions')
    machinery_rental_ids = fields.One2many('machinery.rental', 'renter_member_id', string='Machinery Rentals')
    internal_marketplace_transaction_supplier_ids = fields.One2many('internal.marketplace.transaction', 'supplier_member_id', string='Marketplace Transactions (Supplier)')
    internal_marketplace_transaction_requester_ids = fields.One2many('internal.marketplace.transaction', 'requester_member_id', string='Marketplace Transactions (Requester)')
    service_order_ids = fields.One2many('service.order', 'requester_member_id', string='Service Orders')
    borrower_loan_ids = fields.One2many('internal.loan', 'borrower_member_id', string='Borrowed Loans')
    lender_loan_ids = fields.One2many('internal.loan', 'lender_member_id', string='Lent Loans')
    subsidy_line_ids = fields.One2many('subsidy.disbursement.line', 'member_id', string='Subsidy Lines')
    sign_process_ids = fields.One2many('multi.sign.line', 'signer_member_id', string='Sign Processes')
    joint_procurement_po_member_ids = fields.One2many('joint.procurement.po.member', 'member_id', string='Joint Procurement POs')
    hub_spoke_distribution_line_ids = fields.One2many('hub.spoke.distribution.line', 'destination_member_id', string='Distribution Lines')
    netting_settlement_ids = fields.One2many('netting.settlement', 'member_id', string='Netting Settlements')


class InternalSettlementExtension(models.Model):
    """
    扩展内部结算模型以支持新的功能 [US-042-10, US-042-20, US-042-22]
    """
    _inherit = 'internal.settlement'

    # Add new settlement types for US-19-* stories
    settlement_type = fields.Selection(selection_add=[
        ('resource_rental', 'Resource Rental'),
        ('service_fee', 'Service Fee'),
        ('joint_procurement', 'Joint Procurement'),
        ('marketing_fee', 'Marketing Fee'),
        ('management_fee', 'Management Fee'),
        ('profit_sharing', 'Profit Sharing'),
        ('internal_transaction', 'Internal Transaction'),
        ('subsidy_distribution', 'Subsidy Distribution'),
        ('netting_settlement', 'Netting Settlement'),
    ])

    # US-042-10 and US-042-20 related fields
    joint_procurement_id = fields.Many2one('joint.procurement', string='Joint Procurement')
    joint_po_member_id = fields.Many2one('joint.procurement.po.member', string='Joint PO Member')

    # Add method to support new functionality
    def action_generate_official_document(self):
        """生成正式结算文档"""
        # This would generate official settlement documents in dual language
        pass


class CooperativeEntityExtension(models.Model):
    """
    扩展合作社实体模型以支持新功能 [US-042-06 through US-042-22]
    """
    _inherit = 'cooperative.entity'

    # Add One2many relationships for new models
    member_ids = fields.One2many('cooperative.member', 'cooperative_id', string='Members')
    share_transaction_ids = fields.One2many('share.transaction', string='Share Transactions', compute='_compute_share_transactions')
    dividend_distribution_ids = fields.One2many('dividend.distribution', 'cooperative_id', string='Dividend Distributions')
    internal_credit_ids = fields.One2many('internal.credit', 'cooperative_id', string='Internal Credits')
    shared_machinery_ids = fields.One2many('shared.machinery.pool', 'cooperative_id', string='Shared Machinery')
    quality_control_standard_ids = fields.One2many('quality.control.standard', 'cooperative_id', string='Quality Standards')
    joint_procurement_ids = fields.One2many('joint.procurement', 'cooperative_id', string='Joint Procurements')
    procurement_planning_ids = fields.One2many('procurement.planning', 'cooperative_id', string='Procurement Planning')
    agri_service_ids = fields.One2many('agri.service', 'cooperative_id', string='Agricultural Services')
    cooperative_treasury_ids = fields.One2many('cooperative.treasury', 'cooperative_id', string='Treasury Accounts')
    internal_loan_ids = fields.One2many('internal.loan', 'cooperative_id', string='Internal Loans')
    subsidy_disbursement_ids = fields.One2many('subsidy.disbursement', 'cooperative_id', string='Subsidy Disbursements')
    cooperative_decision_ids = fields.One2many('cooperative.decision', 'cooperative_id', string='Cooperative Decisions')
    multi_sign_process_ids = fields.One2many('multi.sign.process', 'cooperative_id', string='Multi-sign Processes')
    joint_procurement_po_ids = fields.One2many('joint.procurement.po', 'cooperative_id', string='Joint Procurement POs')
    hub_spoke_distribution_ids = fields.One2many('hub.spoke.distribution', 'cooperative_id', string='Hub and Spoke Distributions')
    netting_settlement_ids = fields.One2many('netting.settlement', 'cooperative_id', string='Netting Settlements')

    def _compute_share_transactions(self):
        """计算合作社的股份交易"""
        ShareTransaction = self.env['share.transaction']
        for entity in self:
            members = entity.member_farm_ids.mapped('cooperative_member_ids')
            entity.share_transaction_ids = ShareTransaction.search([('member_id', 'in', members.ids)])


class FarmEntityExtension(models.Model):
    """
    扩展农场实体模型以支持新功能 [US-042-06 through US-042-22]
    """
    _inherit = 'farm.entity'

    # Add One2many relationships for new models
    cooperative_member_ids = fields.One2many('cooperative.member', 'partner_id', string='Cooperative Members')

    def _get_all_related_documents(self):
        """
        获取实体相关的所有文档 [US-042-19]
        This method would be used to retrieve all documents related to this entity
        for audit and compliance checking purposes.
        """
        documents = {
            'purchase_orders': self.env['purchase.order'].search([('company_id', '=', self.company_id.id)]),
            'sales_orders': self.env['sale.order'].search([('company_id', '=', self.company_id.id)]),
            'stock_movements': self.env['stock.picking'].search([('company_id', '=', self.company_id.id)]),
            'financial_records': self.env['account.move'].search([('company_id', '=', self.company_id.id)]),
        }
        return documents

class StockLotExtension(models.Model):
    """
    US-042-27: 产品/批次单社归属唯一性
    Ensures a lot is managed by only one cooperative for traceability/subsidy integrity.
    """
    _inherit = 'stock.lot'

    assigned_cooperative_id = fields.Many2one('cooperative.entity', string="Responsible Cooperative",
                                             help="The single cooperative responsible for this product's compliance/marketing.")
    
    cooperative_purpose = fields.Selection(related='assigned_cooperative_id.purpose_type', string="Cooperative Purpose Context")
    
    is_government_audited = fields.Boolean("Government Audit Passed", default=False)

    def action_assign_cooperative(self, cooperative_id):
        """
        Assigns the lot to a cooperative. 
        Enforces business rule: one lot -> one cooperative.
        """
        self.ensure_one()
        if self.assigned_cooperative_id and self.assigned_cooperative_id.id != cooperative_id:
            from odoo.exceptions import UserError
            raise UserError(_("EXCLUSIVITY VIOLATION: This lot is already assigned to cooperative %s. "
                              "A product lot can only belong to one cooperative for compliance integrity.") % self.assigned_cooperative_id.name)
        self.assigned_cooperative_id = cooperative_id