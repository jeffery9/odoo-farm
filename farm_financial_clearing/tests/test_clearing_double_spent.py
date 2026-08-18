# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError

class TestClearingDoubleSpent(TransactionCase):

    def setUp(self):
        super(TestClearingDoubleSpent, self).setUp()
        self.test_partner = self.env['res.partner'].create({
            'name': 'Ginseng Cooperative Partner',
            'impact_credits': 100.0
        })

    def test_clearing_overdraft_double_spent(self):
        """ Verify balance lock forbids double-spent or spending beyond credits """
        ledger = self.env['agri.clearing.ledger'].create({
            'partner_id': self.test_partner.id,
            'amount_to_clear': 150.0
        })
        with self.assertRaises(UserError, msg="Overdraft credit spends must throw UserError"):
            ledger.action_post_netting_clearing()

    def test_clearing_success(self):
        """ Verify successful clearing subtracts balance correctly """
        ledger = self.env['agri.clearing.ledger'].create({
            'partner_id': self.test_partner.id,
            'amount_to_clear': 40.0
        })
        res = ledger.action_post_netting_clearing()
        self.assertTrue(res)
        self.assertEqual(self.test_partner.impact_credits, 60.0)
        self.assertEqual(ledger.state, 'confirmed')
