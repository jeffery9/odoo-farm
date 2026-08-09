from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

class TestBiologicalAssetReflection(TransactionCase):
    def setUp(self):
        super(TestBiologicalAssetReflection, self).setUp()
        self.Asset = self.env['agri.biological.asset']
        self.Tracking = self.env['stock.matter.tracking']
        self.Package = self.env['stock.package']
        self.Product = self.env['product.product']

        # Set up base product & package
        self.product_pig = self.Product.create({'name': 'Pig', 'is_storable': True})
        self.package = self.Package.create({'name': 'LPN-CARRIER-TEST-10'})

    def test_dynamic_reflection_from_carrier(self):
        # 1. Create Biological Asset
        asset = self.Asset.create({'name': 'PIG-HERD-A', 'agricultural_type': 'animal'})

        # 2. Create Matter Tracking Carrier linked to asset
        tracking = self.Tracking.create({
            'package_id': self.package.id,
            'biological_asset_id': asset.id,
            'current_weight': 420.5,
            'life_stage': 'growing',
            'last_gps_lat': 34.0522,
            'last_gps_lng': -118.2437
        })

        # 3. Assert compute reflection
        asset.invalidate_recordset()
        self.assertAlmostEqual(asset.current_weight, 420.5)
        self.assertEqual(asset.life_stage, 'growing')
        self.assertAlmostEqual(asset.last_gps_lat, 34.0522)
        self.assertAlmostEqual(asset.last_gps_lng, -118.2437)

    def test_cache_invalidation_on_phase_change(self):
        # 1. Create Biological Asset
        asset = self.Asset.create({'name': 'PIG-HERD-B', 'agricultural_type': 'animal'})

        # 2. Create Matter Tracking Carrier linked to asset
        tracking = self.Tracking.create({
            'package_id': self.package.id,
            'biological_asset_id': asset.id,
            'current_weight': 250.0,
            'life_stage': 'growing',
            'last_gps_lat': 34.0522,
            'last_gps_lng': -118.2437,
            'vessel_phase': 'ready'
        })

        # 3. Read dynamic properties (caches the values)
        self.assertAlmostEqual(asset.current_weight, 250.0)

        # 4. Update the tracking carrier status/phase to 'dirty' (filtering it out)
        tracking.write({'vessel_phase': 'dirty'})

        # 5. Assert that the cache has been correctly invalidated and values are updated
        # Without vessel_phase in api.depends, asset.current_weight will remain 250.0 (failing state)
        self.assertAlmostEqual(asset.current_weight, 0.0)

