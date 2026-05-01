from odoo import fields, models, api, _

class IndustryProductCategory(models.Model):
    """Product category data for industry packages"""
    _name = 'farm.industry.product.category'
    _description = 'Industry Package Product Category Data'

    package_id = fields.Many2one(
        'agri.industry.data.package',
        string="Industry Package",
        required=True,
        ondelete='cascade'
    )

    name = fields.Char("Category Name", required=True)
    parent_id = fields.Many2one('product.category', string="Parent Category")
    agricultural_type = fields.Selection([
        ('land_parcel', 'Land Parcel'),
        ('animal', 'Animal'),
        ('animal_group', 'Animal Group'),
        ('equipment', 'Equipment'),
        ('input', 'Input'),
        ('output', 'Output'),
    ], string="Agricultural Type")