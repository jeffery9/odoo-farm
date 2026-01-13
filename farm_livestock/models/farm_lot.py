from odoo import models, fields, api, _
from odoo.exceptions import UserError

class FarmLot(models.Model):
    _inherit = 'stock.lot'

    animal_count = fields.Integer("Animal Count", default=1)
    average_weight = fields.Float("Average Weight (kg)", help="Current average weight of individuals in this lot.")
    
    # 生物阶段 [US-05-04]
    biological_stage = fields.Selection([
        ('born', 'Born/Started'),
        ('growing', 'Growing'),
        ('finished', 'Finished'),
        ('harvested', 'Harvested')
    ], string="Biological Stage", default='born')

    # US-03-01: 生长预测与饲喂核销
    start_weight = fields.Float("Initial Weight (kg)")
    current_predicted_weight = fields.Float("Predicted Weight (kg)", compute='_compute_predicted_weight', store=True)
    average_daily_gain = fields.Float("ADG (kg/day)", default=0.5, help="Average Daily Gain")
    
    active_feeding_bom_id = fields.Many2one('mrp.bom', string="Active Feeding Recipe", 
                                           domain="[('type', '=', 'normal'), ('intervention_type', '=', 'feeding')]")

    @api.depends('create_date', 'start_weight', 'average_daily_gain')
    def _compute_predicted_weight(self):
        today = fields.Date.today()
        for lot in self:
            if lot.create_date and lot.biological_stage in ['born', 'growing']:
                days_passed = (today - lot.create_date.date()).days
                lot.current_predicted_weight = lot.start_weight + (days_passed * lot.average_daily_gain)
            else:
                lot.current_predicted_weight = lot.average_weight

    def _cron_daily_feed_depletion(self):
        """ 定时任务：每日自动生成饲喂干预并冲减库存 [US-03-01] """
        Intervention = self.env['mrp.production']
        active_lots = self.search([('biological_stage', 'in', ['born', 'growing']), ('active_feeding_bom_id', '!=', False)])
        
        for lot in active_lots:
            # 自动创建“已完成”的饲喂干预
            intervention = Intervention.create({
                'product_id': lot.product_id.id,
                'bom_id': lot.active_feeding_bom_id.id,
                'product_qty': lot.animal_count, # 按头数计算
                'intervention_type': 'feeding',
                'lot_producing_id': lot.id,
                'date_start': fields.Datetime.now(),
            })
            intervention.action_confirm()
            # 自动确认完成，触发库存冲减
            intervention.button_mark_done()
            _logger.info("Daily feed depletion recorded for lot %s using BOM %s", lot.name, lot.active_feeding_bom_id.name)
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
