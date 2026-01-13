from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class CooperativeEntity(models.Model):
    """
    合作社实体 [US-19-01]
    """
    _name = 'cooperative.entity'
    _description = 'Cooperative Entity'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Name', required=True)
    code = fields.Char('Code', required=True, copy=False)
    legal_representative = fields.Char('Legal Representative')
    registration_number = fields.Char('Registration Number')
    registration_date = fields.Date('Registration Date')
    address = fields.Text('Address')
    phone = fields.Char('Phone')
    email = fields.Char('Email')
    member_farm_ids = fields.One2many('farm.entity', 'cooperative_id', string='Member Farms')
    is_active = fields.Boolean('Is Active', default=True)
    description = fields.Text('Description')

    @api.model
    def create(self, vals):
        if 'code' not in vals or not vals['code']:
            vals['code'] = self.env['ir.sequence'].next_by_code('cooperative.entity') or '/'
        return super().create(vals)

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, f"{record.code} - {record.name}"))
        return result


class FarmEntity(models.Model):
    """
    农场实体 [US-19-01, US-19-02]
    """
    _name = 'farm.entity'
    _description = 'Farm Entity'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Name', required=True)
    code = fields.Char('Code', required=True, copy=False)
    entity_type = fields.Selection([
        ('farm', 'Farm'),
        ('cooperative', 'Cooperative'),
        ('franchise', 'Franchise Farm'),
        ('subsidiary', 'Subsidiary'),
    ], string='Entity Type', required=True, default='farm')
    parent_entity_id = fields.Many2one('farm.entity', string='Parent Entity')
    child_entity_ids = fields.One2many('farm.entity', 'parent_entity_id', string='Child Entities')
    cooperative_id = fields.Many2one('cooperative.entity', string='Cooperative')
    company_id = fields.Many2one('res.company', string='Company', required=True)
    contact_person = fields.Char('Contact Person')
    phone = fields.Char('Phone')
    email = fields.Char('Email')
    address = fields.Text('Address')
    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date', help='For franchise agreements or membership periods')
    is_active = fields.Boolean('Is Active', default=True)
    data_isolation_level = fields.Selection([
        ('full', 'Full Isolation'),
        ('partial', 'Partial Sharing'),
        ('open', 'Open Sharing'),
    ], string='Data Isolation Level', default='partial', required=True)
    shared_data_types = fields.Many2many(
        'ir.model', 
        'farm_entity_shared_data_rel', 
        'entity_id', 
        'model_id', 
        string='Shared Data Types',
        help='Types of data that can be shared with parent entity'
    )
    description = fields.Text('Description')

    @api.model
    def create(self, vals):
        if 'code' not in vals or not vals['code']:
            vals['code'] = self.env['ir.sequence'].next_by_code('farm.entity') or '/'
        return super().create(vals)

    @api.constrains('parent_entity_id')
    def _check_parent_entity_recursion(self):
        """防止实体关系循环引用"""
        if not self._check_recursion('parent_entity_id'):
            raise ValidationError(_('You cannot create recursive entity relationships.'))

    def name_get(self):
        result = []
        for record in self:
            parent_str = f" ({record.parent_entity_id.name})" if record.parent_entity_id else ""
            result.append((record.id, f"{record.code} - {record.name}{parent_str}"))
        return result

    def get_accessible_data(self, model_name):
        """
        根据数据隔离级别获取可访问的数据 [US-19-02]
        """
        if self.data_isolation_level == 'full':
            # 完全隔离：只能访问本实体数据
            return self.env[model_name].search([('company_id', '=', self.company_id.id)])
        elif self.data_isolation_level == 'partial':
            # 部分共享：可访问本实体和父实体的特定类型数据
            accessible_companies = self._get_accessible_companies()
            if model_name in [data_model.model for data_model in self.shared_data_types]:
                return self.env[model_name].search([('company_id', 'in', accessible_companies.ids)])
            else:
                return self.env[model_name].search([('company_id', '=', self.company_id.id)])
        else:  # open
            # 开放共享：可访问所有关联实体数据
            accessible_companies = self._get_accessible_companies()
            return self.env[model_name].search([('company_id', 'in', accessible_companies.ids)])

    def _get_accessible_companies(self):
        """获取可访问的公司列表"""
        companies = self.company_id  # 本实体公司
        # 添加父实体公司的数据
        current = self
        while current.parent_entity_id:
            current = current.parent_entity_id
            companies |= current.company_id
        # 添加子实体公司的数据
        children = self._get_all_child_entities()
        for child in children:
            companies |= child.company_id
        return companies

    def _get_all_child_entities(self):
        """递归获取所有子实体"""
        children = self.child_entity_ids
        for child in children:
            children |= child._get_all_child_entities()
        return children


class ResourceSharing(models.Model):
    """
    资源共享管理 [US-19-03]
    """
    _name = 'resource.sharing'
    _description = 'Resource Sharing Between Entities'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Name', required=True, compute='_compute_name', store=True)
    source_entity_id = fields.Many2one('farm.entity', string='Source Entity', required=True)
    target_entity_id = fields.Many2one('farm.entity', string='Target Entity', required=True)
    resource_type = fields.Selection([
        ('equipment', 'Equipment'),
        ('personnel', 'Personnel'),
        ('land', 'Land'),
        ('warehouse', 'Warehouse'),
        ('other', 'Other'),
    ], string='Resource Type', required=True)
    resource_id = fields.Integer('Resource ID', help='ID of the shared resource (e.g., equipment ID, employee ID)')
    resource_name = fields.Char('Resource Name', compute='_compute_resource_name', store=True)
    start_date = fields.Date('Start Date', required=True)
    end_date = fields.Date('End Date')
    is_active = fields.Boolean('Is Active', default=True)
    sharing_cost = fields.Float('Sharing Cost', help='Cost per unit time or usage')
    sharing_unit = fields.Selection([
        ('hour', 'Hour'),
        ('day', 'Day'),
        ('trip', 'Trip'),
        ('unit', 'Unit'),
    ], string='Sharing Unit', default='day')
    internal_settlement_id = fields.Many2one('internal.settlement', string='Internal Settlement')
    description = fields.Text('Description')

    @api.depends('source_entity_id', 'target_entity_id', 'resource_type', 'resource_id')
    def _compute_name(self):
        for record in self:
            record.name = f"{record.source_entity_id.code} -> {record.target_entity_id.code}: {record.resource_type}({record.resource_id})"

    @api.depends('resource_type', 'resource_id')
    def _compute_resource_name(self):
        for record in self:
            if record.resource_type == 'equipment' and record.resource_id:
                equipment = self.env['fleet.vehicle'].browse(record.resource_id)
                if equipment.exists():
                    record.resource_name = equipment.name
                else:
                    record.resource_name = f"Equipment ID {record.resource_id}"
            elif record.resource_type == 'personnel' and record.resource_id:
                employee = self.env['hr.employee'].browse(record.resource_id)
                if employee.exists():
                    record.resource_name = employee.name
                else:
                    record.resource_name = f"Employee ID {record.resource_id}"
            else:
                record.resource_name = f"{record.resource_type.title()} ID {record.resource_id}"

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for record in self:
            if record.end_date and record.start_date > record.end_date:
                raise ValidationError(_('Start date must be earlier than end date.'))

    def action_create_internal_settlement(self):
        """创建内部结算单 [US-19-03]"""
        for record in self:
            if not record.internal_settlement_id:
                settlement = self.env['internal.settlement'].create({
                    'from_entity_id': record.target_entity_id.id,
                    'to_entity_id': record.source_entity_id.id,
                    'settlement_type': 'resource_rental',
                    'resource_sharing_id': record.id,
                    'amount': record.sharing_cost,
                    'description': f'Resource sharing fee for {record.resource_name}',
                })
                record.internal_settlement_id = settlement.id


class InternalSettlement(models.Model):
    """
    内部结算 [US-19-04]
    """
    _name = 'internal.settlement'
    _description = 'Internal Settlement Between Entities'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Reference', required=True, default=lambda self: _('New'))
    from_entity_id = fields.Many2one('farm.entity', string='From Entity', required=True)
    to_entity_id = fields.Many2one('farm.entity', string='To Entity', required=True)
    settlement_type = fields.Selection([
        ('resource_rental', 'Resource Rental'),
        ('service_fee', 'Service Fee'),
        ('joint_procurement', 'Joint Procurement'),
        ('marketing_fee', 'Marketing Fee'),
        ('management_fee', 'Management Fee'),
        ('profit_sharing', 'Profit Sharing'),
        ('other', 'Other'),
    ], string='Settlement Type', required=True)
    resource_sharing_id = fields.Many2one('resource.sharing', string='Resource Sharing')
    activity_production_id = fields.Many2one('activity.production', string='Activity Production')
    amount = fields.Float('Amount', required=True)
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    description = fields.Text('Description')
    settlement_date = fields.Date('Settlement Date', default=fields.Date.context_today)
    invoice_id = fields.Many2one('account.move', string='Generated Invoice', readonly=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('invoiced', 'Invoiced'),
        ('paid', 'Paid'),
    ], string='State', default='draft', tracking=True)

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('internal.settlement') or '/'
        return super().create(vals)

    def action_generate_invoice(self):
        """生成结算发票 [US-19-04]"""
        for settlement in self:
            if not settlement.invoice_id:
                # 创建供应商发票
                vendor_bill = self.env['account.move'].create({
                    'move_type': 'in_invoice',
                    'partner_id': settlement.to_entity_id.company_id.partner_id.id,  # 目标实体的公司伙伴
                    'invoice_date': settlement.settlement_date,
                    'invoice_line_ids': [(0, 0, {
                        'name': f'{settlement.get_external_id()[settlement.id]} - {settlement.description or settlement.settlement_type}',
                        'quantity': 1,
                        'price_unit': settlement.amount,
                        'account_id': self.env['account.account'].search([
                            ('company_id', '=', settlement.from_entity_id.company_id.id),
                            ('account_type', '=', 'expense')
                        ], limit=1).id,
                    })],
                    'company_id': settlement.from_entity_id.company_id.id,
                })
                settlement.invoice_id = vendor_bill.id
                settlement.state = 'invoiced'


class FranchiseFarm(models.Model):
    """
    加盟农场管理 [US-19-05]
    """
    _name = 'franchise.farm'
    _description = 'Franchise Farm Management'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Franchise Farm Name', required=True)
    code = fields.Char('Code', required=True, copy=False)
    farm_entity_id = fields.Many2one('farm.entity', string='Farm Entity', required=True)
    franchise_agreement_date = fields.Date('Franchise Agreement Date')
    franchise_expiry_date = fields.Date('Franchise Expiry Date')
    franchise_fee = fields.Float('Franchise Fee')
    royalty_rate = fields.Float('Royalty Rate (%)', help='Percentage of sales as royalty')
    brand_usage_rights = fields.Text('Brand Usage Rights')
    operational_standards = fields.Text('Operational Standards')
    compliance_status = fields.Selection([
        ('compliant', 'Compliant'),
        ('warning', 'Warning'),
        ('non_compliant', 'Non-Compliant'),
    ], string='Compliance Status', default='compliant', tracking=True)
    last_audit_date = fields.Date('Last Audit Date')
    next_audit_date = fields.Date('Next Audit Date')
    audit_notes = fields.Text('Audit Notes')
    is_active = fields.Boolean('Is Active', default=True)
    description = fields.Text('Description')

    @api.model
    def create(self, vals):
        if 'code' not in vals or not vals['code']:
            vals['code'] = self.env['ir.sequence'].next_by_code('franchise.farm') or '/'
        return super().create(vals)

    @api.onchange('franchise_agreement_date')
    def _onchange_agreement_date(self):
        if self.franchise_agreement_date:
            # 设置首次审计日期为协议签署后一年
            from datetime import timedelta
            self.next_audit_date = fields.Date.from_string(self.franchise_agreement_date) + timedelta(days=365)

    def action_perform_compliance_check(self):
        """执行合规检查 [US-19-05]"""
        for farm in self:
            # 这里可以实现具体的合规检查逻辑
            # 检查是否符合品牌标准、操作规程等
            # 更新合规状态
            farm.compliance_status = 'compliant'  # 简化实现，实际应根据检查结果设置
            farm.last_audit_date = fields.Date.today()
            farm.audit_notes = f"Compliance check performed on {fields.Date.today()}"
            
            # 计算下次审计日期
            from datetime import timedelta
            farm.next_audit_date = fields.Date.add(fields.Date.today(), days=365)

    def action_push_operational_standards(self):
        """推送操作标准 [US-19-05]"""
        for farm in self:
            # 这里可以实现向加盟农场推送标准操作规程的逻辑
            # 例如：发送技术路线、生产标准等
            pass