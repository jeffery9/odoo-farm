from odoo import models, fields, api, _

class FarmLoan(models.Model):
    _name = 'farm.loan'
    _description = 'Agricultural Loan'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Loan Reference", default=lambda self: _('New'))
    partner_id = fields.Many2one('res.partner', string="Lender (Bank/Co-op)", required=True)
    loan_type = fields.Selection([
        ('operational', 'Operational (运营贷)'),
        ('equipment', 'Equipment (农机贷)'),
        ('biological', 'Biological Asset Mortgage (活体抵押)')
    ], required=True)
    
    amount_principal = fields.Monetary("Principal Amount", currency_field='currency_id')
    amount_interest = fields.Monetary("Projected Interest", currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    
    date_start = fields.Date("Start Date")
    date_maturity = fields.Date("Maturity Date")
    
    # 抵押物关联
    collateral_lot_ids = fields.Many2many('stock.lot', string="Collateral Assets")
    collateral_value = fields.Monetary("Collateral Valuation", compute='_compute_collateral_value')
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('active', 'Active'),
        ('paid', 'Fully Paid'),
        ('defaulted', 'Defaulted')
    ], default='draft', tracking=True)

    @api.depends('collateral_lot_ids')
    def _compute_collateral_value(self):
        for loan in self:
            # 简单估值：数量 * 品种标准价 (实际可接入评估模型)
            val = 0.0
            for lot in loan.collateral_lot_ids:
                price = lot.product_id.standard_price
                qty = getattr(lot, 'animal_count', 1)
                val += price * qty
            loan.collateral_value = val

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('farm.loan') or _('LOAN')
        return super().create(vals_list)
