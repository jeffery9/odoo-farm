from odoo import models, fields, api, _

class ProductTemplate(models.Model):
    _inherit = 'product.template'

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
    
    # 休药期/安全间隔期 [US-35]
    withdrawal_period_days = fields.Integer("Withdrawal Period (Days)", default=0, help="Days to wait before harvest/slaughter after using this input.")

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
