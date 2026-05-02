from odoo import models, fields, _

class CooperativeMemberExtension(models.Model):
    """
    扩展合作社会员模型以关联新的功能 [US-19-06 through US-19-22]
    """
    _inherit = 'cooperative.member'
    service_order_ids = fields.One2many('service.order', 'requester_member_id', string='Service Orders')

class InternalSettlementExtension(models.Model):
    """
    扩展内部结算模型以支持新的功能 [US-19-10, US-19-20, US-19-22]
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
    ], ondelete={'resource_rental': 'set default', 'service_fee': 'set default', 'joint_procurement': 'set default', 'marketing_fee': 'set default', 'management_fee': 'set default', 'profit_sharing': 'set default', 'internal_transaction': 'set default', 'subsidy_distribution': 'set default', 'netting_settlement': 'set default'})

    def action_generate_official_document(self):
        """生成正式结算文档"""
        pass

class CooperativeEntityExtension(models.Model):
    """
    扩展合作社实体模型以支持新功能 [US-19-06 through US-19-22]
    """
    _inherit = 'cooperative.entity'
    member_ids = fields.One2many('cooperative.member', 'cooperative_id', string='Members')
    agri_service_ids = fields.One2many('agri.service', 'cooperative_id', string='Agricultural Services')

class FarmEntityExtension(models.Model):
    """
    扩展农场实体模型以支持新功能 [US-19-06 through US-19-22]
    """
    _inherit = 'farm.entity'
    cooperative_member_ids = fields.One2many('cooperative.member', 'partner_id', string='Cooperative Members')

    def _get_all_related_documents(self):
        """
        获取实体相关的所有文档 [US-19-19]
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
    US-19-27: 产品/批次单社归属唯一性
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
