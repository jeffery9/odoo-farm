from odoo import models, fields, api, _

class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    # 农业加工配方扩展 [US-14-02]
    industry_type = fields.Selection([
        ('standard', 'Standard'),
        ('baking', 'Baking (烘焙)'),
        ('winemaking', 'Winemaking (酿酒)'),
        ('food_processing', 'Food Processing (食品加工)')
    ], string="Industry Type", default='standard')

    expected_yield_rate = fields.Float("Expected Yield Rate (%)", default=100.0)
    process_description = fields.Text("Recipe/Process Description")
    
    # 预期等级分布
    grade_distribution_ids = fields.One2many('farm.bom.grade.distribution', 'bom_id', string="Expected Grade Distribution")

    # 行业目标参数 [Industry Targets]
    target_temp = fields.Float("Target Temperature (℃)")
    target_ph = fields.Float("Target pH")
    target_brix = fields.Float("Target Brix")
    target_proofing_time = fields.Float("Target Proofing Time (Min)")
    haccp_instructions = fields.Html("HACCP Critical Instructions")

class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    ingredient_role = fields.Selection([
        ('main', 'Main Material (主料)'),
        ('additive', 'Additive (添加剂)'),
        ('yeast', 'Fermentation Agent (发酵剂/菌种)'),
        ('packaging', 'Packaging (包材)')
    ], string="Ingredient Role", default='main')

class FarmBomGradeDistribution(models.Model):
    _name = 'farm.bom.grade.distribution'
    _description = 'Expected Grade Distribution in BOM'

    bom_id = fields.Many2one('mrp.bom', ondelete='cascade')
    quality_grade = fields.Selection([
        ('grade_a', 'Grade A (特级/优等)'),
        ('grade_b', 'Grade B (一级/合格)'),
        ('grade_c', 'Grade C (二级/次品)'),
    ], string="Quality Grade", required=True)
    expected_percentage = fields.Float("Expected %", required=True)

class MrpWorkcenter(models.Model):
    _inherit = 'mrp.workcenter'

    # 能耗核算基础 [US-14-04]
    energy_type = fields.Selection([
        ('electricity', 'Electricity (电)'),
        ('water', 'Water (水)'),
        ('gas', 'Gas (气/煤)'),
    ], string="Primary Energy Type")
    energy_cost_per_hour = fields.Float("Energy Cost per Hour")

class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    # 实际工序能耗记录 [US-14-04]
    actual_energy_consumption = fields.Float("Actual Energy Consumption")
    process_parameters = fields.Text("Process Parameters (e.g. Temperature, Pressure)")

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    # 汇总能耗成本 [US-14-04]
    total_energy_cost = fields.Float("Total Energy Cost", compute='_compute_total_energy_cost', store=True)

    @api.onchange('bom_id')
    def _onchange_bom_industry_targets(self):
        """ 从配方继承行业目标参数 """
        if self.bom_id:
            self.process_mode = self.bom_id.industry_type
            if self.bom_id.industry_type == 'baking':
                self.baking_temp = self.bom_id.target_temp
                self.proofing_time = self.bom_id.target_proofing_time
            elif self.bom_id.industry_type == 'winemaking':
                self.brix_level = self.bom_id.target_brix
                self.ph_level = self.bom_id.target_ph
            elif self.bom_id.industry_type == 'food_processing':
                self.process_temperature = self.bom_id.target_temp

    # 行业化参数 [Industry Specifics]
    process_mode = fields.Selection([
        ('standard', 'Standard'),
        ('baking', 'Baking (烘焙)'),
        ('fermentation', 'Fermentation (发酵/酿造)'),
        ('sterilization', 'Sterilization (杀菌/灌装)')
    ], string="Process Mode", default='standard')

    # 酿酒/酿造参数
    vintage_year = fields.Integer("Vintage (年份)")
    alcohol_content = fields.Float("Alcohol %")
    brix_level = fields.Float("Brix (糖度)")
    ph_level = fields.Float("pH Level")
    
    # 烘培参数
    baking_temp = fields.Float("Baking Temp (℃)")
    proofing_time = fields.Float("Proofing Duration (Min)")
    
    # 食品加工安全
    is_haccp_compliant = fields.Boolean("HACCP Checked", default=False)
    additive_lot_ids = fields.Many2many('stock.lot', string="Additives/Ingredients Lots")

    @api.depends('workorder_ids.actual_energy_consumption')
    def _compute_total_energy_cost(self):
        for mo in self:
            # 简化计算：工序能耗 * 工作中心单价 (实际可能更复杂)
            total = 0.0
            for wo in mo.workorder_ids:
                total += wo.actual_energy_consumption * wo.workcenter_id.energy_cost_per_hour
            mo.total_energy_cost = total

    # 加工能耗记录 [US-17-08]
    energy_meter_start = fields.Float("Energy Meter Start", help="Meter reading before processing")
    energy_meter_end = fields.Float("Energy Meter End", help="Meter reading after processing")
    energy_consumption = fields.Float("Energy Consumption", compute='_compute_energy_consumption', store=True)
    
    # 质量控制扩展
    moisture_content = fields.Float("Moisture Content (%)", help="Final moisture content for dried products")
    process_temperature = fields.Float("Process Temperature (℃)")
    
    # 损耗与平衡校验 [US-04-02]
    scrap_qty = fields.Float("Process Loss (kg)", help="Quantity lost during cleaning/sorting/processing")
    total_output_qty = fields.Float("Total Output Qty", compute='_compute_total_output_qty')
    is_balanced = fields.Boolean("Mass Balanced", compute='_compute_total_output_qty')

    @api.depends('move_finished_ids.product_uom_qty', 'scrap_qty', 'move_raw_ids.product_uom_qty')
    def _compute_total_output_qty(self):
        for mo in self:
            # 产出总量 = 成品 + 副产品 (By-products) + 损耗
            # Odoo 的 move_finished_ids 包含了主产品和所有副产品
            finished_and_byproducts_qty = sum(mo.move_finished_ids.mapped('product_uom_qty'))
            mo.total_output_qty = finished_and_byproducts_qty + mo.scrap_qty
            
            # 投入总量
            raw_qty = sum(mo.move_raw_ids.mapped('product_uom_qty'))
            # 允许 0.1% 的微小舍入误差
            mo.is_balanced = abs(mo.total_output_qty - raw_qty) < (raw_qty * 0.001) if raw_qty > 0 else True

    def button_mark_done(self):
        """ 强制平衡校验并建立批次溯源 [US-15-03] """
        for mo in self:
            if not mo.is_balanced:
                from odoo.exceptions import UserError
                raise UserError(_("MASS BALANCE ERROR: Total input (%s) does not match total output + loss (%s). Please adjust.") % (
                    sum(mo.move_raw_ids.mapped('product_uom_qty')), mo.total_output_qty
                ))
            
            # 建立溯源关联：将成品的批次关联到主要原料的批次
            raw_lots = mo.move_raw_ids.mapped('lot_ids')
            if raw_lots:
                main_raw_lot = raw_lots[0]
                for finished_move in mo.move_finished_ids:
                    for finished_lot in finished_move.lot_ids:
                        finished_lot.parent_lot_id = main_raw_lot.id
                        
        return super().button_mark_done()

class StockLot(models.Model):
    _inherit = 'stock.lot'

    # 批次溯源：指向原材料批次
    parent_lot_id = fields.Many2one('stock.lot', string="Parent Lot/Origin", help="Trace back to the raw material lot")
    child_lot_ids = fields.One2many('stock.lot', 'parent_lot_id', string="Derived Products")
