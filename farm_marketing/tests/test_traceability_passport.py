# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
import json

class TestTraceabilityPassport(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        
        cls.product = cls.env['product.product'].create({
            'name': 'Premium Strawberries',
            'type': 'product',
            'description_sale': 'Grown with zero emissions.'
        })
        
        cls.lot = cls.env['stock.lot'].create({
            'name': 'LOT-STRAW-99',
            'product_id': cls.product.id,
            'company_id': cls.env.company.id
        })
        
        if hasattr(cls.lot, 'quality_grade'):
            cls.lot.write({'quality_grade': 'premium'})

    def test_01_passport_generation(self):
        """
        Scenario:
        1. A consumer scans the QR code on a box of strawberries.
        2. The backend generates a 'Traceability Passport' fetching cross-module data.
        3. Passport reflects 1 harvest intervention, 2 drone flights, and a -5.0kg Carbon Footprint.
        """
        # Simulate interventions
        harvest = self.env['mrp.production'].create({
            'product_id': self.product.id,
            'product_qty': 100,
            'intervention_type': 'harvesting',
            'lot_producing_id': self.lot.id
        })
        
        for _ in range(2):
            self.env['mrp.production'].create({
                'product_id': self.product.id,
                'product_qty': 0, # Service
                'intervention_type': 'aerial_spraying',
                'lot_producing_id': self.lot.id
            })
            
        # Simulate ESG Carbon Data
        if 'agri.carbon.ledger' in self.env:
            # Need a mock factor
            factor = self.env['agri.carbon.factor'].create({
                'name': 'No-Till',
                'category': 'land',
                'emission_factor': 1.0,
                'uom_id': self.env.ref('uom.product_uom_unit').id
            })
            self.env['agri.carbon.ledger'].create({
                'name': 'Sink for Strawberries',
                'impact_type': 'sequestration',
                'co2e_amount': 5.0,
                'lot_id': self.lot.id,
                'source_factor_id': factor.id
            })

        # Fetch passport
        self.lot.invalidate_recordset(['traceability_passport_json'])
        passport_raw = self.lot.traceability_passport_json
        
        self.assertTrue(passport_raw, "JSON passport must be generated.")
        passport = json.loads(passport_raw)
        
        self.assertEqual(passport['product'], 'Premium Strawberries')
        self.assertEqual(passport['interventions_count'], 3, "1 harvest + 2 drone flights")
        self.assertEqual(passport['drone_flights'], 2, "Must reflect 2 aerial spraying interventions")
        
        if 'agri.carbon.ledger' in self.env:
            self.assertEqual(passport['carbon_footprint_co2e'], -5.0, "Must reflect the 5kg carbon sink.")
            
        if hasattr(self.lot, 'quality_grade'):
            self.assertEqual(passport['quality_grade'], 'premium')

