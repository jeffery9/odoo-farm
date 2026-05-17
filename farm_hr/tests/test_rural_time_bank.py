# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestRuralTimeBank(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        
        cls.villager_a = cls.env['res.partner'].create({'name': 'Young Farmer A'})
        cls.villager_b = cls.env['res.partner'].create({'name': 'Elderly Neighbor B'})
        
        cls.worker_a = cls.env['hr.employee'].create({
            'name': 'Worker A',
            'address_home_id': cls.villager_a.id
        })
        
        # We need a project task to attach the worklog to
        try:
            cls.project = cls.env.ref('farm_operation.project_farm_operations')
        except ValueError:
            cls.project = cls.env['project.project'].create({'name': 'Farm Operations'})
            
        cls.task = cls.env['project.task'].create({
            'name': 'Roof Repair / Heavy Lifting',
            'project_id': cls.project.id
        })

    def test_01_time_bank_mutual_aid_flow(self):
        """
        Scenario 20 & 29: Rural Time Bank Labor Sharing & Elderly Care
        1. Farmer A spends 8 hours helping Elderly Neighbor B.
        2. Farmer A logs the work via the Mobile App, flagging it as Mutual Aid.
        3. Upon approval, NO cash transaction occurs.
        4. System automatically credits 8 Labor Credits to Farmer A.
        5. System automatically debits 8 Labor Credits from Neighbor B.
        """
        log = self.env['farm.worklog'].create({
            'employee_id': self.worker_a.id,
            'task_id': self.task.id,
            'work_type': 'packaging', # dummy standard type
            'quantity': 8.0, # 8 hours
            'is_mutual_aid': True,
            'beneficiary_partner_id': self.villager_b.id,
            'notes': 'Helped fix roof and carry fertilizer.'
        })
        
        log.action_approve()
        
        # Verify the ledger entries
        ledgers_a = self.env['farm.time.bank.ledger'].search([('member_id', '=', self.villager_a.id)])
        self.assertTrue(ledgers_a)
        self.assertEqual(ledgers_a[0].credit_amount, 8.0, "Farmer A should earn 8 credits.")
        self.assertEqual(ledgers_a[0].transaction_type, 'earn')
        
        ledgers_b = self.env['farm.time.bank.ledger'].search([('member_id', '=', self.villager_b.id)])
        self.assertTrue(ledgers_b)
        self.assertEqual(ledgers_b[0].credit_amount, -8.0, "Neighbor B should spend 8 credits.")
        self.assertEqual(ledgers_b[0].transaction_type, 'spend')

