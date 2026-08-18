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

    def test_04_quality_record_book_templates(self):
        """ Test reusable Record Book Templates, automatic check generation, and instruction propagation """
        from odoo.exceptions import UserError

        # 1. Create standard quality points
        point1 = self.Point.create({
            'name': 'Sprayer Pressure Check',
            'test_type': 'pass_fail'
        })

        # 2. Create a Quality Record Book Template
        template = self.env['agri.quality.record.book.template'].create({
            'name': 'Pesticide Application Checklist Template',
            'book_type': 'pesticide',
            'description': 'Standard operating template for pesticide operations.',
        })

        # 3. Add instruction steps/lines to the template
        line1 = self.env['agri.quality.record.book.template.line'].create({
            'template_id': template.id,
            'sequence': 10,
            'name': 'Inspect Sprayer Pressure',
            'point_id': point1.id,
            'instruction': 'Verify pressure gauge reads <= 120 PSI before spraying.',
        })
        line2 = self.env['agri.quality.record.book.template.line'].create({
            'template_id': template.id,
            'sequence': 20,
            'name': 'Chemical Lot Verification',
            'instruction': 'Manually record and verify the EPA registration code on the chemical barrel.',
        })

        self.assertEqual(len(template.line_ids), 2)

        # 4. Create a new Quality Record Book in Draft
        book = self.env['agri.quality.record.book'].create({
            'name': 'Morning Pesticide Run - Orchard Section B',
            'book_type': 'pesticide',
            'template_id': template.id,
        })
        self.assertEqual(book.state, 'draft')
        self.assertEqual(len(book.check_ids), 0)

        # 5. Generate quality check records from the template
        book.action_generate_from_template()
        self.assertEqual(len(book.check_ids), 2)

        # 6. Verify that instructions and points are perfectly populated
        check1 = book.check_ids.filtered(lambda c: c.name == 'Inspect Sprayer Pressure')
        self.assertTrue(check1)
        self.assertEqual(check1.point_id.id, point1.id)
        self.assertEqual(check1.instruction, 'Verify pressure gauge reads <= 120 PSI before spraying.')
        self.assertEqual(check1.quality_state, 'none')

        check2 = book.check_ids.filtered(lambda c: c.name == 'Chemical Lot Verification')
        self.assertTrue(check2)
        self.assertFalse(check2.point_id)
        self.assertEqual(check2.instruction, 'Manually record and verify the EPA registration code on the chemical barrel.')
        self.assertEqual(check2.quality_state, 'none')

        # 7. GxP Validation: Test generating checks when not in Draft state
        book.action_activate()
        self.assertEqual(book.state, 'active')
        with self.assertRaises(UserError):
            book.action_generate_from_template()
