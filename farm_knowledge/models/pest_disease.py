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

    # Original field kept for compatibility
    recommended_intervention_id = fields.Many2one(
        'agri.intervention.template',
        string="Recommended Treatment (Technical Route)"
    )

    # New fields to satisfy US-17-13 requirements
    conventional_treatment = fields.Html(string="Conventional Treatment", translate=True,
                                       help="Recommended conventional treatment methods and products")
    organic_treatment = fields.Html(string="Organic/Green Treatment", translate=True,
                                  help="Recommended organic or green treatment methods and products")
    integrated_treatment = fields.Html(string="Integrated Treatment", translate=True,
                                     help="Recommended integrated pest management approach combining different methods")

    # Product recommendations (linking to specific products that can be used)
    conventional_products = fields.Many2many(
        'product.template',
        'pest_disease_conventional_product_rel',
        'pest_disease_id', 'product_id',
        string="Conventional Products",
        domain=[('is_agri_input', '=', True)],
        help="Recommended conventional products for treatment"
    )
    organic_products = fields.Many2many(
        'product.template',
        'pest_disease_organic_product_rel',
        'pest_disease_id', 'product_id',
        string="Organic/Green Products",
        domain=[('is_agri_input', '=', True)],
        help="Recommended organic/green products for treatment"
    )

    # Compliance and certification fields
    compliance_standards = fields.Char(string="Compliance Standards",
                                     help="Standards that treatments must comply with (e.g., NOP, EU Organic)")
    severity_level = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('very_high', 'Very High')
    ], string="Typical Severity Level", help="Typical severity level of this pest/disease")

    # Crop-specific information
    affected_crops = fields.Many2many(
        'product.template',
        'pest_disease_crop_rel',
        'pest_disease_id', 'crop_id',
        string="Affected Crops",
        domain=[('agricultural_type', 'in', ['input', 'output'])],
        help="Crops that are typically affected by this pest/disease"
    )

    # Prevention and monitoring
    prevention_methods = fields.Html(string="Prevention Methods", translate=True)
    monitoring_tips = fields.Html(string="Monitoring Tips", translate=True)
    optimal_conditions = fields.Html(string="Optimal Conditions for Development", translate=True)

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

    def get_treatment_recommendations(self, treatment_type='integrated'):
        """
        US-17-13: Get treatment recommendations based on type (conventional, organic, integrated)
        """
        self.ensure_one()
        if treatment_type == 'conventional':
            return {
                'treatment': self.conventional_treatment,
                'products': self.conventional_products,
                'title': 'Conventional Treatment'
            }
        elif treatment_type == 'organic':
            return {
                'treatment': self.organic_treatment,
                'products': self.organic_products,
                'title': 'Organic/Green Treatment'
            }
        else:  # integrated/default
            return {
                'treatment': self.integrated_treatment or self.conventional_treatment or self.organic_treatment,
                'products': self.conventional_products | self.organic_products,
                'title': 'Integrated Treatment'
            }

    def action_recommend_treatments(self, treatment_type='integrated'):
        """
        Action to provide treatment recommendations based on the pest/disease
        """
        recommendations = self.get_treatment_recommendations(treatment_type)

        # Create an activity or message to notify user of recommendations
        self.message_post(
            body=f"<b>{recommendations['title']} for {self.name}:</b><br/>{recommendations['treatment'] or 'No specific treatment recommendations available.'}",
            subject=f"Treatment Recommendation for {self.name}"
        )

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': f'{recommendations["title"]} for {self.name}',
                'message': f'Based on our pest/disease knowledge base, we recommend: {recommendations["treatment"][:200]}...',
                'type': 'success',
                'sticky': False,
            }
        }
