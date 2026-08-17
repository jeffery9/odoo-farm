# -*- coding: utf-8 -*-
# filepath: odoo-farm-dev/farm_robotics/tests/test_coopetition_lease_scaffold.py
from odoo.tests.common import TransactionCase
from odoo.tests import tagged

@tagged('post_install', '-at_install')
class TestCoopetitionLeaseScaffold(TransactionCase):

    def test_01_model_registration(self):
        """ Assert agri.robotics.lease exists and has the correct fields """
        LeaseModel = self.env['agri.robotics.lease']
        self.assertTrue(LeaseModel._name in self.env, "agri.robotics.lease must be registered in Odoo registry")
        
        fields_to_check = ['name', 'res_model', 'res_id', 'robot_id', 'mission_id', 'start_date', 'expiration_date', 'state']
        for field in fields_to_check:
            self.assertTrue(field in LeaseModel._fields, f"Field '{field}' must exist on agri.robotics.lease")
