from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # 农药/兽药实名制与监管 [US-66]
    is_regulated_input = fields.Boolean("Is Regulated Input (受监管投入品)", default=False)
    reg_cert_no = fields.Char("Registration/Approval No. (登记证号/批文号)")
    is_prohibited_restricted = fields.Boolean("Prohibited/Restricted (禁限用)", default=False)
    prohibited_reason = fields.Text("Prohibited/Restricted Reason")

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    # 农事操作人信息 [US-66]
    operator_id_card = fields.Char("Operator ID Card No. (操作人身份证号)", copy=False)
    
    @api.constrains('operator_id_card')
    def _check_operator_id_card(self):
        for record in self:
            if record.operator_id_card and not record.operator_id_card.isdigit() or len(record.operator_id_card) not in [15, 18]:
                raise ValidationError(_("Operator ID Card No. must be 15 or 18 digits."))

    def action_confirm(self):
        # 扩展确认逻辑，增加投入品实名制校验
        for mo in self:
            has_regulated_input = False
            for move in mo.move_raw_ids:
                if move.product_id.is_regulated_input:
                    has_regulated_input = True
                    if move.product_id.is_prohibited_restricted:
                        raise UserError(_("REGULATION VIOLATION: Input '%s' is Prohibited/Restricted. Reason: %s") % (move.product_id.name, move.product_id.prohibited_reason))
            
            if has_regulated_input and not mo.operator_id_card:
                raise UserError(_("REAL-NAME REQUIRED: Operator ID Card No. is required for regulated inputs."))
        
        return super(MrpProduction, self).action_confirm()

    def action_sync_to_provincial_platform(self):
        """ 模拟向省级农资监管平台同步数据 [US-66] """
        self.ensure_one()
        _logger.info("Simulating data sync to provincial platform for %s. Operator: %s", self.name, self.operator_id_card)
        self.message_post(body=_("Data sync to provincial platform simulated for Intervention %s.") % self.name)
        return True
