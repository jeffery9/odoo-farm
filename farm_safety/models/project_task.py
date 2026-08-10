from odoo import models, fields, api, _
from datetime import timedelta

class ProjectTask(models.Model):
    _inherit = 'project.task'

    prevention_template_id = fields.Many2one(
        'farm.prevention.template', 
        string="Prevention Plan",
        help="Select a template to auto-generate prevention tasks."
    )

    def action_confirm_intervention_safety(self, product_ids):
        """ 
        当干预任务涉及药物时，更新关联批次的休药期截止日。
        供 farm_operation 或 mrp 调用。
        """
        self.ensure_one()
        if not self.biological_lot_id:
            return
            
        products = self.env['product.product'].browse(product_ids)
        max_period = max(products.mapped('withdrawal_period_days') or [0])
        
        if max_period > 0:
            new_expiry = fields.Datetime.now() + timedelta(days=max_period)
            # 更新批次上的截止时间
            if not self.biological_lot_id.withdrawal_end_datetime or new_expiry > self.biological_lot_id.withdrawal_end_datetime:
                self.biological_lot_id.write({'withdrawal_end_datetime': new_expiry})
                self.message_post(body=_("SAFETY: Withdrawal period updated to %s due to medication.") % new_expiry)

    def action_apply_prevention_template(self):
        """ 根据模板生成子任务 """
        self.ensure_one()
        if not self.prevention_template_id or not self.planned_date_begin:
            return False
        
        task_obj = self.env['project.task']
        for line in self.prevention_template_id.line_ids:
            deadline = self.planned_date_begin + timedelta(days=line.delay_days)
            task_obj.create({
                'name': _('Prevention: %s') % line.name,
                'parent_id': self.id,
                'project_id': self.project_id.id,
                'date_deadline': deadline,
                'user_ids': self.user_ids.ids,
                # 未来可在此处预填 MO 逻辑
            })
        return True
