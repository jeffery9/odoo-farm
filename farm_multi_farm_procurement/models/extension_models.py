from odoo import models, fields

class CooperativeMemberExtensionProcurement(models.Model):    _inherit = 'cooperative.member'

    joint_procurement_po_member_ids = fields.One2many('joint.procurement.po.member', 'member_id', string='Joint Procurement POs')
    hub_spoke_distribution_line_ids = fields.One2many('hub.spoke.distribution.line', 'destination_member_id', string='Distribution Lines')
    netting_settlement_ids = fields.One2many('netting.settlement', 'member_id', string='Netting Settlements')

class CooperativeEntityExtensionProcurement(models.Model):    _inherit = 'cooperative.entity'

    joint_procurement_ids = fields.One2many('joint.procurement', 'cooperative_id', string='Joint Procurements')
    procurement_planning_ids = fields.One2many('procurement.planning', 'cooperative_id', string='Procurement Planning')
    joint_procurement_po_ids = fields.One2many('joint.procurement.po', 'cooperative_id', string='Joint Procurement POs')
    hub_spoke_distribution_ids = fields.One2many('hub.spoke.distribution', 'cooperative_id', string='Hub and Spoke Distributions')
    netting_settlement_ids = fields.One2many('netting.settlement', 'cooperative_id', string='Netting Settlements')

class InternalSettlementExtensionProcurement(models.Model):    _inherit = 'internal.settlement'
    
    joint_procurement_id = fields.Many2one('joint.procurement', string='Joint Procurement')
    joint_po_member_id = fields.Many2one('joint.procurement.po.member', string='Joint PO Member')
