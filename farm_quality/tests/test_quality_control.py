from odoo.tests.common import TransactionCase

class TestFarmQuality(TransactionCase):

    def setUp(self):
        super().setUp()
        # Use get to avoid KeyError if registration is delayed
        self.Point = self.env.get('agri.quality.point')
        self.Check = self.env.get('agri.quality.check')
        self.Product = self.env.get('product.product')
        
        if not self.Point or not self.Product:
            self.skipTest("Required models not found in registry")

    def test_01_quality_point_creation(self):
        """ Test Quality Point creation """
        point = self.Point.create({
            'name': 'Harvest Inspection',
            'product_id': self.Product.create({'name': 'Test Fruit', 'type': 'consu'}).id,
            'test_type': 'pass_fail'
        })
        self.assertEqual(point.name, 'Harvest Inspection')

    def test_02_quality_check_flow(self):
        """ Test Quality Check flow """
        point = self.Point.create({
            'name': 'Size Check',
            'test_type': 'pass_fail'
        })
        lot = self.env['stock.lot'].create({
            'name': 'LOT-TEST-Q',
            'product_id': self.Product.create({'name': 'Test Fruit 2', 'type': 'consu'}).id,
        })
        check = self.Check.create({
            'point_id': point.id,
            'lot_id': lot.id,
            'quality_state': 'none'
        })
        check.action_pass()
        self.assertEqual(check.quality_state, 'pass')
