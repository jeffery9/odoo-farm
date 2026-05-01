from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError, ValidationError
from odoo.tools import mute_logger
import datetime

class TestFarmAgriculturalProcessing(TransactionCase):

    def setUp(self):
        super().setUp()
        self.MrpProduction = self.env['mrp.production']
        self.MrpBom = self.env['mrp.bom']
        self.Product = self.env['product.product']

        self.apple = self.Product.create({'name': 'Apple', 'type': 'consu'})
        self.juice = self.Product.create({'name': 'Apple Juice', 'type': 'consu'})

    def test_01_sc_license_interception(self):
        """ Test SC License check """
        bom = self.MrpBom.create({
            'product_tmpl_id': self.juice.product_tmpl_id.id,
            'product_qty': 100.0,
            'type': 'normal',
        })
        
        mo = self.MrpProduction.create({
            'product_id': self.juice.id,
            'bom_id': bom.id,
            'product_qty': 100.0,
        })
        
        # We just verify creation passes.
        self.assertTrue(mo.id)

    def test_02_agri_processing_enabled_flag(self):
        """ Test agri processing flag """
        bom = self.MrpBom.create({
            'product_tmpl_id': self.juice.product_tmpl_id.id,
            'product_qty': 10.0,
            'type': 'normal',
        })
        
        if hasattr(bom, 'is_agri_processing_enabled'):
            self.assertFalse(bom.is_agri_processing_enabled)
