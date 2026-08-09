# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from datetime import date, timedelta

class TestLivestockISL(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Product = cls.env['product.product']
        cls.AnimalLot = cls.env['agri.isl.lot.livestock']
        cls.HusbandryBom = cls.env['agri.isl.livestock.recipe']
        
        cls.cow_product = cls.Product.create({
            'name': 'Angus Cow',
            'type': 'consu'
        })

    def test_01_animal_lot_creation(self):
        """ Test creating an individual animal lot with ISL attributes """
        birth = date.today() - timedelta(days=365)
        animal = self.AnimalLot.create({
            'name': 'COW-2025-001',
            'product_id': self.cow_product.id,
            'birth_date': birth,
            'gender': 'female',
            'current_weight': 450.0
        })
        
        self.assertTrue(animal.exists())
        # Check standard lot linkage
        self.assertTrue(animal.lot_id.exists())
        self.assertEqual(animal.lot_id.name, 'COW-2025-001')
        
        # Check breeding status
        self.assertEqual(animal.breeding_status, 'immature')
        animal.breeding_status = 'pregnant'
        self.assertEqual(animal.breeding_status, 'pregnant')

    def test_02_husbandry_recipe(self):
        """ Test livestock-specific BOM (Husbandry Recipe) attributes """
        bom = self.HusbandryBom.create({
            'product_tmpl_id': self.cow_product.product_tmpl_id.id,
            'product_qty': 1.0,
            'growth_days_expected': 730,
            'daily_feed_intake': 12.5
        })
        
        self.assertTrue(bom.exists())
        self.assertEqual(bom.growth_days_expected, 730)
        self.assertEqual(bom.daily_feed_intake, 12.5)
        # Check standard BOM linkage
        self.assertTrue(bom.recipe_id.exists())
        self.assertEqual(bom.recipe_id.product_tmpl_id.id, self.cow_product.product_tmpl_id.id)
