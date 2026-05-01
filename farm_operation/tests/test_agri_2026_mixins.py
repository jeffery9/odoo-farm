from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
import json

class TestAgri2026Mixins(TransactionCase):

    def setUp(self):
        super().setUp()
        self.product = self.env['product.product'].create({
            'name': '2026 Bio Crop',
            'type': 'consu',
            'standard_price': 100.0,
        })
        self.bom = self.env['mrp.bom'].create({
            'product_tmpl_id': self.product.product_tmpl_id.id,
            'product_qty': 1.0,
            'type': 'normal',
            'nitrogen_qty': 10.0,
            'esg_score': 800,
        })

    def test_01_agri_view_interceptor(self):
        """Test Level 4: AgriViewMixin term replacement logic"""
        # Call the model method directly to verify logic
        arch = '<form string="Manufacturing Orders"><div>Manufacturing Order</div></form>'
        # Access through the mixin model
        new_arch = self.env['agri.view.mixin']._apply_agri_term_mapping(arch)
        self.assertIn('Agricultural Interventions', new_arch)
        self.assertIn('Agricultural Intervention', new_arch)

    def test_02_sustainability_redline(self):
        """Test Level 0: SustainabilityMixin validation"""
        # Limit is 50.0 in farm_core/models/base_mixins.py
        with self.assertRaises(ValidationError):
            self.env['mrp.production'].create({
                'product_id': self.product.id,
                'bom_id': self.bom.id,
                'product_qty': 1.0,
                'carbon_intensity': 60.0,
            })
