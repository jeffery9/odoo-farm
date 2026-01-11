from odoo import models, fields, api, _

class AccountMove(models.Model):
    _inherit = 'account.move'

    agri_task_id = fields.Many2one(
        'project.task', 
        string="Farm Task",
        help="Link this invoice/bill to a specific agricultural task for cost/revenue tracking."
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            # 从来源订单自动带入农事任务 ID
            if not vals.get('agri_task_id'):
                if vals.get('invoice_origin'):
                    # 尝试从采购单匹配
                    po = self.env['purchase.order'].search([('name', '=', vals['invoice_origin'])], limit=1)
                    if po and po.agri_task_id:
                        vals['agri_task_id'] = po.agri_task_id.id
                    else:
                        # 尝试从销售单匹配
                        so = self.env['sale.order'].search([('name', '=', vals['invoice_origin'])], limit=1)
                        if so and hasattr(so, 'agri_task_id') and so.agri_task_id:
                            vals['agri_task_id'] = so.agri_task_id.id
        return super().create(vals_list)

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.onchange('product_id')
    def _onchange_agri_analytic(self):
        """ 自动带入农事任务的核算账户 """
        if self.move_id.agri_task_id and self.move_id.agri_task_id.analytic_account_id:
            self.analytic_distribution = {str(self.move_id.agri_task_id.analytic_account_id.id): 100}

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    agri_task_id = fields.Many2one(
        'project.task', 
        string="Farm Task",
        help="Directly link a payment to a farm task (e.g. cash payment for seasonal labor)."
    )

    def action_post(self):
        """ 支付确认时，如果是直接关联任务的，自动生成分析行 """
        res = super().action_post()
        for payment in self:
            if payment.agri_task_id and payment.agri_task_id.analytic_account_id:
                # 只有在没有关联发票的情况下才手动创建（发票支付会自动通过核销产生分析行，取决于配置）
                if not payment.reconciled_bill_ids and not payment.reconciled_invoice_ids:
                    self.env['account.analytic.line'].create({
                        'name': _('Direct Payment: %s') % payment.ref or payment.name,
                        'account_id': payment.agri_task_id.analytic_account_id.id,
                        'amount': -payment.amount if payment.payment_type == 'outbound' else payment.amount,
                        'date': payment.date,
                        'partner_id': payment.partner_id.id,
                    })
        return res
