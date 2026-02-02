# -*- coding: utf-8 -*-
# [US-78-05] [LOSSLESS] [ISA-88] Scientific VRA Core
from odoo import models, fields, api, _

class AgriInterventionVraStrategy(models.Model):
    """
    VRA Decision Strategy Standard [Refactored to Agri Domain]
    Enhanced with Physiological Growth-Stage Awareness.
    """
    _name = 'agri.intervention.vra.strategy'
    _description = 'VRA Decision Strategy'

    name = fields.Char("Strategy Name", required=True)
    type = fields.Selection([
        ('inverse_ndvi', 'Inverse NDVI (Growth-based)'),
        ('soil_replacement', 'Soil Nutrient Replacement'),
        ('fixed_step', 'Threshold Stepping'),
        ('biomass_deficit', 'Biomass Deficit Compensation'),
        ('mass_balance', 'Nutrient-Biomass Mass Balance')
    ], string="Logic Type", default='inverse_ndvi', required=True)

    # --- Scientific Enhancement ---
    is_stage_aware = fields.Boolean("Physiological Growth-Stage Aware", default=True,
                                   help="If enabled, the prescription will be adjusted based on the current GDD-based growth stage.")
    stage_rule_ids = fields.One2many('agri.vra.stage.rule', 'strategy_id', string="Stage Rules")

    # [US-78-06] Deficit Parameters
    deficit_sensitivity = fields.Float("Deficit Sensitivity", default=1.0, 
                                      help="How aggressively to compensate for biomass deficit. 1.0 means linear compensation.")

    # [US-78-08] Mass Balance Parameters
    target_yield = fields.Float("Target Yield (kg/mu)", default=800.0)
    nutrient_ratio = fields.Float("Nutrient Content Ratio", default=0.02, help="E.g. 0.02 for 2% Nitrogen content in dry matter")
    use_efficiency = fields.Float("Nutrient Use Efficiency (0-1)", default=0.5)

    # [US-78-11] Kinetics Parameters
    is_kinetics_aware = fields.Boolean("Nutrient Transformation Kinetics Aware", default=False,
                                      help="If enabled, the rate will be adjusted based on real-time soil environmental factors.")

    # [US-78-13] Cultivar Parameters
    is_cultivar_aware = fields.Boolean("Cultivar-Specific Response Aware", default=False,
                                      help="If enabled, the rate will be adjusted based on the variety's specific response curve (Mitscherlich).")

    # [US-78-10] RUE Parameters
    is_rue_aware = fields.Boolean("Spatial RUE Aware", default=False,
                                 help="If enabled, the rate will be adjusted based on the historical RUE of each grid cell.")

    # [US-78-12] LAI Parameters
    is_lai_aware = fields.Boolean("LAI Aware", default=False,
                                 help="If enabled, the rate will be adjusted based on the Leaf Area Index (LAI) of each grid cell.")

    # Parameters
    target_ndvi = fields.Float("Target NDVI", default=0.7)
    correction_slope = fields.Float("Correction Slope", default=0.5)
    
    low_threshold = fields.Float("Low NDVI Threshold", default=0.3)
    high_threshold = fields.Float("High NDVI Threshold", default=0.6)
    low_multiplier = fields.Float("Weak Area Multiplier", default=1.3)
    high_multiplier = fields.Float("Strong Area Multiplier", default=0.8)

class AgriVraStageRule(models.Model):
    """
    [US-78-05] Growth-Stage Sensitivity Weights.
    Defines how much to increase/decrease application rate based on physiological phase.
    """
    _name = 'agri.vra.stage.rule'
    _description = 'VRA Growth-Stage Rule'

    strategy_id = fields.Many2one('agri.intervention.vra.strategy', ondelete='cascade')
    stage_id = fields.Many2one('agri.growth.stage', string="Physiological Stage", required=True)
    intensity_multiplier = fields.Float("Intensity Multiplier", default=1.0, required=True,
                                       help="Coefficient to multiply the base rate. E.g., 1.5 for peak nutrient demand.")

class AgriInterventionVraPrescription(models.Model):
    """
    Variable Rate Prescription Standard [Refactored to Agri Domain]
    Enhanced with Biomass Deficit and Stage-Aware logic.
    """
    _name = 'agri.intervention.vra.prescription'
    _description = 'Variable Rate Prescription'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'agri.geospatial.mixin']

    name = fields.Char("Prescription Ref", required=True, copy=False, readonly=True, default=lambda self: _('New'))
    location_id = fields.Many2one('farm.location', string="Target Parcel", required=True, domain=[('is_land_parcel', '=', True)])
    product_id = fields.Many2one('product.template', string="Input Material", required=True)
    strategy_id = fields.Many2one('agri.intervention.vra.strategy', string="VRA Strategy", required=True)
    
    # [US-78-06] Link to the intervention for biological context
    intervention_id = fields.Many2one('mrp.production', string="Biological Context (Intervention)")
    actual_biomass = fields.Float("Actual Measured Biomass (g/m2)", help="Current actual biomass measurement for deficit calculation.")
    
    # [US-78-02] Weather Risk Parameters
    rain_probability = fields.Float("Rain Probability (%)", help="Forecasted rain probability for the next 24h")
    wind_speed = fields.Float("Wind Speed (m/s)", help="Forecasted wind speed at scheduled time")
    weather_risk_hedging = fields.Boolean("Enable Weather Risk Hedging", default=True)

    target_type = fields.Selection([
        ('fertilizer', 'Fertilizer'),
        ('seed', 'Seeding'),
        ('pesticide', 'Pesticide')
    ], string="Application Type", required=True)
    
    base_rate = fields.Float("Base Rate (kg/mu)", required=True, default=10.0)
    
    line_ids = fields.One2many('agri.intervention.vra.prescription.line', 'prescription_id', string="Prescription Grid")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('generated', 'Grid Generated'),
        ('exported', 'Sent to Machine'),
        ('executed', 'Completed')
    ], default='draft', tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('agri.intervention.vra.prescription') or _('VRA-NEW')
        return super(AgriInterventionVraPrescription, self).create(vals_list)

    def action_generate_prescription_map(self):
        """
        [US-78-05/06/07] Advanced Scientific VRA Engine.
        Integrates Spatial NDVI + Temporal Growth Stage + Stress Clipping.
        """
        for rec in self:
            if not rec.location_id.grid_cell_ids:
                rec.location_id.action_generate_precision_grid()
            
            rec.line_ids.unlink()
            lines = []
            strategy = rec.strategy_id
            
            # --- Get Physiological Context ---
            stage_multiplier = 1.0
            deficit_multiplier = 1.0
            cultivar_multiplier = 1.0
            stress_index = 0.0
            
            if rec.intervention_id:
                # 1. Determine current growth stage from intervention (US-78-05)
                if strategy.is_stage_aware:
                    current_stage = rec.intervention_id.current_growth_stage_id
                    rule = strategy.stage_rule_ids.filtered(lambda r: r.stage_id == current_stage)
                    if rule:
                        stage_multiplier = rule[0].intensity_multiplier
                
                # 2. [US-78-06] Calculate Biomass Deficit Multiplier
                if strategy.type == 'biomass_deficit' and rec.actual_biomass > 0:
                    # Theoretical W from Logistic Curve
                    theoretical_w = rec.intervention_id.get_logistic_biomass_prediction()
                    if theoretical_w > 0:
                        deficit_multiplier = 1.0 + ((theoretical_w - rec.actual_biomass) / theoretical_w) * strategy.deficit_sensitivity
                
                # 3. [US-78-13] Cultivar-Specific Response (Mitscherlich Law)
                if strategy.is_cultivar_aware and hasattr(rec.intervention_id, 'physiology_profile_id'):
                    prof = rec.intervention_id.physiology_profile_id
                    if prof and prof.response_efficiency_c:
                        # Logic: High efficiency varieties (high c) need less base push for the same response
                        # We normalize the multiplier against a standard efficiency of 0.003
                        cultivar_multiplier = 0.003 / prof.response_efficiency_c

                # 4. Get biological stress index for safety clipping (US-78-07)
                stress_index = getattr(rec.intervention_id, 'biological_stress_index', 0.0)

            for cell in rec.location_id.grid_cell_ids:
                rate = rec.base_rate
                
                # 5. Spatial/Basic Factor (Level 1)
                if strategy.type == 'inverse_ndvi':
                    rate = rec.base_rate * (1 + (strategy.target_ndvi - cell.ndvi_index) * strategy.correction_slope)
                elif strategy.type == 'soil_replacement':
                    ph_adjustment = 1.2 if cell.soil_ph < 5.5 else 1.0
                    rate = rec.base_rate * ph_adjustment
                elif strategy.type == 'fixed_step':
                    if cell.ndvi_index < strategy.low_threshold:
                        rate *= strategy.low_multiplier
                    elif cell.ndvi_index > strategy.high_threshold:
                        rate *= strategy.high_multiplier
                elif strategy.type == 'biomass_deficit':
                    rate *= deficit_multiplier
                elif strategy.type == 'mass_balance':
                    # Logic: Rate = (Target_Yield - Current_Biomass) * Nutrient_Ratio / Efficiency
                    current_w = rec.actual_biomass or 0.0
                    gap = strategy.target_yield - current_w
                    if gap > 0 and strategy.use_efficiency > 0:
                        rate = (gap * strategy.nutrient_ratio) / strategy.use_efficiency
                    else:
                        rate = 0.0

                # 6. Temporal & Cultivar Multipliers (Scientific Enhancement)
                rate *= (stage_multiplier * cultivar_multiplier)
                
                # 6.1 [US-78-10] Spatial RUE Compensation
                if strategy.is_rue_aware:
                    # Logic: Higher historical RUE allows higher investment
                    # Standard RUE is around 1.2 g/MJ
                    rue_factor = cell.historical_rue / 1.2
                    rate *= rue_factor
                
                # 6.2 [US-78-12] LAI-Driven Potential Calibration
                if strategy.is_lai_aware:
                    # Logic: Nutrient requirement scales with LAI (Photosynthetic potential)
                    # Simplified linear mapping with saturation at LAI=5.0
                    lai_factor = min(1.5, 0.5 + (cell.lai_index / 5.0))
                    rate *= lai_factor

                # 7. [US-78-11] Nutrient Transformation Kinetics (Spatial-Temporal Correction)
                if strategy.is_kinetics_aware:
                    # Logic: Actual_Rate = Target_Rate / Efficiency_Factor
                    ph_efficiency = max(0.6, min(1.0, 1.0 - abs(cell.soil_ph - 6.5) * 0.1))
                    moisture_efficiency = 1.0 - (cell.water_stress / 100.0) * 0.3
                    kinetics_factor = ph_efficiency * moisture_efficiency * 0.9
                    if kinetics_factor > 0:
                        rate = rate / kinetics_factor

                # 8. [US-78-07] Stress-based Safety Clipping
                if stress_index > 35.0:
                    max_allowed = rec.base_rate * 0.8
                    if rate > max_allowed:
                        rate = max_allowed

                # 9. [US-78-02] Weather Risk Hedging
                if rec.weather_risk_hedging:
                    # If high rain probability, reduce fertilizer to prevent runoff
                    if rec.target_type == 'fertilizer' and rec.rain_probability > 70.0:
                        rate *= 0.5 
                    
                    # If high wind, reduce pesticide to prevent drift
                    if rec.target_type == 'pesticide' and rec.wind_speed > 5.0:
                        rate *= 0.7

                lines.append((0, 0, {
                    'grid_cell_id': cell.id,
                    'target_rate': rate,
                    'uom_id': rec.product_id.uom_id.id
                }))
            
            rec.line_ids = lines
            rec.state = 'generated'
            rec.message_post(body=_("VRA Map generated. Stage Multiplier: %s, Deficit: %s, Cultivar: %s, Stress: %s") % 
                             (stage_multiplier, deficit_multiplier, cultivar_multiplier, stress_index))

                lines.append((0, 0, {
                    'grid_cell_id': cell.id,
                    'target_rate': rate,
                    'uom_id': rec.product_id.uom_id.id
                }))
            
            rec.line_ids = lines
            rec.state = 'generated'
            rec.message_post(body=_("VRA Map generated. Stage Multiplier: %s, Deficit Multiplier: %s, Stress Index: %s") % (stage_multiplier, deficit_multiplier, stress_index))

    def action_export_to_machinery(self):
        self.ensure_one()
        self.message_post(body=_("VRA ISO-XML Map Exported with Scientific Audit parameters."))
        self.state = 'exported'
        return True

class AgriInterventionVraPrescriptionLine(models.Model):
    _name = 'agri.intervention.vra.prescription.line'
    _description = 'VRA Grid Rate'

    prescription_id = fields.Many2one('agri.intervention.vra.prescription', ondelete='cascade')
    grid_cell_id = fields.Many2one('agri.geospatial.grid.cell', string="Grid Cell", required=True)
    target_rate = fields.Float("Target Rate", digits=(10, 3))
    uom_id = fields.Many2one('uom.uom', string="Unit")
    actual_rate = fields.Float("Actual Rate Applied", digits=(10, 3))
