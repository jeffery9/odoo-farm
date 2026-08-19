# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestCarbonLedgerFlow(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        
        # 1. Create a Unit of Measure (Liters)
        try:
            cls.uom_liter = cls.env.ref('uom.product_uom_litre')
        except ValueError:
            cls.uom_liter = cls.env['uom.uom'].search([('name', '=', 'L')], limit=1)

        # 2. Create the Diesel Product
        cls.diesel_product = cls.env['product.template'].create({
            'name': 'Diesel Fuel',
            'type': 'consu',
            'uom_id': cls.uom_liter.id,
<<<<<<< HEAD
=======
            'uom_po_id': cls.uom_liter.id,
>>>>>>> 5351cad217860264bdd3ca8394fa45a799fce3d0
        })
        
        # 3. Create Carbon Factor for Diesel (e.g., 2.68 kg CO2e per Liter)
        cls.carbon_factor = cls.env['agri.carbon.factor'].create({
            'name': 'Diesel Combustion',
            'product_id': cls.diesel_product.id,
            'category': 'energy',
            'emission_factor': 2.68,
            'uom_id': cls.uom_liter.id,
            'source': 'IPCC'
        })
        
        # 4. Create a Tractor
        cls.tractor = cls.env['maintenance.equipment'].create({
            'name': 'John Deere 5075E',
            'is_agri_machinery': True,
            'fuel_type': 'diesel',
        })
        
        # 5. Create a Land Parcel (Location)
        cls.parcel = cls.env['farm.location'].create({
            'name': 'Field B2'
        })

    def test_01_equipment_fuel_log_triggers_carbon_ledger(self):
        """
        Scenario:
        1. A tractor consumes 50L of diesel during an operation.
        2. A fuel log is created.
        3. The system automatically intercepts this log, finds the IPCC carbon factor,
           and writes an entry into the Carbon Ledger for Scope 1 emissions.
        """
        # Create fuel log
        log = self.env['farm.equipment.log'].create({
            'equipment_id': self.tractor.id,
            'date': '2026-05-16',
            'engine_hours': 4.5,
            'fuel_consumed': 50.0,
            'notes': 'Ploughing Field B2'
        })
        
<<<<<<< HEAD
        # Verify that a carbon ledger entry was created
        ledger = log.carbon_ledger_id
        
        self.assertTrue(ledger, "A carbon ledger entry must be automatically created when fuel is logged.")
        self.assertEqual(ledger.impact_type, 'emission', "Fuel burning is an emission.")
        
        # 50L * 2.68 = 134.0 kg CO2e
        self.assertAlmostEqual(ledger.total_co2e, 134.0, places=2, msg="Carbon calculation must match Factor * Consumed Volume.")
=======
        # In the implementation, we might need a method or an override on create/write
        # Verify that a carbon ledger entry was created
        ledgers = self.env['agri.carbon.ledger'].search([
            ('origin', '=', f'Equipment Log: {log.id}')
        ])
        
        self.assertTrue(ledgers, "A carbon ledger entry must be automatically created when fuel is logged.")
        self.assertEqual(len(ledgers), 1)
        ledger = ledgers[0]
        
        self.assertEqual(ledger.scope, 'scope1', "Diesel combustion by owned tractor should be Scope 1.")
        self.assertEqual(ledger.impact_type, 'emission', "Fuel burning is an emission.")
        
        # 50L * 2.68 = 134.0 kg CO2e
        self.assertAlmostEqual(ledger.co2e_amount, 134.0, places=2, msg="Carbon calculation must match Factor * Consumed Volume.")
>>>>>>> 5351cad217860264bdd3ca8394fa45a799fce3d0

