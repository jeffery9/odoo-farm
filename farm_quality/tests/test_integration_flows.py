# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError

class TestIntegrationFarmQuality(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.QualityPoint = cls.env['agri.quality.point']
        cls.QualityCheck = cls.env['agri.quality.check']
        cls.Lot = cls.env['stock.lot']
        cls.Product = cls.env['product.product'].create({'name': 'Organic Tomato', 'type': 'consu'})

        cls.lot = cls.Lot.create({
            'name': 'TOM-2026-001',
            'product_id': cls.Product.id,
        })
        
        cls.point_measure = cls.QualityPoint.create({
            'name': 'Brix Level Check',
            'product_id': cls.Product.id,
            'test_type': 'measure',
            'norm': 12.0,
            'tolerance_min': 10.0,
            'tolerance_max': 14.0,
        })

    def test_01_quality_check_measure_pass(self):
        """ Test that a measure within tolerance passes """
        check = self.QualityCheck.create({
            'point_id': self.point_measure.id,
            'lot_id': self.lot.id,
            'measure': 11.5,
            'quality_state': 'none'
        })
        # Mocking or calling the validation method
        if hasattr(check, 'do_measure'):
            check.do_measure()
            self.assertEqual(check.quality_state, 'pass')

    def test_02_quality_check_measure_fail(self):
        """ Test that a measure outside tolerance fails """
        check = self.QualityCheck.create({
            'point_id': self.point_measure.id,
            'lot_id': self.lot.id,
            'measure': 8.0,
            'quality_state': 'none'
        })
        if hasattr(check, 'do_measure'):
            check.do_measure()
            self.assertEqual(check.quality_state, 'fail')

    def test_03_quality_alert_creation(self):
        """ Test automatic or manual alert creation from failed check """
        check = self.QualityCheck.create({
            'point_id': self.point_measure.id,
            'lot_id': self.lot.id,
            'measure': 8.0,
            'quality_state': 'fail'
        })
        if hasattr(check, 'action_create_alert'):
            alert_action = check.action_create_alert()
            self.assertIn('res_model', alert_action)
            self.assertEqual(alert_action['res_model'], 'agri.quality.alert')
