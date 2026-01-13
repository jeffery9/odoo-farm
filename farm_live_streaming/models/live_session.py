from odoo import models, fields, api, _

class LiveStreamingSession(models.Model):
    """
    US-21-03, 06, 07: 直播场次管理
    职责：管理直播时间、关联商品、统计观看与互动数据、存储回放
    """
    _name = 'live.streaming.session'
    _description = 'Live Streaming Session'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Session Title", required=True)
    account_id = fields.Many2one('douyin.account', string="Douyin Account", required=True)
    start_time = fields.Datetime("Scheduled Start")
    end_time = fields.Datetime("Actual End")
    
    state = fields.Selection([
        ('planned', 'Planned'),
        ('live', 'Live'),
        ('ended', 'Ended'),
        ('archived', 'Archived')
    ], default='planned', tracking=True)

    product_ids = fields.Many2many('product.product', string="Featured Products")
    
    # 统计数据 [US-21-05]
    view_count = fields.Integer("View Count", readonly=True)
    like_count = fields.Integer("Likes", readonly=True)
    comment_count = fields.Integer("Comments", readonly=True)
    total_sales = fields.Float("Sales Generated", readonly=True)
    
    # 内容存档 [US-21-07]
    archive_url = fields.Char("Replay Link")
    video_binary = fields.Binary("Clip Archive")
    dy_room_id = fields.Char("Douyin Room ID", help="Actual ID of the live room on Douyin")

    def action_start_live(self):
        self.write({'state': 'live', 'start_time': fields.Datetime.now()})

    def action_end_live(self):
        self.write({'state': 'ended', 'end_time': fields.Datetime.now()})
        # 直播结束时自动拉取一次最终统计和回放
        self.action_refresh_stats()
        self.action_fetch_replay_link()

    def action_refresh_stats(self):
        """ 业务编排：刷新直播统计数据 [US-21-05] """
        for session in self:
            if not session.dy_room_id: continue
            
            # 调用底层账号接口
            res = session.account_id.action_get_live_stats(session.dy_room_id)
            data = res.get('data', {})
            if res.get('error_code') == 0:
                session.write({
                    'view_count': data.get('total_users', 0),
                    'like_count': data.get('total_likes', 0),
                    'comment_count': data.get('total_comments', 0),
                    'total_sales': data.get('total_amount', 0.0) / 100.0,
                })

    def action_fetch_replay_link(self):
        """ 业务编排：拉取并存储回放链接 [US-21-07] """
        for session in self:
            if not session.dy_room_id: continue
            
            res = session.account_id.action_get_live_replay(session.dy_room_id)
            if res.get('error_code') == 0:
                session.archive_url = res.get('data', {}).get('video_url')
