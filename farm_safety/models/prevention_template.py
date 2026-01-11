from odoo import models, fields, api

class FarmPreventionTemplate(models.Model):
    _name = 'farm.prevention.template'
    _description = 'Agri-Prevention Template'

    name = fields.Char("Template Name", required=True)
    active = fields.Boolean(default=True)
    line_ids = fields.One2many('farm.prevention.line', 'template_id', string="Operations")
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)

class FarmPreventionLine(models.Model):
    _name = 'farm.prevention.line'
    _description = 'Prevention Operation Line'
    _order = 'delay_days asc'

    template_id = fields.Many2one('farm.prevention.template', ondelete='cascade')
    name = fields.Char("Operation Name", required=True)
    delay_days = fields.Integer("Delay Days (T+N)", default=0, help="Days after task start to perform this operation.")
    
    # 预设投入品（可选）
    product_id = fields.Many2one('product.product', string="Vaccine/Medicine", help="Predefined input for this operation.")
    qty = fields.Float("Quantity", default=1.0)
