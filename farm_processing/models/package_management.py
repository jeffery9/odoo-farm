# -*- coding: utf-8 -*-
from odoo import fields, models, api, _

class FarmPackageLevel(models.Model):
    _name = 'farm.package.level'
    _description = 'Farm Package Level (e.g., Bottle, Box, Case)'

    name = fields.Char(string='Level Name', required=True, translate=True)
    code = fields.Char(string='Level Code', required=True, help="Unique code for this package level (e.g., BTL, CTN, CSE, PAL)")
    parent_level_id = fields.Many2one('farm.package.level', string='Parent Level', help="The level this package can contain (e.g., Carton contains Items)")
    child_level_ids = fields.One2many('farm.package.level', 'parent_level_id', string='Child Levels')


class FarmPackage(models.Model):
    _name = 'farm.package'
    _description = 'Commercial Product Packaging Traceability'
    _rec_name = 'display_name'

    name = fields.Char(string='Unique Package Reference', default=lambda self: _('New'))
    display_name = fields.Char(string='Display Name', compute='_compute_display_name', store=True, precompute=True)
    
    package_level_id = fields.Many2one('farm.package.level', string='Package Level', required=True)
    product_id = fields.Many2one('product.product', string='Commercial Product', required=True)
    lot_id = fields.Many2one('stock.lot', string='Contained Lot/Serial', required=True, domain="[('product_id', '=', product_id)]")
    quantity = fields.Float(string='Net Fill Quantity', required=True)
    
    capacity = fields.Float(string='Capacity', default=0.0)
    reusable = fields.Boolean(string='Reusable', default=False)

    parent_package_id = fields.Many2one('farm.package', string='Parent Case', help="The commercial package this package is contained within")
    child_package_ids = fields.One2many('farm.package', 'parent_package_id', string='Contained Packages')

    # Converged to native stock.location
    location_id = fields.Many2one('stock.location', string='Location', required=True, help="Current physical stock location")
    
    # Associated logistics carrier package
    stock_package_id = fields.Many2one('stock.package', string='Logistics Package', help="The dynamic LPN package carrier")

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

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('farm.package') or _('New')
        return super().create(vals_list)


class StockMove(models.Model):
    _inherit = 'stock.move'

    def _action_done(self, cancel_backorder=False):
        res = super(StockMove, self)._action_done(cancel_backorder=cancel_backorder)
        # Find all move lines related to these moves
        move_lines = res.mapped('move_line_ids')
        for line in move_lines:
            # Check if there is a result package (destination package) or source package
            target_packages = self.env['stock.package']
            if line.result_package_id:
                target_packages |= line.result_package_id
            if line.package_id:
                target_packages |= line.package_id

            if target_packages and line.location_dest_id:
                # Find any associated farm.packages and update their location in real-time
                farm_pkgs = self.env['farm.package'].search([
                    ('stock_package_id', 'in', target_packages.ids)
                ])
                if farm_pkgs:
                    farm_pkgs.write({
                        'location_id': line.location_dest_id.id
                    })
        return res
