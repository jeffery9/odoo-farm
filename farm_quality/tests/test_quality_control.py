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

    def test_05_quality_spc_analysis(self):
        """ Test Statistical Process Control (SPC) calculation formulas and ASCII run charts """
        # 1. Create a measurement-based Quality Point with explicit tolerance limits
        measure_point = self.Point.create({
            'name': 'Milk Acidity Level (pH)',
            'test_type': 'measure',
            'norm': 50.0,
            'tolerance_min': 45.0,
            'tolerance_max': 55.0,
        })

        # 2. Create a Quality Record Book Template
        template = self.env['agri.quality.record.book.template'].create({
            'name': 'HACCP Dairy Laboratory Template',
            'book_type': 'haccp',
        })

        # 3. Add template instruction line linked to the point
        line = self.env['agri.quality.record.book.template.line'].create({
            'template_id': template.id,
            'sequence': 10,
            'name': 'Measure Acidity of Milk Lot',
            'point_id': measure_point.id,
            'instruction': 'Insert pH sensor and wait for stable reading (Target: 50.0 pH).',
        })

        # 4. Simulate historical inspection batches (5 books / checks)
        historical_measures = [48.5, 51.2, 49.8, 52.0, 47.9]
        lot = self.env['stock.lot'].create({
            'name': 'LOT-MILK-01',
            'product_id': self.Product.create({'name': 'Raw Milk', 'type': 'consu'}).id,
        })

        for i, val in enumerate(historical_measures):
            book = self.env['agri.quality.record.book'].create({
                'name': f'Daily Dairy Log Batch {i+1}',
                'book_type': 'haccp',
                'template_id': template.id,
            })
            book.action_generate_from_template()
            self.assertEqual(len(book.check_ids), 1)
            
            # Record the measurement value
            check = book.check_ids[0]
            check.write({
                'measure': val,
                'quality_state': 'pass' if (45.0 <= val <= 55.0) else 'fail',
            })

        # 5. Open and trigger SPC Analysis Wizard
        wizard = self.env['agri.quality.spc.wizard'].create({
            'template_line_id': line.id,
        })
        wizard.action_calculate()

        # 6. Assert statistical calculations
        self.assertEqual(wizard.sample_count, 5)
        
        # Mean = (48.5 + 51.2 + 49.8 + 52.0 + 47.9) / 5 = 49.88
        self.assertAlmostEqual(wizard.mean_val, 49.88, places=4)
        self.assertEqual(wizard.max_val, 52.0)
        self.assertEqual(wizard.min_val, 47.9)
        
        # Standard Deviation calculation (Sample)
        # diffs: [-1.38, 1.32, -0.08, 2.12, -1.98]
        # squared diffs: [1.9044, 1.7424, 0.0064, 4.4944, 3.9204]
        # sum of squared diffs: 12.068
        # variance: 12.068 / (5 - 1) = 3.017
        # sigma: sqrt(3.017) = 1.73696
        self.assertAlmostEqual(wizard.std_dev, 1.73695, places=4)
        
        # UCL = Mean + 3*sigma = 49.88 + 3*1.73695 = 55.0908
        self.assertAlmostEqual(wizard.ucl, 55.0908, places=3)
        # LCL = Mean - 3*sigma = 49.88 - 3*1.73695 = 44.6691
        self.assertAlmostEqual(wizard.lcl, 44.6691, places=3)

        # Cp = (55 - 45) / (6 * 1.73695) = 10 / 10.4217 = 0.9595
        self.assertAlmostEqual(wizard.cp, 0.9595, places=3)
        
        # Cpk = min((55 - 49.88) / (3*1.73695), (49.88 - 45) / (3*1.73695))
        #     = min(5.12 / 5.21085, 4.88 / 5.21085)
        #     = min(0.9825, 0.9365) = 0.9365
        self.assertAlmostEqual(wizard.cpk, 0.9365, places=3)
        self.assertIn("Marginal", wizard.cpk_status)

        # 7. Check if ASCII chart was successfully generated and contains essential keys
        self.assertTrue(wizard.spc_chart_ascii)
        self.assertIn("UCL", wizard.spc_chart_ascii)
        self.assertIn("Mean", wizard.spc_chart_ascii)
        self.assertIn("LCL", wizard.spc_chart_ascii)
        self.assertIn("*", wizard.spc_chart_ascii)  # Contains plotted data points
        print("\n=== GENERATED SPC RUN CONTROL CHART ===\n")
        print(wizard.spc_chart_ascii)
        print("\n=======================================\n")

    def test_06_quality_record_book_xlsx_export(self):
        """ Test professional GxP Excel Spreadsheet generation, dynamic formulas, formatting and downloads """
        import base64
        import io
        try:
            from openpyxl import load_workbook
        except ImportError:
            self.skipTest("openpyxl library not installed")

        # 1. Create standard points, templates and lines
        point = self.Point.create({
            'name': 'Pesticide Concentration Check',
            'test_type': 'measure',
            'norm': 12.0,
            'tolerance_min': 10.0,
            'tolerance_max': 14.0,
        })
        template = self.env['agri.quality.record.book.template'].create({
            'name': 'Standard Chemical Wash Template',
            'book_type': 'pesticide',
        })
        line = self.env['agri.quality.record.book.template.line'].create({
            'template_id': template.id,
            'sequence': 10,
            'name': 'Inspect Chemical Spray Wash',
            'point_id': point.id,
            'instruction': 'Run sprayer wash and verify pesticide concentration reads exactly 12.0 %.',
        })

        # 2. Create a Record Book
        book = self.env['agri.quality.record.book'].create({
            'name': 'Weekly Wash Log - Block C',
            'book_type': 'pesticide',
            'template_id': template.id,
        })
        book.action_generate_from_template()
        self.assertEqual(len(book.check_ids), 1)

        # 3. Enter values and complete check
        check = book.check_ids[0]
        
        # Verify related fields are properly exposed for the spreadsheet UX
        self.assertEqual(check.norm, 12.0)
        self.assertEqual(check.tolerance_min, 10.0)
        self.assertEqual(check.tolerance_max, 14.0)

        # Test spreadsheet-style dynamic onchange auto-evaluation
        check.measure = 12.35
        check._onchange_measure()
        self.assertEqual(check.quality_state, 'pass')

        check.measure = 15.6
        check._onchange_measure()
        self.assertEqual(check.quality_state, 'fail')

        # Write final passing values to commit the GxP record
        check.write({
            'measure': 12.35,
            'quality_state': 'pass',
        })

        # 4. Seal & Sign the Record Book to generate SHA-256 seal (GxP Audit)
        book.action_activate()
        book.action_lock()
        self.assertEqual(book.state, 'locked')
        self.assertTrue(book.cryptographic_signature)

        # 5. Export Spreadsheet
        action = book.action_export_spreadsheet()
        self.assertEqual(action['type'], 'ir.actions.act_url')
        self.assertIn('/web/content/', action['url'])
        self.assertIn('download=true', action['url'])

        # 6. Verify ir.attachment was successfully saved
        attachment = self.env['ir.attachment'].search([
            ('res_model', '=', 'agri.quality.record.book'),
            ('res_id', '=', book.id)
        ])
        self.assertTrue(attachment)
        self.assertEqual(attachment.mimetype, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

        # 7. Decode binary data and parse Excel using openpyxl
        file_bytes = base64.b64decode(attachment.datas)
        file_stream = io.BytesIO(file_bytes)
        
        # Load workbook in formulas-preserving mode
        wb = load_workbook(file_stream)
        ws = wb["Quality Record Book Log"]
        self.assertEqual(ws.title, "Quality Record Book Log")

        # 8. Assert Grid layout content and dynamic Excel formulas
        # Title Banner
        self.assertEqual(ws["A1"].value, "GxP QUALITY RECORD BOOK AUDIT SHEET")
        
        # Metadata values
        self.assertEqual(ws["B4"].value, book.code)
        self.assertEqual(ws["B5"].value, book.name)
        self.assertEqual(ws["B6"].value, "LOCKED")
        self.assertEqual(ws["B7"].value, book.cryptographic_signature)

        # Grid Data item (Row 11 is title row, Row 12 is first data row)
        self.assertEqual(ws["A12"].value, 1)  # Sequence
        self.assertEqual(ws["B12"].value, "Inspect Chemical Spray Wash")  # Step Name
        self.assertEqual(ws["C12"].value, "Pesticide Concentration Check")  # Target Point
        self.assertEqual(ws["F12"].value, 12.35)  # Actual numeric measure
        self.assertEqual(ws["G12"].value, "Passed")  # Evaluated Pass state

        # Statistical calculations (Dynamic Excel formulas)
        # Total checklist items (Row 14 is label, Cell B14 holds dynamic COUNTA formula)
        self.assertEqual(ws["B14"].value, "=COUNTA(B12:B12)")
        # Passed Items count (Cell B15 holds dynamic COUNTIF formula)
        self.assertEqual(ws["B15"].value, '=COUNTIF(G12:G12, "Passed")')
        # Overall Yield Rate (Cell B17 holds dynamic division formula)
        self.assertEqual(ws["B17"].value, '=B16/B15')

        # GxP Authenticated box (Cells F15/F16 holds seal hash)
        self.assertEqual(ws["F16"].value, book.cryptographic_signature)
        self.assertEqual(ws["F17"].value, "COMPLIANT")

        print("\n=== SUCCESS: EXCEL SPREADSHEET FORMULAS AND GXP ALIGNMENT VERIFIED ===\n")

    def test_07_quality_check_replicates(self):
        """ Verify US-LIMS Replicate Measurements, auto-expansion, average computation, and auto-evaluation """
        # 1. Create a quality point with 3 replicates required
        point_replicates = self.Point.create({
            'name': 'Pasteurizer Temperature Replicates',
            'test_type': 'measure',
            'norm': 72.0,
            'tolerance_min': 71.5,
            'tolerance_max': 73.0,
            'replicate_count': 3,
        })
        self.assertEqual(point_replicates.replicate_count, 3)

        # 2. Create a template pointing to this point
        template = self.env['agri.quality.record.book.template'].create({
            'name': 'Pasteurization GxP Template',
            'book_type': 'pesticide',
        })
        self.env['agri.quality.record.book.template.line'].create({
            'name': 'Check Pasteurization Outlet Temp',
            'template_id': template.id,
            'point_id': point_replicates.id,
            'instruction': 'Record 3 outlet temperature replicates after stabilizing flows.',
        })

        # 3. Create a record book and instantiate from template
        book = self.env['agri.quality.record.book'].create({
            'name': 'Pasteurizer Run #1042',
            'book_type': 'pesticide',
            'template_id': template.id,
        })
        book.action_generate_from_template()

        # 4. Verify that exactly 1 check is created and it automatically generated 3 blank measurement lines
        self.assertEqual(len(book.check_ids), 1)
        check = book.check_ids[0]
        self.assertEqual(check.replicate_count, 3)
        self.assertEqual(len(check.measure_line_ids), 3)

        # 5. Populate replicate values and verify real-time mathematical average computation
        check.measure_line_ids[0].value = 71.6
        check.measure_line_ids[1].value = 72.0
        check.measure_line_ids[2].value = 72.4

        # Trigger recompute or onchange simulation
        check._compute_measure()
        self.assertAlmostEqual(check.measure, 72.0)
        check._onchange_measure()
        self.assertEqual(check.quality_state, 'pass')

        # 6. Change one replicate to fail tolerance limit
        check.measure_line_ids[0].value = 75.2
        check._compute_measure()
        self.assertAlmostEqual(check.measure, 73.2)
        check._onchange_measure()
        self.assertEqual(check.quality_state, 'fail')

        print("\n=== SUCCESS: GXP REPLICATES MEASUREMENT AND AUTO-COMPUTATION VERIFIED ===\n")
