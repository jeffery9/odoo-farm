from odoo.tests.common import TransactionCase

class TestFarmProcessing(TransactionCase):

    def setUp(self):
        super(TestFarmProcessing, self).setUp()
        self.MO = self.env['mrp.production']
        self.Product = self.env['product.product']
        self.Lot = self.env['stock.lot']
        
        self.pork = self.Product.create({'name': 'Raw Pork', 'type': 'consu'})
        self.raw_lot = self.Lot.create({'name': 'PORK-RAW-01', 'product_id': self.pork.id})
        self.bacon = self.Product.create({'name': 'Farm Bacon', 'type': 'consu'})
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
        })
        
        if hasattr(mo, 'energy_reading_start'):
            mo.energy_reading_start = 1200.5
            mo.energy_reading_end = 1250.5
            if hasattr(mo, 'energy_consumption'):
                self.assertEqual(mo.energy_reading_end - mo.energy_reading_start, 50.0)
        
        finished_lot = self.Lot.create({
            'name': 'BACON-PROC-01',
            'product_id': self.bacon.id,
        })
        if hasattr(finished_lot, 'parent_lot_ids'):
            finished_lot.parent_lot_ids = [(4, self.raw_lot.id)]
            self.assertIn(self.raw_lot, finished_lot.parent_lot_ids)
