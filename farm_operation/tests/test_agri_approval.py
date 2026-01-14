# -*- coding: utf-8 -*-
from odoo.tests import common

class TestAgriApproval(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(TestAgriApproval, cls).setUpClass()
        cls.mo_model = cls.env['mrp.production']
        cls.product = cls.env['product.product'].create({
            'name': 'Wheat Harvest',
            'type': 'product',
        })
        cls.user_manager = cls.env.ref('mrp.group_mrp_manager').users[0]
        
    def test_simplified_approval_flow(self):
        """ Test the simplified approval workflow [Draft] -> [To Approve] -> [Approved] """
        # 1. Create Draft
        mo = self.mo_model.create({
            'product_id': self.product.id,
            'product_qty': 100.0,
        })
        self.assertEqual(mo.approval_state, 'draft')
        self.assertEqual(mo.simplified_state, 'draft')
        
        # 2. Submit for Approval
        mo.action_submit_for_approval()
        self.assertEqual(mo.approval_state, 'to_approve')
        self.assertEqual(mo.simplified_state, 'approval')
        
        # 3. Approve
        mo.with_user(self.user_manager).action_approve()
        self.assertEqual(mo.approval_state, 'approved')
        self.assertEqual(mo.state, 'confirmed')
        self.assertEqual(mo.simplified_state, 'ready')
        
        # 4. Start Work
        mo.action_start_work()
        self.assertTrue(mo.is_working)
        self.assertEqual(mo.state, 'progress')
        self.assertEqual(mo.simplified_state, 'progress')
        
        # 5. Stop Work and Done
        mo.action_stop_work()
        self.assertFalse(mo.is_working)
        mo.button_mark_done()
        self.assertEqual(mo.state, 'done')
        self.assertEqual(mo.simplified_state, 'done')
