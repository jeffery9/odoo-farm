from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class FarmEntity(models.Model):
    """
    农场实体模型 [US-19-01]
    用于管理合作社、农场、加盟农场等实体
    """
    _name = 'farm.entity'
    _description = 'Farm Entity (Cooperative, Farm, etc.)'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Entity Name', required=True)
    entity_type = fields.Selection([
        ('cooperative', 'Cooperative'),
        ('farm', 'Farm'),
        ('franchise', 'Franchise Farm'),
        ('member', 'Member Farm'),
    ], string='Entity Type', required=True, default='farm')

    company_id = fields.Many2one('res.company', string='Associated Company',
                                 help='关联的公司实体')
    parent_entity_id = fields.Many2one('farm.entity', string='Parent Entity',
                                       help='上级实体，如合作社下的农场')
    child_entity_ids = fields.One2many('farm.entity', 'parent_entity_id',
                                       string='Child Entities')

    start_date = fields.Date('Start Date', help='关系开始日期')
    end_date = fields.Date('End Date', help='关系结束日期（如加盟期限）')
    is_active = fields.Boolean('Is Active', default=True)

    # 合作社相关字段
    cooperative_id = fields.Many2one('farm.entity', string='Cooperative',
                                     domain=[('entity_type', '=', 'cooperative')])

    # 加盟相关字段
    franchise_agreement = fields.Binary('Franchise Agreement',
                                        help='加盟协议文件')
    franchise_fee = fields.Float('Franchise Fee', help='加盟费用')

    def name_get(self):
        result = []
        for record in self:
            name = f"[{record.entity_type.upper()}] {record.name}"
            if record.parent_entity_id:
                name = f"{record.parent_entity_id.name} / {name}"
            result.append((record.id, name))
        return result


class FarmEntityLink(models.Model):
    """
    实体链接模型 [US-19-01]
    用于建立实体间的关系
    """
    _name = 'farm.entity.link'
    _description = 'Farm Entity Link'

    name = fields.Char('Link Name', compute='_compute_name', store=True)
    source_entity_id = fields.Many2one('farm.entity', string='Source Entity', required=True)
    target_entity_id = fields.Many2one('farm.entity', string='Target Entity', required=True)
    link_type = fields.Selection([
        ('membership', 'Membership'),
        ('franchise', 'Franchise'),
        ('partnership', 'Partnership'),
        ('supplier', 'Supplier'),
        ('customer', 'Customer'),
    ], string='Link Type', required=True)

    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')
    is_active = fields.Boolean('Is Active', default=True)

    @api.constrains('source_entity_id', 'target_entity_id')
    def _check_different_entities(self):
        for link in self:
            if link.source_entity_id == link.target_entity_id:
                raise UserError(_("Source and target entities must be different."))

    @api.depends('source_entity_id', 'target_entity_id', 'link_type')
    def _compute_name(self):
        for link in self:
            if link.source_entity_id and link.target_entity_id:
                link.name = f"{link.source_entity_id.name} -> {link.target_entity_id.name} ({link.link_type})"


class FarmDataSharingRule(models.Model):
    """
    数据共享规则 [US-19-02]
    定义不同实体间的数据共享规则
    """
    _name = 'farm.data.sharing.rule'
    _description = 'Farm Data Sharing Rule'

    name = fields.Char('Rule Name', required=True)
    source_entity_id = fields.Many2one('farm.entity', string='Source Entity', required=True)
    target_entity_id = fields.Many2one('farm.entity', string='Target Entity', required=True)

    data_type = fields.Selection([
        ('production', 'Production Data'),
        ('financial', 'Financial Data'),
        ('inventory', 'Inventory Data'),
        ('quality', 'Quality Data'),
        ('hr', 'HR Data'),
    ], string='Data Type', required=True)

    access_level = fields.Selection([
        ('read', 'Read Only'),
        ('read_write', 'Read/Write'),
        ('none', 'No Access'),
    ], string='Access Level', default='read')

    is_active = fields.Boolean('Is Active', default=True)
    description = fields.Text('Description')


class FarmSharedResource(models.AbstractModel):
    """
    共享资源抽象模型 [US-19-03]
    为所有可共享的资源提供统一接口
    """
    _name = 'farm.shared.resource'
    _description = 'Farm Shared Resource (Abstract)'

    can_be_shared = fields.Boolean("Can Be Shared", default=False,
                                   help="Allow this resource to be shared with other entities.")
    shared_entity_ids = fields.Many2many('farm.entity',
                                         'shared_resource_entity_rel',
                                         'resource_id', 'entity_id',
                                         string="Shared With Entities")
    sharing_cost = fields.Float("Sharing Cost", help="Cost per unit time or usage")


class ResCompany(models.Model):
    _inherit = 'res.company'

    is_cooperative_member = fields.Boolean("Is Cooperative Member", default=False,
                                           help="Mark this company as part of a cooperative for resource sharing.")
    farm_entity_id = fields.Many2one('farm.entity', string='Farm Entity',
                                     help='关联的农场实体')


class FarmVehicle(models.Model):
    _name = 'farm.vehicle'
    _inherit = ['farm.shared.resource', 'mail.thread', 'mail.activity.mixin']
    _description = 'Farm Vehicle/Equipment'

    name = fields.Char('Vehicle Name', required=True)
    license_plate = fields.Char('License Plate')
    vehicle_type = fields.Selection([
        ('tractor', 'Tractor'),
        ('harvester', 'Harvester'),
        ('sprayer', 'Sprayer'),
        ('transport', 'Transport'),
        ('other', 'Other'),
    ], string='Type', required=True)

    company_id = fields.Many2one('res.company', string='Company', required=True,
                                 default=lambda self: self.env.company)
    status = fields.Selection([
        ('available', 'Available'),
        ('in_use', 'In Use'),
        ('maintenance', 'Maintenance'),
        ('out_of_service', 'Out of Service'),
    ], string='Status', default='available', required=True)

    # 继承自 farm.shared.resource
    # can_be_shared = fields.Boolean("Can Be Shared", default=False)
    # shared_entity_ids = fields.Many2many('farm.entity', ...)


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    can_be_shared = fields.Boolean("Can Be Shared", default=False,
                                   help="Allow this employee to be shared with other cooperative members.")
    shared_entity_ids = fields.Many2many('farm.entity',
                                         'hr_employee_entity_rel',
                                         'employee_id', 'entity_id',
                                         string="Shared With Entities")


class ProjectTask(models.Model):
    _inherit = 'project.task'

    # 跨公司资源调度 [US-19-03]
    shared_vehicle_id = fields.Many2one('farm.vehicle', string="Shared Vehicle")
    shared_employee_id = fields.Many2one('hr.employee', string="Shared Employee")
    assigned_entity_id = fields.Many2one('farm.entity', string='Assigned Entity',
                                         help='实体分配的任务')

    # 跨实体资源约束检查
    @api.constrains('shared_vehicle_id', 'company_id')
    def _check_shared_vehicle_company(self):
        for task in self:
            if task.shared_vehicle_id and task.company_id:
                # 检查车辆是否属于当前公司或被共享给当前公司
                if (task.shared_vehicle_id.company_id != task.company_id and
                    task.company_id not in task.shared_vehicle_id.mapped('shared_entity_ids.company_id')):
                    raise UserError(_("Shared Vehicle '%s' is not available to your company '%s'.") %
                                   (task.shared_vehicle_id.name, task.company_id.name))

    @api.constrains('shared_employee_id', 'company_id')
    def _check_shared_employee_company(self):
        for task in self:
            if task.shared_employee_id and task.company_id:
                # 检查员工是否属于当前公司或被共享给当前公司
                if (task.shared_employee_id.company_id != task.company_id and
                    task.company_id not in task.shared_employee_id.mapped('shared_entity_ids.company_id')):
                    raise UserError(_("Shared Employee '%s' is not available to your company '%s'.") %
                                   (task.shared_employee_id.name, task.company_id.name))


class FarmInternalSettlement(models.Model):
    """
    内部结算 [US-19-03, US-19-04]
    """
    _name = 'farm.internal.settlement'
    _description = 'Cooperative Internal Settlement'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Reference", default=lambda self: _('New'))
    from_entity_id = fields.Many2one('farm.entity', string="From Entity", required=True)
    to_entity_id = fields.Many2one('farm.entity', string="To Entity", required=True)
    from_company_id = fields.Many2one('res.company', string="From Company", required=True)
    to_company_id = fields.Many2one('res.company', string="To Company", required=True)

    settlement_type = fields.Selection([
        ('vehicle_rental', 'Vehicle Rental'),
        ('labor_service', 'Labor Service'),
        ('material_transfer', 'Material Transfer'),
        ('land_rental', 'Land Rental'),
        ('processing_service', 'Processing Service'),
        ('marketing_fee', 'Marketing Fee'),
    ], string="Settlement Type", required=True)

    amount = fields.Monetary("Amount", currency_field='currency_id', required=True)
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)

    related_task_id = fields.Many2one('project.task', string="Related Task")
    invoice_id = fields.Many2one('account.move', string="Generated Invoice", readonly=True)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('invoiced', 'Invoiced'),
        ('paid', 'Paid'),
    ], default='draft', tracking=True)

    description = fields.Text('Description')
    settlement_date = fields.Date('Settlement Date', default=fields.Date.context_today)

    def action_generate_invoice(self):
        self.ensure_one()
        if self.invoice_id:
            raise UserError(_("Invoice already generated for this settlement."))

        # 生成发票
        invoice_vals = {
            'partner_id': self.to_company_id.partner_id.id,
            'move_type': 'out_invoice',
            'invoice_date': fields.Date.today(),
            'invoice_line_ids': [(0, 0, {
                'name': _("Internal Settlement for %s: %s") % (self.settlement_type, self.description or ''),
                'quantity': 1,
                'price_unit': self.amount,
            })]
        }
        invoice = self.env['account.move'].create(invoice_vals)
        self.write({'invoice_id': invoice.id, 'state': 'invoiced'})
        return {
            'name': _('Generated Invoice'),
            'view_mode': 'form',
            'res_model': 'account.move',
            'res_id': invoice.id,
            'type': 'ir.actions.act_window',
            'target': 'current',
        }


class FarmCooperativeReport(models.Model):
    """
    合作社报表 [US-19-04]
    """
    _name = 'farm.cooperative.report'
    _description = 'Cooperative Financial Report'

    name = fields.Char('Report Name', required=True)
    cooperative_entity_id = fields.Many2one('farm.entity', string='Cooperative',
                                            domain=[('entity_type', '=', 'cooperative')])
    report_date = fields.Date('Report Date', default=fields.Date.context_today)
    report_type = fields.Selection([
        ('income_statement', 'Income Statement'),
        ('balance_sheet', 'Balance Sheet'),
        ('cost_allocation', 'Cost Allocation'),
        ('production_summary', 'Production Summary'),
    ], string='Report Type', required=True)

    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')

    content = fields.Html('Content', readonly=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('generated', 'Generated'),
    ], default='draft')

    def action_generate_report(self):
        """生成报表 [US-19-04]"""
        for report in self:
            # 这里应该实现具体的报表生成逻辑
            # 汇总各农场的财务数据
            content = self._generate_report_content(report)
            report.write({
                'content': content,
                'state': 'generated'
            })

    def _generate_report_content(self, report):
        """生成报表内容的辅助方法"""
        # 示例报表内容生成
        content = f"""
        <h2>{report.name}</h2>
        <p><strong>Cooperative:</strong> {report.cooperative_entity_id.name}</p>
        <p><strong>Period:</strong> {report.start_date} to {report.end_date}</p>
        <p><strong>Type:</strong> {dict(report.fields_get(allfields=['report_type'])['report_type']['selection'])[report.report_type]}</p>

        <h3>Financial Summary</h3>
        <table class="table table-bordered">
            <thead>
                <tr>
                    <th>Farm</th>
                    <th>Revenue</th>
                    <th>Cost</th>
                    <th>Profit</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Sample Farm 1</td>
                    <td>100,000</td>
                    <td>70,000</td>
                    <td>30,000</td>
                </tr>
                <tr>
                    <td>Sample Farm 2</td>
                    <td>80,000</td>
                    <td>60,000</td>
                    <td>20,000</td>
                </tr>
            </tbody>
        </table>
        """
        return content


class FarmStandardProcedure(models.Model):
    """
    标准操作规程 [US-19-05]
    用于加盟农场的标准化管理
    """
    _name = 'farm.standard.procedure'
    _description = 'Farm Standard Procedure'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Procedure Name', required=True)
    code = fields.Char('Code', required=True, copy=False)
    category = fields.Selection([
        ('planting', 'Planting Standards'),
        ('fertilization', 'Fertilization Standards'),
        ('pest_control', 'Pest Control Standards'),
        ('harvesting', 'Harvesting Standards'),
        ('processing', 'Processing Standards'),
        ('marketing', 'Marketing Standards'),
    ], string='Category', required=True)

    description = fields.Text('Description')
    procedure_document = fields.Binary('Procedure Document',
                                       help='标准操作规程文档')
    document_name = fields.Char('Document Name')

    applicable_entities = fields.Many2many('farm.entity',
                                           string='Applicable to Entities')
    is_mandatory = fields.Boolean('Is Mandatory', default=True,
                                  help='是否为强制性标准')
    effective_date = fields.Date('Effective Date')
    expiry_date = fields.Date('Expiry Date')

    compliance_check_ids = fields.One2many('farm.compliance.check',
                                           'procedure_id',
                                           string='Compliance Checks')

    @api.constrains('code')
    def _check_unique_code(self):
        for record in self:
            existing = self.search([('code', '=', record.code), ('id', '!=', record.id)])
            if existing:
                raise UserError(_("Code must be unique. '%s' already exists.") % record.code)


class FarmComplianceCheck(models.Model):
    """
    合规检查 [US-19-05]
    用于监控加盟农场的合规情况
    """
    _name = 'farm.compliance.check'
    _description = 'Farm Compliance Check'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Check Name', required=True)
    procedure_id = fields.Many2one('farm.standard.procedure',
                                   string='Standard Procedure', required=True)
    entity_id = fields.Many2one('farm.entity', string='Entity', required=True)

    check_date = fields.Date('Check Date', default=fields.Date.context_today)
    compliance_status = fields.Selection([
        ('compliant', 'Compliant'),
        ('non_compliant', 'Non-Compliant'),
        ('pending', 'Pending'),
    ], string='Compliance Status', default='pending', required=True)

    notes = fields.Text('Notes')
    corrective_actions = fields.Text('Corrective Actions Required')
    next_check_date = fields.Date('Next Check Date')

    attachment_ids = fields.Many2many('ir.attachment',
                                      string='Evidence Attachments')

    @api.model
    def create_compliance_check(self, entity_id, procedure_id):
        """为实体和规程创建合规检查"""
        return self.create({
            'name': f"Check for {self.env['farm.entity'].browse(entity_id).name} - {self.env['farm.standard.procedure'].browse(procedure_id).name}",
            'entity_id': entity_id,
            'procedure_id': procedure_id,
            'check_date': fields.Date.context_today(self),
        })