from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class JointProcurementPO(models.Model):
    """
    统购虚拟合并与供应商统一对账 [US-042-20]
    """
    _name = 'joint.procurement.po'
    _description = 'Joint Procurement Purchase Order'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('PO Reference', required=True, default=lambda self: _('New'))
    cooperative_id = fields.Many2one('cooperative.entity', string='Cooperative', required=True)
    supplier_id = fields.Many2one('res.partner', string='Supplier', required=True)
    procurement_date = fields.Date('Procurement Date', default=fields.Date.context_today, required=True)
    total_amount = fields.Float('Total Amount', required=True)
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    description = fields.Text('Description')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('confirmed', 'Confirmed'),
        ('approved', 'Approved'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='State', default='draft', required=True)

    # US-042-20 specific fields
    parent_po_id = fields.Many2one('purchase.order', string='Parent PO')
    child_po_ids = fields.One2many('joint.procurement.po.member', 'parent_po_id', string='Member POs')
    unified_invoice_id = fields.Many2one('account.move', string='Unified Invoice')

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('joint.procurement.po') or '/'
        return super().create(vals)

    def action_confirm(self):
        """确认统购PO"""
        for po in self:
            po.state = 'confirmed'

    def action_create_member_pos(self):
        """为各成员创建子PO"""
        JointPOMember = self.env['joint.procurement.po.member']
        for po in self:
            # Create member POs based on the parent PO
            for child_line in po.child_po_ids:
                member_po = JointPOMember.create({
                    'parent_po_id': po.id,
                    'member_id': child_line.member_id.id,
                    'product_id': child_line.product_id.id,
                    'quantity': child_line.quantity,
                    'unit_price': child_line.unit_price,
                    'amount': child_line.amount,
                    'state': 'draft',
                })

        # Update parent PO state
        self.state = 'done'


class JointProcurementPOMember(models.Model):
    """
    统购子PO [US-042-20]
    """
    _name = 'joint.procurement.po.member'
    _description = 'Joint Procurement Member PO'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    parent_po_id = fields.Many2one('joint.procurement.po', string='Parent PO', required=True, ondelete='cascade')
    member_id = fields.Many2one('cooperative.member', string='Member', required=True)
    product_id = fields.Many2one('product.product', string='Product', required=True)
    quantity = fields.Float('Quantity', required=True)
    unit_price = fields.Float('Unit Price', required=True)
    amount = fields.Float('Amount', compute='_compute_amount', store=True, precompute=True)
    delivery_date = fields.Date('Delivery Date')
    description = fields.Text('Description')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='State', default='draft', required=True)

    # Field for US-042-20: Internal debt to cooperative
    internal_debt_id = fields.Many2one('internal.settlement', string='Internal Debt')

    @api.depends('quantity', 'unit_price')
    def _compute_amount(self):
        for record in self:
            record.amount = record.quantity * record.unit_price

    def action_create_internal_debt(self):
        """创建内部债务"""
        for member_po in self:
            if not member_po.internal_debt_id:
                settlement = self.env['internal.settlement'].create({
                    'from_entity_id': member_po.member_id.partner_id.company_id.id,
                    'to_entity_id': member_po.parent_po_id.cooperative_id.company_id.id,
                    'settlement_type': 'joint_procurement',
                    'amount': member_po.amount,
                    'description': f'Internal debt for joint procurement {member_po.parent_po_id.name}',
                    'settlement_date': member_po.parent_po_id.procurement_date,
                })
                member_po.internal_debt_id = settlement.id


class HubSpokeDistribution(models.Model):
    """
    统配物流拆分与配送存证 [US-042-21]
    """
    _name = 'hub.spoke.distribution'
    _description = 'Hub and Spoke Distribution'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Distribution Reference', required=True, default=lambda self: _('New'))
    cooperative_id = fields.Many2one('cooperative.entity', string='Cooperative', required=True)
    source_location = fields.Char('Source Location', required=True)
    distribution_date = fields.Date('Distribution Date', default=fields.Date.context_today, required=True)
    total_quantity = fields.Float('Total Quantity', required=True)
    description = fields.Text('Description')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
    ], string='State', default='draft', required=True)

    distribution_lines = fields.One2many('hub.spoke.distribution.line', 'distribution_id', string='Distribution Lines')

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hub.spoke.distribution') or '/'
        return super().create(vals)

    def action_start_delivery(self):
        """开始配送"""
        for distribution in self:
            distribution.state = 'in_transit'

    def action_confirm_delivery(self):
        """确认配送"""
        for distribution in self:
            distribution.state = 'delivered'
            # Confirm all distribution lines
            for line in distribution.distribution_lines:
                line.confirm_receipt()


class HubSpokeDistributionLine(models.Model):
    """
    统配物流明细 [US-042-21]
    """
    _name = 'hub.spoke.distribution.line'
    _description = 'Hub and Spoke Distribution Line'

    distribution_id = fields.Many2one('hub.spoke.distribution', string='Distribution', required=True, ondelete='cascade')
    destination_member_id = fields.Many2one('cooperative.member', string='Destination Member', required=True)
    product_id = fields.Many2one('product.product', string='Product', required=True)
    quantity = fields.Float('Quantity', required=True)
    delivery_date = fields.Date('Expected Delivery Date')
    actual_delivery_date = fields.Date('Actual Delivery Date')
    delivery_confirmed = fields.Boolean('Delivery Confirmed', default=False)
    receiver_signature = fields.Char('Receiver Signature')
    delivery_notes = fields.Text('Delivery Notes')

    def confirm_receipt(self):
        """确认收货"""
        for line in self:
            if not line.delivery_confirmed:
                line.delivery_confirmed = True
                line.actual_delivery_date = fields.Date.context_today(self)


class NettingSettlement(models.Model):
    """
    内部交易零余额对冲结算 [US-042-22]
    """
    _name = 'netting.settlement'
    _description = 'Netting Settlement'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Settlement Reference', required=True, default=lambda self: _('New'))
    cooperative_id = fields.Many2one('cooperative.entity', string='Cooperative', required=True)
    member_id = fields.Many2one('cooperative.member', string='Member', required=True)
    settlement_date = fields.Date('Settlement Date', default=fields.Date.context_today, required=True)
    receivable_amount = fields.Float('Receivable Amount', help='Amount member should receive from sales')
    payable_amount = fields.Float('Payable Amount', help='Amount member should pay for purchases')
    net_amount = fields.Float('Net Amount', compute='_compute_net_amount', store=True, precompute=True)
    settlement_direction = fields.Selection([
        ('to_member', 'To Member'),
        ('from_member', 'From Member'),
    ], string='Settlement Direction', compute='_compute_settlement_direction', store=True, precompute=True)
    description = fields.Text('Description')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('calculated', 'Calculated'),
        ('processed', 'Processed'),
        ('completed', 'Completed'),
    ], string='State', default='draft', required=True)

    receivable_lines = fields.One2many('netting.receivable.line', 'settlement_id', string='Receivable Lines')
    payable_lines = fields.One2many('netting.payable.line', 'settlement_id', string='Payable Lines')
    final_settlement_id = fields.Many2one('internal.settlement', string='Final Settlement')

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('netting.settlement') or '/'
        return super().create(vals)

    @api.depends('receivable_amount', 'payable_amount')
    def _compute_net_amount(self):
        for record in self:
            record.net_amount = record.receivable_amount - record.payable_amount

    @api.depends('net_amount')
    def _compute_settlement_direction(self):
        for record in self:
            if record.net_amount > 0:
                record.settlement_direction = 'to_member'
            elif record.net_amount < 0:
                record.settlement_direction = 'from_member'
            else:
                record.settlement_direction = False

    def action_calculate_settlement(self):
        """计算对冲结算"""
        for settlement in self:
            # Calculate receivables and payables
            settlement._calculate_receivables()
            settlement._calculate_payables()
            settlement.state = 'calculated'

    def _calculate_receivables(self):
        """计算应收金额"""
        # This would aggregate member's sales receipts, product deliveries, etc.
        # For now, we'll use a placeholder
        self.receivable_amount = 0.0

    def _calculate_payables(self):
        """计算应付金额"""
        # This would aggregate member's purchase debts, input costs, etc.
        # For now, we'll use a placeholder
        self.payable_amount = 0.0

    def action_process_settlement(self):
        """处理结算"""
        for settlement in self:
            if settlement.state != 'calculated':
                continue

            # Create the final settlement record
            final_settlement = self.env['internal.settlement'].create({
                'from_entity_id': (settlement.member_id.partner_id.company_id.id
                                  if settlement.net_amount < 0
                                  else settlement.cooperative_id.company_id.id),
                'to_entity_id': (settlement.cooperative_id.company_id.id
                               if settlement.net_amount < 0
                               else settlement.member_id.partner_id.company_id.id),
                'settlement_type': 'netting_settlement',
                'amount': abs(settlement.net_amount),
                'description': f'Netting settlement for {settlement.member_id.name} - '
                              f'Net amount: {settlement.net_amount}',
                'settlement_date': settlement.settlement_date,
            })
            settlement.final_settlement_id = final_settlement.id
            settlement.state = 'processed'


class NettingReceivableLine(models.Model):
    """
    对冲应收明细 [US-042-22]
    """
    _name = 'netting.receivable.line'
    _description = 'Netting Receivable Line'

    settlement_id = fields.Many2one('netting.settlement', string='Settlement', required=True, ondelete='cascade')
    source_document = fields.Reference([
        ('sale.order', 'Sale Order'),
        ('account.move', 'Invoice'),
        ('product.supply', 'Product Supply'),
    ], string='Source Document')
    amount = fields.Float('Amount', required=True)
    description = fields.Text('Description')
    due_date = fields.Date('Due Date')


class NettingPayableLine(models.Model):
    """
    对冲应付明细 [US-042-22]
    """
    _name = 'netting.payable.line'
    _description = 'Netting Payable Line'

    settlement_id = fields.Many2one('netting.settlement', string='Settlement', required=True, ondelete='cascade')
    source_document = fields.Reference([
        ('purchase.order', 'Purchase Order'),
        ('account.move', 'Bill'),
        ('input.delivery', 'Input Delivery'),
    ], string='Source Document')
    amount = fields.Float('Amount', required=True)
    description = fields.Text('Description')
    due_date = fields.Date('Due Date')