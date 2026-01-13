from odoo import models, fields, api, _
from odoo.exceptions import UserError

class FarmQualityPoint(models.Model):
    _name = 'farm.quality.point'
    _description = 'Quality Control Point'

    name = fields.Char("Title", required=True)
    product_id = fields.Many2one('product.product', string="Product/Variety")
    test_type = fields.Selection([
        ('pass_fail', 'Pass - Fail (通过/失败)'),
        ('measure', 'Measure (数值测量)')
    ], string="Test Type", default='pass_fail', required=True)
    
    # 测量标准
    norm = fields.Float("Norm")
    tolerance_min = fields.Float("Min Tolerance")
    tolerance_max = fields.Float("Max Tolerance")
    
    active = fields.Boolean(default=True)

class FarmQualityCheck(models.Model):
    _name = 'farm.quality.check'
    _description = 'Quality Check'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Reference", required=True, default=lambda self: _('New'))
    point_id = fields.Many2one('farm.quality.point', string="Control Point")
    lot_id = fields.Many2one('stock.lot', string="Lot/Batch", required=True)
    sample_id = fields.Many2one('farm.quality.sample', string="Linked Sample", 
                               help="The physical sample used for this check.")
    task_id = fields.Many2one('project.task', string="Production Task")
    
    test_type = fields.Selection(related='point_id.test_type', store=True)
    measure = fields.Float("Actual Measure")
    
    quality_state = fields.Selection([
        ('none', 'To do'),
        ('pass', 'Passed'),
        ('fail', 'Failed')
    ], string="Status", default='none', tracking=True)
    
    user_id = fields.Many2one('res.users', string="Responsible", default=lambda self: self.env.user)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('farm.quality.check') or _('QC')
        return super().create(vals_list)

    def action_pass(self):
        self.write({'quality_state': 'pass'})
        self.lot_id.write({'quality_status': 'passed'})

    def action_fail(self):
        self.write({'quality_state': 'fail'})
        self.lot_id.write({'quality_status': 'failed'})

    def action_done(self):
        """ 对于测量型检查，根据范围自动判定 """
        self.ensure_one()
        if self.test_type == 'measure':
            if self.point_id.tolerance_min <= self.measure <= self.point_id.tolerance_max:
                self.action_pass()
            else:
                self.action_fail()
        else:
            self.action_pass()

    def action_open_quality_alert(self):
        """ 创建并返回质量告警记录 """
        self.ensure_one()
        alert = self.env['farm.quality.alert'].create({
            'name': _('Alert for %s') % self.lot_id.name,
            'check_id': self.id,
            'lot_id': self.lot_id.id,
            'product_id': self.lot_id.product_id.id,
        })
        return alert

class FarmQualityAlert(models.Model):
    _name = 'farm.quality.alert'
    _description = 'Quality Alert'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Title", required=True)
    check_id = fields.Many2one('farm.quality.check', string="Source Check")
    lot_id = fields.Many2one('stock.lot', string="Lot/Batch", required=True)
    product_id = fields.Many2one('product.product', string="Product")
    
    user_id = fields.Many2one('res.users', string="Responsible", default=lambda self: self.env.user)
    priority = fields.Selection([('0', 'Low'), ('1', 'Normal'), ('2', 'High')], default='1')
    
    description = fields.Text("Description")
    cause = fields.Text("Root Cause")
    action_taken = fields.Text("Action Taken")
    
    state = fields.Selection([
        ('new', 'New'),
        ('confirmed', 'Confirmed'),
        ('action_proposed', 'Action Proposed'),
        ('closed', 'Closed'),
    ], string="Status", default='new', tracking=True)

    def action_confirm(self):
        self.write({'state': 'confirmed'})

    def action_close_scrapped(self):
        self.message_post(body=_("Alert closed: Asset marked for scrapping."))
        self.write({'state': 'closed'})
        # 此处可进一步调用 stock.scrap 逻辑

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        """ 质量与放行拦截逻辑 [US-05-04, US-15-05] """
        for picking in self:
            if picking.picking_type_code in ['outgoing', 'internal']:
                for move in picking.move_ids:
                    for lot in move.lot_ids:
                        # 1. 检查质量状态
                        if lot.quality_status == 'failed':
                            raise UserError(_("QUALITY ALERT: Lot %s has failed quality inspection.") % lot.name)
                        
                        # 2. 检查放行状态 [US-15-05]
                        if lot.qc_release_state == 'locked':
                            raise UserError(_("QC LOCKED: Lot %s is pending release and cannot be moved.") % lot.name)
                            
        return super().button_validate()

class FarmLotQuality(models.Model):
    _inherit = 'stock.lot'

    quality_status = fields.Selection([
        ('none', 'Not Tested'),
        ('passed', 'Passed'),
        ('failed', 'Failed')
    ], string="Quality Status", default='none', tracking=True)
    
    # US-15-05: 默认锁定与释放
    qc_release_state = fields.Selection([
        ('locked', 'Locked (待检锁定)'),
        ('released', 'Released (已放行)'),
    ], string="QC Release Status", default='locked', tracking=True)

    quality_check_ids = fields.One2many('farm.quality.check', 'lot_id', string="Quality Checks")

    def action_qc_release(self):
        """ 手动放行批次 """
        self.ensure_one()
        # 权限校验通常在视图中通过 groups 属性处理，这里仅做逻辑切换
        self.write({'qc_release_state': 'released'})
        self.message_post(body=_("QC RELEASE: Lot has been manually released for sale/transfer."))
