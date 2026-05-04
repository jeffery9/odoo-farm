# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestESGCompliance(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Compliance = cls.env['farm.export.compliance']
        cls.Country = cls.env['res.country'].create({'name': 'Testland'})
        cls.Product = cls.env['product.template'].create({'name': 'Organic Apples'})
        
    def test_01_export_compliance_status_computation(self):
        """ Test that export compliance status evaluates correctly based on MRL and Certs """
        compliance = self.Compliance.create({
            'name': 'EXP-2026-001',
            'target_market_id': self.Country.id,
            'product_id': self.Product.id,
            'residue_limit_ok': False,
            'phytosanitary_cert_ok': False,
            'labeling_ok': False,
        })
        
        # Trigger compute
        compliance._compute_compliance_status()
        self.assertEqual(compliance.compliance_status, 'blocked')
        
        # Partial compliance
        compliance.write({
            'residue_limit_ok': True,
            'phytosanitary_cert_ok': True,
        })
        compliance._compute_compliance_status()
        self.assertEqual(compliance.compliance_status, 'blocked') # Missing labeling
        
        # Full compliance
        compliance.write({
            'labeling_ok': True,
        })
        compliance._compute_compliance_status()
        self.assertEqual(compliance.compliance_status, 'ready')
