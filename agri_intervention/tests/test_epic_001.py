# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError, UserError

class TestEpic001AgriculturalMasterData(TransactionCase):
    """ BDD Test for Epic 001 Agricultural Master Data """

    def setUp(self):
        super(TestEpic001AgriculturalMasterData, self).setUp()
        self.Project = self.env['project.project']
        self.FarmActivity = self.env['farm.activity']
        self.Location = self.env['agri.location']
        self.SoilAnalysis = self.env['agri.soil.analysis']
        self.Lot = self.env['stock.lot']
        self.Kinship = self.env['agri.lot.kinship']
        self.Product = self.env['product.product']
        self.SaleOrder = self.env['sale.order']
        self.Partner = self.env['res.partner'].create({'name': 'Test Partner'})

    def test_01_multi_format_activity_classification(self):
        """
        Scenario: Multi-format activity classification
        Verify multi-format activity classification on farm.activity
        """
        project_planting = self.FarmActivity.create({
            'name': 'Organic Wheat 2026',
            'is_agri_activity': True,
            'activity_family': 'planting'
        })
        self.assertEqual(project_planting.activity_family, 'planting', "Activity family should be set to planting.")

        project_livestock = self.FarmActivity.create({
            'name': 'Dairy Herd Management',
            'is_agri_activity': True,
            'activity_family': 'livestock'
        })
        self.assertEqual(project_livestock.activity_family, 'livestock', "Activity family should be set to livestock.")

    def test_02_parcel_gis_digitization(self):
        """
        Scenario: Parcel GIS digitization
        Verify parcel GIS digitization and soil analysis tracking
        """
        # Create an agri location with geo_polygon (semicolon separated as expected by plugins)
        parcel = self.Location.create({
            'name': 'North Field A1',
            'location_type': 'field',
            'geo_polygon': '121.47,31.23;121.48,31.23;121.48,31.24;121.47,31.24;121.47,31.23'
        })
        self.assertTrue(parcel.geo_polygon, "Geo polygon should be stored.")

        # Verify soil analysis record
        analysis = self.SoilAnalysis.create({
            'name': 'Soil Analysis 2026-Q1',
            'nitrogen_content': 45.0,
            'phosphorus_content': 12.5,
            'potassium_content': 30.0,
        })
        self.assertEqual(analysis.nitrogen_content, 45.0, "Soil nitrogen content should match.")

    def test_03_biological_asset_pedigree_tracking(self):
        """
        Scenario: Biological Asset Pedigree tracking
        Verify kinship tracking between biological lots
        """
        product_cow = self.Product.create({
            'name': 'Holstein Cow',
            'type': 'consu',
            'tracking': 'serial'
        })
        
        parent_lot = self.Lot.create({
            'name': 'MATRIARCH-01',
            'product_id': product_cow.id,
        })
        child_lot = self.Lot.create({
            'name': 'HEIFER-01',
            'product_id': product_cow.id,
        })

        # Establish kinship using the domain standard model
        self.Kinship.create_kinship(
            parent_lot=parent_lot,
            child_lot=child_lot,
            derivation_type='breeding'
        )

        # Verify parent/child links
        self.assertIn(child_lot, parent_lot.child_kinship_ids.mapped('child_lot_id'), "Child lot should be linked to parent.")
        self.assertIn(parent_lot, child_lot.parent_kinship_ids.mapped('parent_lot_id'), "Parent lot should be linked to child.")

