# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta
import json

class TestFarmProcessing(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.user_admin = cls.env.ref('base.user_admin')
        cls.product_tmpl_product = cls.env.ref('product.product_product_template')
        cls.product_product = cls.env.ref('product.product_product')
        cls.stock_location_stock = cls.env.ref('stock.stock_location_stock')
        cls.partner_agrolait = cls.env.ref('base.res_partner_agrolait')

        # Create basic SC categories
        cls.sc_cat_juice = cls.env['farm.sc.category'].create({'name': 'Fruit Juice', 'code': 'JUICE'})
        cls.sc_cat_other = cls.env['farm.sc.category'].create({'name': 'Other Food', 'code': 'OTHER'})

        # Create basic products for testing
        cls.product_apple = cls.env['product.product'].create({
            'name': 'Apple',
            'type': 'product',
            'default_code': 'APP',
            'tracking': 'lot',
            'is_agri_product': True,
            'npk_n': 0.1,
            'npk_p': 0.05,
            'npk_k': 0.15,
        })
        cls.product_apple_sweet = cls.env['product.product'].create({
            'name': 'Sweet Apple',
            'type': 'product',
            'default_code': 'APP_SWEET',
            'tracking': 'lot',
            'is_agri_product': True,
            'npk_n': 0.08,
            'npk_p': 0.04,
            'npk_k': 0.12,
        })
        cls.product_juice = cls.env['product.product'].create({
            'name': 'Apple Juice',
            'type': 'product',
            'default_code': 'AJ',
            'tracking': 'lot',
            'is_agri_product': True,
            'sc_category_ids': [(6, 0, [cls.sc_cat_juice.id])],
        })
        cls.product_sugar = cls.env['product.product'].create({
            'name': 'Sugar',
            'type': 'product',
            'default_code': 'SUGAR',
            'tracking': 'none',
        })
        cls.product_pectin = cls.env['product.product'].create({
            'name': 'Pectin',
            'type': 'product',
            'default_code': 'PECT',
            'tracking': 'none',
        })
        cls.product_apple_pulp = cls.env['product.product'].create({
            'name': 'Apple Pulp',
            'type': 'product',
            'default_code': 'APULP',
            'tracking': 'lot',
            'is_agri_product': True,
        })
        cls.product_crate = cls.env['product.product'].create({
            'name': 'Crate',
            'type': 'product',
            'default_code': 'CRATE',
            'tracking': 'none',
        })
        cls.product_bottle = cls.env['product.product'].create({
            'name': 'Bottle',
            'type': 'product',
            'default_code': 'BOTTLE',
            'tracking': 'none',
        })
        cls.product_label = cls.env['product.product'].create({
            'name': 'Label',
            'type': 'product',
            'default_code': 'LABEL',
            'tracking': 'none',
        })

        # Create a packaging type
        cls.packaging_bottle_1l = cls.env['product.packaging'].create({
            'name': 'Bottle (1L)',
            'product_id': cls.product_juice.id,
            'qty': 1,
        })
        cls.packaging_crate_12 = cls.env['product.packaging'].create({
            'name': 'Crate (12 Bottles)',
            'product_id': cls.product_juice.id,
            'qty': 12,
        })

        # Create BoMs
        cls.bom_juice_seasonal = cls.env['mrp.bom'].create({
            'product_tmpl_id': cls.product_juice.product_tmpl_id.id,
            'product_qty': 100.0,
            'type': 'normal',
            'is_agri_processing': True,
            'is_seasonal': True,
            'area_to_treat': 5.0, # Default area in BOM
            'dilution_ratio': 10.0,
            'solution_volume_per_hectare': 20.0,
            'bom_line_ids': [
                (0, 0, {'product_id': cls.product_apple.id, 'product_qty': 200.0}),
                (0, 0, {'product_id': cls.product_sugar.id, 'product_qty': 10.0}),
                (0, 0, {'product_id': cls.product_pectin.id, 'product_qty': 2.0}),
            ],
            'byproduct_ids': [
                (0, 0, {'product_id': cls.product_apple_pulp.id, 'product_qty': 50.0, 'cost_share': 20.0}),
            ],
            'packaging_line_ids': [
                (0, 0, {'product_id': cls.product_juice.id, 'packaging_id': cls.packaging_bottle_1l.id, 'quantity': 100}),
                (0, 0, {'product_id': cls.product_crate.id, 'packaging_id': False, 'quantity': 8}), # Example: 8 crates needed
            ],
            'loss_tolerance_percentage': 5.0, # 5% allowed loss
        })

        cls.bom_juice_non_seasonal = cls.env['mrp.bom'].create({
            'product_tmpl_id': cls.product_juice.product_tmpl_id.id,
            'product_qty': 50.0,
            'type': 'normal',
            'is_agri_processing': True,
            'is_seasonal': False,
            'bom_line_ids': [
                (0, 0, {'product_id': cls.product_apple.id, 'product_qty': 100.0}),
            ],
        })

        # Create some stock for components
        cls.env['stock.quant']._update_available_quantity(cls.product_apple, cls.stock_location_stock, 500.0)
        cls.env['stock.quant']._update_available_quantity(cls.product_sugar, cls.stock_location_stock, 100.0)
        cls.env['stock.quant']._update_available_quantity(cls.product_pectin, cls.stock_location_stock, 50.0)

        # Create a default rejection reason
        cls.rejection_reason_defect = cls.env['mrp.production.rejection.reason'].create({
            'name': 'Product Defect',
            'description': 'Product did not meet quality standards due to defects.',
        })

        # Create an active SC license
        cls.sc_license = cls.env['farm.sc.license'].create({
            'name': 'SC123456789',
            'expiry_date': fields.Date.today() + timedelta(days=365),
            'category_ids': [(6, 0, [cls.sc_cat_juice.id])],
        })

    def test_01_create_agri_processing_mo(self):
        """ Test creation of an agri-processing MO from a seasonal BOM """
        mo = self.env['mrp.production'].create({
            'product_id': self.product_juice.id,
            'product_qty': 100.0,
            'bom_id': self.bom_juice_seasonal.id,
        })
        self.assertTrue(mo.exists())
        self.assertTrue(mo.is_agri_processing, "MO should be marked as agri-processing")
        self.assertEqual(mo.area_to_treat, self.bom_juice_seasonal.area_to_treat, "Area to treat should be inherited from BOM")
        self.assertEqual(mo.dilution_ratio, self.bom_juice_seasonal.dilution_ratio, "Dilution ratio should be inherited from BOM")
        self.assertEqual(mo.solution_volume_per_hectare, self.bom_juice_seasonal.solution_volume_per_hectare, "Solution volume should be inherited from BOM")
        self.assertEqual(mo.total_solution_volume, mo.area_to_treat * mo.solution_volume_per_hectare, "Total solution volume should be computed correctly")
        self.assertTrue(mo.created_from_seasonal_bom, "MO should be marked as created from seasonal BOM")
        self.assertEqual(len(mo.packaging_line_ids), 2, "Packaging lines should be inherited from BOM")
        self.assertEqual(mo.packaging_line_ids[0].packaging_id, self.packaging_bottle_1l)

    def test_02_agri_processing_mo_non_seasonal_bom_restriction(self):
        """ Test restriction for agri-processing MOs not created from a seasonal BOM """
        mo = self.env['mrp.production'].create({
            'product_id': self.product_juice.id,
            'product_qty': 100.0,
            'bom_id': self.bom_juice_non_seasonal.id, # This is an agri-processing BOM but not seasonal
        })
        mo.onchange_bom_id() # Trigger onchange to update fields

        # Attempt to confirm, which should trigger the validation
        with self.assertRaises(UserError, msg="Should prevent confirmation if not from seasonal BOM"):
            mo.button_mark_as_todo()

    def test_03_recalculate_quantities_button(self):
        """ Test the recalculate quantities button functionality """
        mo = self.env['mrp.production'].create({
            'product_id': self.product_juice.id,
            'product_qty': 100.0,
            'bom_id': self.bom_juice_seasonal.id,
            'area_to_treat': 5.0,
        })
        mo.onchange_bom_id()
        mo.product_qty = 120.0 # Manually change qty to test recalculation
        mo.area_to_treat = 6.0 # Manually change area to test recalculation

        mo.button_recalculate_quantities()
        # Assuming theoretical yield per hectare is 100.0/5.0 = 20.0 (from BOM)
        # So for 6.0 ha, product_qty should be 6.0 * 20.0 = 120.0
        self.assertEqual(mo.area_to_treat, 6.0, "Area to treat should be 6.0 after manual change")
        self.assertEqual(mo.product_qty, 120.0, "Product quantity should be 120.0 after recalculation based on 6ha")

        # Verify packaging lines are re-inherited
        self.assertEqual(len(mo.packaging_line_ids), 2, "Packaging lines should be re-inherited after recalculation")

    def test_04_byproduct_cost_share(self):
        """ Test byproduct cost share calculation and constraint """
        mo = self.env['mrp.production'].create({
            'product_id': self.product_juice.id,
            'product_qty': 100.0,
            'bom_id': self.bom_juice_seasonal.id,
        })
        self.assertEqual(mo.byproduct_cost_share_total, 20.0, "Byproduct cost share total should be 20%")
        self.assertEqual(mo.finished_product_cost_share, 80.0, "Finished product cost share should be 80%")

        # Test constraint for > 100%
        with self.assertRaises(ValidationError, msg="Should not allow byproduct cost share > 100%"):
            self.bom_juice_seasonal.byproduct_ids[0].cost_share = 110.0
            mo._compute_byproduct_cost_share_total() # Manually recompute
            mo._check_byproduct_cost_share_total() # Manually check constraint

        self.bom_juice_seasonal.byproduct_ids[0].cost_share = 20.0 # Reset for other tests

    def test_05_quality_check_flow(self):
        """ Test the quality check and quality gate flow """
        mo = self.env['mrp.production'].create({
            'product_id': self.product_juice.id,
            'product_qty': 100.0,
            'bom_id': self.bom_juice_seasonal.id,
        })
        mo.button_mark_as_todo()
        mo.action_confirm()
        self.assertEqual(mo.quality_gate_status, 'pending', "Quality gate status should be pending after confirmation")

        # Perform a passing quality check
        self.env['mrp.production.quality.check'].create({
            'production_id': mo.id,
            'check_type': 'visual',
            'result': 'pass',
            'notes': 'Looks good.',
        })
        self.assertEqual(mo.quality_gate_status, 'approved', "Quality gate status should be approved after passing check")

        # Attempt to mark done
        mo.button_mark_done()
        self.assertEqual(mo.state, 'done', "MO should be marked as done if quality gate approval")

    def test_06_rejection_wizard(self):
        """ Test MO rejection through the wizard and activity creation """
        mo = self.env['mrp.production'].create({
            'product_id': self.product_juice.id,
            'product_qty': 100.0,
            'bom_id': self.bom_juice_seasonal.id,
        })
        mo.button_mark_as_todo()
        mo.action_confirm()

        # Simulate rejection through the wizard
        rejection_wizard = self.env['mrp.production.rejection.wizard'].create({
            'production_id': mo.id,
            'rejection_reason_id': self.rejection_reason_defect.id,
            'notes': 'Too many defects to be salvaged.',
        })
        rejection_wizard.action_reject()
        self.assertEqual(mo.quality_gate_status, 'rejected', "MO should be rejected")
        self.assertEqual(mo.rejection_reason_id, self.rejection_reason_defect, "Rejection reason should be set")

        # Verify activity creation
        activity = self.env['mail.activity'].search([
            ('res_id', '=', mo.id),
            ('res_model', '=', 'mrp.production'),
            ('summary', 'ilike', 'Rejected')
        ], limit=1)
        self.assertTrue(activity, "Activity should be created for rejected MO")

    def test_07_rework_wizard(self):
        """ Test rework MO creation through the wizard and activity creation """
        mo = self.env['mrp.production'].create({
            'product_id': self.product_juice.id,
            'product_qty': 100.0,
            'bom_id': self.bom_juice_seasonal.id,
        })
        mo.button_mark_as_todo()
        mo.action_confirm()
        mo.action_rework_quality_gate() # Manually set to rework for test

        # Verify activity creation for rework
        activity = self.env['mail.activity'].search([
            ('res_id', '=', mo.id),
            ('res_model', '=', 'mrp.production'),
            ('summary', 'ilike', 'Rework Required')
        ], limit=1)
        self.assertTrue(activity, "Activity should be created for rework required MO")

        rework_wizard = self.env['mrp.production.rework.wizard'].create({
            'original_production_id': mo.id,
            'product_id': mo.product_id.id,
            'product_qty': 50.0,
            'bom_id': mo.bom_id.id,
            'notes': 'Reworking half of the batch.',
        })
        rework_wizard.action_create_rework_mo()

        self.assertTrue(mo.rework_mo_id, "Rework MO should be linked to original MO")
        self.assertEqual(mo.rework_mo_id.product_qty, 50.0, "Rework MO should have specified quantity")

    def test_08_packaging_creation_and_lot_association(self):
        """ Test creation of packages and association with product lots """
        mo = self.env['mrp.production'].create({
            'product_id': self.product_juice.id,
            'product_qty': 100.0,
            'bom_id': self.bom_juice_seasonal.id,
        })
        mo.button_mark_as_todo()
        mo.action_confirm()

        # Simulate production
        mo.qty_producing = 100.0
        mo.button_mark_done() # This will call _post_process_production

        self.assertTrue(mo.produced_package_id, "Produced package should be created")
        
        # Create a lot for the finished product
        lot_juice = self.env['stock.lot'].create({
            'name': 'JUICE-LOT-001',
            'product_id': self.product_juice.id,
            'company_id': self.env.company.id,
        })

        # Manually link the lot to the produced package for testing main_produced_package_id
        mo.produced_package_id.quant_ids.filtered(lambda q: q.product_id == self.product_juice).lot_id = lot_juice

        # Recompute main_produced_package_id
        mo._compute_main_produced_package()
        self.assertEqual(mo.main_produced_package_id, mo.produced_package_id, "Main produced package should be set")

    def test_09_substitute_components_wizard(self):
        """ Test substitute components wizard """
        mo = self.env['mrp.production'].create({
            'product_id': self.product_juice.id,
            'product_qty': 100.0,
            'bom_id': self.bom_juice_seasonal.id,
        })
        mo.button_mark_as_todo()
        mo.action_confirm()

        # Get initial component (apple)
        apple_move = mo.move_raw_ids.filtered(lambda m: m.product_id == self.product_apple)
        initial_apple_qty = apple_move.product_qty

        # Create a substitute product
        product_apple_sub = self.env['product.product'].create({
            'name': 'Green Apple (Substitute)',
            'type': 'product',
            'default_code': 'GAPP',
            'tracking': 'lot',
            'is_agri_product': True,
        })
        self.env['stock.quant']._update_available_quantity(product_apple_sub, self.stock_location_stock, 200.0)

        # Open and fill the substitute wizard
        sub_wizard = self.env['mrp.production.substitute.wizard'].create({
            'production_id': mo.id,
            'substitute_line_ids': [(0, 0, {
                'original_product_id': self.product_apple.id,
                'substitute_product_id': product_apple_sub.id,
                'quantity_to_substitute': 50.0, # Substitute 50 units of apple
            })]
        })
        sub_wizard.action_substitute_components()

        # Verify component move is updated
        new_apple_move = mo.move_raw_ids.filtered(lambda m: m.product_id == self.product_apple)
        new_sub_apple_move = mo.move_raw_ids.filtered(lambda m: m.product_id == product_apple_sub)

        self.assertEqual(new_apple_move.product_qty, initial_apple_qty - 50.0, "Original apple qty should be reduced")
        self.assertEqual(new_sub_apple_move.product_qty, 50.0, "Substitute apple qty should be added")

    def test_10_lot_npk_content_computation(self):
        """ Test NPK content computation for lots based on consumed components """
        mo = self.env['mrp.production'].create({
            'product_id': self.product_juice.id,
            'product_qty': 100.0,
            'bom_id': self.bom_juice_seasonal.id,
        })
        mo.button_mark_as_todo()
        mo.action_confirm()

        # Create a lot for the main input (apple) with specific NPK
        lot_apple = self.env['stock.lot'].create({
            'name': 'APPLE-LOT-001',
            'product_id': self.product_apple.id,
            'company_id': self.env.company.id,
            'npk_n': 0.2, # Override default for test
            'npk_p': 0.1,
            'npk_k': 0.3,
        })
        # Assign lot to consumed move line
        mo.move_raw_ids.filtered(lambda m: m.product_id == self.product_apple).move_line_ids.lot_id = lot_apple

        mo.qty_producing = 100.0
        mo.button_mark_done()

        # Check the NPK of the produced lot
        produced_lot = mo.finished_move_line_ids.filtered(lambda ml: ml.product_id == self.product_juice and ml.lot_id).lot_id
        self.assertTrue(produced_lot, "A lot should be created for the produced juice")
        self.assertAlmostEqual(produced_lot.npk_n, lot_apple.npk_n, places=5)

    def test_11_recall_wizard(self):
        """ Test recall wizard functionality """
        product_recalled = self.env['product.product'].create({
            'name': 'Recalled Product',
            'type': 'product',
            'tracking': 'lot',
        })
        lot_recalled = self.env['stock.lot'].create({
            'name': 'LOT-RECALL-001',
            'product_id': product_recalled.id,
            'company_id': self.env.company.id,
        })
        self.env['stock.quant']._update_available_quantity(product_recalled, self.stock_location_stock, 100.0, lot_id=lot_recalled)

        recall_wizard = self.env['mrp.production.recall.wizard'].create({
            'name': 'Urgent Product Recall',
            'recall_line_ids': [(0, 0, {
                'product_id': product_recalled.id,
                'lot_id': lot_recalled.id,
                'quantity': 50.0,
            })]
        })
        recall_wizard.action_initiate_recall()

        picking = self.env['stock.picking'].search([
            ('origin', '=', 'Product Recall: Urgent Product Recall'),
            ('state', 'not in', ['draft', 'cancel'])
        ], limit=1)
        self.assertTrue(picking, "A stock picking should be created for the recall")

    def test_22_quantity_balance_validation(self):
        """ Test the quantity balance validation during MO completion. """
        mo = self.env['mrp.production'].create({
            'product_id': self.product_juice.id,
            'product_qty': 100.0,
            'bom_id': self.bom_juice_seasonal.id,
        })
        mo.button_mark_as_todo()
        mo.action_confirm()

        for move in mo.move_raw_ids:
            if move.product_id == self.product_apple:
                move.quantity_done = 200.0
            elif move.product_id == self.product_sugar:
                move.quantity_done = 10.0
            elif move.product_id == self.product_pectin:
                move.quantity_done = 2.0
        
        # Test Case 1: Within allowed loss tolerance
        mo.qty_producing = 98.0
        for move_line in mo.finished_move_line_ids:
            if move_line.product_id == self.product_juice:
                move_line.quantity_done = 98.0
            elif move_line.product_id == self.product_apple_pulp:
                move_line.quantity_done = 50.0

        mo.quality_gate_status = 'approved'
        mo.button_mark_done()
        self.assertEqual(mo.state, 'done')

        # Test Case 2: Exceeding allowed loss tolerance
        mo_exceed = self.env['mrp.production'].create({
            'product_id': self.product_juice.id,
            'product_qty': 100.0,
            'bom_id': self.bom_juice_seasonal.id,
        })
        mo_exceed.button_mark_as_todo()
        mo_exceed.action_confirm()

        for move in mo_exceed.move_raw_ids:
            if move.product_id == self.product_apple:
                move.quantity_done = 200.0
            elif move.product_id == self.product_sugar:
                move.quantity_done = 10.0
            elif move.product_id == self.product_pectin:
                move.quantity_done = 2.0
        
        mo_exceed.qty_producing = 80.0
        for move_line in mo_exceed.finished_move_line_ids:
            if move_line.product_id == self.product_juice:
                move_line.quantity_done = 80.0
            elif move_line.product_id == self.product_apple_pulp:
                move_line.quantity_done = 50.0

        mo_exceed.quality_gate_status = 'approved'
        with self.assertRaisesRegex(UserError, "Quantity balance check failed!"):
            mo_exceed.button_mark_done()

    def test_23_lot_inheritance_traceability(self):
        """ Test that produced lots correctly inherit parent_lot_ids. """
        lot_apple_1 = self.env['stock.lot'].create({
            'name': 'APPLE-LOT-001',
            'product_id': self.product_apple.id,
            'company_id': self.env.company.id,
        })
        mo_trace = self.env['mrp.production'].create({
            'product_id': self.product_juice.id,
            'product_qty': 100.0,
            'bom_id': self.bom_juice_seasonal.id,
        })
        mo_trace.button_mark_as_todo()
        mo_trace.action_confirm()

        for move in mo_trace.move_raw_ids:
            if move.product_id == self.product_apple:
                move.move_line_ids.create({
                    'move_id': move.id,
                    'product_id': self.product_apple.id,
                    'lot_id': lot_apple_1.id,
                    'qty_done': 200.0,
                    'location_id': move.location_id.id,
                    'location_dest_id': move.location_dest_id.id,
                })
                move.quantity_done = 200.0

        mo_trace.qty_producing = 100.0
        produced_lot_juice = self.env['stock.lot'].create({
            'name': 'PROD-JUICE-LOT-001',
            'product_id': self.product_juice.id,
            'company_id': self.env.company.id,
        })
        for move_line in mo_trace.finished_move_line_ids:
            if move_line.product_id == self.product_juice:
                move_line.lot_id = produced_lot_juice.id
                move_line.quantity_done = 100.0

        mo_trace.quality_gate_status = 'approved'
        mo_trace.button_mark_done()
        self.assertIn(lot_apple_1, produced_lot_juice.parent_lot_ids)

    def test_24_expired_component_lot_hard_block(self):
        """ Test the hard-block for using expired component lots. """
        today = fields.Date.today()
        expired_apple_lot = self.env['stock.lot'].create({
            'name': 'EXPIRED-APPLE-LOT-001',
            'product_id': self.product_apple.id,
            'company_id': self.env.company.id,
            'expiration_date': today - timedelta(days=1),
        })
        self.env['stock.quant']._update_available_quantity(self.product_apple, self.stock_location_stock, 100.0, lot_id=expired_apple_lot)

        mo = self.env['mrp.production'].create({
            'product_id': self.product_juice.id,
            'product_qty': 10.0,
            'bom_id': self.bom_juice_seasonal.id,
        })
        mo.button_mark_as_todo()
        apple_move = mo.move_raw_ids.filtered(lambda m: m.product_id == self.product_apple)
        self.env['stock.move.line'].create({
            'move_id': apple_move.id,
            'product_id': self.product_apple.id,
            'lot_id': expired_apple_lot.id,
            'qty_done': 10.0,
            'location_id': apple_move.location_id.id,
            'location_dest_id': apple_move.location_dest_id.id,
        })
        apple_move.quantity_done = 10.0

        with self.assertRaisesRegex(UserError, "Expired component lot detected!"):
            mo.action_confirm()

    def test_25_terroir_attributes_weighting(self):
        """ Test terroir attributes weighting. """
        lot_apple_regular = self.env['stock.lot'].create({
            'name': 'APPLE-REG-LOT',
            'product_id': self.product_apple.id,
            'company_id': self.env.company.id,
            'terroir_attributes_json': json.dumps({"sweetness": 7.0, "region": "North"}),
        })
        lot_apple_sweet = self.env['stock.lot'].create({
            'name': 'APPLE-SWT-LOT',
            'product_id': self.product_apple_sweet.id,
            'company_id': self.env.company.id,
            'terroir_attributes_json': json.dumps({"sweetness": 9.0, "region": "South"}),
        })

        bom_juice_blended = self.env['mrp.bom'].create({
            'product_tmpl_id': self.product_juice.product_tmpl_id.id,
            'product_qty': 100.0,
            'type': 'normal',
            'is_agri_processing': True,
            'is_seasonal': True,
            'bom_line_ids': [
                (0, 0, {'product_id': self.product_apple.id, 'product_qty': 100.0}),
                (0, 0, {'product_id': self.product_apple_sweet.id, 'product_qty': 200.0}),
            ],
            'loss_tolerance_percentage': 10.0,
        })

        mo = self.env['mrp.production'].create({
            'product_id': self.product_juice.id,
            'product_qty': 100.0,
            'bom_id': bom_juice_blended.id,
        })
        mo.button_mark_as_todo()
        mo.action_confirm()

        for move in mo.move_raw_ids:
            if move.product_id == self.product_apple:
                self.env['stock.move.line'].create({
                    'move_id': move.id, 'product_id': self.product_apple.id, 'lot_id': lot_apple_regular.id, 'qty_done': 100.0,
                    'location_id': move.location_id.id, 'location_dest_id': move.location_dest_id.id,
                })
                move.quantity_done = 100.0
            elif move.product_id == self.product_apple_sweet:
                self.env['stock.move.line'].create({
                    'move_id': move.id, 'product_id': self.product_apple_sweet.id, 'lot_id': lot_apple_sweet.id, 'qty_done': 200.0,
                    'location_id': move.location_id.id, 'location_dest_id': move.location_dest_id.id,
                })
                move.quantity_done = 200.0

        produced_lot = self.env['stock.lot'].create({
            'name': 'PROD-TERROIR-LOT', 'product_id': self.product_juice.id, 'company_id': self.env.company.id,
        })
        for move_line in mo.finished_move_line_ids:
            if move_line.product_id == self.product_juice:
                move_line.lot_id = produced_lot.id
                move_line.quantity_done = 100.0

        mo.quality_gate_status = 'approved'
        mo.button_mark_done()

        self.assertTrue(produced_lot.terroir_attributes_json)
        terroir_attrs = json.loads(produced_lot.terroir_attributes_json)
        self.assertAlmostEqual(terroir_attrs['sweetness'], (7.0 * 100 + 9.0 * 200) / 300, places=3)

    def test_26_sc_license_verification_hard_block(self):
        """ Test SC license verification hard-block. """
        # Product with no license coverage
        product_unlicensed = self.env['product.product'].create({
            'name': 'Unlicensed Product',
            'type': 'product',
            'sc_category_ids': [(6, 0, [self.sc_cat_other.id])],
        })
        bom_unlicensed = self.env['mrp.bom'].create({
            'product_tmpl_id': product_unlicensed.product_tmpl_id.id,
            'product_qty': 1.0,
            'type': 'normal',
            'is_agri_processing': True,
            'is_seasonal': True,
        })

        mo = self.env['mrp.production'].create({
            'product_id': product_unlicensed.id,
            'product_qty': 1.0,
            'bom_id': bom_unlicensed.id,
        })
        mo.button_mark_as_todo()
        
        with self.assertRaisesRegex(UserError, "not fully covered by active Production Licenses"):
            mo.action_confirm()

        # Success case: Juice product covered by license
        mo_success = self.env['mrp.production'].create({
            'product_id': self.product_juice.id,
            'product_qty': 10.0,
            'bom_id': self.bom_juice_seasonal.id,
        })
        mo_success.button_mark_as_todo()
        mo_success.action_confirm() # Should not raise
        self.assertEqual(mo_success.state, 'confirmed')
