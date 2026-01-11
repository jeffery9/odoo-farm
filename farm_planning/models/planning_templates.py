from odoo import models, fields, api, _

class AgriInterventionTemplate(models.Model):
    _name = 'agri.intervention.template'
    _description = 'Intervention Template'

    name = fields.Char("Operation Name", required=True) # e.g., Standard Sowing
    intervention_type = fields.Selection([
        ('tillage', 'Soil Preparation (耕作)'),
        ('sowing', 'Sowing (播种)'),
        ('fertilizing', 'Fertilizing (施肥)'),
        ('protection', 'Protection (植保)'),
        ('harvesting', 'Harvesting (收获)')
    ], required=True)
    
    # 预设资源需求
    labor_hours_per_unit = fields.Float("Labor Hours per Hectare/Group")
    input_ids = fields.One2many('agri.intervention.template.input', 'template_id', string="Required Inputs")

class AgriInterventionTemplateInput(models.Model):
    _name = 'agri.intervention.template.input'
    _description = 'Intervention Template Input'

    template_id = fields.Many2one('agri.intervention.template', ondelete='cascade')
    product_id = fields.Many2one('product.product', string="Material", required=True)
    qty_per_unit = fields.Float("Qty per Area/Unit")

class AgriTechnicalRoute(models.Model):
    _name = 'agri.technical.route'
    _description = 'Technical Route (Itinéraire Cultural)'

    name = fields.Char("Route Name", required=True) # e.g., Organic Wheat Route
    family = fields.Selection([
        ('planting', 'Planting'),
        ('livestock', 'Livestock')
    ], default='planting')
    
    line_ids = fields.One2many('agri.technical.route.line', 'route_id', string="Operation Sequence")

class AgriTechnicalRouteLine(models.Model):
    _name = 'agri.technical.route.line'
    _description = 'Technical Route Sequence'
    _order = 'sequence'

    route_id = fields.Many2one('agri.technical.route', ondelete='cascade')
    sequence = fields.Integer("Sequence", default=10)
    template_id = fields.Many2one('agri.intervention.template', string="Operation", required=True)
    delay_from_start = fields.Integer("Delay Days (T+N)", default=0)
