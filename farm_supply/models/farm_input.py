from odoo import models, fields, api, _

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_agri_input = fields.Boolean("Is Agri Input", default=False)

    is_agri_input = fields.Boolean("Is Agri Input", default=False)
    input_type = fields.Selection([
        ('seed', 'Seed/Variety (种子/种苗)'),
        ('fertilizer', 'Fertilizer (化肥/有机肥)'),
        ('pesticide', 'Pesticide (农药/植保)'),
        ('feed', 'Feed (饲料)'),
        ('medicine', 'Medicine (兽药/防疫)'),
        ('other', 'Other Supplies (其他物资)')
    ], string="Input Type")
    
    is_safety_approved = fields.Boolean("Safety Approved", default=True, help="Is this input compliant with organic/safety standards?")
    active_ingredient = fields.Char("Active Ingredient", help="e.g. Glyphosate, Nitrogen content")
    
    # 养分含量 [US-01-03]
    n_content = fields.Float("Nitrogen (%)", help="Nitrogen percentage")
    p_content = fields.Float("Phosphorus (%)", help="Phosphorus percentage")
    k_content = fields.Float("Potassium (%)", help="Potassium percentage")
    
    # 休药期/安全间隔期 [US-11-03]
    withdrawal_period_days = fields.Integer("Withdrawal Period (Days)", default=0, help="Days to wait before harvest/slaughter after using this input.")
    
    # 生长周期 [US-03-01]
    growth_cycle_days = fields.Integer("Growth Cycle (Days)", default=0, help="Typical duration from start to harvest.")

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        """ 检查生长周期提前期 [US-03-01] """
        for order in self:
            for line in order.order_line:
                product = line.product_id
                if product.growth_cycle_days > 0:
                    # 假定交付日期为 commitment_date 或 request_date
                    delivery_date = order.commitment_date or order.expected_date
                    if delivery_date:
                        delivery_date = fields.Date.to_date(delivery_date)
                        min_date = fields.Date.add(fields.Date.today(), days=product.growth_cycle_days)
                        if delivery_date < min_date:
                            # 发出警告（此处使用 message_post，因为 action_confirm 通常不适合抛出 UserError 阻止确认，除非非常严重）
                            order.message_post(body=_("WARNING: Lead time insufficient for product %s. Growth cycle is %s days, but delivery is scheduled in %s days.") % (
                                product.name, product.growth_cycle_days, (delivery_date - fields.Date.today()).days
                            ))
        return super(SaleOrder, self).action_confirm()

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    agri_task_id = fields.Many2one(
        'project.task', 
        string="Origin Agri Task",
        help="The specific production task that triggered this procurement."
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'procurement_group_id' in vals and not vals.get('agri_task_id'):
                group = self.env['procurement.group'].browse(vals['procurement_group_id'])
                if hasattr(group, 'agri_task_id') and group.agri_task_id:
                    vals['agri_task_id'] = group.agri_task_id.id
        return super().create(vals_list)

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    is_compliance_warning = fields.Boolean("Compliance Warning", compute='_compute_compliance_warning', store=True)

    @api.depends('product_id')
    def _compute_compliance_warning(self):
        for line in self:
            if line.product_id.is_agri_input and not line.product_id.is_safety_approved:
                line.is_compliance_warning = True
            else:
                line.is_compliance_warning = False
