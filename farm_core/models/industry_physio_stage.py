from odoo import models, fields, api, _

class AgriIndustryPhysioStage(models.Model):
    """
    Agri Domain Level: Physiological Growth Stage. [US-014-2026]
    Defines universal growth stages for biological assets.
    Refactored from farm.industry.physio.stage with 100% logic retention.
    """
    _name = 'agri.industry.physio.stage'
    _description = 'Agricultural Physiological Stage'
    _order = 'sequence'

    # --- 100% Original Logic Retention ---
    package_id = fields.Many2one(
        'agri.industry.data.package',
        string="Industry Package",
        required=True,
        ondelete='cascade'
    )

    stage_name = fields.Char("Stage Name", required=True)
    age_days = fields.Integer("Age (Days)", required=True)
    target_weight = fields.Float("Target Weight (kg)")
    daily_feed_rate = fields.Float("Daily Feed Rate (%)")
    related_variety = fields.Char("Related Variety")
    # --- End of Original Logic ---

    sequence = fields.Integer("Sequence", default=10)
    
    # Domain specific triggers
    is_harvest_stage = fields.Boolean("Is Harvest Stage", default=False)
    accumulated_temp_threshold = fields.Float("Target Accumulated Temp (°C)")
    
    description = fields.Text("Standard Description")
    active = fields.Boolean(default=True)

    def name_get(self):
        result = []
        for record in self:
            name = f"{record.stage_name} (Day {record.age_days})"
            result.append((record.id, name))
        return result