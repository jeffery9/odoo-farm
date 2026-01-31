from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
import json

class TestAgri2026Mixins(TransactionCase):

    def setUp(self):
        super(TestAgri2026Mixins, self).setUp()
        # Setup basic data: product, bom, location
        self.uom_unit = self.env.ref('uom.product_uom_unit')
        self.product = self.env['product.product'].create({
            'name': '2026 Bio Crop',
            'type': 'product',
            'standard_price': 100.0,
        })
        self.bom = self.env['mrp.bom'].create({
            'product_tmpl_id': self.product.product_tmpl_id.id,
            'product_qty': 1.0,
            'type': 'normal',
            'nitrogen_qty': 10.0, # L1 Mixin data
            'esg_score': 800,     # L0 Mixin data
        })

    def test_01_agri_view_interceptor(self):
        """Test Level 0: AgriViewMixin UI term replacement"""
        # We simulate fields_view_get call
        view = self.env['mrp.production'].fields_view_get(view_type='form')
        arch = view.get('arch', '')
        # Check if 'Manufacturing Order' is replaced with 'Agricultural Intervention'
        # Note: In test environment, translations might depend on active lang.
        # We check for the logic.
        self.assertIn('Agricultural Intervention', arch, "UI Interceptor failed to replace MO term")

    def test_02_sustainability_redline(self):
        """Test Level 0: SustainabilityMixin validation"""
        # Create an intervention with high carbon intensity
        with self.assertRaises(ValidationError):
            self.env['mrp.production'].create({
                'product_id': self.product.id,
                'bom_id': self.bom.id,
                'product_qty': 1.0,
                'carbon_intensity': 60.0, # Limit is 50.0
            })

    def test_03_nutrient_mass_balance(self):
        """Test Level 1: NutrientMixin calculation"""
        # Simulate a simple mass balance
        input_mock = self.env['mrp.bom.line'].new({'nitrogen_qty': 100.0})
        output_mock = self.env['mrp.bom'].new({'nitrogen_qty': 80.0})
        
        balance = self.bom.calculate_mass_balance([input_mock], [output_mock])
        self.assertEqual(balance['n_efficiency'], 0.8)
        self.assertTrue(balance['is_sustainable'])

    def test_04_clearing_and_fingerprint(self):
        """Test Level 3: ClearingEngineMixin and Fingerprint"""
        intervention = self.env['mrp.production'].create({
            'product_id': self.product.id,
            'bom_id': self.bom.id,
            'product_qty': 1.0,
            'carbon_intensity': 5.0,
            'geo_point': '120.1234,30.5678', # L1
        })
        
        # Finalize clearing
        intervention.action_finalize_clearing()
        
        self.assertEqual(intervention.clearing_status, 'calculated')
        self.assertTrue(intervention.impact_credits > 0)
        
        # Verify Fingerprint
        fingerprint = json.loads(intervention.quality_fingerprint)
        self.assertEqual(fingerprint['spatial']['grid_id'], 'G_120.1234_30.5678')
        self.assertEqual(fingerprint['model'], 'mrp.production')
