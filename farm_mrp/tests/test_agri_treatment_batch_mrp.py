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
        """ Test that agri.treatment.batch in farm_mrp validates workcenter_id """
        batch = self.TreatmentBatch.create({
            'treatment_temperature': 37.0,
            'carrier_ids': [(6, 0, [self.carrier1.id])]
        })
        self.assertEqual(batch.state, 'draft')

        # 1. Start batch WITHOUT workcenter (should raise UserError from farm_mrp inheritance!)
        with self.assertRaises(UserError):
            batch.action_start()

        # 2. Set workcenter and start batch successfully
        batch.workcenter_id = self.test_workcenter.id
        batch.action_start()
        self.assertEqual(batch.state, 'processing')
        self.assertEqual(self.carrier1.carrier_state, 'processing')

        # 3. Complete batch successfully
        batch.action_complete()
        self.assertEqual(batch.state, 'done')
        self.assertEqual(self.carrier1.carrier_state, 'qc')
