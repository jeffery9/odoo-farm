from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class AgriCooperativeResourceSharing(models.Model):
    """
    US-057-05: 合作社/产业园资源跨场协同 (Cooperative/Industrial Park Cycle)
    Model for coordinating resource sharing between farms in cooperatives/parks
    """
    _name = 'agri.cooperative.resource.sharing'
    _description = 'Cooperative Resource Sharing Platform'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Resource Sharing Plan', required=True, copy=False)
    description = fields.Text('Description')

    # Cooperative information
    cooperative_id = fields.Many2one('res.partner', string='Cooperative/Industrial Park',
                                     domain=[('is_cooperative', '=', True)])
    sharing_type = fields.Selection([
        ('waste_exchange', 'Waste Exchange'),
        ('resource_sharing', 'Resource Sharing'),
        ('equipment_sharing', 'Equipment Sharing'),
        ('knowledge_exchange', 'Knowledge Exchange'),
    ], string='Sharing Type', required=True)

    # Supply/Demand matching
    demand_farm_id = fields.Many2one('res.partner', string='Demand Farm',
                                     help='Farm that needs resources')
    supply_farm_id = fields.Many2one('res.partner', string='Supply Farm',
                                     help='Farm that has excess resources')
    resource_type = fields.Char('Resource Type', help='Type of resource being shared')
    quantity = fields.Float('Quantity')
    unit_uom = fields.Many2one('uom.uom', string='Unit of Measure')

    # A2A coordination (Agent-to-Agent)
    demand_agent_id = fields.Many2one('res.users', string='Demand Agent')
    supply_agent_id = fields.Many2one('res.users', string='Supply Agent')
    a2a_signal_status = fields.Selection([
        ('published', 'Published'),
        ('matched', 'Matched'),
        ('in_transit', 'In Transit'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], string='A2A Signal Status', default='published')

    # Netting engine integration
    netting_transaction_id = fields.Char('Netting Transaction ID',
                                         help='For automatic reconciliation engine')
    logistics_cost = fields.Float('Logistics Cost')
    resource_value = fields.Float('Resource Value', compute='_compute_resource_value', store=True, precompute=True)

    # Timeline
    publish_date = fields.Date('Publish Date', default=fields.Date.context_today)
    match_date = fields.Date('Match Date')
    delivery_date = fields.Date('Delivery Date')
    completion_date = fields.Date('Completion Date')

    # Status
    status = fields.Selection([
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('matched', 'Matched'),
        ('in_transit', 'In Transit'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ], string='Status', default='draft')

    # Related circular flows
    circular_flow_id = fields.Many2one('agri.sustainability.circular.flow', string='Circular Flow')

    @api.depends('quantity', 'unit_uom')
    def _compute_resource_value(self):
        """Compute resource value based on quantity and market rates"""
        for record in self:
            # Simplified calculation - in real implementation would use market rates
            record.resource_value = record.quantity * 100 if record.quantity else 0.0

    @api.constrains('quantity')
    def _check_positive_quantity(self):
        for record in self:
            if record.quantity <= 0:
                raise ValidationError(_("Quantity must be positive."))

    def action_publish_signal(self):
        """Publish supply/demand signal for A2A coordination"""
        for record in self:
            record.status = 'published'
            record.a2a_signal_status = 'published'
            record.publish_date = fields.Date.context_today(record)
            record.message_post(body=_("Supply/demand signal published for A2A coordination"))

    def action_match_resources(self):
        """Match supply with demand (A2A protocol coordination)"""
        for record in self:
            if not record.demand_farm_id or not record.supply_farm_id:
                raise ValidationError(_("Both demand and supply farms must be specified."))

            record.status = 'matched'
            record.a2a_signal_status = 'matched'
            record.match_date = fields.Date.context_today(record)

            # Generate netting transaction ID
            record.netting_transaction_id = self.env['ir.sequence'].next_by_code('agri.resource.sharing.transaction') or '/'

            record.message_post(body=_("Supply and demand matched. Netting transaction: %s") % record.netting_transaction_id)

    def action_start_transit(self):
        """Mark resource as in transit"""
        for record in self:
            record.status = 'in_transit'
            record.a2a_signal_status = 'in_transit'
            record.message_post(body=_("Resource in transit from %s to %s") %
                              (record.supply_farm_id.name, record.demand_farm_id.name))

    def action_complete_transaction(self):
        """Complete the resource sharing transaction"""
        for record in self:
            record.status = 'completed'
            record.a2a_signal_status = 'completed'
            record.completion_date = fields.Date.context_today(record)

            # Create circular flow record
            circular_flow = self.env['agri.sustainability.circular.flow'].create({
                'name': f'Resource Sharing: {record.name}',
                'flow_type': 'recycling' if 'waste' in record.resource_type.lower() else 'waste_to_resource',
                'input_product_id': self.env.ref('product.product_product_1').id, # Placeholder - would need to select proper product
                'output_product_id': self.env.ref('product.product_product_1').id, # Placeholder
                'input_quantity': record.quantity,
                'output_quantity': record.quantity * 0.9, # Assume 10% loss
                'status': 'completed',
                'revenue': record.resource_value,
            })
            record.circular_flow_id = circular_flow

            record.message_post(body=_("Resource sharing transaction completed. Circular flow created: %s") %
                              record.circular_flow_id.name if record.circular_flow_id else 'N/A')


class AgriInternalNettingEngine(models.Model):
    """
    Internal netting engine for cross-farm resource accounting
    """
    _name = 'agri.internal.netting.engine'
    _description = 'Internal Netting Engine for Cross-Farm Reconciliation'

    transaction_id = fields.Char('Transaction ID', required=True, copy=False)
    cooperative_id = fields.Many2one('res.partner', string='Cooperative')

    # Resource flow details
    supply_farm_id = fields.Many2one('res.partner', string='Supply Farm')
    demand_farm_id = fields.Many2one('res.partner', string='Demand Farm')
    resource_type = fields.Char('Resource Type')
    quantity = fields.Float('Quantity')
    value_amount = fields.Float('Value Amount')

    # Logistics and cost accounting
    logistics_cost = fields.Float('Logistics Cost')
    net_value = fields.Float('Net Value', compute='_compute_net_value', store=True, precompute=True)

    # Accounting
    debit_farm_id = fields.Many2one('res.partner', string='Debit Farm')
    credit_farm_id = fields.Many2one('res.partner', string='Credit Farm')
    accounting_date = fields.Date('Accounting Date', default=fields.Date.context_today)

    # Status
    status = fields.Selection([
        ('pending', 'Pending'),
        ('reconciled', 'Reconciled'),
        ('settled', 'Settled'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='pending')

    # Related transactions
    related_sharing_id = fields.Many2one('agri.cooperative.resource.sharing', string='Related Sharing')

    @api.depends('value_amount', 'logistics_cost')
    def _compute_net_value(self):
        for record in self:
            record.net_value = record.value_amount - record.logistics_cost

    @api.model
    def create(self, vals):
        if 'transaction_id' not in vals or not vals['transaction_id']:
            vals['transaction_id'] = self.env['ir.sequence'].next_by_code('agri.netting.transaction') or '/'
        return super().create(vals)

    def action_reconcile_transaction(self):
        """Reconcile the cross-farm resource transaction"""
        for record in self:
            record.status = 'reconciled'
            record.message_post(body=_("Transaction reconciled between %s and %s") %
                              (record.supply_farm_id.name, record.demand_farm_id.name))

    def action_settle_transaction(self):
        """Settle the transaction (final accounting)"""
        for record in self:
            if record.status != 'reconciled':
                raise ValidationError(_("Transaction must be reconciled before settlement."))

            record.status = 'settled'
            record.message_post(body=_("Transaction settled. Net value: %s") % record.net_value)