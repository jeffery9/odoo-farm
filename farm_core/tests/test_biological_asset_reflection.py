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

    def test_event_driven_write_hook_sync(self):
        from unittest.mock import patch, MagicMock

        # Create a dummy lot
        lot = self.env['stock.lot'].create({
            'name': 'LOT-PIG-TEST',
            'product_id': self.product_pig.id,
            'company_id': self.env.company.id,
        })

        # Create Biological Asset
        asset = self.Asset.create({'name': 'PIG-HERD-B', 'agricultural_type': 'animal'})

        # Setup mock for farm.livestock.event
        mock_create = MagicMock()
        mock_event_model = MagicMock()
        mock_event_model.create = mock_create
        mock_recordset = MagicMock()
        mock_recordset.create = mock_create
        mock_event_model._browse.return_value = mock_recordset

        # Mock the __contains__ and __getitem__ of self.env to simulate model registry presence safely
        orig_getitem = type(self.env).__getitem__
        
        def my_contains(*args, **kwargs):
            item = args[1] if len(args) == 2 else args[0]
            if item == 'farm.livestock.event':
                return True
            return item in self.env.registry

        def my_getitem(*args, **kwargs):
            key = args[1] if len(args) == 2 else args[0]
            if key == 'farm.livestock.event':
                return mock_event_model
            return orig_getitem(self.env, key)

        with patch.object(type(self.env), '__contains__', side_effect=my_contains), \
             patch.object(type(self.env), '__getitem__', side_effect=my_getitem):

            # 1. Create tracking first
            tracking = self.Tracking.create({
                'package_id': self.package.id,
                'biological_asset_id': asset.id,
                'current_weight': 100.0,
                'life_stage': 'juvenile'
            })

            # 2. Create quant linked directly to the resolved tracking package_id
            self.env['stock.quant'].create({
                'product_id': self.product_pig.id,
                'location_id': self.env.ref('stock.stock_location_stock').id,
                'package_id': tracking.package_id.id,
                'lot_id': lot.id,
                'quantity': 1.0,
            })

            # Flush and invalidate to ensure One2many computes can resolve newly created quants
            self.env.flush_all()
            tracking.package_id.invalidate_recordset(['quant_ids'])
            tracking.invalidate_recordset()
            tracking._compute_lot_ids()

            # Trigger write of physical state
            tracking.write({'current_weight': 115.0})
            self.assertEqual(asset.current_weight, 115.0)

            # Verify that mock create was called for weight update
            mock_create.assert_any_call({
                'lot_id': lot.id,
                'event_type': 'weight',
                'event_date': mock_create.call_args_list[0][0][0]['event_date'], # dynamically match datetime
                'notes': f"Auto-sync from Matter Carrier: {tracking.package_id.name}. Weight: 115.0 kg."
            })

            # Trigger write of stage update
            tracking.write({'life_stage': 'growing'})
            mock_create.assert_any_call({
                'lot_id': lot.id,
                'event_type': 'movement',
                'event_date': mock_create.call_args_list[-1][0][0]['event_date'],
                'notes': f"Growth transition to growing."
            })

