from odoo import models, fields, api

class CooperativeMemberExtension(models.Model):
    _inherit = 'cooperative.member'

class InternalSettlementExtension(models.Model):
    _inherit = 'internal.settlement'
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

class CooperativeEntityExtension(models.Model):
    _inherit = 'cooperative.entity'

class FarmEntityExtension(models.Model):
    _inherit = 'farm.entity'
    
    def action_generate_official_document(self):
        return True
        
    def get_related_documents(self):
        return {}

class StockLotExtension(models.Model):
    _inherit = 'stock.lot'
