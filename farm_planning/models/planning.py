from odoo import models, fields, api, _

class AgriInterventionTemplate(models.Model):
    _name = 'agri.intervention.template'
    _description = 'Agricultural Intervention Template'

    name = fields.Char("Operation Name", required=True) # e.g., Standard Sowing
    intervention_type = fields.Selection([
        ('tillage', 'Soil Preparation'),
        ('sowing', 'Sowing/Planting'),
        ('fertilizing', 'Fertilizing'),
        ('protection', 'Crop Protection'),
        ('harvesting', 'Harvesting'),
    ], string="Category", required=True)
    
    # 预设投入品
    input_ids = fields.One2many('agri.intervention.template.input', 'template_id', string="Estimated Inputs")
    
    # 预设工时 (小时)
    estimated_labor_hours = fields.Float("Estimated Labor (Hours)", default=1.0)

class AgriInterventionTemplateInput(models.Model):
    _name = 'agri.intervention.template.input'
    _description = 'Template Input Requirement'

    template_id = fields.Many2one('agri.intervention.template', ondelete='cascade')
    product_id = fields.Many2one('product.product', string="Product", required=True)
    quantity = fields.Float("Quantity per Unit Area", default=1.0)

class AgriTechnicalRoute(models.Model):
    _name = 'agri.technical.route'
    _description = 'Technical Route (Cultural Itinerary)'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Route Name", required=True) # e.g., Winter Wheat Standard
    activity_family = fields.Selection([
        ('planting', 'Planting'),
        ('livestock', 'Livestock'),
        ('aquaculture', 'Aquaculture')
    ], required=True)
    
    line_ids = fields.One2many('agri.technical.route.line', 'route_id', string="Intervention Sequence")

class AgriTechnicalRouteLine(models.Model):
    _name = 'agri.technical.route.line'
    _description = 'Route Sequence Line'
    _order = 'sequence'

    route_id = fields.Many2one('agri.technical.route', ondelete='cascade')
    sequence = fields.Integer("Sequence", default=10)
    template_id = fields.Many2one('agri.intervention.template', string="Operation", required=True)
    
    # 相对于产季开始的偏移天数 (Ekylibre 风格)
    delay_days = fields.Integer("Delay from Start (Days)", default=0)

class AgriTechnicalRoute(models.Model):
    _inherit = 'agri.technical.route'

    def action_apply_to_project(self, project_id, start_date, land_parcel_id=False):
        """ 
        根据技术路线生成一系列预定的农事任务。
        """
        self.ensure_one()
        from datetime import timedelta
        task_obj = self.env['project.task']
        
        for line in self.line_ids:
            planned_date = fields.Date.from_string(start_date) + timedelta(days=line.delay_days)
            task_vals = {
                'name': _('[%s] %s') % (self.name, line.template_id.name),
                'project_id': project_id,
                'planned_date_begin': planned_date,
                'date_deadline': planned_date + timedelta(days=1), # 默认1天
                'land_parcel_id': land_parcel_id,
                'description': _('Generated from Route: %s\nOperation: %s') % (self.name, line.template_id.name),
                # 预估工时
                'allocated_hours': line.template_id.estimated_labor_hours,
            }
            task = task_obj.create(task_vals)
            
            # 未来可进一步在此处创建草稿干预单 (MO) 并填入预估投入品
        
        return True
