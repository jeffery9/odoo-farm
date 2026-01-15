from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from datetime import timedelta

class TestFarmAgriculturalProcessing(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.user_admin = cls.env.ref('base.user_admin')

        # Load necessary models
        cls.ProductProduct = cls.env['product.product']
        cls.MrpBom = cls.env['mrp.bom']
        cls.MrpProduction = cls.env['mrp.production']
        cls.FarmScCategory = cls.env['farm.sc.category']
        cls.FarmScLicense = cls.env['farm.sc.license']
        cls.ResConfigSettings = cls.env['res.config.settings']
        
        # Create basic data
        cls.product_uom_unit = cls.env.ref('uom.product_uom_unit')
        cls.product_finished = cls.ProductProduct.create({
            'name': 'Processed Product',
            'type': 'product',
            'uom_id': cls.product_uom_unit.id,
            'default_code': 'PP-1',
        })
        cls.product_raw = cls.ProductProduct.create({
            'name': 'Raw Product',
            'type': 'product',
            'uom_id': cls.product_uom_unit.id,
            'default_code': 'RP-1',
        })

        # Create SC Category
        cls.sc_category_food = cls.FarmScCategory.create({
            'name': 'Food Production',
            'code': 'SP001',
        })
        cls.sc_category_drink = cls.FarmScCategory.create({
            'name': 'Beverage Production',
            'code': 'SP002',
        })

    def test_01_sc_license_interception(self):
        """ Test US-14-21: SC License Interception on MO confirmation. """
        # Create a BOM that requires a specific SC category
        bom = self.MrpBom.create({
            'product_tmpl_id': self.product_finished.product_tmpl_id.id,
            'product_qty': 1,
            'type': 'normal',
            'bom_line_ids': [
                (0, 0, {'product_id': self.product_raw.id, 'product_qty': 1}),
            ],
            'sc_category_id': self.sc_category_food.id,
        })

        # Scenario 1: No valid SC license for the required category
        mo_no_license = self.MrpProduction.create({
            'product_id': self.product_finished.id,
            'product_qty': 1,
            'bom_id': bom.id,
        })
        with self.assertRaises(UserError, msg="MO confirmation should be blocked without a valid SC license"):
            mo_no_license.action_confirm()
        self.assertEqual(mo_no_license.state, 'draft', "MO state should remain draft")

        # Scenario 2: Create a valid SC license
        self.FarmScLicense.create({
            'name': 'SC-LIC-001',
            'expiry_date': fields.Date.today() + timedelta(days=365),
            'category_ids': [(4, self.sc_category_food.id)],
        })
        
        mo_with_license = self.MrpProduction.create({
            'product_id': self.product_finished.id,
            'product_qty': 1,
            'bom_id': bom.id,
        })
        mo_with_license.action_confirm() # Should pass now
        self.assertEqual(mo_with_license.state, 'confirmed', "MO should be confirmed with a valid SC license")
        
        # Scenario 3: Expired SC license
        self.FarmScLicense.create({
            'name': 'SC-LIC-002',
            'expiry_date': fields.Date.today() - timedelta(days=1), # Expired
            'category_ids': [(4, self.sc_category_food.id)],
        })
        mo_expired_license = self.MrpProduction.create({
            'product_id': self.product_finished.id,
            'product_qty': 1,
            'bom_id': bom.id,
        })
        with self.assertRaises(UserError, msg="MO confirmation should be blocked with an expired SC license"):
            mo_expired_license.action_confirm()
        self.assertEqual(mo_expired_license.state, 'draft', "MO state should remain draft")
        
        # Scenario 4: Wrong SC category
        self.FarmScLicense.create({
            'name': 'SC-LIC-003',
            'expiry_date': fields.Date.today() + timedelta(days=365),
            'category_ids': [(4, self.sc_category_drink.id)], # Wrong category
        })
        mo_wrong_category = self.MrpProduction.create({
            'product_id': self.product_finished.id,
            'product_qty': 1,
            'bom_id': bom.id,
        })
        with self.assertRaises(UserError, msg="MO confirmation should be blocked with wrong SC category"):
            mo_wrong_category.action_confirm()
        self.assertEqual(mo_wrong_category.state, 'draft', "MO state should remain draft")

    def test_02_agri_processing_enabled_flag(self):
        """ Test `is_agri_processing_enabled` flag on BOM and MO. """
        # Initial check: module is not explicitly enabled in settings, so should be False
        bom = self.MrpBom.create({
            'product_tmpl_id': self.product_finished.product_tmpl_id.id,
            'product_qty': 1,
            'type': 'normal',
        })
        mo = self.MrpProduction.create({
            'product_id': self.product_finished.id,
            'bom_id': bom.id,
            'product_qty': 1,
        })
        self.assertFalse(bom.is_agri_processing_enabled, "is_agri_processing_enabled should be False by default on BOM")
        self.assertFalse(mo.is_agri_processing_enabled, "is_agri_processing_enabled should be False by default on MO")

        # Enable the module
        config_settings = self.ResConfigSettings.create({})
        config_settings.module_farm_agricultural_processing = True
        config_settings.execute() # This saves the config parameter
        
        # Refresh records
        bom.invalidate_cache(['is_agri_processing_enabled'])
        mo.invalidate_cache(['is_agri_processing_enabled'])
        
        self.assertTrue(bom.is_agri_processing_enabled, "is_agri_processing_enabled should be True after enabling module on BOM")
        self.assertTrue(mo.is_agri_processing_enabled, "is_agri_processing_enabled should be True after enabling module on MO")

        # Disable the module
        config_settings = self.ResConfigSettings.create({})
        config_settings.module_farm_agricultural_processing = False
        config_settings.execute()
        
        # Refresh records
        bom.invalidate_cache(['is_agri_processing_enabled'])
        mo.invalidate_cache(['is_agri_processing_enabled'])

        self.assertFalse(bom.is_agri_processing_enabled, "is_agri_processing_enabled should be False after disabling module on BOM")
        self.assertFalse(mo.is_agri_processing_enabled, "is_agri_processing_enabled should be False after disabling module on MO")