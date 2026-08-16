# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase, tagged
from odoo.exceptions import ValidationError

@tagged('post_install', '-at_install')
class TestMultiAgentSwarmDelegation(TransactionCase):

    def setUp(self):
        super(TestMultiAgentSwarmDelegation, self).setUp()
        
        # 1. Scaffolding standard company contexts
        self.company_a = self.env['res.company'].create({'name': 'Agri-Company-A'})
        self.company_b = self.env['res.company'].create({'name': 'UAV-Corp'})
        self.company_c = self.env['res.company'].create({'name': 'Power-Corp'})

        # 2. Scaffolding partners with credit balances
        self.internal_leader = self.env['res.partner'].create({
            'name': 'Company-Internal-Leader',
            'company_id': self.company_a.id
        })
        self.internal_worker = self.env['res.partner'].create({
            'name': 'Company-Internal-Worker',
            'company_id': self.company_a.id
        })
        self.uav_agent = self.env['res.partner'].create({
            'name': 'Main-UAV-Agent',
            'company_id': self.company_b.id,
            'impact_credits': 200.0
        })
        self.solar_agent = self.env['res.partner'].create({
            'name': 'Solar-Station-Agent',
            'company_id': self.company_c.id,
            'impact_credits': 50.0
        })

        # 3. Create Odoo tasks (using farm.task scaffold)
        project_a = self.env['project.project'].create({'name': 'Proj A', 'company_id': self.company_a.id})
        project_b = self.env['project.project'].create({'name': 'Proj B', 'company_id': self.company_b.id})
        project_c = self.env['project.project'].create({'name': 'Proj C', 'company_id': self.company_c.id})

        self.parent_task_internal = self.env['farm.task'].create({
            'name': 'Harvesting Mission #1',
            'project_id': project_a.id,
            'activity_family': 'harvesting'
        })
        self.sub_task_internal = self.env['farm.task'].create({
            'name': 'UAV Spraying #1-1',
            'project_id': project_a.id,
            'activity_family': 'planting'
        })

        self.parent_task_b2b = self.env['farm.task'].create({
            'name': 'Regional Patrol',
            'project_id': project_b.id,
            'activity_family': 'processing'
        })
        self.sub_task_b2b = self.env['farm.task'].create({
            'name': 'Recharge Mission',
            'project_id': project_c.id,
            'activity_family': 'processing'
        })

    def test_01_company_internal_task_delegation(self):
        """ Scenario 1: Verify synchronous company-internal task tree delegation """
        contract = self.env['agri.agent.task.delegation'].create({
            'parent_task_id': self.parent_task_internal.id,
            'sub_task_id': self.sub_task_internal.id,
            'delegator_id': self.internal_leader.id,
            'delegatee_id': self.internal_worker.id,
            'escrow_credits': 0.0
        })
        self.assertTrue(contract.name, "Sequence contract ID must generate!")
        self.assertEqual(contract.delegator_company_id, self.company_a, "Company context must propagate.")
        self.assertEqual(contract.delegatee_company_id, self.company_a, "Company context must propagate.")
        self.assertEqual(contract.state, 'draft', "Initial state must be draft.")

    def test_02_inter_company_delegation_escrow_locking_and_checks(self):
        """ Scenario 2: Verify B2B delegation credit checks, lock, and hold """
        contract = self.env['agri.agent.task.delegation'].create({
            'parent_task_id': self.parent_task_b2b.id,
            'sub_task_id': self.sub_task_b2b.id,
            'delegator_id': self.uav_agent.id,
            'delegatee_id': self.solar_agent.id,
            'escrow_credits': 50.0
        })
        
        # Lock Escrow
        contract.action_lock_escrow()
        self.assertEqual(contract.state, 'escrow', "State must transition to escrow.")
        # Balance must decrement to 150.0 to reserve the credits
        self.assertEqual(self.uav_agent.impact_credits, 150.0, "Delegator credits must decrease immediately in memory to prevent double spend.")
        self.assertTrue(contract.ledger_id, "Draft reservation ledger record must exist.")
        self.assertEqual(contract.ledger_id.state, 'draft', "Reservation ledger line must remain draft (payment hold).")

        # Insufficient balance test
        failed_contract = self.env['agri.agent.task.delegation'].create({
            'parent_task_id': self.parent_task_b2b.id,
            'sub_task_id': self.sub_task_b2b.id,
            'delegator_id': self.uav_agent.id,
            'delegatee_id': self.solar_agent.id,
            'escrow_credits': 300.0
        })
        with self.assertRaises(ValidationError):
            failed_contract.action_lock_escrow()

    def test_03_contract_successful_completion_with_merkle_release(self):
        """ Scenario 3: Verify proof release converts draft hold and credits delegatee """
        contract = self.env['agri.agent.task.delegation'].create({
            'parent_task_id': self.parent_task_b2b.id,
            'sub_task_id': self.sub_task_b2b.id,
            'delegator_id': self.uav_agent.id,
            'delegatee_id': self.solar_agent.id,
            'escrow_credits': 50.0
        })
        contract.action_lock_escrow()
        contract.action_approve_execution()
        
        # Submit valid proof
        proof = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        contract.action_complete_clearing(proof)
        
        self.assertEqual(contract.state, 'completed')
        self.assertEqual(contract.merkle_proof, proof)
        
        # Check permanent ledger confirmation and double-entry release
        self.assertEqual(contract.ledger_id.state, 'confirmed', "Escrow reserve debit must become confirmed.")
        # Ensure delegator is not double-deducted during confirmation
        self.assertEqual(self.uav_agent.impact_credits, 150.0, "Delegator credits remains subtracted permanently.")
        self.assertEqual(self.solar_agent.impact_credits, 100.0, "Delegatee credits must increase by released escrow amount (50.0 + 50.0 = 100.0).")

    def test_04_contract_cancellation_and_graceful_refund(self):
        """ Scenario 4: Verify cancellation deletes draft ledger line and refunds credits """
        contract = self.env['agri.agent.task.delegation'].create({
            'parent_task_id': self.parent_task_b2b.id,
            'sub_task_id': self.sub_task_b2b.id,
            'delegator_id': self.uav_agent.id,
            'delegatee_id': self.solar_agent.id,
            'escrow_credits': 50.0
        })
        contract.action_lock_escrow()
        self.assertEqual(self.uav_agent.impact_credits, 150.0)
        
        # Cancel and refund
        contract.action_cancel_refund()
        self.assertEqual(contract.state, 'cancelled')
        self.assertFalse(contract.ledger_id, "Reserved draft ledger record must be physically unlinked/deleted.")
        self.assertEqual(self.uav_agent.impact_credits, 200.0, "Delegator credits must be fully restored and refunded.")
