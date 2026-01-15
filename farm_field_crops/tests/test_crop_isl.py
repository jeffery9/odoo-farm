# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase, Form
from odoo.exceptions import UserError

class TestCropISL(TransactionCase):
    def setUp(self):
        super(TestCropISL, self).setUp()
        self.Product = self.env['product.product']
        self.Location = self.env['stock.location']
        
        self.corn = self.Product.create({'name': 'Corn', 'type': 'product'})
        self.plot = self.Location.create({
            'name': 'East Field 1',
            'usage': 'internal',
            'is_land_parcel': True,
            'calculated_area_ha': 10.0
        })

    def test_01_gis_form_validation(self):
        """ Test GIS area validation through Form UI interaction. """
        # Simulate creating a crop order via ISL form
        with Form(self.env['farm.crop.production']) as f:
            f.product_id = self.corn
            f.location_src_id = self.plot
            f.area_to_treat = 9.0
            
        isl_mo = f.save()
        self.assertEqual(isl_mo.area_to_treat, 9.0)
        
        # Test Constraint directly on the ISL record
        with self.assertRaises(UserError):
            isl_mo.area_to_treat = 12.0
            isl_mo._check_spatial_limit()
