# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

class TestBackpressureConstraints(TransactionCase):
    def setUp(self):
        super(TestBackpressureConstraints, self).setUp()
        self.Location = self.env['stock.location']
        self.Tracking = self.env['stock.matter.tracking']
        self.Package = self.env['stock.package']
        self.Product = self.env['product.product']
        self.Lot = self.env['stock.lot']
        self.Quant = self.env['stock.quant']

        # Create a base product
        self.product_pig = self.Product.create({
            'name': 'Backpressure Pig',
            'is_storable': True,
        })

        # Create a holding location
        self.holding_location = self.Location.create({
            'name': 'Backpressure holding plot',
            'is_land_parcel': True,
            'gps_lat': 12.0,
            'gps_lng': 34.0,
            'land_area': 100.0,  # 100 sqm
            'max_capacity_volume_m3': 200.0,
            'max_stocking_density': 1.5  # 1.5 animals per sqm => Max 150 animals
        })

        self.package = self.Package.create({'name': 'LPN-CARRIER-TEST-BC'})

    def test_capacity_fields_declaration(self):
        # Verify land location physical constraints fields
        self.assertEqual(self.holding_location.max_capacity_volume_m3, 200.0)
        self.assertEqual(self.holding_location.max_stocking_density, 1.5)

        # Verify tracking carrier physical volumetric capacity
        tracking = self.Tracking.create({
            'package_id': self.package.id,
            'max_capacity_volume_m3': 50.0
        })
        self.assertEqual(tracking.max_capacity_volume_m3, 50.0)

    def test_stocking_density_interlock_validation(self):
        # Create a lot for breeding sows
        lot = self.Lot.create({
            'name': 'SOW-LOT-TEST-99',
            'product_id': self.product_pig.id,
            'company_id': self.env.company.id,
        })

        # Attempt to create quants inside the holding location totaling 160 animals (Max is 150)
        # Relocation/create that pushes density above 1.5 raises ValidationError
        with self.assertRaises(ValidationError):
            self.Quant.create({
                'product_id': self.product_pig.id,
                'location_id': self.holding_location.id,
                'lot_id': lot.id,
                'quantity': 160.0
            })

    def test_carrier_volumetric_interlock_validation(self):
        lot = self.Lot.create({
            'name': 'SOW-LOT-TEST-100',
            'product_id': self.product_pig.id,
            'company_id': self.env.company.id,
        })

        # Create a carrier with max volumetric capacity of 10.0 m³
        tracking = self.Tracking.create({
            'package_id': self.package.id,
            'max_capacity_volume_m3': 10.0
        })

        # Creating quant inside this carrier package exceeding 10.0 raises ValidationError
        with self.assertRaises(ValidationError):
            self.Quant.create({
                'product_id': self.product_pig.id,
                'location_id': self.env.ref('stock.stock_location_stock').id,
                'package_id': tracking.package_id.id,
                'lot_id': lot.id,
                'quantity': 12.0  # exceeds 10.0
            })
