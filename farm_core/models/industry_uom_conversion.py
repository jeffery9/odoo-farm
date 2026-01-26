from odoo import fields, models, api, _

class IndustryUOMConversion(models.Model):
    """UOM conversion data for industry packages"""
    _name = 'farm.industry.uom.conversion'
    _description = 'Industry Package UOM Conversion Data'

    package_id = fields.Many2one(
        'farm.industry.data.package',
        string="Industry Package",
        required=True,
        ondelete='cascade'
    )

    from_uom_id = fields.Many2one('uom.uom', string="From UOM", required=True)
    to_uom_id = fields.Many2one('uom.uom', string="To UOM", required=True)
    factor = fields.Float("Conversion Factor", required=True, default=1.0)

    description = fields.Text("Description")