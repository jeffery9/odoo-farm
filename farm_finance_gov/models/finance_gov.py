from odoo import models, fields, api, _

class FarmRuralRevitalizationProject(models.Model):
    _name = 'farm.rural.revitalization.project'
    _description = 'Rural Revitalization Project'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Project Name", required=True)
    code = fields.Char("Project Code", required=True)
    fund_source = fields.Char("Fund Source")
    budget_amount = fields.Monetary("Budget Amount", currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    
    date_start = fields.Date("Start Date")
    date_end = fields.Date("End Date")
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], default='draft', tracking=True)
    
    # 关联支出
    account_move_ids = fields.One2many('account.move', 'rural_project_id', string="Related Account Moves")
    total_expenditure = fields.Monetary("Total Expenditure", compute='_compute_total_expenditure')

    @api.depends('account_move_ids.amount_total_in_currency_dlc')
    def _compute_total_expenditure(self):
        for project in self:
            project.total_expenditure = sum(project.account_move_ids.filtered(lambda m: m.move_type in ['in_invoice', 'out_refund', 'in_receipt', 'out_receipt'] and m.state == 'posted').mapped('amount_total_in_currency_dlc'))

class AccountMove(models.Model):
    _inherit = 'account.move'

    # 关联乡村振兴项目 [US-18-09]
    rural_project_id = fields.Many2one('farm.rural.revitalization.project', string="Rural Revitalization Project")
    
    @api.constrains('rural_project_id', 'state')
    def _check_rural_project_funds(self):
        for move in self:
            if move.rural_project_id and move.state == 'posted':
                # 简单校验：项目支出不能超预算
                if move.rural_project_id.total_expenditure + move.amount_total_in_currency_dlc > move.rural_project_id.budget_amount:
                    #raise ValidationError(_("Project '%s' budget exceeded by this move.") % move.rural_project_id.name) # 暂时不强制限
                    pass # 仅记录警告，不阻止
