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

    def test_03_quality_record_book_lifecycle(self):
        """ Test the entire GxP lifecycle of AgriQualityRecordBook and its anti-tampering enforcement """
        from odoo.exceptions import UserError
        
        # 1. Create a quality record book
        book = self.env['agri.quality.record.book'].create({
            'name': 'Pesticide Application Record Book 2026',
            'book_type': 'pesticide',
        })
        self.assertEqual(book.state, 'draft')
        self.assertTrue(book.code.startswith('RB'))

        # 2. Create a check and associate it
        point = self.Point.create({
            'name': 'Pesticide Level',
            'test_type': 'pass_fail'
        })
        lot = self.env['stock.lot'].create({
            'name': 'LOT-TEST-P',
            'product_id': self.Product.create({'name': 'Test Apple', 'type': 'consu'}).id,
        })
        check = self.Check.create({
            'point_id': point.id,
            'lot_id': lot.id,
            'record_book_id': book.id,
            'quality_state': 'none'
        })
        self.assertEqual(check.record_book_id.id, book.id)

        # 3. Activate the book
        book.action_activate()
        self.assertEqual(book.state, 'active')

        # 4. Seal & sign the book (GxP)
        book.action_lock()
        self.assertEqual(book.state, 'locked')
        self.assertTrue(book.cryptographic_signature)
        self.assertTrue(book.signature_date)

        # 5. GxP Anti-Tampering: attempt to modify locked book should raise UserError
        with self.assertRaises(UserError):
            book.name = "Tampered Name"

        # 6. GxP Anti-Tampering: attempt to modify checks of locked book should raise UserError
        with self.assertRaises(UserError):
            check.measure = 12.5

        # 7. GxP Anti-Tampering: attempt to delete checks of locked book should raise UserError
        with self.assertRaises(UserError):
            check.unlink()

        # 8. GxP Anti-Tampering: attempt to delete locked book should raise UserError
        with self.assertRaises(UserError):
            book.unlink()
