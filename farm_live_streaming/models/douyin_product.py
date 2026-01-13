from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class DouyinProduct(models.Model):
    """
    US-21-02: 抖音商品同步管理
    职责：处理产品映射、库存同步、溯源内容推送
    """
    _name = 'douyin.product'
    _description = 'Douyin Shop Product Sync'

    account_id = fields.Many2one('douyin.account', string="Douyin Account", required=True)
    product_id = fields.Many2one('product.product', string="Odoo Product", required=True)
    douyin_item_id = fields.Char("Douyin Item ID", help="ID in Douyin Shop")
    
    sync_state = fields.Selection([
        ('pending', 'Pending'),
        ('synced', 'Synced'),
        ('error', 'Error')
    ], default='pending', tracking=True)
    
    last_sync_time = fields.Datetime("Last Sync")

    def action_sync_to_douyin(self):
        """ 执行同步：推送产品信息与溯源故事 [US-21-02, US-21-03] """
        for rec in self:
            if rec.account_id.state != 'authorized':
                raise UserError(_("Account not authorized!"))

            # 1. 抓取最新的农业溯源故事
            latest_lot = self.env['stock.lot'].search([('product_id', '=', rec.product_id.id)], order='create_date desc', limit=1)
            story = latest_lot.story_content if latest_lot else "Naturally grown on our farm."
            
            # 2. 构建 API 载荷
            payload = {
                'title': rec.product_id.name,
                'description': story,
                'price': int(rec.product_id.list_price * 100),
                'stock': int(rec.product_id.qty_available),
                'out_id': str(rec.product_id.id),
            }
            
            # 3. 调用 API
            endpoint = "/item/create/" if not rec.douyin_item_id else "/item/update/"
            if rec.douyin_item_id: payload['item_id'] = rec.douyin_item_id
                
            response = rec.account_id._do_douyin_request(endpoint, params=payload)
            
            if response.get('data', {}).get('error_code') == 0:
                rec.write({
                    'douyin_item_id': response['data'].get('item_id', rec.douyin_item_id),
                    'sync_state': 'synced',
                    'last_sync_time': fields.Datetime.now()
                })
            else:
                rec.sync_state = 'error'

    def action_sync_stock_only(self):
        """ 仅同步库存量：供库存变动钩子调用 [US-21-08] """
        for rec in self:
            if not rec.douyin_item_id or rec.account_id.state != 'authorized':
                continue
            
            payload = {
                'item_id': rec.douyin_item_id,
                'stock': int(rec.product_id.qty_available),
            }
            # 调用专门的库存更新 API
            rec.account_id._do_douyin_request("/item/update_stock/", params=payload)
            rec.last_sync_time = fields.Datetime.now()

class StockQuant(models.Model):
    _inherit = 'stock.quant'

    @api.model_create_multi
    def create(self, vals_list):
        quants = super().create(vals_list)
        quants._trigger_douyin_stock_sync()
        return quants

    def write(self, vals):
        res = super().write(vals)
        if 'inventory_quantity' in vals or 'quantity' in vals:
            self._trigger_douyin_stock_sync()
        return res

    def _trigger_douyin_stock_sync(self):
        """ 触发该产品关联的所有抖音铺货库存同步 """
        for quant in self:
            douyin_mappings = self.env['douyin.product'].search([('product_id', '=', quant.product_id.id)])
            for mapping in douyin_mappings:
                # 异步或通过定时任务触发，这里简化为直接调用
                mapping.action_sync_stock_only()
