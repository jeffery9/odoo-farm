# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
import hashlib

class TestEpic038(TransactionCase):
    """ Agri-Quality & Inspection [US-038] """

    def setUp(self):
        super(TestEpic038, self).setUp()
        self.Product = self.env['product.product']
        self.Lot = self.env['stock.lot']
        self.QCPoint = self.env['agri.quality.point']
        self.QCCheck = self.env['agri.quality.check']
        
        self.apple = self.Product.create({'name': 'Organic Apple', 'type': 'consu', 'is_storable': True})
        self.lot_01 = self.Lot.create({'name': 'LOT-APP-001', 'product_id': self.apple.id, 'company_id': self.env.company.id})

    def test_01_define_quality_inspection_points_and_tolerance_ranges(self):
        """ Verify bilingual standard definitions [US-038-01] """
        point = self.QCPoint.create({
            'name': 'Brix Level / 含糖量',
            'product_id': self.apple.id,
            'test_type': 'measure',
            'norm': 12.0,
            'tolerance_min': 10.0,
            'tolerance_max': 15.0
        })
        self.assertEqual(point.name, 'Brix Level / 含糖量')
        self.assertEqual(point.tolerance_min, 10.0)

    def test_02_automated_quality_check_trigger_and_lot_locking(self):
        """ Verify lot locking upon production completion [US-038-02] """
        self.assertEqual(self.lot_01.qc_release_state, 'locked')
        
        point = self.QCPoint.create({
            'name': 'Visual Inspection',
            'product_id': self.apple.id,
            'test_type': 'pass_fail'
        })
        check = self.QCCheck.create({
            'point_id': point.id,
            'lot_id': self.lot_01.id
        })
        check.action_pass()
        self.assertEqual(self.lot_01.quality_status, 'passed')
        
        self.lot_01.action_qc_release()
        self.assertEqual(self.lot_01.qc_release_state, 'released')

    def test_04_handling_of_failed_quality_inspections_and_sales_blocking(self):
        """ Verify mandatory approval flow for failed QC [US-038-04] """
        point = self.QCPoint.create({
            'name': 'Pesticide Residue',
            'product_id': self.apple.id,
            'test_type': 'measure',
            'tolerance_min': 0,
            'tolerance_max': 0.01
        })
        check = self.QCCheck.create({
            'point_id': point.id,
            'lot_id': self.lot_01.id,
            'measure': 0.05
        })
        check.action_done()
        self.assertEqual(check.quality_state, 'fail')
        self.assertEqual(self.lot_01.quality_status, 'failed')
        
        # Verify sales blocking logic
        picking = self.env['stock.picking'].create({
            'picking_type_id': self.env.ref('stock.picking_type_out').id,
            'location_id': self.env.ref('stock.stock_location_stock').id,
            'location_dest_id': self.env.ref('stock.stock_location_customers').id,
        })
        move = self.env['stock.move'].create({
            'product_id': self.apple.id,
            'product_uom_qty': 1,
            'product_uom': self.apple.uom_id.id,
            'picking_id': picking.id,
            'location_id': picking.location_id.id,
            'location_dest_id': picking.location_dest_id.id,
        })
        move.quantity = 1
        move.lot_ids = [self.lot_01.id]
        
        with self.assertRaises(UserError):
            picking.button_validate()

    def test_09_digital_quality_fingerprint_generation_and_valuation_link(self):
        """ Verify SHA-256 hash generation for quality results [US-038-09] """
        point = self.QCPoint.create({
            'name': 'Weight Check',
            'product_id': self.apple.id,
            'test_type': 'measure',
            'tolerance_min': 100,
            'tolerance_max': 200
        })
        check = self.QCCheck.create({
            'point_id': point.id,
            'lot_id': self.lot_01.id,
            'measure': 150
        })
        check.action_pass()
        self.assertTrue(check.blockchain_hash)
        self.assertEqual(len(check.blockchain_hash), 64) # SHA-256 is 64 chars
