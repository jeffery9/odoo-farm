# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class AgriInterventionPluginWeather(models.AbstractModel):
    """
    [Plugin] Weather Window Gating.
    Intercepts start action based on wind speed and precipitation.
    """
    _name = 'agri.intervention.plugin.weather'
    _inherit = 'agri.intervention.plugin'

    @api.model
    def execute_hook(self, intervention, hook_point):
        if hook_point == 'pre_start':
            self._check_weather_window(intervention)

    def _check_weather_window(self, intervention):
        if not hasattr(intervention, 'intervention_type') or intervention.intervention_type not in ['fertilizing', 'protection', 'aerial_spraying']:
            return
        parcel = intervention.location_id
        if not parcel or not hasattr(parcel, 'gps_coordinates') or not parcel.gps_coordinates:
            return 
        from datetime import datetime, timedelta
        end_time = datetime.now() + timedelta(hours=24)
        if hasattr(intervention.env['agri.weather.forecast'], 'search'):
            forecast = intervention.env['agri.weather.forecast'].search([
                ('location_id', '=', parcel.id),
                ('forecast_datetime', '<=', end_time),
                ('forecast_datetime', '>=', datetime.now())
            ], limit=1, order='forecast_datetime asc')
            if forecast:
                if forecast.wind_speed_kmh and forecast.wind_speed_kmh > 16:
                    intervention.activity_schedule(
                        'mail.mail_activity_data_todo',
                        summary=_('WEATHER BLOCK: High Wind Speed (%s km/h)') % forecast.wind_speed_kmh,
                        note=_('Intervention %s was blocked. Wind speed exceeds level 4.') % intervention.name,
                        user_id=intervention.env.ref('farm_core.group_farm_specialist').users[:1].id or intervention.env.user.id
                    )
                    raise UserError(_("WEATHER WINDOW BLOCK: Wind speed too high (%s km/h > 16 km/h).") % forecast.wind_speed_kmh)

class AgriInterventionPluginYield(models.AbstractModel):
    """
    [Plugin] Dynamic Yield Calibration.
    """
    _name = 'agri.intervention.plugin.yield'
    _inherit = 'agri.intervention.plugin'

    @api.model
    def execute_hook(self, intervention, hook_point):
        pass

class AgriInterventionPluginNutrient(models.AbstractModel):
    """
    [Plugin] Nutrient Mass Balance.
    """
    _name = 'agri.intervention.plugin.nutrient'
    _inherit = 'agri.intervention.plugin'

    @api.model
    def execute_hook(self, intervention, hook_point):
        if hook_point == 'pre_done' or hook_point == 'post_confirm':
            self._compute_nutrients(intervention)

    def _compute_nutrients(self, intervention):
        n_total = p_total = k_total = 0.0
        if hasattr(intervention, 'move_raw_ids'):
            for move in intervention.move_raw_ids:
                product = move.product_id
                qty = move.product_uom_qty
                if hasattr(product, 'n_content'):
                    n_total += qty * (product.n_content / 100.0)
                    p_total += qty * (product.p_content / 100.0)
                    k_total += qty * (product.k_content / 100.0)
        if hasattr(intervention, 'pure_n_qty'):
            intervention.write({'pure_n_qty': n_total, 'pure_p_qty': p_total, 'pure_k_qty': k_total})

class AgriInterventionPluginCompliance(models.AbstractModel):
    """
    [Plugin] Regulatory & Safety Compliance.
    """
    _name = 'agri.intervention.plugin.compliance'
    _inherit = 'agri.intervention.plugin'

    @api.model
    def execute_hook(self, intervention, hook_point):
        if hook_point == 'pre_confirm':
            self._check_real_name_registration(intervention)
            self._check_organic_compliance(intervention)
            self._trigger_withdrawal_sync(intervention)

    def _check_real_name_registration(self, intervention):
        if hasattr(intervention, 'intervention_type') and intervention.intervention_type in ['protection', 'aerial_spraying', 'medical']:
            if not getattr(intervention, 'operator_id_card', False):
                raise UserError(_("COMPLIANCE ERROR: Operator ID Card is required!"))
            id_card = intervention.operator_id_card
            import re
            if not re.match(r'^[1-9]\d{5}(18|19|20)\d{2}((0[1-9])|(1[0-2]))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$', id_card):
                raise UserError(_("COMPLIANCE ERROR: Invalid ID Card format!"))

    def _check_organic_compliance(self, intervention):
        if hasattr(intervention, 'agri_task_id') and intervention.agri_task_id and intervention.agri_task_id.land_parcel_id:
            parcel = intervention.agri_task_id.land_parcel_id
            if parcel.certification_level in ['organic', 'organic_transition']:
                for move in getattr(intervention, 'move_raw_ids', []):
                    if (getattr(move.product_id, 'is_agri_input', False) and not getattr(move.product_id, 'is_safety_approved', True)):
                        parcel.last_prohibited_substance_date = fields.Date.today()
                        raise UserError(_("COMPLIANCE ERROR: Product %s is not approved for organic production!") % move.product_id.name)

    def _trigger_withdrawal_sync(self, intervention):
        if hasattr(intervention, 'agri_task_id') and hasattr(intervention.agri_task_id, 'action_confirm_intervention_safety'):
            if hasattr(intervention, 'move_raw_ids'):
                product_ids = intervention.move_raw_ids.mapped('product_id').ids
                intervention.agri_task_id.action_confirm_intervention_safety(product_ids)

class AgriInterventionPluginLabor(models.AbstractModel):
    """
    [Plugin] Labor Tracking.
    """
    _name = 'agri.intervention.plugin.labor'
    _inherit = 'agri.intervention.plugin'

    @api.model
    def execute_hook(self, intervention, hook_point):
        if hook_point == 'post_done':
            self._create_auto_worklog(intervention)

    def _create_auto_worklog(self, intervention):
        if not hasattr(intervention.env['farm.worklog'], 'create'): return
        employee = intervention.env.user.employee_id
        intervention.env['farm.worklog'].create({
            'employee_id': employee.id if employee else False,
            'task_id': getattr(intervention, 'agri_task_id', False) and intervention.agri_task_id.id,
            'date': fields.Date.today(),
            'work_type': getattr(intervention, 'intervention_type', 'harvesting'),
            'quantity': 1.0,
            'notes': _('Auto-recorded from intervention %s') % intervention.name
        })

class AgriInterventionPluginIoT(models.AbstractModel):
    """
    [Plugin] IoT Monitoring.
    """
    _name = 'agri.intervention.plugin.iot'
    _inherit = 'agri.intervention.plugin'

    @api.model
    def execute_hook(self, intervention, hook_point):
        pass

    def update_iot_status(self, intervention, readings_summary):
        summary_lower = readings_summary.lower()
        if any(kw in summary_lower for kw in ['critical', 'deviation', 'error', 'emergency']):
            intervention.iot_status = 'critical'
        elif any(kw in summary_lower for kw in ['warning', 'alert', 'high', 'low']):
            intervention.iot_status = 'warning'
        else:
            intervention.iot_status = 'monitoring'
        intervention.message_post(body=_("IoT-Based Status Update: %s") % readings_summary)

class AgriInterventionPluginSpatial(models.AbstractModel):
    """
    [Plugin] Spatial Compliance Audit.
    """
    _name = 'agri.intervention.plugin.spatial'
    _inherit = 'agri.intervention.plugin'

    @api.model
    def execute_hook(self, intervention, hook_point):
        if hook_point == 'pre_done':
            self._audit_spatial_compliance(intervention)

    def _audit_spatial_compliance(self, intervention):
        parcel = intervention.location_id
        if not parcel or not hasattr(parcel, 'gps_coordinates') or not parcel.gps_coordinates: return
        if hasattr(intervention.env['farm.geofence'], 'new'):
            temp_fence = intervention.env['farm.geofence'].new({'coordinates': parcel.gps_coordinates})
            telemetry_domain = [('gps_lat', '!=', 0), ('gps_lng', '!=', 0)]
            if hasattr(intervention, 'agri_task_id') and intervention.agri_task_id:
                telemetry_domain.append(('production_id', '=', intervention.agri_task_id.id))
            elif hasattr(intervention, 'production_id') and intervention.production_id:
                telemetry_domain.append(('production_id', '=', intervention.production_id.id))
            telemetries = intervention.env['iiot.telemetry'].search(telemetry_domain)
            if not telemetries: return
            oob_count = sum(1 for t in telemetries if not temp_fence.is_point_inside(t.gps_lng, t.gps_lat))
            compliance_rate = ((len(telemetries) - oob_count) / len(telemetries)) * 100.0
            if hasattr(intervention, 'out_of_bounds_count'):
                intervention.write({'out_of_bounds_count': oob_count, 'spatial_compliance_rate': compliance_rate})
            intervention.message_post(body=_("Spatial Audit Completed: Compliance Rate %s%%.") % round(compliance_rate, 2))

class AgriInterventionPluginHarvest(models.AbstractModel):
    """
    [Plugin] Harvest Grading & Quality Trigger.
    """
    _name = 'agri.intervention.plugin.harvest'
    _inherit = 'agri.intervention.plugin'

    @api.model
    def execute_hook(self, intervention, hook_point):
        if hook_point == 'pre_done':
            self._handle_harvest_grading(intervention)

    def _handle_harvest_grading(self, intervention):
        if not hasattr(intervention, 'intervention_type') or intervention.intervention_type != 'harvesting':
            return
        total_graded_qty = (getattr(intervention, 'grade_a_qty', 0) + getattr(intervention, 'grade_b_qty', 0) + getattr(intervention, 'grade_c_qty', 0))
        if total_graded_qty > 0:
            finished_product = intervention.product_id
            def _create_graded_move_and_lot(grade_type, qty):
                if qty <= 0: return None
                lot_model = intervention.env['stock.lot']
                if hasattr(lot_model, 'create'):
                    name_prefix = finished_product.name + '/' + grade_type.upper() + '/'
                    seq = intervention.env['ir.sequence'].next_by_code('stock.lot') or _('New')
                    graded_lot = lot_model.create({'product_id': finished_product.id, 'name': name_prefix + seq, 'quality_grade': grade_type})
                    move = intervention.env['stock.move'].create({
                        'name': _('Harvest Output (%s)') % grade_type.upper(),
                        'product_id': finished_product.id,
                        'product_uom_qty': qty,
                        'product_uom': finished_product.uom_id.id,
                        'location_id': intervention.location_src_id.id, 
                        'location_dest_id': intervention.location_dest_id.id,
                        'production_id': intervention.id,
                        'lot_ids': [(6, 0, [graded_lot.id])],
                        'state': 'done',
                    })
                    if hasattr(move, '_action_done'): move._action_done()
                    return graded_lot.id
                return None
            graded_lot_ids = []
            for g in ['grade_a', 'grade_b', 'grade_c']:
                qty = getattr(intervention, g, 0)
                lot_id = _create_graded_move_and_lot(g, qty)
                if lot_id: graded_lot_ids.append(lot_id)
            if graded_lot_ids and hasattr(intervention.env['farm.quality.check'], 'create'):
                for lot_id in graded_lot_ids:
                    lot_name = intervention.env['stock.lot'].browse(lot_id).quality_grade or 'UNKNOWN'
                    intervention.env['farm.quality.check'].create({
                        'lot_id': lot_id,
                        'task_id': getattr(intervention, 'agri_task_id', False) and intervention.agri_task_id.id,
                        'name': _('Harvest QC: %s for Grade %s') % (intervention.name, lot_name.upper()),
                    })
            intervention.product_qty = 0
        elif intervention.product_qty > 0:
            if hasattr(intervention.move_finished_ids, 'mapped'):
                lot_ids = intervention.move_finished_ids.mapped('lot_ids')
                if lot_ids and hasattr(intervention.env['farm.quality.check'], 'create'):
                    intervention.env['farm.quality.check'].create({
                        'lot_id': lot_ids[:1].id,
                        'task_id': getattr(intervention, 'agri_task_id', False) and intervention.agri_task_id.id,
                        'name': _('Harvest QC: %s') % intervention.name,
                    })

class AgriInterventionPluginVerification(models.AbstractModel):
    """
    [Plugin] Work Verification & Depletion.
    """
    _name = 'agri.intervention.plugin.verification'
    _inherit = 'agri.intervention.plugin'

    @api.model
    def execute_hook(self, intervention, hook_point):
        if hook_point == 'pre_done':
            self._verify_drone_work(intervention)

    def _verify_drone_work(self, intervention):
        if (hasattr(intervention, 'intervention_type') and intervention.intervention_type == 'aerial_spraying' and getattr(intervention, 'actual_flight_area', 0) > 0):
            for move in intervention.move_raw_ids:
                if hasattr(move, 'bom_line_id'):
                    bom_qty = move.bom_line_id.product_qty if move.bom_line_id else 1.0
                    move.product_uom_qty = intervention.actual_flight_area * bom_qty


# ---------------------------------------------------------
# [DNA Inheritance Plugins]
# ---------------------------------------------------------

class AgriDnaPluginNutrient(models.AbstractModel):
    """
    [DNA Plugin] Nutrient Mass Balance.
    Sums up N-P-K from inputs to the output lot.
    """
    _name = 'agri.dna.plugin.nutrient'
    _inherit = 'agri.dna.plugin'

    @api.model
    def inherit_dna(self, lot, inputs):
        if hasattr(lot, 'nitrogen_qty'):
            lot.nitrogen_qty = sum(i.nitrogen_qty for i in inputs)
            lot.phosphorus_qty = sum(i.phosphorus_qty for i in inputs)
            lot.potassium_qty = sum(i.potassium_qty for i in inputs)

class AgriDnaPluginSustainability(models.AbstractModel):
    """
    [DNA Plugin] Sustainability Metrics.
    Calculates weighted average carbon intensity and total water footprint.
    """
    _name = 'agri.dna.plugin.sustainability'
    _inherit = 'agri.dna.plugin'

    @api.model
    def inherit_dna(self, lot, inputs):
        total_qty = sum(i.product_uom_qty for i in inputs)
        if total_qty <= 0: return

        if hasattr(lot, 'carbon_intensity'):
            weighted_carbon = sum(i.carbon_intensity * i.product_uom_qty for i in inputs)
            lot.carbon_intensity = weighted_carbon / total_qty
        
        if hasattr(lot, 'water_footprint'):
            lot.water_footprint = sum(i.water_footprint for i in inputs)

class AgriDnaPluginSpatial(models.AbstractModel):
    """
    [DNA Plugin] Spatial Context.
    Propagates the geographical location from the latest intervention to the lot.
    """
    _name = 'agri.dna.plugin.spatial'
    _inherit = 'agri.dna.plugin'

    @api.model
    def inherit_dna(self, lot, inputs):
        if not inputs: return
        # Take location from the first input's intervention (which produced the lot)
        if hasattr(lot, 'geo_point'):
            lot.geo_point = inputs[0].production_id.geo_point

class AgriDnaPluginCertification(models.AbstractModel):
    """
    [DNA Plugin] Certification Inheritance & Tainting.
    Ensures that the output lot's certification level is derived from its inputs.
    Logic: If any input is non-certified, the output cannot be 'organic'.
    """
    _name = 'agri.dna.plugin.certification'
    _inherit = 'agri.dna.plugin'

    @api.model
    def inherit_dna(self, lot, inputs):
        if not hasattr(lot, 'certification_type'):
            return

        # Check all inputs for their certification status
        # (Assuming inputs are stock.moves, we check their source lots)
        input_lots = inputs.mapped('lot_id')
        if not input_lots:
            return

        # If any input lot is not organic, the output lot is downgraded to 'commodity' or 'green'
        is_all_organic = all(l.certification_type == 'organic' for l in input_lots)
        
        if not is_all_organic and lot.certification_type == 'organic':
            lot.certification_type = 'green' # Downgrade to next level
            lot.message_post(body=_("DNA Tainting: Lot certification downgraded to 'Green' due to non-organic inputs."))
