# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError

class TestAgriTreatmentBatchMrp(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(TestAgriTreatmentBatchMrp, cls).setUpClass()
        cls.Workcenter = cls.env['mrp.workcenter']
        cls.TreatmentBatch = cls.env['agri.treatment.batch']
        cls.Tracking = cls.env['stock.matter.tracking']

        # Create workcenter workstation
        cls.test_workcenter = cls.Workcenter.create({
            'name': 'Winery Fermentation Reactor #3',
            'code': 'FERM-03'
        })

        # Create carrier containers
        cls.carrier_p1 = cls.env['stock.package'].create({'name': 'SFC-MRP-01'})
        cls.carrier1 = cls.Tracking.create({
            'package_id': cls.carrier_p1.id,
            'dna_integrity_score': 100.0,
            'carrier_state': 'idle'
        })
        cls.carrier1.write({'carrier_state': 'loading'})

    def test_agri_treatment_batch_mrp_flow(self):
        """ Test that agri.treatment.batch in farm_mrp validates workcenter_id and synchronizes process phase """
        # Create a dummy product template and BOM to satisfy required fields on routing operations
        product_tmpl = self.env['product.template'].create({
            'name': 'Test Route Product Template',
            'type': 'consu'
        })
        bom = self.env['mrp.bom'].create({
            'product_tmpl_id': product_tmpl.id,
            'product_qty': 1.0,
            'type': 'normal'
        })

        # Create a specific routing operation step linked to our test workcenter
        operation = self.env['mrp.routing.workcenter'].create({
            'name': 'Active Wine Processing Step #1',
            'workcenter_id': self.test_workcenter.id,
            'bom_id': bom.id,
            'agri_activity_type': 'processing',
            'gxp_phase_type': 'fermentation'
        })

        batch = self.TreatmentBatch.create({
            'treatment_temperature': 37.0,
            'carrier_ids': [(6, 0, [self.carrier1.id])]
        })
        self.assertEqual(batch.state, 'draft')

        # 1. Start batch WITHOUT workcenter (should raise UserError from farm_mrp inheritance!)
        with self.assertRaises(UserError):
            batch.action_start()

        # 2. Test Onchange Defaulting of workcenter_id from operation_id
        batch.operation_id = operation.id
        batch._onchange_operation_id()
        self.assertEqual(batch.workcenter_id.id, self.test_workcenter.id, "Onchange must default workcenter_id from selected operation.")

        # 3. Start batch successfully and assert current_phase_id is synchronized
        batch.action_start()
        self.assertEqual(batch.state, 'processing')
        self.assertEqual(self.carrier1.carrier_state, 'processing')
        self.assertEqual(self.carrier1.current_phase_id.id, operation.id, "Starting batch must synchronize the operation phase onto linked carriers.")

        # 4. Complete batch successfully and assert current_phase_id is cleared
        batch.action_complete()
        self.assertEqual(batch.state, 'done')
        self.assertEqual(self.carrier1.carrier_state, 'qc')
        self.assertFalse(self.carrier1.current_phase_id, "Completing batch must clear active process phase on carriers.")

    def test_agri_operation_mixin_inheritance(self):
        """ Verify that mrp.routing.workcenter correctly inherits from agri.operation.mixin """
        RoutingWorkcenter = self.env['mrp.routing.workcenter']
        
        # Check that mixin fields exist on the model
        self.assertIn('agri_activity_type', RoutingWorkcenter._fields)
        self.assertIn('technical_manual', RoutingWorkcenter._fields)
        self.assertIn('param_monitoring_required', RoutingWorkcenter._fields)
        self.assertIn('target_value', RoutingWorkcenter._fields)
        self.assertIn('tolerance_range', RoutingWorkcenter._fields)
        self.assertIn('gxp_phase_type', RoutingWorkcenter._fields)

        # Create dummy product template and BOM to satisfy not-null constraints on bom_id
        product_tmpl = self.env['product.template'].create({
            'name': 'Test Operation Product Template',
            'type': 'consu'
        })
        bom = self.env['mrp.bom'].create({
            'product_tmpl_id': product_tmpl.id,
            'product_qty': 1.0,
            'type': 'normal'
        })

        # Create an operational step with mixin values and linked bom_id
        operation = RoutingWorkcenter.create({
            'name': 'Sterilization Phase 1',
            'workcenter_id': self.test_workcenter.id,
            'bom_id': bom.id,
            'agri_activity_type': 'processing',
            'gxp_phase_type': 'sterilization',
            'param_monitoring_required': True,
            'target_value': 121.5,
            'tolerance_range': 1.5,
            'technical_manual': '<p>Heat the sterilization vessel to 121.5C for 20 minutes.</p>'
        })

        self.assertEqual(operation.agri_activity_type, 'processing')
        self.assertEqual(operation.gxp_phase_type, 'sterilization')
        self.assertTrue(operation.param_monitoring_required)
        self.assertAlmostEqual(operation.target_value, 121.5)
        self.assertAlmostEqual(operation.tolerance_range, 1.5)

    def test_agri_treatment_batch_recipe_validation(self):
        """ Test GxP recipe compatibility validation inside action_start """
        # Create products as storable products to support stock.quant creation per Odoo 19 conventions
        product_yeast = self.env['product.product'].create({
            'name': 'Wine Yeast',
            'type': 'consu',
            'is_storable': True
        })
        product_grapes = self.env['product.product'].create({
            'name': 'Wine Grapes',
            'type': 'consu',
            'is_storable': True
        })
        product_apples = self.env['product.product'].create({
            'name': 'Incompatible Apples',
            'type': 'consu',
            'is_storable': True
        })

        # Create Wine Fermentation BOM (Recipe)
        bom = self.env['mrp.bom'].create({
            'product_tmpl_id': product_yeast.product_tmpl_id.id,
            'product_qty': 1.0,
            'type': 'normal',
            'bom_line_ids': [
                (0, 0, {'product_id': product_grapes.id, 'product_qty': 100.0})
            ]
        })

        # Put Apple product on carrier quant
        # First find or create a native location for storage
        location = self.env['stock.location'].create({
            'name': 'Fermentation Storage',
            'usage': 'internal'
        })
        quant = self.env['stock.quant'].create({
            'product_id': product_apples.id,
            'location_id': location.id,
            'quantity': 50.0,
            'package_id': self.carrier_p1.id
        })
        # Invalidate cache and trigger manual compute of lot_ids to satisfy dependencies
        self.carrier1.package_id.invalidate_recordset(['quant_ids'])
        self.carrier1.invalidate_recordset(['lot_ids'])
        self.carrier1._compute_lot_ids()

        # Create a Treatment Batch linked to our carrier
        batch = self.TreatmentBatch.create({
            'treatment_temperature': 37.0,
            'workcenter_id': self.test_workcenter.id,
            'bom_id': bom.id,
            'carrier_ids': [(6, 0, [self.carrier1.id])]
        })

        # Try to start batch with incompatible carrier products (should raise UserError!)
        with self.assertRaises(UserError) as cm:
            batch.action_start()
        self.assertIn("GxP Recipe Compatibility Violation", str(cm.exception))

        # Change the carrier product to Wine Grapes (compatible!)
        quant.product_id = product_grapes.id
        # Invalidate cache and trigger manual compute of lot_ids again
        self.carrier1.package_id.invalidate_recordset(['quant_ids'])
        self.carrier1.invalidate_recordset(['lot_ids'])
        self.carrier1._compute_lot_ids()

        # Try to start batch now (should succeed perfectly!)
        batch.action_start()
        self.assertEqual(batch.state, 'processing')
