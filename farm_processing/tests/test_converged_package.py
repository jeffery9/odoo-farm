# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase, tagged
from odoo.exceptions import ValidationError

@tagged('post_install', '-at_install')
class TestConvergedPackage(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(TestConvergedPackage, cls).setUpClass()
        # Retrieve necessary models
        cls.Location = cls.env['stock.location']
        cls.Product = cls.env['product.product']
        cls.Lot = cls.env['stock.lot']
        cls.StockPackage = cls.env['stock.package']
        cls.FarmPackage = cls.env['farm.package']
        cls.FarmPackageLevel = cls.env['farm.package.level']
        cls.StockMove = cls.env['stock.move']

        # Create basic levels
        cls.level_bottle = cls.FarmPackageLevel.create({
            'name': 'Bottle',
            'code': 'BTL'
        })
        cls.level_case = cls.FarmPackageLevel.create({
            'name': 'Case',
            'code': 'CSE'
        })

        # Create sample product and lot
        cls.product = cls.Product.create({
            'name': 'Estate Red Wine',
            'type': 'consu',
            'tracking': 'lot'
        })
        cls.lot = cls.Lot.create({
            'name': 'WINE-2026-001',
            'product_id': cls.product.id
        })

        # Create converged locations
        cls.loc_cellar = cls.Location.create({
            'name': 'Cellar Room A',
            'usage': 'internal',
            'location_type': 'barn',
            'is_land_parcel': False
        })
        cls.loc_shipping = cls.Location.create({
            'name': 'Shipping Bay 1',
            'usage': 'internal',
            'location_type': 'processing',
            'is_land_parcel': False
        })

    def test_farm_package_commercial_fields(self):
        """ Verify farm.package acts as a static commercial package registry pointing to stock.location """
        # Create a static commercial package in Cellar Room A
        pkg = self.FarmPackage.create({
            'name': 'FP-BTL-001',
            'package_level_id': self.level_bottle.id,
            'product_id': self.product.id,
            'lot_id': self.lot.id,
            'quantity': 0.75,
            'location_id': self.loc_cellar.id
        })

        self.assertEqual(pkg.name, 'FP-BTL-001')
        self.assertEqual(pkg.location_id, self.loc_cellar)
        self.assertEqual(pkg.product_id, self.product)
        self.assertEqual(pkg.lot_id, self.lot)
        self.assertEqual(pkg.quantity, 0.75)

    def test_location_synchronization_via_stock_move(self):
        """ Verify that moving a stock.package automatically updates its associated farm.package's location """
        # 1. Create a dynamic logistics stock.package
        stock_pkg = self.StockPackage.create({
            'name': 'LPN-CASE-999'
        })

        # 2. Create a static farm.package registered under that stock.package in the Cellar
        farm_pkg = self.FarmPackage.create({
            'name': 'FP-CSE-001',
            'package_level_id': self.level_case.id,
            'product_id': self.product.id,
            'lot_id': self.lot.id,
            'quantity': 12.0,
            'location_id': self.loc_cellar.id,
            'stock_package_id': stock_pkg.id
        })

        # Verify initial state
        self.assertEqual(farm_pkg.location_id, self.loc_cellar)
        self.assertEqual(farm_pkg.stock_package_id, stock_pkg)

        # 3. Create a stock picking and move
        picking_type = self.env['stock.picking.type'].search([('code', '=', 'internal')], limit=1)
        if not picking_type:
            picking_type = self.env['stock.picking.type'].search([], limit=1)

        picking = self.env['stock.picking'].create({
            'picking_type_id': picking_type.id,
            'location_id': self.loc_cellar.id,
            'location_dest_id': self.loc_shipping.id,
        })

        move = self.StockMove.create({
            'product_id': self.product.id,
            'product_uom_qty': 12.0,
            'product_uom': self.product.uom_id.id,
            'picking_id': picking.id,
            'location_id': self.loc_cellar.id,
            'location_dest_id': self.loc_shipping.id,
        })
        
        # Confirm picking
        picking.action_confirm()
        picking.action_assign()
        
        # Setup move line
        move_line = self.env['stock.move.line'].search([('move_id', '=', move.id)], limit=1)
        if move_line:
            move_line.write({
                'quantity': 12.0,
                'package_id': stock_pkg.id,
                'result_package_id': stock_pkg.id,
                'lot_id': self.lot.id
            })
        else:
            self.env['stock.move.line'].create({
                'move_id': move.id,
                'picking_id': picking.id,
                'product_id': self.product.id,
                'product_uom_id': self.product.uom_id.id,
                'quantity': 12.0,
                'location_id': self.loc_cellar.id,
                'location_dest_id': self.loc_shipping.id,
                'package_id': stock_pkg.id,
                'result_package_id': stock_pkg.id,
                'lot_id': self.lot.id
            })

        # Validate the picking
        picking.button_validate()

        # 4. Assert that the static farm.package location was automatically synchronized to the destination location!
        farm_pkg.invalidate_recordset()
        self.assertEqual(farm_pkg.location_id, self.loc_shipping)
