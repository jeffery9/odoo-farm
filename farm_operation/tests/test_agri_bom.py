from odoo.tests.common import TransactionCase

class TestAgriBOM(TransactionCase):

    def setUp(self):
        super(TestAgriBOM, self).setUp()
        self.BOM = self.env['mrp.bom']
        self.Product = self.env['product.product']
        
        # 1. 创建原药
        self.pesticide = self.Product.create({'name': 'Pesticide X', 'type': 'product', 'uom_id': self.env.ref('uom.product_uom_litre').id})
        
        # 2. 创建作业成品
        self.spraying_liquid = self.Product.create({'name': 'Spraying Liquid', 'type': 'service', 'uom_id': self.env.ref('uom.product_uom_litre').id})
        
        # 3. 创建农业 BOM：稀释比例 1:500
        self.bom = self.BOM.create({
            'product_tmpl_id': self.spraying_liquid.product_tmpl_id.id,
            'product_qty': 1.0,
            'type': 'normal',
            'bom_line_ids': [(0, 0, {
                'product_id': self.pesticide.id,
                'product_qty': 1.0,
                'dilution_ratio': 500.0 # 1单位原药对应500单位成品
            })]
        })

    def test_01_dilution_calculation(self):
        """ 测试稀释比例自动计算投入量 [US-01-04] """
        # 创建一个 1000L 的喷洒任务
        mo = self.env['mrp.production'].create({
            'product_id': self.spraying_liquid.id,
            'bom_id': self.bom.id,
            'product_qty': 1000.0,
        })
        
        # 根据 1:500，1000L 成品应消耗 2L 原药
        pesticide_move = mo.move_raw_ids.filtered(lambda m: m.product_id == self.pesticide)
        self.assertEqual(pesticide_move.product_uom_qty, 2.0, "1000L成品应对应2L原药")
