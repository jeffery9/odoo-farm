from odoo.tests.common import TransactionCase
from odoo import fields


class TestAgriculturalProcessingAdditionalFeatures(TransactionCase):
    """Test additional agricultural processing features"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))

        # Load required models
        cls.ProductProduct = cls.env['product.product']
        cls.ProductTemplate = cls.env['product.template']
        cls.FarmProcessingBom = cls.env['farm.processing.bom']
        cls.FarmSeasonalBom = cls.env['farm.seasonal.bom']
        cls.FarmSeasonalBomMaterial = cls.env['farm.seasonal.bom.material']
        cls.FarmSeasonalBomParameter = cls.env['farm.seasonal.bom.parameter']

        # Create basic data
        cls.product_uom_unit = cls.env.ref('uom.product_uom_unit')
        cls.product_template = cls.ProductTemplate.create({
            'name': 'Seasonal Product',
            'type': 'consu',
            'uom_id': cls.product_uom_unit.id,
        })
        cls.product_raw = cls.ProductProduct.create({
            'name': 'Raw Product',
            'type': 'consu',
            'uom_id': cls.product_uom_unit.id,
        })
        cls.product_material = cls.ProductProduct.create({
            'name': 'Seasonal Material',
            'type': 'consu',
            'uom_id': cls.product_uom_unit.id,
        })

    def test_seasonal_bom_creation(self):
        """Test US-04-06: Seasonal 'Versioned' Recipe Management"""
        # Create base BOM
        base_bom = self.FarmProcessingBom.create({
            'product_tmpl_id': self.product_template.id,
            'product_qty': 1,
            'type': 'normal',
            'bom_line_ids': [
                (0, 0, {'product_id': self.product_raw.id, 'product_qty': 1}),
            ],
        })

        # Create seasonal BOM
        seasonal_bom = self.FarmSeasonalBom.create({
            'product_tmpl_id': self.product_template.id,
            'bom_id': base_bom.id,
            'season_name': 'Summer 2024',
            'version_number': 1,
            'season_start_date': fields.Date.from_string('2024-06-01'),
            'season_end_date': fields.Date.from_string('2024-08-31'),
            'base_yield_factor': 1.0,
            'state': 'active',
        })

        self.assertEqual(seasonal_bom.season_name, 'Summer 2024')
        self.assertEqual(seasonal_bom.state, 'active')
        self.assertEqual(seasonal_bom.base_yield_factor, 1.0)

    def test_seasonal_material_adjustments(self):
        """Test seasonal material adjustments"""
        # Create base BOM
        base_bom = self.FarmProcessingBom.create({
            'product_tmpl_id': self.product_template.id,
            'product_qty': 1,
            'type': 'normal',
            'bom_line_ids': [
                (0, 0, {'product_id': self.product_raw.id, 'product_qty': 1}),
            ],
        })

        # Create seasonal BOM
        seasonal_bom = self.FarmSeasonalBom.create({
            'product_tmpl_id': self.product_template.id,
            'bom_id': base_bom.id,
            'season_name': 'Winter Adjustments',
            'version_number': 1,
            'season_start_date': fields.Date.from_string('2024-12-01'),
            'season_end_date': fields.Date.from_string('2025-02-28'),
            'state': 'active',
        })

        # Add seasonal material adjustment
        seasonal_material = self.FarmSeasonalBomMaterial.create({
            'seasonal_bom_id': seasonal_bom.id,
            'product_id': self.product_material.id,
            'base_qty': 10.0,
            'seasonal_qty': 15.0,
            'adjustment_reason': 'Winter season requires more material',
        })

        self.assertEqual(seasonal_material.seasonal_qty, 15.0)
        self.assertEqual(seasonal_material.adjustment_reason, 'Winter season requires more material')
        self.assertEqual(seasonal_material.qty_difference, 5.0)  # 15 - 10

    def test_seasonal_parameter_adjustments(self):
        """Test seasonal parameter adjustments"""
        # Create base BOM
        base_bom = self.FarmProcessingBom.create({
            'product_tmpl_id': self.product_template.id,
            'product_qty': 1,
            'type': 'normal',
            'bom_line_ids': [
                (0, 0, {'product_id': self.product_raw.id, 'product_qty': 1}),
            ],
        })

        # Create seasonal BOM
        seasonal_bom = self.FarmSeasonalBom.create({
            'product_tmpl_id': self.product_template.id,
            'bom_id': base_bom.id,
            'season_name': 'Summer Processing',
            'version_number': 1,
            'season_start_date': fields.Date.from_string('2024-06-01'),
            'season_end_date': fields.Date.from_string('2024-08-31'),
            'state': 'active',
        })

        # Add seasonal parameter adjustment
        seasonal_parameter = self.FarmSeasonalBomParameter.create({
            'seasonal_bom_id': seasonal_bom.id,
            'parameter_name': 'Temperature',
            'base_value': 20.0,
            'seasonal_value': 25.0,
            'unit_of_measure': 'C',
            'adjustment_reason': 'Summer requires higher temperature',
        })

        self.assertEqual(seasonal_parameter.seasonal_value, 25.0)
        self.assertEqual(seasonal_parameter.parameter_name, 'Temperature')
        self.assertEqual(seasonal_parameter.value_difference, 5.0)  # 25 - 20

    def test_seasonal_bom_date_validation(self):
        """Test seasonal BOM date validation to prevent overlaps"""
        # Create base BOM
        base_bom = self.FarmProcessingBom.create({
            'product_tmpl_id': self.product_template.id,
            'product_qty': 1,
            'type': 'normal',
            'bom_line_ids': [
                (0, 0, {'product_id': self.product_raw.id, 'product_qty': 1}),
            ],
        })

        # Create first seasonal BOM
        seasonal_bom1 = self.FarmSeasonalBom.create({
            'product_tmpl_id': self.product_template.id,
            'bom_id': base_bom.id,
            'season_name': 'Spring Season',
            'version_number': 1,
            'season_start_date': fields.Date.from_string('2024-03-01'),
            'season_end_date': fields.Date.from_string('2024-05-31'),
            'state': 'active',
        })

        # Create second seasonal BOM with overlapping dates (should be prevented by constraint)
        with self.assertRaises(Exception, msg="Should prevent overlapping seasonal BOMs for same product"):
            self.FarmSeasonalBom.create({
                'product_tmpl_id': self.product_template.id,
                'bom_id': base_bom.id,
                'season_name': 'Overlap Season',
                'version_number': 2,
                'season_start_date': fields.Date.from_string('2024-05-15'),  # Overlaps with first
                'season_end_date': fields.Date.from_string('2024-07-31'),
                'state': 'active',
            })

    def test_get_applicable_seasonal_bom(self):
        """Test getting applicable seasonal BOM for a date"""
        # Create base BOM
        base_bom = self.FarmProcessingBom.create({
            'product_tmpl_id': self.product_template.id,
            'product_qty': 1,
            'type': 'normal',
            'bom_line_ids': [
                (0, 0, {'product_id': self.product_raw.id, 'product_qty': 1}),
            ],
        })

        # Create seasonal BOM for summer
        summer_bom = self.FarmSeasonalBom.create({
            'product_tmpl_id': self.product_template.id,
            'bom_id': base_bom.id,
            'season_name': 'Summer Season',
            'version_number': 1,
            'season_start_date': fields.Date.from_string('2024-06-01'),
            'season_end_date': fields.Date.from_string('2024-08-31'),
            'state': 'active',
        })

        # Create seasonal BOM for winter
        winter_bom = self.FarmSeasonalBom.create({
            'product_tmpl_id': self.product_template.id,
            'bom_id': base_bom.id,
            'season_name': 'Winter Season',
            'version_number': 2,
            'season_start_date': fields.Date.from_string('2024-12-01'),
            'season_end_date': fields.Date.from_string('2025-02-28'),
            'state': 'active',
        })

        # Test getting summer BOM for a summer date
        summer_date = fields.Date.from_string('2024-07-15')
        applicable_bom_summer = self.FarmSeasonalBom.get_applicable_seasonal_bom(self.product_template.id, summer_date)
        self.assertEqual(applicable_bom_summer.id, summer_bom.id)

        # Test getting winter BOM for a winter date
        winter_date = fields.Date.from_string('2024-12-15')
        applicable_bom_winter = self.FarmSeasonalBom.get_applicable_seasonal_bom(self.product_template.id, winter_date)
        self.assertEqual(applicable_bom_winter.id, winter_bom.id)

        # Test getting no BOM for a date outside all seasons
        off_season_date = fields.Date.from_string('2024-11-15')
        applicable_bom_none = self.FarmSeasonalBom.get_applicable_seasonal_bom(self.product_template.id, off_season_date)
        self.assertIsNone(applicable_bom_none)