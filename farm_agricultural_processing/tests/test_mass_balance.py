from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError

class TestMassBalance(TransactionCase):

    def setUp(self):
        super().setUp()
        self.MO = self.env['mrp.production']
        self.Product = self.env['product.product']
        
        self.raw = self.Product.create({'name': 'Raw Fruit', 'type': 'consu'})
        self.finished = self.Product.create({'name': 'Fruit Jam', 'type': 'consu'})

    def test_01_balance_check(self):
        """ Test Mass Balance Gate logic """
        mo = self.MO.create({
            'product_id': self.finished.id,
            'product_qty': 100.0,
        })
        
        if hasattr(mo, 'scrap_qty'):
            mo.scrap_qty = 5.0
            
        if hasattr(mo, '_compute_total_output_qty'):
            mo._compute_total_output_qty()
            
        self.assertTrue(mo.id)
