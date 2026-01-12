from odoo import models, fields, api, _
from odoo.exceptions import UserError

class FarmWageRule(models.Model):
    _name = 'farm.wage.rule'
    _description = 'Piece-rate Wage Rule'

    work_type = fields.Selection([
        ('tillage', 'Tillage (耕作)'),
        ('sowing', 'Sowing (播种)'),
        ('harvesting', 'Harvesting (收获)'),
        ('packaging', 'Packaging (包装)'),
        ('feeding', 'Feeding (饲喂)')
    ], string="Work Type", required=True)
    
    price_per_unit = fields.Float("Price per Unit", required=True, help="Wage per unit of work (e.g. 0.5 per kg)")
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)

class FarmLaborPayment(models.Model):
    _name = 'farm.labor.payment'
    _description = 'Labor Piece-rate Payment'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Reference", required=True, copy=False, readonly=True, default=lambda self: _('New'))
    employee_id = fields.Many2one('hr.employee', string="Worker", required=True)
    date_from = fields.Date("Date From", required=True)
    date_to = fields.Date("Date To", required=True)
    
    line_ids = fields.One2many('farm.labor.payment.line', 'payment_id', string="Details")
    total_amount = fields.Monetary("Total Amount", compute='_compute_total_amount', store=True)
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    
    # Accounting Integration
    journal_id = fields.Many2one('account.journal', string="Journal", domain=[('type', 'in', ['purchase', 'cash', 'bank'])])
    move_id = fields.Many2one('account.move', string="Journal Entry", readonly=True)
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('paid', 'Paid'),
        ('cancel', 'Cancelled')
    ], string="Status", default='draft', tracking=True)

    @api.depends('line_ids.subtotal')
    def _compute_total_amount(self):
        for payment in self:
            payment.total_amount = sum(payment.line_ids.mapped('subtotal'))

    def action_post_to_accounting(self):
        """ 创建会计凭证 (Journal Entry) 并建立连接 [US-13-04] """
        self.ensure_one()
        if not self.journal_id:
            raise UserError(_("Please select a Journal before posting."))
            
        move_vals = {
            'journal_id': self.journal_id.id,
            'date': fields.Date.today(),
            'ref': self.name,
            'move_type': 'entry',
            'line_ids': [],
        }
        
        # 贷方：应付工资或银行 (Credit)
        move_vals['line_ids'].append((0, 0, {
            'name': _('Labor Settlement: %s') % self.employee_id.name,
            'account_id': self.journal_id.default_account_id.id,
            'credit': self.total_amount,
            'debit': 0.0,
        }))
        
        # 借方：工资费用 (Debit)，按任务/核算账户拆分
        for line in self.line_ids:
            analytic_account = line.worklog_id.task_id.analytic_account_id
            analytic_distribution = {str(analytic_account.id): 100} if analytic_account else False
            
            move_vals['line_ids'].append((0, 0, {
                'name': _('Labor: %s - %s') % (self.employee_id.name, line.worklog_id.work_type),
                'account_id': self.employee_id.address_id.property_account_payable_id.id or self.journal_id.default_account_id.id, # 示例逻辑
                'debit': line.subtotal,
                'credit': 0.0,
                'analytic_distribution': analytic_distribution,
            }))
            
        move = self.env['account.move'].create(move_vals)
        move.action_post()
        self.write({'move_id': move.id, 'state': 'paid'})
        return True

    def action_view_move(self):
        self.ensure_one()
        return {
            'name': _('Journal Entry'),
            'view_mode': 'form',
            'res_model': 'account.move',
            'type': 'ir.actions.act_window',
            'res_id': self.move_id.id,
        }

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('farm.labor.payment') or _('PAY')
        return super().create(vals_list)

    def action_compute_sheet(self):
        """ 根据工时记录和单价规则自动计算结算单 """
        self.ensure_one()
        self.line_ids.unlink()
        
        worklogs = self.env['farm.worklog'].search([
            ('employee_id', '=', self.employee_id.id),
            ('date', '>=', self.date_from),
            ('date', '<=', self.date_to)
        ])
        
        lines = []
        for log in worklogs:
            rule = self.env['farm.wage.rule'].search([('work_type', '=', log.work_type)], limit=1)
            price = rule.price_per_unit if rule else 0.0
            lines.append((0, 0, {
                'worklog_id': log.id,
                'quantity': log.quantity,
                'price_unit': price,
                'subtotal': log.quantity * price
            }))
        
        self.write({'line_ids': lines})

class FarmLaborPaymentLine(models.Model):
    _name = 'farm.labor.payment.line'
    _description = 'Labor Payment Line'

    payment_id = fields.Many2one('farm.labor.payment', ondelete='cascade')
    worklog_id = fields.Many2one('farm.worklog', string="Worklog")
    quantity = fields.Float("Quantity")
    price_unit = fields.Float("Unit Price")
    subtotal = fields.Float("Subtotal")
