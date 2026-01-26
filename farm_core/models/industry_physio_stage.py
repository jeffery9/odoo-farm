from odoo import fields, models, api, _

class IndustryPhysioStage(models.Model):
    """Physiological stage data for industry packages"""
    _name = 'farm.industry.physio.stage'
    _description = 'Industry Package Physiological Stage Data'

    package_id = fields.Many2one(
        'farm.industry.data.package',
        string="Industry Package",
        required=True,
        ondelete='cascade'
    )

    stage_name = fields.Char("Stage Name", required=True)
    age_days = fields.Integer("Age (Days)", required=True)
    target_weight = fields.Float("Target Weight (kg)")
    daily_feed_rate = fields.Float("Daily Feed Rate (%)")
    related_variety = fields.Char("Related Variety")

    description = fields.Text("Description")