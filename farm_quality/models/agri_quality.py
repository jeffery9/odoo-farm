from odoo import models, fields, api, _
from odoo.exceptions import UserError
import hashlib
import json

class AgriQualityPoint(models.Model):
    _name = 'agri.quality.point'
    _description = 'Agricultural Quality Control Point'

    name = fields.Char("Title", required=True)
    product_id = fields.Many2one('product.product', string="Product/Variety")
    test_type = fields.Selection([
        ('pass_fail', 'Pass - Fail'),
        ('measure', 'Measure'),
        ('sensory', 'Sensory Evaluation'),
        ('hplc', 'HPLC Lab Test')
    ], string="Test Type", default='pass_fail', required=True)

    # 测量标准
    norm = fields.Float("Norm")
    tolerance_min = fields.Float("Min Tolerance")
    tolerance_max = fields.Float("Max Tolerance")

    active = fields.Boolean(default=True)

class AgriQualityCheck(models.Model):
    _name = 'agri.quality.check'
    _description = 'Agricultural Quality Check'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Reference", required=True, default=lambda self: _('New'))
    point_id = fields.Many2one('agri.quality.point', string="Control Point")
    lot_id = fields.Many2one('stock.lot', string="Lot/Batch", required=True)
    sample_id = fields.Many2one('agri.quality.sample', string="Linked Sample",
                               help="The physical sample used for this check.")
    task_id = fields.Many2one('project.task', string="Production Task")
    purchase_order_line_id = fields.Many2one('purchase.order.line', string="Purchase Order Line",
                                            help="Link to purchase order line for acquisition quality checks (US-009-19)")

    test_type = fields.Selection(related='point_id.test_type', store=True)
    measure = fields.Float("Actual Measure")

    quality_state = fields.Selection([
        ('none', 'To do'),
        ('pass', 'Passed'),
        ('fail', 'Failed')
    ], string="Status", default='none', tracking=True)

    user_id = fields.Many2one('res.users', string="Responsible", default=lambda self: self.env.user)

    # US-038-07: 现场快速检测 (Quick-Test)
    is_quick_test = fields.Boolean("Is Quick Test", default=False)
    quick_test_photo = fields.Binary("Test Strip Photo", attachment=True)

    # US-038-08: 数字化感官评价 (Sensory Profile)
    appearance_score = fields.Integer("Appearance (1-10)", default=5)
    aroma_score = fields.Integer("Aroma (1-10)", default=5)
    flavor_score = fields.Integer("Flavor (1-10)", default=5)
    texture_score = fields.Integer("Texture (1-10)", default=5)
    sensory_notes = fields.Text("Sensory Notes")

    # US-038-09: 区块链存证指纹 (Blockchain Mock)
    blockchain_hash = fields.Char("Blockchain Hash", readonly=True)

    # US-038-11: LIMS 集成
    lims_source_data = fields.Text("LIMS Raw Data")
    lims_device_id = fields.Char("LIMS Device ID")

    # 盲样相关字段 [US-038-06] - 用于测试人员界面控制
    is_blind_view = fields.Boolean("Blind View", compute='_compute_blind_view', help="Whether the current user should see masked information")

    def _compute_blind_view(self):
        """ 计算当前用户是否应以盲样视图查看 [US-038-06] """
        for record in self:
            if (record.sample_id and record.sample_id.is_blind_test and
                record.sample_id.blind_tester_id and
                record.sample_id.blind_tester_id.id == self.env.uid):
                record.is_blind_view = True
            else:
                record.is_blind_view = False

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('agri.quality.check') or _('QC')
        return super().create(vals_list)

    def action_pass(self):
        self._generate_blockchain_hash()
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

    def _generate_blockchain_hash(self):
        """ US-038-09: Generate an immutable hash of the test result """
        self.ensure_one()
        data = {
            'ref': self.name,
            'lot': self.lot_id.name,
            'measure': self.measure,
            'state': 'pass',
            'user': self.user_id.name,
            'date': fields.Datetime.now().isoformat()
        }
        hash_str = hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()
        self.blockchain_hash = hash_str

    def action_check_ccp_violations(self):
        """ US-038-10: CCP Hard-Block check based on IoT/Task time """
        self.ensure_one()
        if self.task_id and self.task_id.actual_start_date and self.task_id.actual_end_date:
            duration = (self.task_id.actual_end_date - self.task_id.actual_start_date).total_seconds() / 60
            # Example: If pasteurization (杀菌) duration is less than 15 mins, fail
            if "pasteurize" in (self.task_id.name or "").lower() and duration < 15:
                self.message_post(body=_("CCP VIOLATION: Pasteurization time too short (%s mins).") % duration)
                self.action_fail()
                return False
        return True

class AgriQualityAlert(models.Model):
    _name = 'agri.quality.alert'
    _description = 'Agricultural Quality Alert'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Title", required=True)
    check_id = fields.Many2one('agri.quality.check', string="Source Check")
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

class StockPicking(models.Model):    _inherit = 'stock.picking'

    def button_validate(self):
        for picking in self:
            if picking.picking_type_code in ['outgoing', 'internal']:
                for move in picking.move_ids:
                    for lot in move.lot_ids:
                        if lot.quality_status == 'failed':
                            raise UserError(_("QUALITY ALERT: Lot %s has failed quality inspection.") % lot.name)
                        if lot.qc_release_state == 'locked':
                            raise UserError(_("QC LOCKED: Lot %s is pending release and cannot be moved.") % lot.name)
        return super().button_validate()

class AgriLotQuality(models.Model):    _inherit = 'stock.lot'

    quality_status = fields.Selection([
        ('none', 'Not Tested'),
        ('passed', 'Passed'),
        ('failed', 'Failed')
    ], string="Quality Status", default='none', tracking=True)

    qc_release_state = fields.Selection([
        ('locked', 'Locked'),
        ('released', 'Released'),
    ], string="QC Release Status", default='locked', tracking=True)

    quality_check_ids = fields.One2many('agri.quality.check', 'lot_id', string="Quality Checks")

    def action_qc_release(self):
        self.ensure_one()
        self.write({'qc_release_state': 'released'})

    def action_lock(self):
        self.ensure_one()
        self.write({'qc_release_state': 'locked'})