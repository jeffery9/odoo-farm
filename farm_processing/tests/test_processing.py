from odoo.tests.common import TransactionCase

class TestFarmProcessing(TransactionCase):

    def setUp(self):
        super(TestFarmProcessing, self).setUp()
        self.MO = self.env['mrp.production']
        self.Product = self.env['product.product']
        self.Lot = self.env['stock.lot']
        
        # 1. 原始材料：生猪肉
        self.pork = self.Product.create({'name': 'Raw Pork', 'type': 'product', 'tracking': 'lot'})
        self.raw_lot = self.Lot.create({'name': 'PORK-RAW-01', 'product_id': self.pork.id})
        
        # 2. 加工品：腊肉
        self.bacon = self.Product.create({'name': 'Farm Bacon', 'type': 'product', 'tracking': 'lot'})
        
        # 3. BOM
        self.bom = self.env['mrp.bom'].create({
            'product_tmpl_id': self.bacon.product_tmpl_id.id,
            'product_qty': 1.0,
            'type': 'normal',
            'bom_line_ids': [(0, 0, {'product_id': self.pork.id, 'product_qty': 1.2})]
        })

    def test_01_processing_energy_and_trace(self):
        """ 测试加工能耗记录与批次溯源关联 """
        # 创建加工订单
        mo = self.MO.create({
            'product_id': self.bacon.id,
            'bom_id': self.bom.id,
            'product_qty': 10.0,
            'energy_meter_start': 1200.5,
        })
        
        # 模拟加工结束
        mo.energy_meter_end = 1250.5
        mo._compute_energy_consumption()
        self.assertEqual(mo.energy_consumption, 50.0, "能耗应为50个单位")
        
        # 模拟产生加工后批次并建立关联
        finished_lot = self.Lot.create({
            'name': 'BACON-PROC-01',
            'product_id': self.bacon.id,
            'parent_lot_id': self.raw_lot.id # 追溯到原材料批次
        })
        self.assertEqual(finished_lot.parent_lot_id.id, self.raw_lot.id)
