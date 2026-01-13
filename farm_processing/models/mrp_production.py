from odoo import models, fields, api, _

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    # US-14-01 & US-14-02: 农业加工类型与模式
    processing_type = fields.Selection([
        ('primary', 'Primary (Sorting/Cleaning)'),
        ('deep', 'Deep (Transformation)'),
        ('packaging', 'Packaging Conversion')
    ], string='Processing Type', default='primary', required=True)

    process_mode = fields.Selection([
        ('standard', 'Standard'),
        ('baking', 'Baking (烘焙)'),
        ('fermentation', 'Fermentation (发酵/酿造)'),
        ('sterilization', 'Sterilization (杀菌/灌装)')
    ], string="Process Mode", default='standard')

    # 行业化参数 [US-16-02]
    vintage_year = fields.Integer("Vintage (年份)")
    alcohol_content = fields.Float("Alcohol %")
    brix_level = fields.Float("Brix (糖度)")
    ph_level = fields.Float("pH Level")
    baking_temp = fields.Float("Baking Temp (℃)")
    proofing_time = fields.Float("Proofing Duration (Min)")
    process_temperature = fields.Float("Process Temperature (℃)")
    
    # 质量控制 [US-15-01]
    moisture_content = fields.Float("Moisture Content (%)")
    is_haccp_compliant = fields.Boolean("HACCP Checked", default=False)

    # 溯源 [US-14-03]
    harvest_lot_ids = fields.Many2many('stock.lot', 'mrp_production_harvest_lot_rel', string='Source Harvest Lots')
    additive_lot_ids = fields.Many2many('stock.lot', 'mrp_production_additive_lot_rel', string="Additives/Ingredients Lots")

    # 能耗与成本 [US-14-04 & US-14-13]
    water_meter_start = fields.Float('Water Meter Start')
    water_meter_end = fields.Float('Water Meter End')
    water_consumption = fields.Float('Water Consumed', compute='_compute_consumption', store=True)
    
    electricity_meter_start = fields.Float('Electricity Meter Start')
    electricity_meter_end = fields.Float('Electricity Meter End')
    electricity_consumption = fields.Float('Electricity Consumed', compute='_compute_consumption', store=True)

    total_energy_cost = fields.Float("Total Energy Cost", compute='_compute_total_energy_cost', store=True)

    # 损耗与物料平衡 [US-04-02, US-14-06]
    scrap_qty = fields.Float("Process Loss (kg)", help="Physical waste/scraps recorded during process.")
    loss_rate = fields.Float("Loss Rate (%)", compute='_compute_total_output_qty', store=True)
    total_output_qty = fields.Float("Total Output Qty", compute='_compute_total_output_qty', store=True)
    is_balanced = fields.Boolean("Mass Balanced", compute='_compute_total_output_qty', store=True)

    @api.depends('water_meter_start', 'water_meter_end', 'electricity_meter_start', 'electricity_meter_end')
    def _compute_consumption(self):
        for reg in self:
            reg.water_consumption = max(0, reg.water_meter_end - reg.water_meter_start)
            reg.electricity_consumption = max(0, reg.electricity_meter_end - reg.electricity_meter_start)

    @api.depends('workorder_ids.actual_energy_consumption')
    def _compute_total_energy_cost(self):
        for mo in self:
            total = 0.0
            for wo in mo.workorder_ids:
                total += wo.actual_energy_consumption * wo.workcenter_id.energy_cost_per_hour
            mo.total_energy_cost = total

    @api.depends('move_finished_ids.product_uom_qty', 'scrap_qty', 'move_raw_ids.product_uom_qty')
    def _compute_total_output_qty(self):
        for mo in self:
            finished_and_byproducts_qty = sum(mo.move_finished_ids.mapped('product_uom_qty'))
            raw_qty = sum(mo.move_raw_ids.mapped('product_uom_qty'))
            
            mo.total_output_qty = finished_and_byproducts_qty + mo.scrap_qty
            mo.is_balanced = abs(mo.total_output_qty - raw_qty) < (raw_qty * 0.001) if raw_qty > 0 else True
            
            if raw_qty > 0:
                mo.loss_rate = (mo.scrap_qty / raw_qty) * 100.0
            else:
                mo.loss_rate = 0.0

    @api.onchange('bom_id')
    def _onchange_bom_id_farm(self):
        if self.bom_id:
            self.processing_type = getattr(self.bom_id, 'processing_type', 'primary')
            self.process_mode = getattr(self.bom_id, 'industry_type', 'standard')
            # 继承目标参数
            if hasattr(self.bom_id, 'target_temp'):
                self.process_temperature = self.bom_id.target_temp
                self.baking_temp = self.bom_id.target_temp
            if hasattr(self.bom_id, 'target_brix'):
                self.brix_level = self.bom_id.target_brix

    def button_mark_done(self):
        """ 强制平衡校验、关键质量拦截并建立批次溯源 [US-04-02, US-14-03, US-14-19] """
        for mo in self:
            # 1. 物料平衡校验 [US-14-06]
            if not mo.is_balanced:
                from odoo.exceptions import UserError
                raise UserError(_("MASS BALANCE ERROR: Total input (%s) does not match total output + loss (%s).") % (
                    sum(mo.move_raw_ids.mapped('product_uom_qty')), mo.total_output_qty
                ))
            
            # 2. 关键工艺质量硬拦截 [US-14-19] (Core-Closure)
            if mo.process_mode == 'fermentation' and (mo.ph_level < 3.0 or mo.ph_level > 4.5):
                from odoo.exceptions import ValidationError
                raise ValidationError(_(
                    "CORE-CLOSURE: 关键质量拦截 (熔断)。\n"
                    "当前发酵液 pH 值为 %s，超出了安全范围 (3.0 - 4.5)。\n"
                    "严禁将质量异常的半成品标记为完成，请执行【报废】或【异常处理】流程。"
                ) % mo.ph_level)

            if mo.process_mode == 'sterilization' and mo.process_temperature < 121.0:
                from odoo.exceptions import ValidationError
                raise ValidationError(_(
                    "CORE-CLOSURE: 杀菌温度不合规。\n"
                    "实际杀菌温度为 %s℃，未达到工艺要求的 121.0℃ 瞬时杀菌标准。\n"
                    "该批次存在微生物超标风险，严禁标记为完成。"
                ) % mo.process_temperature)

            # 3. 建立溯源关联
            raw_lots = mo.move_raw_ids.mapped('lot_ids') | mo.harvest_lot_ids
            if raw_lots:
                main_raw_lot = raw_lots[0]
                # 计算全路径：当前上游路径 + 本次批次 ID
                upstream_path = main_raw_lot.full_traceability_path or ""
                new_path = f"{upstream_path}/{main_raw_lot.id}" if upstream_path else str(main_raw_lot.id)
                
                for finished_move in mo.move_finished_ids:
                    for finished_lot in finished_move.lot_ids:
                        finished_lot.write({
                            'parent_lot_id': main_raw_lot.id,
                            'full_traceability_path': new_path
                        })
                        
        return super(MrpProduction, self).button_mark_done()
