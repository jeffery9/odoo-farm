from odoo import fields, models, api, _

class FarmPackageLevel(models.Model):
    _name = 'farm.package.level'
    _description = 'Farm Package Level (e.g., Item, Inner Carton, Pallet)'

    name = fields.Char(string='Level Name', required=True, translate=True)
    code = fields.Char(string='Level Code', required=True, help="Unique code for this package level (e.g., ITM, INC, OUC, PAL)")
    parent_level_id = fields.Many2one('farm.package.level', string='Parent Level', help="The level this package can contain (e.g., Carton contains Items)")
    child_level_ids = fields.One2many('farm.package.level', 'parent_level_id', string='Child Levels')

class FarmPackage(models.Model):
    _name = 'farm.package'
    _description = 'Farm Package Instance'
    _rec_name = 'display_name'

    name = fields.Char(string='Package Reference', default=lambda self: _('New'))
    display_name = fields.Char(string='Display Name', compute='_compute_display_name', store=True)
    
    package_level_id = fields.Many2one('farm.package.level', string='Package Level', required=True)
    product_id = fields.Many2one('product.product', string='Contained Product', required=True)
    lot_id = fields.Many2one('stock.lot', string='Contained Lot/Serial', domain="[('product_id', '=', product_id)]")
    quantity = fields.Float(string='Quantity', required=True)

    parent_package_id = fields.Many2one('farm.package', string='Contained In Package', help="The package this package is contained within")
    child_package_ids = fields.One2many('farm.package', 'parent_package_id', string='Contains Packages')

    location_id = fields.Many2one('stock.location', string='Location')
    create_date = fields.Datetime(string='Creation Date', default=fields.Datetime.now)
    barcode = fields.Char(string='Barcode', copy=False, help="Barcode of the package for scanning")

    @api.depends('name', 'package_level_id', 'product_id', 'lot_id')
    def _compute_display_name(self):
        for rec in self:
            name = rec.name if rec.name != _('New') else ''
            level = rec.package_level_id.name if rec.package_level_id else ''
            product = rec.product_id.name if rec.product_id else ''
            lot = rec.lot_id.name if rec.lot_id else ''
            rec.display_name = f"{name} ({level}) {product} [{lot}]".strip()

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('farm.package') or _('New')
        return super().create(vals)

