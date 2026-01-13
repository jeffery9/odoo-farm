from odoo import models, fields, api, _
from odoo.exceptions import UserError

class AgriIntervention(models.Model):
    _inherit = 'mrp.production'
    _description = 'Agricultural Intervention (农事干预/作业)'

    agri_task_id = fields.Many2one(
        'project.task', 
        string="Production Task",
        help="The specific production task this intervention belongs to."
    )
    
    # 农业特有的作业分类 [核心字段 - 已恢复]
    intervention_type = fields.Selection([
        ('tillage', 'Soil Preparation (耕作)'),
        ('sowing', 'Sowing/Planting (播种/移栽)'),
        ('fertilizing', 'Fertilizing (施肥)'),
        ('irrigation', 'Irrigation (灌溉)'),
        ('protection', 'Crop Protection (植保)'),
        ('harvesting', 'Harvesting (收获)'),
        ('feeding', 'Feeding (饲喂)'),
        ('medical', 'Medical/Prevention (医疗/防疫)'),
    ], string="Intervention Type")

    # Ekylibre Mapping: Intervention Parameters [US-Mapping]
    doer_ids = fields.Many2many('hr.employee', string="Doers/Workers")
    tool_ids = fields.Many2many('maintenance.equipment', string="Tools/Machinery")
    
    procedure_name = fields.Char("Procedure/Method", help="e.g. Mechanical sowing, manual weeding")

    # Harvest Grading [US-02-04]
    grade_a_qty = fields.Float("Grade A Quantity")
    grade_b_qty = fields.Float("Grade B Quantity")
    grade_c_qty = fields.Float("Grade C Quantity")

    @api.constrains('grade_a_qty', 'grade_b_qty', 'grade_c_qty')
    def _check_graded_quantities(self):
        for intervention in self:
            if intervention.intervention_type == 'harvesting' and (intervention.grade_a_qty < 0 or intervention.grade_b_qty < 0 or intervention.grade_c_qty < 0):
                raise UserError(_("Graded quantities cannot be negative."))

    # Ekylibre Mapping: Costing [US-Mapping]
    input_cost = fields.Float("Input Cost", compute='_compute_agri_costs', store=True)
    tool_cost = fields.Float("Tool/Machinery Cost", compute='_compute_agri_costs', store=True)
    doer_cost = fields.Float("Labor Cost", compute='_compute_agri_costs', store=True)
    total_agri_cost = fields.Float("Total Intervention Cost", compute='_compute_agri_costs', store=True)

    # US-02-03: Soil Nutrient Inputs
    pure_n_qty = fields.Float("Pure Nitrogen (N) kg", compute='_compute_agri_costs', store=True)
    pure_p_qty = fields.Float("Pure Phosphorus (P) kg", compute='_compute_agri_costs', store=True)
    pure_k_qty = fields.Float("Pure Potassium (K) kg", compute='_compute_agri_costs', store=True)

    @api.depends('move_raw_ids.state', 'move_raw_ids.product_uom_qty', 'workorder_ids.duration')
    def _compute_agri_costs(self):
        for mo in self:
            # 1. 投入品成本与养分计算
            inputs = 0.0
            n_total = p_total = k_total = 0.0
            for move in mo.move_raw_ids:
                inputs += move.product_uom_qty * move.product_id.standard_price
                # 计算养分 (假设 UOM 是 kg)
                n_total += move.product_uom_qty * (move.product_id.n_content / 100.0)
                p_total += move.product_uom_qty * (move.product_id.p_content / 100.0)
                k_total += move.product_uom_qty * (move.product_id.k_content / 100.0)
            
            # 2. 劳动力成本 (基于工单或工时)
            labor = sum(mo.workorder_ids.mapped('duration')) / 60.0 * 50.0 # 假设 50/小时
            
            # 3. 工具成本 (示例：基于工单中的工作中心费率)
            tools = sum(mo.workorder_ids.mapped(lambda w: w.duration / 60.0 * w.workcenter_id.costs_hour))
            
            mo.input_cost = inputs
            mo.doer_cost = labor
            mo.tool_cost = tools
            mo.total_agri_cost = inputs + labor + tools
            mo.pure_n_qty = n_total
            mo.pure_p_qty = p_total
            mo.pure_k_qty = k_total

    # 工时追踪 [US-13-03]
    work_start_datetime = fields.Datetime("Work Start")
    is_working = fields.Boolean("In Progress", default=False)

    def action_start_work(self):
        """ 一键打卡：开始作业 """
        self.ensure_one()
        self.write({
            'work_start_datetime': fields.Datetime.now(),
            'is_working': True
        })
        self.message_post(body=_("Labor: Work started at %s") % self.work_start_datetime)

    def action_stop_work(self):
        """ 一键打卡：停止作业并自动创建工时记录 """
        self.ensure_one()
        if not self.work_start_datetime:
            return
            
        now = fields.Datetime.now()
        if hasattr(self.env['farm.worklog'], 'create'):
            employee = self.env.user.employee_id
            self.env['farm.worklog'].create({
                'employee_id': employee.id if employee else False,
                'task_id': self.agri_task_id.id,
                'date': fields.Date.today(),
                'work_type': self.intervention_type or 'harvesting',
                'quantity': 1.0, 
                'notes': _('Auto-recorded from intervention %s') % self.name
            })
            
        self.write({
            'is_working': False,
            'work_start_datetime': False
        })
        self.message_post(body=_("Labor: Work stopped and recorded at %s") % now)

    def action_confirm(self):
        """ 扩展确认逻辑，进行安全拦截 [US-03-04] 并传递任务 ID 到供应端 [US-03-02] """
        for mo in self:
            # 1. 检查有机拦截
            is_organic_parcel = mo.agri_task_id.land_parcel_id.certification_level in ['organic', 'organic_transition']
            for move in mo.move_raw_ids:
                if move.product_id.is_agri_input and not move.product_id.is_safety_approved:
                    if is_organic_parcel:
                        # 如果是有机地块，记录违规日期以重置转换期 [US-12-02]
                        mo.agri_task_id.land_parcel_id.last_prohibited_substance_date = fields.Date.today()
                        # 发出警告而非强制报错（取决于农场策略），这里选择报错以严格合规
                        raise UserError(_("COMPLIANCE ERROR: Product %s is not approved for organic production on parcel %s!") % (
                            move.product_id.name, mo.agri_task_id.land_parcel_id.name
                        ))
            
            # 2. 传递 agri_task_id 到采购逻辑 (通过 procurement_group)
            if mo.agri_task_id and mo.procurement_group_id:
                mo.procurement_group_id.agri_task_id = mo.agri_task_id.id

            # 3. 触发休药期更新 (调用 farm_safety 注入的方法)
            if hasattr(mo.agri_task_id, 'action_confirm_intervention_safety'):
                mo.agri_task_id.action_confirm_intervention_safety(mo.move_raw_ids.mapped('product_id').ids)
                
        return super(AgriIntervention, self).action_confirm()

    def button_mark_done(self):
        """ Extend the done logic to handle graded harvesting outputs and trigger quality check [US-05-02]. """
        for intervention in self:
            if intervention.intervention_type == 'harvesting':
                # Handle graded quantities logic
                total_graded_qty = intervention.grade_a_qty + intervention.grade_b_qty + intervention.grade_c_qty
                
                if total_graded_qty > 0:
                    # Logic to create separate stock moves and lots for each grade
                    finished_product = intervention.product_id
                    
                    def _create_graded_move_and_lot(grade_type, qty):
                        if qty <= 0:
                            return None
                        
                        # Create a new lot with the specified grade
                        graded_lot = self.env['stock.lot'].create({
                            'product_id': finished_product.id,
                            'name': finished_product.name + '/' + grade_type.upper() + '/' + (self.env['ir.sequence'].next_by_code('stock.lot') or _('New')),
                            'quality_grade': grade_type,
                        })
                        
                        # Create a stock move for this graded quantity
                        move = self.env['stock.move'].create({
                            'name': _('Harvest Output (%s)') % grade_type.upper(),
                            'product_id': finished_product.id,
                            'product_uom_qty': qty,
                            'product_uom': finished_product.uom_id.id,
                            'location_id': intervention.location_src_id.id, # Production location
                            'location_dest_id': intervention.location_dest_id.id, # Destination (stock) location
                            'production_id': intervention.id,
                            'lot_ids': [(6, 0, [graded_lot.id])],
                            'state': 'done', # Mark as done directly
                        })
                        move._action_done() # Finalize the move
                        return graded_lot.id
                        
                    graded_lot_ids = []
                    graded_lot_ids.append(_create_graded_move_and_lot('grade_a', intervention.grade_a_qty))
                    graded_lot_ids.append(_create_graded_move_and_lot('grade_b', intervention.grade_b_qty))
                    graded_lot_ids.append(_create_graded_move_and_lot('grade_c', intervention.grade_c_qty))
                    
                    graded_lot_ids = [lot_id for lot_id in graded_lot_ids if lot_id]

                    # US-05-02: Trigger quality check for custom created graded lots
                    if graded_lot_ids:
                        for lot_id in graded_lot_ids:
                            try:
                                self.env['farm.quality.check'].create({
                                    'lot_id': lot_id,
                                    'task_id': intervention.agri_task_id.id,
                                    'name': _('Harvest QC: %s for Grade %s') % (intervention.name, self.env['stock.lot'].browse(lot_id).quality_grade.upper()),
                                })
                            except Exception:
                                pass

                    # Prevent base MRP from creating duplicate finished moves
                    # by setting product_qty to 0 for the super call if custom moves are created
                    intervention.product_qty = 0

            # US-05-02: Trigger quality check for non-graded harvesting
            elif intervention.intervention_type == 'harvesting' and intervention.product_qty > 0:
                try:
                    lot_ids = intervention.move_finished_ids.mapped('lot_ids')
                    self.env['farm.quality.check'].create({
                        'lot_id': lot_ids[:1].id if lot_ids else False,
                        'task_id': intervention.agri_task_id.id,
                        'name': _('Harvest QC: %s') % intervention.name,
                    })
                except Exception:
                    pass 

        # Call super method to handle other MRP production logic (e.g., raw material consumption, state change)
        res = super(AgriIntervention, self).button_mark_done()
        return res

class ProcurementGroup(models.Model):
    _inherit = 'procurement.group'

    agri_task_id = fields.Many2one('project.task', string="Agri Task")