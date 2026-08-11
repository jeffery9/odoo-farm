from odoo import models, fields, api, _

class ProjectTask(models.Model):
    _inherit = 'project.task'

    analytic_account_id = fields.Many2one(
        'account.analytic.account', 
        string='Analytic Account', 
        ondelete='set null', 
        copy=False,
        help="Analytic account used to aggregate all costs related to this production task."
    )
    
    total_production_costs = fields.Float(
        string="Total Costs", 
        compute='_compute_total_costs', 
        store=True,
        help="Sum of all analytic lines associated with this task."
    )

    @api.depends('analytic_account_id')
    def _compute_total_costs(self):
        for task in self:
            if task.analytic_account_id:
                # 获取该核算账户下的所有行，amount 取负数（因为支出在 analytic line 里通常是负数）
                lines = self.env['account.analytic.line'].search([
                    ('account_id', '=', task.analytic_account_id.id)
                ])
                task.total_production_costs = -sum(lines.mapped('amount'))
            else:
                task.total_production_costs = 0.0

    @api.model_create_multi
    def create(self, vals_list):
        tasks = super().create(vals_list)
        for task in tasks:
            # 如果是农业任务且没有核算账户，自动创建一个
            if not task.analytic_account_id:
                plan = self.env['account.analytic.plan'].search([('name', '=', 'Agri-Projects')], limit=1)
                if not plan:
                    plan = self.env['account.analytic.plan'].create({'name': 'Agri-Projects'})
                
                analytic_account = self.env['account.analytic.account'].create({
                    'name': task.name,
                    'plan_id': plan.id,
                    'company_id': task.company_id.id or self.env.company.id,
                })
                task.write({'analytic_account_id': analytic_account.id})
        return tasks

    def action_view_analytic_lines(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("farm_financial.project_task_action_view_analytic")
        action['domain'] = [('account_id', '=', self.analytic_account_id.id)]
        action['context'] = {'default_account_id': self.analytic_account_id.id}
        return action
