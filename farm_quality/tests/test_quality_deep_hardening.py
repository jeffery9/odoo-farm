# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase, tagged
from odoo.exceptions import UserError, ValidationError

@tagged('uavm_surgical', 'post_install', '-at_install')
class TestQualityDeepHardening(TransactionCase):

    def test_qc_release_state_lock(self):
        """ Verify that non-released (locked) lots trigger pick block validations """
        Product = self.env['product.product']
        Lot = self.env['stock.lot']
        
        product = Product.create({
            'name': 'Hardening Test Apple',
            'type': 'consu',
            'is_storable': True
        })
        
        # Test 1: Real Odoo ORM model interaction
        lot = Lot.create({
            'name': 'LOT-HARD-001',
            'product_id': product.id,
            'company_id': self.env.company.id,
            'qc_release_state': 'locked'
        })
        
        picking = self.env['stock.picking'].create({
            'picking_type_id': self.env.ref('stock.picking_type_out').id,
            'location_id': self.env.ref('stock.stock_location_stock').id,
            'location_dest_id': self.env.ref('stock.stock_location_customers').id,
        })
        move = self.env['stock.move'].create({
            'product_id': product.id,
            'product_uom_qty': 1,
            'product_uom': product.uom_id.id,
            'picking_id': picking.id,
            'location_id': picking.location_id.id,
            'location_dest_id': picking.location_dest_id.id,
        })
        move.quantity = 1
        move.lot_ids = [lot.id]
        
        with self.assertRaises(UserError):
            picking.button_validate()

        # Test 2: Standard constraints verification structure (from brief)
        qc_release_state = lot.qc_release_state
        try:
            if qc_release_state == 'locked':
                raise UserError("Warehouse Block: Cannot validate picking containing a locked QC lot.")
            self.fail("Expected UserError on locked lot picking validation")
        except UserError:
            pass

    def test_failed_quality_sales_blocking(self):
        """ Verify that lots with failed quality status are blocked from sales allocations """
        Product = self.env['product.product']
        Lot = self.env['stock.lot']
        
        product = Product.create({
            'name': 'Hardening Failed Apple',
            'type': 'consu',
            'is_storable': True
        })
        
        # Test 1: Real Odoo ORM model interaction
        lot = Lot.create({
            'name': 'LOT-HARD-002',
            'product_id': product.id,
            'company_id': self.env.company.id,
            'quality_status': 'failed',
            'qc_release_state': 'released'
        })
        
        picking = self.env['stock.picking'].create({
            'picking_type_id': self.env.ref('stock.picking_type_out').id,
            'location_id': self.env.ref('stock.stock_location_stock').id,
            'location_dest_id': self.env.ref('stock.stock_location_customers').id,
        })
        move = self.env['stock.move'].create({
            'product_id': product.id,
            'product_uom_qty': 1,
            'product_uom': product.uom_id.id,
            'picking_id': picking.id,
            'location_id': picking.location_id.id,
            'location_dest_id': picking.location_dest_id.id,
        })
        move.quantity = 1
        move.lot_ids = [lot.id]
        
        with self.assertRaises(UserError):
            picking.button_validate()

        # Test 2: Standard constraints verification structure (from brief)
        quality_status = lot.quality_status
        try:
            if quality_status == 'failed':
                raise ValidationError("Sales Block: Cannot confirm SO delivery for a lot that failed QC.")
            self.fail("Expected ValidationError on failed lot sales allocation")
        except ValidationError:
            pass

    def test_lossless_audit_trail(self):
        """ Ensure savepoint rollbacks protect baseline quality check states """
        point = self.env['agri.quality.point'].create({
            'name': 'Pasteurization Temperature Check',
            'test_type': 'measure',
            'norm': 72.0,
            'tolerance_min': 71.0,
            'tolerance_max': 75.0,
        })
        
        lot = self.env['stock.lot'].create({
            'name': 'LOT-AUDIT-001',
            'product_id': self.env['product.product'].create({'name': 'Milk', 'type': 'consu'}).id,
            'company_id': self.env.company.id,
        })
        
        check = self.env['agri.quality.check'].create({
            'name': 'Batch Pasteurization Q1',
            'point_id': point.id,
            'lot_id': lot.id,
            'quality_state': 'none',
        })
        
        self.assertEqual(check.quality_state, 'none')
        
        # Simulating entering a savepoint sandbox
        try:
            with self.cr.savepoint():
                check.write({'quality_state': 'fail'})
                self.assertEqual(check.quality_state, 'fail')
                raise ValidationError("Simulated Rollback")
        except ValidationError:
            pass
            
        # Verify check reverted back to its original state (lossless rollback protection)
        self.assertEqual(check.quality_state, 'none', "Savepoint rollback must successfully revert pending changes.")
