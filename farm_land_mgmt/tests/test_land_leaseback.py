# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestLandLeaseback(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        
        cls.farmer_li = cls.env['res.partner'].create({'name': 'Farmer Li'})
        cls.coop = cls.env['res.partner'].create({'name': 'Mega Farm Operator'})
        
        cls.plot_1 = cls.env['farm.location'].create({'name': 'Li Plot 1'})
        cls.plot_2 = cls.env['farm.location'].create({'name': 'Li Plot 2'})

    def test_01_land_consolidation_preserves_dna(self):
        """
        Scenario 28: Digital Land Rights & Leaseback
        1. A large operator leases 2 micro-plots from Farmer Li.
        2. The lease is activated.
        3. The operator consolidates the 2 micro-plots into a "Mega Field" for tractor operations.
        4. The system preserves Farmer Li's original ownership DNA on the micro-plots, preventing boundary loss.
        """
        contract = self.env['farm.land.lease'].create({
            'name': 'LEASE-LI-2026',
            'farmer_id': self.farmer_li.id,
            'operator_id': self.coop.id,
            'land_parcel_ids': [(6, 0, [self.plot_1.id, self.plot_2.id])],
            'start_date': '2026-01-01',
            'end_date': '2036-01-01',
            'annual_rent': 1000.0
        })
        
        # Step 2: Activate
        contract.action_activate()
        self.assertEqual(contract.state, 'active')
        self.assertEqual(self.plot_1.original_owner_id.id, self.farmer_li.id, "Ownership DNA must be stamped.")
        self.assertEqual(self.plot_1.lease_contract_id.id, contract.id)
        
        # Step 3: Consolidate
        mega_field = contract.action_consolidate_parcels("North Mega Field A")
        
        # Step 4: Verify DNA Preservation
        self.assertTrue(mega_field, "Mega field should be created.")
        self.assertTrue(self.plot_1.is_consolidated, "Micro-plot must be marked as consolidated.")
        self.assertEqual(self.plot_1.mega_field_id.id, mega_field.id, "Micro-plot must be linked to the parent Mega-Field.")
        self.assertEqual(self.plot_1.original_owner_id.id, self.farmer_li.id, "Ownership DNA MUST NOT be erased upon consolidation.")

