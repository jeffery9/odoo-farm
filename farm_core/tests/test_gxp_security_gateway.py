# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase, tagged
from odoo.exceptions import ValidationError

@tagged('post_install', '-at_install')
class TestGxPSecurityGateway(TransactionCase):

    def setUp(self):
        super(TestGxPSecurityGateway, self).setUp()
        self.Request = self.env['agri.agent.tool.request']

    def test_gxp_approval_generates_signature(self):
        """ Ensure approving a pending request enforces state change and generates SHA-256 """
        request = self.Request.create({
            'agent_identifier': 'Agent-Alpha',
            'target_action': 'open_water_valve',
            'payload': '{"valve_id": 42, "duration_sec": 300}',
            'risk_tier': 'red'
        })
        self.assertEqual(request.state, 'pending')
        
        request.action_approve()
        
        self.assertEqual(request.state, 'approved')
        self.assertTrue(request.digital_signature, "Digital signature must be generated on approval")
        self.assertEqual(request.approver_id, self.env.user, "Approver must be logged")

    def test_gxp_reject_blocks_execution(self):
        """ Ensure rejecting blocks state transitions properly """
        request = self.Request.create({
            'agent_identifier': 'Agent-Beta',
            'target_action': 'apply_fertilizer',
            'payload': '{}',
            'risk_tier': 'red'
        })
        request.action_reject()
        self.assertEqual(request.state, 'rejected')
        
        with self.assertRaises(ValidationError):
            request.action_approve()
