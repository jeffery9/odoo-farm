from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError

class TestMassBalance(TransactionCase):

    def setUp(self):
        super(TestMassBalance, self).setUp()
        self.MO = self.env['mrp.production']
        self.Product = self.env['product.product']
        
        self.raw = self.Product.create({'name': 'Raw Fruit', 'type': 'product'})
        self.clean = self.Product.create({'name': 'Cleaned Fruit', 'type': 'product'})
        
        self.bom = self.env['mrp.bom'].create({
            'product_tmpl_id': self.clean.product_tmpl_id.id,
            'product_qty': 1.0,
            'type': 'normal',
            'bom_line_ids': [(0, 0, {'product_id': self.raw.id, 'product_qty': 1.0})]
        })

    def test_01_balance_check(self):
        """ 测试总量平衡拦截逻辑 """
        mo = self.MO.create({
            'product_id': self.clean.id,
            'bom_id': self.bom.id,
            'product_qty': 100.0, # 投入 100kg
        })
        
        # 模拟：产出 90kg，记录损耗 5kg -> 总计 95kg
        mo.scrap_qty = 5.0
        mo._compute_total_output_qty()
        self.assertFalse(mo.is_balanced)
        
        # 尝试标记完成，应报错
        with self.assertRaises(UserError):
            mo.button_mark_done()
            
        # 修正：产出 90kg，损耗 10kg -> 总计 100kg
        mo.scrap_qty = 10.0
        mo._compute_total_output_qty()
        self.assertTrue(mo.is_balanced)
