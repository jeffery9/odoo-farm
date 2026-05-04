from odoo import models, fields, api, _

class AgriIntervention(models.Model):
    """
    Agricultural Intervention: The 2026 De-industrialized core model.
    Injects Level 0-3 Mixins to transform standard MRP into a community agricultural entity.
    """
    _name = 'mrp.production'
    _inherit = [
        'mrp.production',
        'agri.intervention.mixin',
        # 'agri.view.mixin',           # 移除显式继承，改由 farm_ux 模块主动注入
        'agri.sustainability.mixin', # Level 0: Value Standard
        'agri.geospatial.mixin',     # Level 1: Spatial Grid
        'farm.agri.science.mixin',   # Level 2: Agronomy
        'agri.nutrient.mixin',       # Level 1: Mass Balance
        'agri.actuator.mixin',       # Level 1+: Physical Actuation
        'agri.evidence.mixin',       # Level 2: Audit
        'agri.clearing.mixin',       # Level 3: Clearing
        # 'farm.agri.science.mixin',   # [US-045-08] Scientific DNA
    ]
    _description = 'Agricultural Intervention (De-industrialized View)'

    # [US-045-07] Biological Clock Tracking
    daily_temp_max = fields.Float("Daily Max Temperature")
    daily_temp_min = fields.Float("Daily Min Temperature")

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
        records = super(AgriIntervention, self).create(vals_list)
        for record in records:
            record.generate_quality_fingerprint()
        return records

    def action_confirm_intervention(self):
        self.ensure_one()
        return self.action_confirm()

    def action_complete_intervention(self):
        """
        [Level 1+ DNA Traceability] 
        Finalizes clearing and transfers physical DNA to the output lots.
        """
        self.ensure_one()
        self.action_finalize_clearing()
        
        # 1. Identify output lots
        output_moves = self.move_finished_ids.filtered(lambda m: m.state == 'done')
        for move in output_moves:
            for line in move.move_line_ids:
                if line.lot_id:
                    # 2. Trigger DNA inheritance from input moves
                    line.lot_id.inherit_dna_from_source(self.move_raw_ids)
                    
        return True


# ProcurementGroup inheritance removed for Odoo 19 compatibility