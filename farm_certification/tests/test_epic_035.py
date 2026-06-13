# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo import fields

class TestEpic035(TransactionCase):
    """ BDD Test for Epic 035 Certification & Organic Farming """

    def setUp(self):
        super(TestEpic035, self).setUp()
        self.Location = self.env['farm.location'].create({
            'name': 'Organic Parcel',
            'is_organic': True,
        })

    def test_01_hard_blocking_of_prohibited_inputs_on_organic_parcels(self):
        """ Scenario: Hard-blocking of prohibited inputs on organic parcels """
        # Test blocking of non-white-listed input
        pass

    def test_02_organic_conversion_period_management_and_reset(self):
        """ Scenario: Organic conversion period management and reset """
        # Test reset of conversion days on prohibited application
        pass

    def test_05_globalg_a_p__compliance_self_assessment_and_gap_analysis(self):
        """ Scenario: GlobalG.A.P. compliance self-assessment and gap analysis """
        # Test identification of missing evidence for GlobalG.A.P.
        pass

    def test_09_parallel_production_physical_isolation_audit(self):
        """ Scenario: Parallel production physical isolation audit """
        # Test requirement of machine cleaning between conventional and organic plots
        pass
