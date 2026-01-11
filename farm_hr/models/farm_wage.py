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
