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

    def test_02_sandbox_green_tier_execution(self):
        """ Verify green-tier action executes immediately without any restrictions """
        valve = self.env['farm.water.valve'].create({'name': 'Green Valve', 'status': 'cutoff'})
        # Execute action using the sandbox mixin
        valve.action_invoke_agent_tool(
            agent_id='OptimalHarvestAgent',
            action_name='write',
            payload_data={'status': 'open'},
            risk_tier='green'
        )
        self.assertEqual(valve.status, 'open')

    def test_03_sandbox_yellow_tier_execution_and_chatter(self):
        """ Verify yellow-tier action executes immediately and posts logs to chatter """
        valve = self.env['farm.water.valve'].create({'name': 'Yellow Valve', 'status': 'cutoff'})
        valve.action_invoke_agent_tool(
            agent_id='OptimalHarvestAgent',
            action_name='write',
            payload_data={'status': 'open'},
            risk_tier='yellow'
        )
        self.assertEqual(valve.status, 'open')
        # Check chatter log was posted to the unified request model
        request = self.Request.search([('agent_identifier', '=', 'OptimalHarvestAgent'), ('risk_tier', '=', 'yellow')], limit=1)
        self.assertTrue(request.exists())
        messages = self.env['mail.message'].search([('model', '=', 'agri.agent.tool.request'), ('res_id', '=', request.id)])
        self.assertTrue(any("Yellow-Tier GxP Tool Auto-Executed" in m.body for m in messages))

    def test_04_sandbox_red_tier_gating_and_approval_flow(self):
        """ Verify red-tier action blocks transaction, creates a request, and runs dynamically on approval """
        # 1. Create and commit the physical valve in a separate setup cursor so other cursors can see it
        setup_cr = self.registry.cursor()
        setup_cr.execute("INSERT INTO farm_water_valve (name, status, pressure_psi) VALUES ('Red Valve', 'cutoff', 0.0) RETURNING id")
        valve_id = setup_cr.fetchone()[0]
        setup_cr.commit()
        setup_cr.close()

        active_cr = self.registry.cursor()
        try:
            active_env = self.env(cr=active_cr)
            active_valve = active_env['farm.water.valve'].browse(valve_id)
            
            from odoo.exceptions import ValidationError
            with self.assertRaises(ValidationError) as context:
                active_valve.action_invoke_agent_tool(
                    agent_id='OptimalHarvestAgent',
                    action_name='farm.water.valve,write',
                    payload_data={'res_id': valve_id, 'args': {'status': 'open'}},
                    risk_tier='red'
                )
            self.assertIn("GXP_RED_TIER_APPROVAL_REQUIRED", str(context.exception))
            
            # Since active_cr is a separate cursor, we open a new cursor or query the database to find the committed record
            verify_cr = self.registry.cursor()
            try:
                verify_env = self.env(cr=verify_cr)
                request = verify_env['agri.agent.tool.request'].search([
                    ('agent_identifier', '=', 'OptimalHarvestAgent'),
                    ('state', '=', 'pending')
                ], limit=1)
                self.assertTrue(request.exists())
                self.assertEqual(request.risk_tier, 'red')
                
                # Approve request to generate signature
                request.action_approve()
                self.assertEqual(request.state, 'approved')
                
                # Execute payload dynamically
                request.action_execute_payload()
                self.assertEqual(request.state, 'executed')
            finally:
                verify_cr.commit()
                verify_cr.close()
                
            # Verify the valve state has updated successfully on active_cr!
            active_valve.invalidate_model()
            self.assertEqual(active_valve.status, 'open')
        finally:
            active_cr.rollback()
            active_cr.close()
            # Clean up the committed request and valve records to keep database clean
            cleanup_cr = self.registry.cursor()
            try:
                cleanup_cr.execute("DELETE FROM agri_agent_tool_request WHERE agent_identifier = 'OptimalHarvestAgent'")
                cleanup_cr.execute("DELETE FROM farm_water_valve WHERE id = %s", (valve_id,))
                cleanup_cr.commit()
            finally:
                cleanup_cr.close()
