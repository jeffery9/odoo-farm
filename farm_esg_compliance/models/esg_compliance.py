from odoo import models, fields, api, _

class FarmSubsidy(models.Model):
    _name = 'farm.subsidy'
    _description = 'Agricultural Subsidy Tracking'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Subsidy Program", required=True)
    subsidy_type = fields.Selection([
        ('land', 'Land-based Subsidy'),
        ('input', 'Input/Fertilizer Subsidy'),
        ('machinery', 'Machinery Subsidy'),
        ('disaster', 'Disaster Relief')
    ], string="Type", required=True)
    
    amount = fields.Monetary("Subsidy Amount", currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    
    application_date = fields.Date("Application Date")
    disbursement_date = fields.Date("Disbursement Date")
    
    location_id = fields.Many2one('farm.location', string="Target Land Parcel")
    compliance_verified = fields.Boolean("Compliance Check Passed", default=False)
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('applied', 'Application Submitted'),
        ('approved', 'Approved'),
        ('paid', 'Disbursed'),
        ('cancel', 'Cancelled')
    ], default='draft', tracking=True)

class FarmBiodiversityMetric(models.Model):
    _name = 'farm.biodiversity.metric'
    _description = 'Biodiversity Monitoring'

    name = fields.Char("Observation Point", required=True)
    location_id = fields.Many2one('farm.location', string="Farm Location")
    date = fields.Date("Monitoring Date", default=fields.Date.today)
    
    species_count = fields.Integer("Native Species Count")
    habitat_quality = fields.Selection([
        ('1', 'Poor'), ('2', 'Fair'), ('3', 'Good'), ('4', 'Excellent')
    ], string="Habitat Quality", default='2')
    
    soil_health_index = fields.Float("Soil Health Index (0-100)")
    notes = fields.Text("Observation Details")

class FarmExportCompliance(models.Model):
    _name = 'farm.export.compliance'
    _description = 'Export Compliance Checker'

    name = fields.Char("Export Ref", required=True)
    target_market_id = fields.Many2one('res.country', string="Target Country", required=True)
    product_id = fields.Many2one('product.template', string="Product")
    
    residue_limit_ok = fields.Boolean("MRL Compliance (Pesticides)", default=False)
    phytosanitary_cert_ok = fields.Boolean("Phytosanitary Certificate", default=False)
    labeling_ok = fields.Boolean("Market-specific Labeling", default=False)
    
    compliance_status = fields.Selection([
        ('pending', 'Pending Review'),
        ('ready', 'Export Ready'),
        ('blocked', 'Compliance Blocked')
    ], compute='_compute_compliance_status', store=True)

    @api.depends('residue_limit_ok', 'phytosanitary_cert_ok', 'labeling_ok')
    def _compute_compliance_status(self):
        for rec in self:
            if rec.residue_limit_ok and rec.phytosanitary_cert_ok and rec.labeling_ok:
                rec.compliance_status = 'ready'
            else:
                rec.compliance_status = 'blocked'

class FarmCertificationProcess(models.Model):
    _name = 'farm.certification.process'
    _description = 'Sustainability Certification'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Certification Name", required=True)
    cert_type = fields.Selection([
        ('organic', 'Organic Certification'),
        ('fair_trade', 'Fair Trade'),
        ('gap', 'Good Agricultural Practices'),
        ('carbon', 'Carbon Neutrality')
    ], string="Type", required=True)
    
    valid_from = fields.Date("Valid From")
    valid_to = fields.Date("Expiry Date")
    
    audit_date = fields.Date("Last Audit Date")
    auditor_id = fields.Many2one('res.partner', string="Audit Body")
    
    state = fields.Selection([
        ('plan', 'Planned'),
        ('in_audit', 'Audit in Progress'),
        ('certified', 'Certified'),
        ('expired', 'Expired'),
        ('failed', 'Certification Failed')
    ], default='plan', tracking=True)
