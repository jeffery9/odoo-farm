# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions
from odoo.tools.safe_eval import safe_eval
from datetime import timedelta
import logging

_logger = logging.getLogger(__name__)

# ==============================================================================
# EPIC-134: Dynamic Recipe Formulation (动态配方补偿引擎)
# ==============================================================================
class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    is_dynamic_formulation = fields.Boolean("Dynamic Formulation", default=False)
    dynamic_formula = fields.Char("Compensation Formula (Python AST)", help="e.g., base_qty + (12 - brix) * 0.5")
    min_qty = fields.Float("Min Limit Qty")
    max_qty = fields.Float("Max Limit Qty")

    @api.constrains('dynamic_formula', 'min_qty', 'max_qty')
    def _check_dynamic_formula_bounds(self):
        for line in self:
            if line.is_dynamic_formulation and line.dynamic_formula:
                if line.min_qty >= line.max_qty:
                    raise exceptions.ValidationError("Max Qty must be strictly greater than Min Qty for Dynamic Formulation bounds.")
                # Basic AST verification
                try:
                    dummy_dict = {'base_qty': 1.0, 'brix': 10.0, 'moisture': 50.0}
                    safe_eval(line.dynamic_formula, dummy_dict)
                except Exception as e:
                    raise exceptions.ValidationError(f"Invalid Formula Syntax: {e}")

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    def action_apply_dynamic_formula(self):
        """
        US-134-02: Triggered during production draft/confirmed state to dynamically adjust 
        excipient requirements based on main ingredient's lot properties.
        """
        for production in self:
            # Mock: Fetching properties from the primary raw material lot
            # In a real flow, this queries move_raw_ids.lot_id.lot_properties
            mock_brix = 9.0 
            
            for move in production.move_raw_ids:
                if move.bom_line_id and move.bom_line_id.is_dynamic_formulation and move.bom_line_id.dynamic_formula:
                    try:
                        localdict = {
                            'base_qty': move.bom_line_id.product_qty,
                            'brix': mock_brix
                        }
                        raw_calc = safe_eval(move.bom_line_id.dynamic_formula, localdict)
                        # Apply Min/Max boundaries
                        new_qty = max(move.bom_line_id.min_qty, min(raw_calc, move.bom_line_id.max_qty))
                        
                        # Update consumption requirement
                        move.product_uom_qty = new_qty
                        
                        # Log Traceability Snapshot (US-134-03)
                        production.message_post(body=f"🧪 Dynamic Formulation Applied to {move.product_id.name}: <br/>"
                                                     f"Standard: {move.bom_line_id.product_qty} -> Adjusted: {new_qty} <br/>"
                                                     f"Reason: Brix offset detected ({mock_brix}%).")
                    except Exception as e:
                        _logger.error(f"Dynamic formula calculation failed: {e}")

# ==============================================================================
# EPIC-135: Toll Manufacturing Trust (委外加工信任与物料平衡)
# ==============================================================================
class MrpBom(models.Model):
    _inherit = 'mrp.bom'
    
    min_yield_tolerance_pct = fields.Float("Min Yield Tolerance (%)", default=0.0, help="Used for Subcontracting Mass Balance.")

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        """
        US-135-01: Intercept incoming shipments to check Toll Manufacturing Mass Balance.
        """
        for picking in self:
            if picking.picking_type_id.code == 'incoming':
                for move in picking.move_ids:
                    # Check if this is a subcontracting receipt (Odoo Native or ISL)
                    if hasattr(move, 'is_subcontract') and move.is_subcontract and move.bom_id:
                        bom = move.bom_id
                        if bom.min_yield_tolerance_pct > 0:
                            # Simplified Mass Balance Logic
                            # In reality, this requires looking up the corresponding raw material output picking
                            produced_qty = move.quantity
                            consumed_qty = 1000.0 # Mocked raw material sent
                            if consumed_qty > 0:
                                actual_yield = (produced_qty / consumed_qty) * 100
                                if actual_yield < bom.min_yield_tolerance_pct:
                                    raise exceptions.ValidationError(
                                        f"🚨 Mass Balance Anomaly (US-135-01):\n"
                                        f"Toll Manufacturer yielded {actual_yield:.1f}% (Below {bom.min_yield_tolerance_pct}% tolerance).\n"
                                        f"Validation blocked to prevent material theft."
                                    )
        return super(StockPicking, self).button_validate()

# ==============================================================================
# EPIC-136 & 137: WIP Shelf-Life & Granular Carbon Allocation
# ==============================================================================
class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    # EPIC-136
    wip_exposure_hours = fields.Float("WIP Exposure Duration (h)")
    avg_env_temperature = fields.Float("Avg Workcenter Temperature (°C)")
    wip_exposure_status = fields.Selection([
        ('normal', 'Normal'),
        ('orange', 'Threshold Alert (80%)'),
        ('red', 'Meltdown Warning (100%)')
    ], string="Exposure Status", compute='_compute_wip_exposure_status', store=True)

    @api.depends('wip_exposure_hours')
    def _compute_wip_exposure_status(self):
        for wo in self:
            threshold = 10.0 # Mock threshold for demo
            if wo.wip_exposure_hours >= threshold:
                wo.wip_exposure_status = 'red'
            elif wo.wip_exposure_hours >= threshold * 0.8:
                wo.wip_exposure_status = 'orange'
            else:
                wo.wip_exposure_status = 'normal'

    # EPIC-137
    power_consumption_kwh = fields.Float("Energy Consumption (kWh)")

    def button_finish(self):
        """
        Intercept workorder completion to inject Biological and ESG calculations.
        """
        res = super(MrpWorkorder, self).button_finish()
        for wo in self:
            # US-136-02: Dynamic Expiration Penalty
            if wo.wip_exposure_hours > 1.0 and wo.avg_env_temperature > 20.0:
                penalty_hours = (wo.wip_exposure_hours - 1.0) * 12 # Mock degradation formula
                
                # Apply actual penalty to the produced lot if available
                if wo.production_id.lot_producing_id:
                    lot = wo.production_id.lot_producing_id
                    if lot.expiration_date:
                        lot.expiration_date -= timedelta(hours=penalty_hours)
                
                wo.production_id.message_post(
                    body=f"⚠️ <b>WIP Shelf-Life Penalty Applied</b><br/>"
                         f"WIP exposed for {wo.wip_exposure_hours}h at {wo.avg_env_temperature}°C.<br/>"
                         f"Final lot expiration date reduced by {penalty_hours} hours."
                )

            # US-137-02 & 03: Granular Carbon & Cost Allocation
            if wo.power_consumption_kwh > 0:
                grid_emission_factor = 0.5  # kg CO2e / kWh
                carbon_kg = wo.power_consumption_kwh * grid_emission_factor
                electricity_rate = 0.15 # $0.15 / kWh
                financial_cost = wo.power_consumption_kwh * electricity_rate
                
                # Create Stock Valuation Layer for the cost (US-137-02)
                if wo.production_id.move_finished_ids:
                    move = wo.production_id.move_finished_ids[0]
                    self.env['stock.valuation.layer'].create({
                        'value': financial_cost,
                        'unit_cost': 0,
                        'quantity': 0,
                        'remaining_qty': 0,
                        'stock_move_id': move.id,
                        'description': f"Energy Cost Allocation: {wo.power_consumption_kwh} kWh for {wo.name}",
                        'product_id': move.product_id.id,
                        'company_id': wo.company_id.id,
                    })

                wo.production_id.message_post(
                    body=f"🌱 <b>ESG & Cost Allocation (Scope 2)</b><br/>"
                         f"Metered Energy: {wo.power_consumption_kwh} kWh<br/>"
                         f"Allocated Cost: ${financial_cost:.2f}<br/>"
                         f"Carbon Footprint: {carbon_kg} kg CO2e."
                )
                
                # Interface with Agri Carbon Ledger if available
                if 'agri.carbon.ledger' in self.env:
                    factor = self.env['agri.carbon.factor'].search([('name', 'ilike', 'Electricity')], limit=1)
                    if not factor:
                        factor = self.env['agri.carbon.factor'].create({
                            'name': 'Electricity (Grid)',
                            'category': 'energy',
                            'emission_factor': grid_emission_factor,
                            'uom_id': self.env.ref('uom.product_uom_unit').id # Mock UoM
                        })
                    
                    self.env['agri.carbon.ledger'].create({
                        'name': f'Scope 2 Emissions from {wo.name}',
                        'factor_id': factor.id,
                        'quantity': wo.power_consumption_kwh,
                        'lot_id': wo.production_id.lot_producing_id.id if wo.production_id.lot_producing_id else False
                    })
        return res
