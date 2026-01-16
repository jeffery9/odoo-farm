from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class QualityControlStandard(models.Model):
    """
    统一质检与品牌准入 [US-19-09]
    """
    _name = 'quality.control.standard'
    _description = 'Quality Control Standard'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Standard Name', required=True)
    code = fields.Char('Standard Code', required=True, copy=False)
    cooperative_id = fields.Many2one('cooperative.entity', string='Cooperative', required=True)
    product_category_id = fields.Many2one('product.category', string='Product Category')
    quality_threshold = fields.Float('Quality Threshold (%)', help='Minimum合格率 to pass')
    inspection_criteria = fields.Text('Inspection Criteria')
    certification_required = fields.Boolean('Certification Required')
    certification_standard = fields.Char('Certification Standard')
    is_active = fields.Boolean('Is Active', default=True)
    description = fields.Text('Description')

    @api.model
    def create(self, vals):
        if 'code' not in vals or not vals['code']:
            vals['code'] = self.env['ir.sequence'].next_by_code('quality.control.standard') or '/'
        return super().create(vals)

    def check_product_compliance(self, product_id, quality_score):
        """检查产品是否符合标准"""
        # This would be called to check if a product meets the quality standards
        if quality_score >= self.quality_threshold:
            return True
        return False


class ProductCertification(models.Model):
    """
    产品认证 [US-19-09]
    """
    _name = 'product.certification'
    _description = 'Product Certification'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Certification Name', required=True)
    code = fields.Char('Certification Code', required=True, copy=False)
    cooperative_id = fields.Many2one('cooperative.entity', string='Cooperative', required=True)
    member_id = fields.Many2one('cooperative.member', string='Member', required=True)
    product_id = fields.Many2one('product.product', string='Product', required=True)
    standard_id = fields.Many2one('quality.control.standard', string='Quality Standard', required=True)
    certification_date = fields.Date('Certification Date', default=fields.Date.context_today)
    expiry_date = fields.Date('Expiry Date')
    quality_score = fields.Float('Quality Score (%)')
    is_certified = fields.Boolean('Is Certified', compute='_compute_certified_status', store=True)
    certification_document = fields.Binary('Certification Document')
    document_name = fields.Char('Document Name')
    description = fields.Text('Description')
    state = fields.Selection([
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('expired', 'Expired'),
    ], string='State', default='pending', required=True)

    @api.model
    def create(self, vals):
        if 'code' not in vals or not vals['code']:
            vals['code'] = self.env['ir.sequence'].next_by_code('product.certification') or '/'
        return super().create(vals)

    @api.depends('quality_score', 'standard_id', 'expiry_date', 'state')
    def _compute_certified_status(self):
        for record in self:
            if (record.state == 'approved' and
                record.quality_score and
                record.standard_id and
                record.quality_score >= record.standard_id.quality_threshold and
                (not record.expiry_date or record.expiry_date >= fields.Date.context_today(self))):
                record.is_certified = True
            else:
                record.is_certified = False

    def action_approve(self):
        """批准认证"""
        for certification in self:
            certification.state = 'approved'

    def action_reject(self):
        """拒绝认证"""
        for certification in self:
            certification.state = 'rejected'


class JointProcurement(models.Model):
    """
    统购统销内部清算 [US-19-10]
    """
    _name = 'joint.procurement'
    _description = 'Joint Procurement'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Procurement Reference', required=True, default=lambda self: _('New'))
    cooperative_id = fields.Many2one('cooperative.entity', string='Cooperative', required=True)
    procurement_date = fields.Date('Procurement Date', default=fields.Date.context_today, required=True)
    supplier_id = fields.Many2one('res.partner', string='Supplier', required=True)
    total_amount = fields.Float('Total Amount', required=True)
    markup_rate = fields.Float('Markup Rate (%)', default=0.0, help='Markup rate applied to members')
    procurement_type = fields.Selection([
        ('fertilizer', 'Fertilizer'),
        ('pesticide', 'Pesticide'),
        ('feed', 'Feed'),
        ('seeds', 'Seeds'),
        ('equipment', 'Equipment'),
        ('other', 'Other'),
    ], string='Procurement Type', required=True)
    description = fields.Text('Description')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], string='State', default='draft', required=True)

    procurement_lines = fields.One2many('joint.procurement.line', 'procurement_id', string='Procurement Lines')
    settlement_lines = fields.One2many('internal.settlement', 'joint_procurement_id', string='Settlement Lines')

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('joint.procurement') or '/'
        return super().create(vals)

    def action_confirm(self):
        """确认采购"""
        for procurement in self:
            procurement.state = 'confirmed'

    def action_complete(self):
        """完成采购并生成结算"""
        for procurement in self:
            procurement.state = 'completed'
            # Generate settlements for each member's share
            for line in procurement.procurement_lines:
                settlement = self.env['internal.settlement'].create({
                    'from_entity_id': line.member_id.partner_id.company_id.id,
                    'to_entity_id': procurement.cooperative_id.company_id.id,
                    'settlement_type': 'joint_procurement',
                    'joint_procurement_id': procurement.id,
                    'activity_production_id': False,
                    'amount': line.member_amount,
                    'description': f'Share of joint procurement {procurement.name} for {line.product_id.name}',
                    'settlement_date': procurement.procurement_date,
                })
                line.settlement_id = settlement.id


class JointProcurementLine(models.Model):
    """
    统购统销明细 [US-19-10]
    """
    _name = 'joint.procurement.line'
    _description = 'Joint Procurement Line'

    procurement_id = fields.Many2one('joint.procurement', string='Procurement', required=True, ondelete='cascade')
    member_id = fields.Many2one('cooperative.member', string='Member', required=True)
    product_id = fields.Many2one('product.product', string='Product', required=True)
    quantity = fields.Float('Quantity', required=True)
    unit_price = fields.Float('Unit Price', required=True)
    member_amount = fields.Float('Member Amount', compute='_compute_member_amount', store=True)
    markup_amount = fields.Float('Markup Amount', compute='_compute_markup_amount', store=True)
    settlement_id = fields.Many2one('internal.settlement', string='Settlement')

    @api.depends('quantity', 'unit_price')
    def _compute_member_amount(self):
        for line in self:
            line.member_amount = line.quantity * line.unit_price

    @api.depends('member_amount')
    def _compute_markup_amount(self):
        for line in self:
            if line.procurement_id:
                markup_rate = line.procurement_id.markup_rate / 100.0
                line.markup_amount = line.member_amount * markup_rate


class InternalMarketplace(models.Model):
    """
    内部余缺调剂平台 [US-19-11]
    """
    _name = 'internal.marketplace'
    _description = 'Internal Marketplace'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Listing Title', required=True)
    cooperative_id = fields.Many2one('cooperative.entity', string='Cooperative', required=True)
    supplier_member_id = fields.Many2one('cooperative.member', string='Supplier Member', required=True)
    listing_type = fields.Selection([
        ('surplus', 'Surplus'),
        ('demand', 'Demand'),
    ], string='Listing Type', required=True)
    product_id = fields.Many2one('product.product', string='Product', required=True)
    quantity = fields.Float('Quantity', required=True)
    unit_of_measure = fields.Many2one('uom.uom', string='Unit of Measure')
    unit_price = fields.Float('Unit Price')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    start_date = fields.Date('Available From', default=fields.Date.context_today)
    end_date = fields.Date('Available Until')
    location = fields.Char('Location')
    description = fields.Text('Description')
    is_active = fields.Boolean('Is Active', default=True)
    state = fields.Selection([
        ('open', 'Open'),
        ('matched', 'Matched'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], string='State', default='open', required=True)

    demand_matches = fields.One2many('marketplace.demand.match', 'listing_id', string='Demand Matches')
    transaction_id = fields.Many2one('internal.marketplace.transaction', string='Transaction')

    def action_match_demand(self):
        """匹配供需"""
        # Find matching demands for surplus listings or matching surplus for demand listings
        pass

    def action_complete_transaction(self):
        """完成交易"""
        for listing in self:
            if listing.state == 'matched':
                # Create transaction and update state
                transaction = self.env['internal.marketplace.transaction'].create({
                    'supplier_member_id': listing.supplier_member_id.id,
                    'requester_member_id': listing.demand_matches[0].member_id.id if listing.demand_matches else False,
                    'product_id': listing.product_id.id,
                    'quantity': min(listing.quantity, listing.demand_matches[0].quantity) if listing.demand_matches else listing.quantity,
                    'unit_price': listing.unit_price,
                    'listing_id': listing.id,
                })
                listing.transaction_id = transaction.id
                listing.state = 'completed'


class MarketplaceDemandMatch(models.Model):
    """
    市场供需匹配 [US-19-11]
    """
    _name = 'marketplace.demand.match'
    _description = 'Marketplace Demand Match'

    listing_id = fields.Many2one('internal.marketplace', string='Listing', required=True, ondelete='cascade')
    member_id = fields.Many2one('cooperative.member', string='Member', required=True)
    quantity = fields.Float('Quantity', required=True)
    priority = fields.Integer('Priority', default=1)
    match_date = fields.Date('Match Date', default=fields.Date.context_today)


class InternalMarketplaceTransaction(models.Model):
    """
    市场平台交易 [US-19-11]
    """
    _name = 'internal.marketplace.transaction'
    _description = 'Internal Marketplace Transaction'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Transaction Reference', required=True, default=lambda self: _('New'))
    supplier_member_id = fields.Many2one('cooperative.member', string='Supplier Member', required=True)
    requester_member_id = fields.Many2one('cooperative.member', string='Requester Member', required=True)
    product_id = fields.Many2one('product.product', string='Product', required=True)
    quantity = fields.Float('Quantity', required=True)
    unit_price = fields.Float('Unit Price', required=True)
    total_amount = fields.Float('Total Amount', compute='_compute_total_amount', store=True)
    transaction_date = fields.Date('Transaction Date', default=fields.Date.context_today)
    listing_id = fields.Many2one('internal.marketplace', string='Listing')
    picking_id = fields.Many2one('stock.picking', string='Stock Picking')
    settlement_id = fields.Many2one('internal.settlement', string='Settlement')
    state = fields.Selection([
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
        ('completed', 'Completed'),
    ], string='State', default='pending', required=True)

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('internal.marketplace.transaction') or '/'
        return super().create(vals)

    @api.depends('quantity', 'unit_price')
    def _compute_total_amount(self):
        for record in self:
            record.total_amount = record.quantity * record.unit_price

    def action_confirm(self):
        """确认交易"""
        for transaction in self:
            transaction.state = 'confirmed'

    def action_create_picking(self):
        """创建调拨单"""
        for transaction in self:
            # This would create a stock picking between the entities
            pass

    def action_create_settlement(self):
        """创建结算"""
        for transaction in self:
            settlement = self.env['internal.settlement'].create({
                'from_entity_id': transaction.requester_member_id.partner_id.company_id.id,
                'to_entity_id': transaction.supplier_member_id.partner_id.company_id.id,
                'settlement_type': 'internal_transaction',
                'amount': transaction.total_amount,
                'description': f'Marketplace transaction for {transaction.product_id.name}',
                'settlement_date': transaction.transaction_date,
            })
            transaction.settlement_id = settlement.id


class ProcurementPlanning(models.Model):
    """
    农资统筹预分配 [US-19-12]
    """
    _name = 'procurement.planning'
    _description = 'Procurement Planning'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Planning Name', required=True)
    cooperative_id = fields.Many2one('cooperative.entity', string='Cooperative', required=True)
    planning_date = fields.Date('Planning Date', default=fields.Date.context_today, required=True)
    planning_period = fields.Selection([
        ('quarterly', 'Quarterly'),
        ('bi_annual', 'Bi-annual'),
        ('annual', 'Annual'),
    ], string='Planning Period', required=True)
    season = fields.Char('Season')
    description = fields.Text('Description')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('executed', 'Executed'),
        ('cancelled', 'Cancelled'),
    ], string='State', default='draft', required=True)

    planning_lines = fields.One2many('procurement.planning.line', 'planning_id', string='Planning Lines')

    def action_confirm(self):
        """确认计划"""
        for planning in self:
            planning.state = 'confirmed'

    def action_execute(self):
        """执行计划"""
        for planning in self:
            planning.state = 'executed'


class ProcurementPlanningLine(models.Model):
    """
    农资统筹预分配明细 [US-19-12]
    """
    _name = 'procurement.planning.line'
    _description = 'Procurement Planning Line'

    planning_id = fields.Many2one('procurement.planning', string='Planning', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Product', required=True)
    total_required = fields.Float('Total Required', required=True)
    total_available = fields.Float('Total Available', default=0.0)
    total_allocated = fields.Float('Total Allocated', compute='_compute_total_allocated', store=True)
    remaining_quantity = fields.Float('Remaining Quantity', compute='_compute_remaining', store=True)

    allocation_lines = fields.One2many('procurement.allocation.line', 'planning_line_id', string='Allocation Lines')


    @api.depends('allocation_lines.quantity')
    def _compute_total_allocated(self):
        for line in self:
            line.total_allocated = sum(allocation.quantity for allocation in line.allocation_lines)

    @api.depends('total_available', 'total_allocated')
    def _compute_remaining(self):
        for line in self:
            line.remaining_quantity = line.total_available - line.total_allocated


class ProcurementAllocationLine(models.Model):
    """
    农资分配明细 [US-19-12]
    """
    _name = 'procurement.allocation.line'
    _description = 'Procurement Allocation Line'

    planning_line_id = fields.Many2one('procurement.planning.line', string='Planning Line', required=True, ondelete='cascade')
    member_id = fields.Many2one('cooperative.member', string='Member', required=True)
    quantity = fields.Float('Quantity', required=True)
    priority_score = fields.Float('Priority Score', help='Based on historical contribution or other factors')
    allocation_date = fields.Date('Allocation Date', default=fields.Date.context_today)


class AgriService(models.Model):
    """
    社会化服务产能共享 [US-19-13]
    """
    _name = 'agri.service'
    _description = 'Agricultural Service'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Service Name', required=True)
    code = fields.Char('Service Code', required=True, copy=False)
    cooperative_id = fields.Many2one('cooperative.entity', string='Cooperative', required=True)
    provider_member_id = fields.Many2one('cooperative.member', string='Provider Member', required=True)
    service_category = fields.Selection([
        ('spraying', 'Spraying/Flying'),
        ('tillage', 'Tillage'),
        ('harvesting', 'Harvesting'),
        ('transport', 'Transport'),
        ('pruning', 'Pruning'),
        ('other', 'Other'),
    ], string='Service Category', required=True)
    capacity = fields.Float('Capacity', help='Service capacity per unit time')
    capacity_unit = fields.Char('Capacity Unit', default='hectares/day')
    unit_rate = fields.Float('Unit Rate', required=True)
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    available_from = fields.Datetime('Available From', default=fields.Datetime.now)
    available_to = fields.Datetime('Available To')
    location = fields.Char('Service Location')
    description = fields.Text('Description')
    is_active = fields.Boolean('Is Active', default=True)

    @api.model
    def create(self, vals):
        if 'code' not in vals or not vals['code']:
            vals['code'] = self.env['ir.sequence'].next_by_code('agri.service') or '/'
        return super().create(vals)

    def action_set_available(self):
        """设置为可用"""
        self.available_from = fields.Datetime.now()
        self.is_active = True

    def action_set_unavailable(self):
        """设置为不可用"""
        self.is_active = False


class ServiceOrder(models.Model):
    """
    服务订单 [US-19-13]
    """
    _name = 'service.order'
    _description = 'Service Order'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Order Reference', required=True, default=lambda self: _('New'))
    service_id = fields.Many2one('agri.service', string='Service', required=True)
    requester_member_id = fields.Many2one('cooperative.member', string='Requester Member', required=True)
    order_date = fields.Date('Order Date', default=fields.Date.context_today, required=True)
    required_date = fields.Date('Required Date', required=True)
    service_quantity = fields.Float('Service Quantity', required=True)
    unit_rate = fields.Float('Unit Rate', related='service_id.unit_rate')
    total_amount = fields.Float('Total Amount', compute='_compute_total_amount', store=True)
    description = fields.Text('Service Description')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], string='State', default='draft', required=True)

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('service.order') or '/'
        return super().create(vals)

    @api.depends('service_quantity', 'unit_rate')
    def _compute_total_amount(self):
        for record in self:
            record.total_amount = record.service_quantity * record.unit_rate

    def action_confirm(self):
        """确认订单"""
        for order in self:
            order.state = 'confirmed'

    def action_start_service(self):
        """开始服务"""
        for order in self:
            order.state = 'in_progress'

    def action_complete_service(self):
        """完成服务"""
        for order in self:
            order.state = 'completed'
            # Create settlement
            settlement = self.env['internal.settlement'].create({
                'from_entity_id': order.requester_member_id.partner_id.company_id.id,
                'to_entity_id': order.service_id.provider_member_id.partner_id.company_id.id,
                'settlement_type': 'service_fee',
                'amount': order.total_amount,
                'description': f'Service fee for {order.service_id.name}',
                'settlement_date': order.order_date,
            })