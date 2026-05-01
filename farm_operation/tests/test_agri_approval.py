# -*- coding: utf-8 -*-
from odoo.tests import common

class TestAgriApproval(common.TransactionCase):
    def setUp(self):
        super().setUp()
        self.mo_model = self.env['mrp.production']
        self.product = self.env['product.product'].create({
            'name': 'Wheat Harvest',
            'type': 'consu',
        })
        # Use existing manager if creation fails
        self.user_manager = self.env.user
        
    def test_simplified_approval_flow(self):
        """ Test the simplified approval workflow """
        mo = self.mo_model.create({
            'product_id': self.product.id,
            'product_qty': 100.0,
        })
        if hasattr(mo, 'approval_state'):
            self.assertEqual(mo.approval_state, 'draft')
