from odoo import models, fields, api, _

class AgriInterventionMrp(models.Model):
    """
    Agricultural Intervention: The 2026 De-industrialized core model.
    Injects Level 0-3 Mixins to transform standard MRP into a community agricultural entity.
    """
    _inherit = [
        'mrp.production',
        'agri.intervention.mixin',
        'agri.sustainability.mixin', # Level 0: Value Standard
        'agri.weather.sensitive.mixin', # Level 2: Weather Gating
        'agri.agent.instruction.mixin', # Level 4: Orchestration
        'agri.geospatial.mixin',     # Level 1: Spatial Grid
        'farm.agri.science.mixin',   # Level 2: Agronomy
        'agri.nutrient.mixin',       # Level 1: Mass Balance
        'agri.actuator.mixin',       # Level 1+: Physical Actuation
        'agri.evidence.mixin',       # Level 2: Audit
        'agri.clearing.mixin',       # Level 3: Clearing
    ]
    _description = 'Agricultural Intervention (De-industrialized View)'

    agri_task_id = fields.Many2one('project.task', string="Parent Activity Task")
    biological_asset_id = fields.Many2one('agri.biological.asset', string="Target Biological Asset")
    
    intervention_type = fields.Selection([
        ('tillage', 'Soil Preparation'),
        ('sowing', 'Sowing/Planting'),
        ('fertilizing', 'Fertilizing'),
        ('irrigation', 'Irrigation'),
        ('protection', 'Crop Protection'),
        ('aerial_spraying', 'Aerial Spraying'),
        ('harvesting', 'Harvesting'),
        ('feeding', 'Feeding'),
        ('medical', 'Medical/Prevention'),
        ('process', 'General Process'),
    ], string='Intervention Type', default='process')

    # [US-044-01] Drive Modes
    drive_mode = fields.Selection([
        ('material', 'Material Driven'),
        ('parameter', 'Parameter Driven')
    ], string="Drive Mode", default='material')
    
    state = fields.Selection(selection_add=[('hold', 'On Hold')], ondelete={'hold': 'cascade'})

    # [US-045-07] Biological Clock Tracking
    daily_temp_max = fields.Float("Daily Max Temperature")
    daily_temp_min = fields.Float("Daily Min Temperature")

    pure_n_qty = fields.Float("Pure Nitrogen (kg)", compute='_compute_pure_nutrients', store=True)
    pure_p_qty = fields.Float("Pure Phosphorus (kg)", compute='_compute_pure_nutrients', store=True)
    pure_k_qty = fields.Float("Pure Potassium (kg)", compute='_compute_pure_nutrients', store=True)

    @api.depends('move_raw_ids', 'move_raw_ids.product_uom_qty', 'move_raw_ids.state')
    def _compute_pure_nutrients(self):
        for mo in self:
            n, p, k = 0.0, 0.0, 0.0
            for move in mo.move_raw_ids:
                if move.state != 'cancel':
                    # Assuming fields like 'n_content' exist on product.product (from agri_nutrient_mixin)
                    qty = move.product_uom_qty
                    n += qty * (getattr(move.product_id, 'n_content', 0.0) / 100.0)
                    p += qty * (getattr(move.product_id, 'p_content', 0.0) / 100.0)
                    k += qty * (getattr(move.product_id, 'k_content', 0.0) / 100.0)
            mo.pure_n_qty = n
            mo.pure_p_qty = p
            mo.pure_k_qty = k

    def trigger_spc_hold(self, reason):
        """ US-044-03: Execution hold on critical deviation. """
        self.ensure_one()
        self.write({'state': 'hold'})
        self.message_post(body=_("SPC LOCK: Production held due to: %s") % reason)

    def record_daily_environmental_data(self, t_max, t_min):
        """ 记录每日温差并累加生理热量 (GDD) """
        self.ensure_one()
        increment = self.calculate_gdd_increment(t_max, t_min)
        self.write({
            'cumulative_gdd': self.cumulative_gdd + increment,
            'daily_temp_max': t_max,
            'daily_temp_min': t_min,
        })
        self._action_log_scientific_audit(_("Accumulated %s GDD from environmental sync.") % round(increment, 2))

    def _action_log_scientific_audit(self, message):
        """ 记录科学审计日志 """
        self.message_post(body=f"<b>[Scientific Audit]</b> {message}")

    def _get_embedding_content(self):
        self.ensure_one()
        return f"Intervention {self.name}: {self.product_id.display_name} at grid {self.spatial_grid_id}."

    @api.model_create_multi
    def create(self, vals_list):
        records = super(AgriInterventionMrp, self).create(vals_list)
        for record in records:
            if hasattr(record, 'generate_quality_fingerprint'):
                record.generate_quality_fingerprint()
        return records

    @api.onchange('bom_id', 'product_qty', 'product_uom_id')
    def _onchange_bom_id(self):
        """ 拦截并根据稀释比例和饲喂比例修正物料需求量 """
        res = super(AgriInterventionMrp, self)._onchange_bom_id()
        for mo in self:
            lot = mo.agri_task_id.biological_lot_id if hasattr(mo, 'agri_task_id') else False
            for move in mo.move_raw_ids:
                bom_line = mo.bom_id.bom_line_ids.filtered(lambda l: l.product_id == move.product_id)
                if not bom_line:
                    continue
                if bom_line.dilution_ratio > 0:
                    move.product_uom_qty = mo.product_qty / bom_line.dilution_ratio
                elif bom_line.feeding_ratio > 0 and lot:
                    tracking = self.env['stock.matter.tracking']
                    quants = lot.quant_ids.filtered(lambda q: q.package_id and getattr(q.package_id, 'is_matter_tracking', False))
                    if not quants:
                        quants = lot.quant_ids.filtered(lambda q: q.package_id and q.package_id._name == 'stock.matter.tracking')
                    if quants:
                        tracking = quants[0].package_id

                    if tracking:
                        animal_count = getattr(tracking, 'animal_count', 1) or 1
                        weight = getattr(tracking, 'current_weight', 0.0) or 0.0
                    else:
                        animal_count = getattr(lot, 'animal_count', 0) or 0
                        weight = getattr(lot, 'average_weight', 0.0) or getattr(lot, 'current_weight', 0.0) or 0.0

                    total_biomass = animal_count * weight
                    move.product_uom_qty = total_biomass * (bom_line.feeding_ratio / 100.0)
        return res

    def _get_moves_raw_values(self):
        """ 针对实际保存逻辑的覆盖（后台创建 MO 时生效） """
        res = super(AgriInterventionMrp, self)._get_moves_raw_values()
        for move_vals in res:
            bom_line = self.env['mrp.bom.line'].browse(move_vals.get('bom_line_id'))
            if bom_line and bom_line.dilution_ratio > 0:
                move_vals['product_uom_qty'] = self.product_qty / bom_line.dilution_ratio
        return res

    def button_mark_done(self):
        """ [Level 0 Lifecycle] Hook into standard MRP completion to trigger plugins. """
        for mo in self:
            if hasattr(mo, 'action_done_base'):
                mo.action_done_base() # Triggers 'pre_done' and 'post_done' plugins
            mo._trigger_post_intervention_growth()
        return super(AgriInterventionMrp, self).button_mark_done()

    def action_confirm(self):
        """ [Level 0: DNA Gate] Validate ESG and Weather compliance. """
        for mo in self:
            if hasattr(mo, 'action_confirm_base'):
                mo.action_confirm_base() # Triggers 'pre_confirm' and 'post_confirm' plugins
            if hasattr(mo, 'check_weather_window'):
                activity_type = 'spraying' if 'spray' in (mo.product_id.name or '').lower() else 'general'
                mo.check_weather_window(activity_type)
            
        return super(AgriInterventionMrp, self).action_confirm()

    def action_confirm_intervention(self):
        self.ensure_one()
        return self.action_confirm()

    def action_complete_intervention(self):
        """
        [Level 1+ DNA Traceability] 
        Finalizes clearing and transfers physical DNA to the output lots.
        """
        self.ensure_one()
        if hasattr(self, 'action_done_base'):
            self.action_done_base()  # Use base engine completion (triggers plugins)
        if hasattr(self, 'action_finalize_clearing'):
            self.action_finalize_clearing()
        
        # 1. Identify output lots
        output_moves = self.move_finished_ids.filtered(lambda m: m.state == 'done')
        for move in output_moves:
            for line in move.move_line_ids:
                if line.lot_id:
                    # 2. Trigger DNA inheritance from input moves
                    line.lot_id.inherit_dna_from_source(self.move_raw_ids)
                    
        return True

    def _trigger_post_intervention_growth(self):
        """ [US-045-08] Trigger scientific weight gain calculation. """
        for mo in self:
            if mo.biological_asset_id and mo.intervention_type == 'feeding':
                # Simplified: gain = feed * 0.4 (FCR=2.5)
                feed_qty = sum(mo.move_raw_ids.mapped('product_uom_qty'))
                gain = feed_qty * 0.4
                if hasattr(mo.biological_asset_id, 'base_weight_kg'):
                    mo.biological_asset_id.write({
                        'base_weight_kg': mo.biological_asset_id.base_weight_kg + gain
                    })
                    if hasattr(mo.biological_asset_id, 'trigger_financial_revaluation'):
                        mo.biological_asset_id.trigger_financial_revaluation(_("Feeding Outcome: %skg weight gain") % round(gain, 2))
                    mo.message_post(body=_("SCIENTIFIC GROWTH: Asset %s gained %skg weight from feeding.") % 
                                   (mo.biological_asset_id.name, round(gain, 2)))
