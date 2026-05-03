# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class FarmProcessingProductionPackagingExtension(models.Model):
    """
    Extension to Processing ISL Production Model for Packaging - US-14-10
    """
    _inherit = 'farm.processing.production'

    # Packaging specific fields
    package_batch_no = fields.Char('Package Batch No.', default=lambda self: self._default_package_batch())
    package_type = fields.Selection([
        ('individual', 'Individual Package'),
        ('box', 'Box'),
        ('pallet', 'Pallet'),
    ], string='Package Type')

    # Barcode generation
    individual_barcodes = fields.Text('Individual Barcodes')
    box_barcode = fields.Char('Box Barcode')
    pallet_barcode = fields.Char('Pallet Barcode')

    # Contents tracking
    contained_lot_ids = fields.Many2many('stock.lot', 'production_contained_lot_rel', 'production_id', 'lot_id', string='Contained Product Lots')
    total_items = fields.Integer('Total Items')

    def _default_package_batch(self):
        """Default package batch number generation"""
        return 'PKG/' + fields.Date.to_string(fields.Date.today()) + '/' + str(self.id or 0)


class AgriProcessingPackaging(models.Model):
    """
    Multi-level Packaging Hierarchy Management - US-14-10
    """
    _name = 'agri.processing.packaging'
    _description = 'Multi-level Packaging Hierarchy Management'
    _order = 'creation_date desc'

    name = fields.Char('Package ID', required=True, default=lambda self: self._default_package_id())
    parent_package_id = fields.Many2one('agri.processing.packaging', string='Parent Package', index=True)
    child_package_ids = fields.One2many('agri.processing.packaging', 'parent_package_id', string='Child Packages')

    # Package type and level
    package_type = fields.Selection([
        ('individual', 'Individual Package'),
        ('box', 'Box'),
        ('pallet', 'Pallet'),
        ('container', 'Container'),
    ], string='Package Type', required=True, default='individual')

    package_level = fields.Integer('Package Level', compute='_compute_package_level', store=True)

    # Product and lot tracking
    product_id = fields.Many2one('product.product', string='Product')
    lot_id = fields.Many2one('stock.lot', string='Lot')
    quantity = fields.Float('Quantity')

    # Barcode and identification
    barcode = fields.Char('Barcode')
    qr_code = fields.Char('QR Code')
    package_sequence = fields.Char('Package Sequence')

    # Creation and tracking
    creation_date = fields.Datetime('Creation Date', default=fields.Datetime.now)
    created_by = fields.Many2one('res.users', string='Created By', default=lambda self: self.env.user)

    # Dimensions and weight
    length = fields.Float('Length (cm)')
    width = fields.Float('Width (cm)')
    height = fields.Float('Height (cm)')
    weight = fields.Float('Weight (kg)')

    # Status
    is_active = fields.Boolean('Is Active', default=True)
    is_sealed = fields.Boolean('Is Sealed', default=False)
    seal_date = fields.Datetime('Seal Date')

    @api.model
    def create(self, vals):
        if 'name' not in vals or not vals['name']:
            vals['name'] = self._default_package_id()
        return super().create(vals)

    @api.model
    def _default_package_id(self):
        """Generate default package ID"""
        return 'PKG/' + fields.Date.to_string(fields.Date.today()) + '/' + str(self.id or len(self.search([])) + 1)

    @api.depends('parent_package_id', 'parent_package_id.package_level')
    def _compute_package_level(self):
        """Compute package level in the hierarchy"""
        for record in self:
            if record.parent_package_id:
                record.package_level = record.parent_package_id.package_level + 1
            else:
                record.package_level = 1

    def action_seal_package(self):
        """Seal the package and prevent further modifications"""
        for record in self:
            record.is_sealed = True
            record.seal_date = fields.Datetime.now()

    def get_full_hierarchy(self):
        """Get the full packaging hierarchy for this package"""
        hierarchy = []
        current = self
        while current:
            hierarchy.append(current)
            current = current.parent_package_id
        return list(reversed(hierarchy))

    def get_all_child_packages(self):
        """Recursively get all child packages in the hierarchy"""
        all_children = self.child_package_ids
        for child in self.child_package_ids:
            all_children += child.get_all_child_packages()
        return all_children