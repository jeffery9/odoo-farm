from odoo.tests.common import TransactionCase
import json

class TestA2ACollaboration(TransactionCase):

    def setUp(self):
        super().setUp()
        self.product = self.env['product.product'].create({'name': 'AI Tomato', 'type': 'consu'})
        self.intervention = self.env['mrp.production'].create({
            'product_id': self.product.id,
            'product_qty': 10.0,
        })

    def test_01_message_construction(self):
        """ Test A2A Message logic """
        if 'agri.a2a.message' not in self.env:
            return
        msg = self.env['agri.a2a.message'].create({
            'sender_agent': 'agent_scout',
            'receiver_agent': 'agent_planner',
            'intent': 'task_request',
            'content': 'Check pest levels in sector 5'
        })
        self.assertEqual(msg.sender_agent, 'agent_scout')
