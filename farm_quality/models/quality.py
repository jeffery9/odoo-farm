from odoo import models, fields, api, _

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

class FarmLotQuality(models.Model):
    _inherit = 'stock.lot'

    quality_status = fields.Selection([
        ('none', 'Not Tested'),
        ('passed', 'Passed'),
        ('failed', 'Failed')
    ], string="Quality Status", default='none', tracking=True)
    
    quality_check_ids = fields.One2many('farm.quality.check', 'lot_id', string="Quality Checks")
