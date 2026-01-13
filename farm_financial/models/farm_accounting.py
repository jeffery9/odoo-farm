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
            # Automatically fetch Farm Task ID from origin order
            if not vals.get('agri_task_id'):
                if vals.get('invoice_origin'):
                    # Attempt matching from Purchase Order
                    po = self.env['purchase.order'].search([('name', '=', vals['invoice_origin'])], limit=1)
                    if po and po.agri_task_id:
                        vals['agri_task_id'] = po.agri_task_id.id
                    else:
                        # Attempt matching from Sales Order
                        so = self.env['sale.order'].search([('name', '=', vals['invoice_origin'])], limit=1)
                        if so and hasattr(so, 'agri_task_id') and so.agri_task_id:
                            vals['agri_task_id'] = so.agri_task_id.id
        return super().create(vals_list)

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.onchange('product_id')
    def _onchange_agri_analytic(self):
        """ Automatically fetch Farm Task analytic account """
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
            # Read energy readings from mrp.production
            water_cons = getattr(rec.production_id, 'water_consumption', 0)
            elec_cons = getattr(rec.production_id, 'electricity_consumption', 0)
            
            rec.total_water_cost = water_cons * rec.water_rate
            rec.total_electricity_cost = elec_cons * rec.electricity_rate
            rec.total_processing_cost = rec.total_water_cost + rec.total_electricity_cost + rec.other_indirect_costs

    def action_allocate_costs(self):
        """ Write calculated costs to processing product analytic account [US-14-13] """
        self.ensure_one()
        if self.total_processing_cost > 0:
            # Find processing product analytic account (通过 mrp.production 关联的农事任务或产品的分析账户)
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

class AgriCostWIPTransfer(models.AbstractModel):
    """
    US-14-15: 生产性生物资产成本归集与结转逻辑
    """
    _name = 'farm.cost.wip.transfer'
    _description = 'WIP to Finished Goods Cost Transfer'

    def action_transfer_wip_to_lot(self, task_id, lot_id):
        """
        Allocate accumulated WIP costs to harvest lots during harvest transfer
        """
        if not task_id.analytic_account_id:
            return 0.0
            
        # 1. Sum all analytic line costs under this task (支出为负)
        analytic_lines = self.env['account.analytic.line'].search([
            ('account_id', '=', task_id.analytic_account_id.id)
        ])
        total_wip_cost = abs(sum(analytic_lines.mapped('amount')))
        
        if total_wip_cost > 0 and lot_id:
            # 2. Distribute costs to lots (存储在 lot 的成本价字段，或通过 valuation 调整)
            # Assume lot has a standard price field
            if hasattr(lot_id, 'standard_price'):
                # 按产量分摊 (简单实现：总量分摊)
                lot_id.write({'standard_price': total_wip_cost / (lot_id.product_qty or 1.0)})
                
            # Record audit logs
            lot_id.message_post(body=_("WIP COST TRANSFERRED: %s total cost absorbed from task %s") % (total_wip_cost, task_id.name))
            
        return total_wip_cost

class AgriMortalityAmortization(models.AbstractModel):
    """
    US-03-05: 死亡成本自动重分配 (Core-Closure)
    When a biological asset dies, its accumulated costs are amortized across surviving individuals.
    """
    _name = 'farm.mortality.amortization'
    _description = 'Mortality Cost Absorption Logic'

    def action_absorb_mortality_cost(self, dead_lot_id, surviving_lot_id):
        """
        :param dead_lot_id: Mortality asset lot (Individual)
        :param surviving_lot_id: Surviving lot absorbing costs (通常是同一个大 Lot)
        """
        if not dead_lot_id or not surviving_lot_id:
            return False

        # 1. Look for associated analytic account (通过任务关联)
        task = self.env['project.task'].search([('lot_ids', 'in', [dead_lot_id.id])], limit=1)
        if not task or not task.analytic_account_id:
            return False

        # 2. Aggregate incurred WIP costs
        analytic_lines = self.env['account.analytic.line'].search([
            ('account_id', '=', task.analytic_account_id.id),
            ('lot_id', '=', dead_lot_id.id) # Assume analytic lines have lot links
        ])
        mortality_cost = abs(sum(analytic_lines.mapped('amount')))

        if mortality_cost > 0:
            # 3. Create cost transfer line (均摊给存活者)
            self.env['account.analytic.line'].create({
                'name': _('Mortality Cost Absorption: %s') % dead_lot_id.name,
                'account_id': task.analytic_account_id.id,
                'amount': -mortality_cost, # Still an expense, but marked as mortality absorption in reports
                'lot_id': surviving_lot_id.id,
                'unit_amount': 0, # Do not count yield
            })
            
            surviving_lot_id.message_post(body=_(
                "CORE-CLOSURE: Absorbed %s cost from deceased asset [%s]."
            ) % (mortality_cost, dead_lot_id.name))
            
        return True
