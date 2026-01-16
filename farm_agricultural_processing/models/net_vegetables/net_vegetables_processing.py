# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class FarmProcessingProductionNetVegetablesExtension(models.Model):
    """
    Extension to Processing ISL Production Model for Net Vegetables - US-14-08
    """
    _inherit = 'farm.processing.production'

    # Processing type and mode for agricultural processing
    processing_type = fields.Selection([
        ('primary', 'Primary (Sorting/Cleaning)'),
        ('deep', 'Deep (Transformation)'),
        ('packaging', 'Packaging Conversion')
    ], string='Processing Type', default='primary', required=True)

    process_mode = fields.Selection([
        ('standard', 'Standard'),
        ('baking', 'Baking'),
        ('fermentation', 'Fermentation'),
        ('sterilization', 'Sterilization')
    ], string="Process Mode", default='standard')

    # Industry parameter fields [US-16-02]
    vintage_year = fields.Integer("Vintage")
    alcohol_content = fields.Float("Alcohol %")
    brix_level = fields.Float("Brix")
    ph_level = fields.Float("pH Level")
    baking_temp = fields.Float("Baking Temp (℃)")
    proofing_time = fields.Float("Proofing Duration (Min)")
    process_temperature = fields.Float("Process Temperature (℃)")

    # Quality control fields [US-15-01]
    moisture_content = fields.Float("Moisture Content (%)")
    is_haccp_compliant = fields.Boolean("HACCP Checked", default=False)

    # Traceability fields [US-14-03]
    harvest_lot_ids = fields.Many2many('stock.lot', 'production_harvest_lot_rel', 'production_id', 'lot_id', string='Source Harvest Lots')
    additive_lot_ids = fields.Many2many('stock.lot', 'production_additive_lot_rel', 'production_id', 'lot_id', string="Additives/Ingredients Lots")

    # Consumption tracking for energy/water [US-14-04 & US-14-13]
    water_meter_start = fields.Float('Water Meter Start')
    water_meter_end = fields.Float('Water Meter End')
    water_consumption = fields.Float('Water Consumed', compute='_compute_consumption', store=True)

    electricity_meter_start = fields.Float('Electricity Meter Start')
    electricity_meter_end = fields.Float('Electricity Meter End')
    electricity_consumption = fields.Float('Electricity Consumed', compute='_compute_consumption', store=True)
    total_energy_cost = fields.Float("Total Energy Cost", compute='_compute_total_energy_cost', store=True)

    # Net vegetable specific fields extending the existing ISL model
    net_vegetable_batch_no = fields.Char('Net Vegetable Batch No.', default=lambda self: self._default_net_vegetable_batch())
    raw_material_lot_id = fields.Many2one('stock.lot', string='Raw Material Lot')
    raw_material_qty = fields.Float('Raw Material Input (kg)')
    quality_grade = fields.Selection([
        ('a', 'Grade A'),
        ('b', 'Grade B'),
        ('c', 'Grade C'),
        ('reject', 'Rejected'),
    ], string='Final Quality Grade')

    # Processing specific
    final_output_qty = fields.Float('Final Output (kg)')
    total_loss_qty = fields.Float('Total Loss (kg)')
    yield_rate = fields.Float('Yield Rate (%)')

    # Loss tracking for mass balance [US-04-02, US-14-06]
    scrap_qty = fields.Float("Process Loss (kg)", help="Physical waste/scraps recorded during process.")
    loss_rate = fields.Float("Loss Rate (%)", compute='_compute_total_output_qty', store=True)
    total_output_qty = fields.Float("Total Output Qty", compute='_compute_total_output_qty', store=True)
    is_balanced = fields.Boolean("Mass Balanced", compute='_compute_total_output_qty', store=True)

    state = fields.Selection(selection_add=[
        ('draft', 'Draft'),
        ('processing', 'Processing'),
        ('done', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], string='State')

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
            # Inherit target parameters
            if hasattr(self.bom_id, 'target_temp'):
                self.process_temperature = self.bom_id.target_temp
                self.baking_temp = self.bom_id.target_temp
            if hasattr(self.bom_id, 'target_brix'):
                self.brix_level = self.bom_id.target_brix

    def button_mark_done(self):
        """ Quality checks and balance verification [US-04-02, US-14-03, US-14-16, US-14-19] """
        for mo in self:
            # 1. Mass balance verification [US-14-06]
            if not mo.is_balanced:
                from odoo.exceptions import UserError
                raise UserError(_("MASS BALANCE ERROR: Total input (%s) does not match total output + loss (%s).") % (
                    sum(mo.move_raw_ids.mapped('product_uom_qty')), mo.total_output_qty
                ))

            # 2. Loss tolerance hard blocking [US-14-16] (Core-Closure)
            if (hasattr(mo.bom_id, 'max_loss_rate') and mo.bom_id and
                mo.bom_id.max_loss_rate and mo.loss_rate > mo.bom_id.max_loss_rate):
                # Create exception handling Activity [Workflow] - quality supervisor approval
                quality_user = self.env.ref('farm_core.group_quality_supervisor').users[:1] if self.env.ref('farm_core.group_quality_supervisor', False) else self.env.user
                mo.activity_schedule(
                    'mail.mail_activity_data_todo',
                    summary=_('HARD-BLOCK: Loss Rate Exceeded [%s%% > %s%%] for %s') % (mo.loss_rate, mo.bom_id.max_loss_rate, mo.name),
                    note=_('Process loss rate exceeds the maximum allowable rate set in the BOM (%s%%).\n'
                           'Current loss rate: %s%%.\n'
                           'This MO cannot be completed until a quality supervisor reviews and authorizes an exception or corrective action.') % (mo.bom_id.max_loss_rate, mo.loss_rate),
                    user_id=quality_user.id if quality_user else mo.user_id.id
                )
                from odoo.exceptions import ValidationError
                raise ValidationError(_(
                    "CORE-CLOSURE: Loss rate hard blocking activated.\n"
                    "Actual loss rate was %s%%, which exceeds the maximum allowable rate of %s%%.\n"
                    "An exception handling task has been automatically created for the quality supervisor."
                ) % (mo.loss_rate, mo.bom_id.max_loss_rate))

            # 3. Critical process quality hard blocking [US-14-19] (Core-Closure)
            if mo.process_mode == 'fermentation' and (mo.ph_level < 3.0 or mo.ph_level > 4.5):
                # Create exception handling Activity [Workflow]
                mo.activity_schedule(
                    'mail.mail_activity_data_todo',
                    summary=_('Quality Block: Fermentation pH Abnormal [%s]') % mo.ph_level,
                    note=_('Fermentation pH value is outside the safety range. Please assign a technician to execute the [Exception Handling] process or manually authorize scrapping.'),
                    user_id=mo.user_id.id
                )
                from odoo.exceptions import ValidationError
                raise ValidationError(_(
                    "CORE-CLOSURE: Critical Quality Interception.\n"
                    "Current fermentation pH value is %s, which is outside the safety range (3.0 - 4.5).\n"
                    "An exception handling todo has been automatically created for the workshop supervisor."
                ) % mo.ph_level)

            if mo.process_mode == 'sterilization' and mo.process_temperature < 121.0:
                # Create exception handling Activity [Workflow]
                mo.activity_schedule(
                    'mail.mail_activity_data_todo',
                    summary=_('Quality Block: Sterilization Temp Below Standard [%s℃]') % mo.process_temperature,
                    note=_('The sterilization temperature for this batch did not reach 121.0℃. Direct entry to inventory is strictly prohibited; please execute re-sterilization or downgrading process.'),
                    user_id=mo.user_id.id
                )
                from odoo.exceptions import ValidationError
                raise ValidationError(_(
                    "CORE-CLOSURE: Sterilization temperature non-compliant.\n"
                    "Actual sterilization temperature was %s℃, failing to meet the process requirement of 121.0℃.\n"
                    "Risk detected for this batch; exception handling todo created."
                ) % mo.process_temperature)

            # 4. Establish traceability links
            raw_lots = mo.move_raw_ids.mapped('move_line_ids.lot_id') | mo.harvest_lot_ids
            if raw_lots:
                main_raw_lot = raw_lots[0]
                # Calculate full path: current upstream path + this batch ID
                upstream_path = main_raw_lot.full_traceability_path or ""
                new_path = f"{upstream_path}/{main_raw_lot.id}" if upstream_path else str(main_raw_lot.id)

                for finished_move in mo.move_finished_ids:
                    for finished_lot in finished_move.move_line_ids.lot_id:
                        finished_lot.write({
                            'parent_lot_id': main_raw_lot.id,
                            'full_traceability_path': new_path
                        })

        # Call parent method at the end
        return super().button_mark_done()

    @api.model
    def _default_net_vegetable_batch(self):
        return 'NETVEG/' + fields.Date.to_string(fields.Date.today()) + '/' + str(self.id or 0)


class FarmProcessingBomNetVegetablesExtension(models.Model):
    """
    Extension to Processing ISL BOM Model for Net Vegetables - US-14-08
    """
    _inherit = 'farm.processing.bom'

    # Processing steps for net vegetables
    processing_steps = fields.One2many('farm.processing.step', 'processing_bom_id', string='Processing Steps')


class FarmProcessingStepNetVegetables(models.Model):
    """
    Processing Step for Net Vegetables - US-14-08
    """
    _name = 'farm.processing.step'
    _description = 'Net Vegetable Processing Step'
    _order = 'sequence'

    processing_bom_id = fields.Many2one('farm.processing.bom', string='Processing BOM', ondelete='cascade')
    sequence = fields.Integer('Sequence', default=10)
    step_name = fields.Char('Step Name', required=True)
    step_type = fields.Selection([
        ('washing', 'Washing'),
        ('cutting', 'Cutting'),
        ('sterilization', 'Sterilization'),
        ('packaging', 'Packaging'),
        ('quality_check', 'Quality Check'),
    ], string='Step Type', required=True)

    # Input/output tracking
    input_qty = fields.Float('Input Quantity (kg)')
    output_qty = fields.Float('Output Quantity (kg)')
    loss_qty = fields.Float('Loss Quantity (kg)')

    # IoT device integration
    iot_device_id = fields.Many2one('farm.iot.device', string='IoT Device')
    temperature = fields.Float('Temperature (°C)')
    humidity = fields.Float('Humidity (%)')
    processing_time = fields.Float('Processing Duration (min)')

    # Quality parameters
    ph_level = fields.Float('pH Level')
    quality_notes = fields.Text('Quality Notes')

    completion_date = fields.Datetime('Completion Date')
    completed_by = fields.Many2one('res.users', string='Completed By')

    @api.onchange('input_qty', 'output_qty')
    def _onchange_qty(self):
        if self.input_qty and self.output_qty:
            self.loss_qty = max(0, self.input_qty - self.output_qty)