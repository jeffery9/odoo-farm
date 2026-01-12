from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ResCompany(models.Model):
    _inherit = 'res.company'

    is_cooperative_member = fields.Boolean("Is Cooperative Member", default=False, help="Mark this company as part of a cooperative for resource sharing.")

class FarmVehicle(models.Model):
    _inherit = 'farm.vehicle'

    can_be_shared = fields.Boolean("Can Be Shared", default=False, help="Allow this vehicle to be shared with other cooperative members.")
    shared_company_ids = fields.Many2many('res.company', 'farm_vehicle_company_rel', 'vehicle_id', 'company_id', string="Shared With Companies")

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    can_be_shared = fields.Boolean("Can Be Shared", default=False, help="Allow this employee to be shared with other cooperative members.")
    shared_company_ids = fields.Many2many('res.company', 'hr_employee_company_rel', 'employee_id', 'company_id', string="Shared With Companies")

class ProjectTask(models.Model):
    _inherit = 'project.task'

    # 跨公司资源调度
    shared_vehicle_id = fields.Many2one('farm.vehicle', string="Shared Vehicle")
    shared_employee_id = fields.Many2one('hr.employee', string="Shared Employee")

    @api.constrains('shared_vehicle_id', 'company_id')
    def _check_shared_vehicle_company(self):
        for task in self:
            if task.shared_vehicle_id and task.company_id and task.company_id != task.shared_vehicle_id.company_id and task.company_id not in task.shared_vehicle_id.shared_company_ids:
                raise UserError(_("Shared Vehicle '%s' is not available to your company '%s'.") % (task.shared_vehicle_id.name, task.company_id.name))

    @api.constrains('shared_employee_id', 'company_id')
    def _check_shared_employee_company(self):
        for task in self:
            if task.shared_employee_id and task.company_id and task.company_id != task.shared_employee_id.company_id and task.company_id not in task.shared_employee_id.shared_company_ids:
                raise UserError(_("Shared Employee '%s' is not available to your company '%s'.") % (task.shared_employee_id.name, task.company_id.name))

class FarmInternalSettlement(models.Model):
    _name = 'farm.internal.settlement'
    _description = 'Cooperative Internal Settlement'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Reference", default=lambda self: _('New'))
    from_company_id = fields.Many2one('res.company', string="From Company", required=True)
    to_company_id = fields.Many2one('res.company', string="To Company", required=True)
    settlement_type = fields.Selection([
        ('vehicle_rental', 'Vehicle Rental'),
        ('labor_service', 'Labor Service'),
        ('material_transfer', 'Material Transfer')
    ], string="Settlement Type", required=True)
    
    amount = fields.Monetary("Amount", currency_field='currency_id', required=True)
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    
    related_task_id = fields.Many2one('project.task', string="Related Task")
    invoice_id = fields.Many2one('account.move', string="Generated Invoice", readonly=True)
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('invoiced', 'Invoiced')
    ], default='draft', tracking=True)

    def action_generate_invoice(self):
        self.ensure_one()
        if self.invoice_id:
            raise UserError(_("Invoice already generated for this settlement."))
        
        # 简化版：生成一张草稿发票
        invoice_vals = {
            'partner_id': self.to_company_id.partner_id.id,
            'move_type': 'out_invoice',
            'invoice_date': fields.Date.today(),
            'invoice_line_ids': [(0, 0, {
                'name': _("Internal Settlement for %s") % self.settlement_type,
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