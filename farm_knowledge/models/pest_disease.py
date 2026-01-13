from odoo import models, fields, api, _

class FarmPestDisease(models.Model):
    """
    农场病虫害数据库 [US-17-07]
    """
    _name = 'farm.pest.disease'
    _description = 'Pest & Disease Database'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name", required=True, translate=True)
    scientific_name = fields.Char(string="Scientific Name")
    category = fields.Selection([
        ('pest', 'Pest'),
        ('disease', 'Disease'),
        ('weed', 'Weed')
    ], string="Category", required=True)

    symptoms = fields.Html(string="Symptoms Description", translate=True)
    cause = fields.Text(string="Cause/Etiology", translate=True)
    prevention = fields.Html(string="Prevention Measures", translate=True)
    photo = fields.Binary(string="Reference Photo")
    image_name = fields.Char("Image Name")

    recommended_intervention_id = fields.Many2one(
        'agri.intervention.template',
        string="Recommended Treatment (Technical Route)"
    )

    description = fields.Text(string="Detailed Description", translate=True)
    active = fields.Boolean(default=True)

    def action_view_treatment(self):
        self.ensure_one()
        if self.recommended_intervention_id:
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'agri.intervention.template',
                'res_id': self.recommended_intervention_id.id,
                'view_mode': 'form',
                'target': 'current',
            }
