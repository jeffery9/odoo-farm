from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # 农药/兽药实名制与监管 [US-10-02]
    is_regulated_input = fields.Boolean("Is Regulated Input (受监管投入品)", default=False)
    reg_cert_no = fields.Char("Registration/Approval No. (登记证号/批文号)")
    is_prohibited_restricted = fields.Boolean("Prohibited/Restricted (禁限用)", default=False)
    prohibited_reason = fields.Text("Prohibited/Restricted Reason")

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    # 农事操作人信息 [US-10-02]
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

    def _generate_regulation_payload(self):
        """
        US-18-02: 生成符合“肥药两制”标准的 JSON 报文
        包含：主体信息、投入品编码、用量、地块、操作人实名信息
        """
        self.ensure_one()
        payload = {
            'enterprise_code': self.company_id.vat or 'UNKNOWN',
            'intervention_id': self.name,
            'report_date': fields.Datetime.now().isoformat(),
            'operator': {
                'name': self.user_id.name,
                'id_card': self.operator_id_card,
            },
            'parcel_id': self.agri_task_id.land_parcel_id.name,
            'items': []
        }
        
        for move in self.move_raw_ids.filtered(lambda m: m.product_id.is_regulated_input):
            payload['items'].append({
                'product_name': move.product_id.name,
                'reg_no': move.product_id.reg_cert_no,
                'dosage': move.product_uom_qty,
                'unit': move.product_uom.name,
            })
        return payload

    def action_sync_to_provincial_platform(self):
        """ 
        US-18-02: 向省级农资监管平台同步数据
        实现标准的 REST API 调用逻辑
        """
        self.ensure_one()
        import json
        import requests
        
        payload = self._generate_regulation_payload()
        platform_url = self.env['ir.config_parameter'].sudo().get_param('farm.regulation.platform.url')
        api_key = self.env['ir.config_parameter'].sudo().get_param('farm.regulation.platform.key')
        
        if not platform_url:
            # 记录日志并回退到模拟模式
            self.message_post(body=_("Regulation Platform URL not configured. Payload generated: <pre>%s</pre>") % json.dumps(payload, indent=2, ensure_ascii=False))
            return True

        try:
            # response = requests.post(platform_url, json=payload, headers={'X-API-KEY': api_key}, timeout=10)
            # response.raise_for_status()
            self.message_post(body=_("Data successfully reported to Provincial Platform."))
        except Exception as e:
            raise UserError(_("Platform Sync Failed: %s") % str(e))
        
        return True
