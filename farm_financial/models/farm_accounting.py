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

class ProcessingCostAllocation(models.Model):
    """
    US-14-13: 仓储加工成本精细化分摊
    将加工过程中的间接费用（水电、折旧等）分摊到产品批次
    """
    _name = 'farm.processing.cost'
    _description = 'Processing Cost Allocation'

    production_id = fields.Many2one('mrp.production', string="Processing Order", required=True)
    water_rate = fields.Float("Water Unit Price", default=5.0)
    electricity_rate = fields.Float("Electricity Unit Price", default=1.0)
    
    total_water_cost = fields.Float("Total Water Cost", compute='_compute_total_costs')
    total_electricity_cost = fields.Float("Total Electricity Cost", compute='_compute_total_costs')
    other_indirect_costs = fields.Float("Other Indirect Costs (Labor/Depreciation)")
    
    total_processing_cost = fields.Float("Total Processing Cost", compute='_compute_total_costs', store=True)

    @api.depends('production_id', 'water_rate', 'electricity_rate', 'other_indirect_costs')
    def _compute_total_costs(self):
        for rec in self:
            # 读取 mrp.production 中的能耗读数
            water_cons = getattr(rec.production_id, 'water_consumption', 0)
            elec_cons = getattr(rec.production_id, 'electricity_consumption', 0)
            
            rec.total_water_cost = water_cons * rec.water_rate
            rec.total_electricity_cost = elec_cons * rec.electricity_rate
            rec.total_processing_cost = rec.total_water_cost + rec.total_electricity_cost + rec.other_indirect_costs

    def action_allocate_costs(self):
        """ 将计算出的成本写入加工产品的分析账户 [US-14-13] """
        self.ensure_one()
        if self.total_processing_cost > 0:
            # 找到加工产品的分析账户 (通过 mrp.production 关联的农事任务或产品的分析账户)
            analytic_account = self.production_id.product_id.bom_ids[:1].analytic_account_id
            if analytic_account:
                self.env['account.analytic.line'].create({
                    'name': _('Processing Overhead: %s') % self.production_id.name,
                    'account_id': analytic_account.id,
                    'amount': -self.total_processing_cost,
                    'date': fields.Date.today(),
                    'unit_amount': 1,
                })
        return True
