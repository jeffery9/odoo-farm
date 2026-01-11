from odoo import models, fields, api, _
from odoo.exceptions import UserError

class FarmLot(models.Model):
    _inherit = 'stock.lot'

    def action_record_death(self, qty, reason, notes=False):
        """ 记录减员并发布审计消息 """
        self.ensure_one()
        if qty <= 0:
            raise UserError(_("Quantity must be positive."))
        
        body = _("DEATH RECORDED: %s animals decreased. Reason: %s. Notes: %s") % (qty, reason, notes or "")
        self.message_post(body=body)
        
        # 此处未来可扩展：自动生成库存报废单 (stock.scrap)
        return True

    def action_merge_from(self, source_group):
        """ 将源群组合并到当前群组 """
        self.ensure_one()
        if source_group.product_id != self.product_id:
            raise UserError(_("Cannot merge groups of different products."))
        
        body = _("MERGE: Group %s has been merged into this group.") % source_group.name
        self.message_post(body=body)
        
        # 标记源群组为已结束
        source_group.write({'biological_stage': 'harvested', 'active': False})
        return True
