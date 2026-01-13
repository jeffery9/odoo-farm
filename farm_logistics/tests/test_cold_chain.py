from odoo.tests.common import TransactionCase

class TestColdChain(TransactionCase):

    def setUp(self):
        super(TestColdChain, self).setUp()
        self.Picking = self.env['stock.picking']
        self.Product = self.env['product.product']
        self.TempLog = self.env['farm.transport.temperature']
        
        # 创建冷链产品
        self.milk = self.Product.create({
            'name': 'Fresh Milk',
            'requires_cold_chain': True,
            'target_temperature_min': 2.0,
            'target_temperature_max': 6.0,
            'type': 'product'
        })

    def test_01_cold_chain_detection(self):
        """ 测试调拨单自动识别冷链需求 [US-14-11] """
        picking = self.Picking.create({
            'picking_type_id': self.env.ref('stock.picking_type_out').id,
            'location_id': self.env.ref('stock.stock_location_stock').id,
            'location_dest_id': self.env.ref('stock.stock_location_customers').id,
            'move_ids': [(0, 0, {
                'name': 'Milk Move',
                'product_id': self.milk.id,
                'product_uom_qty': 10,
                'location_id': self.env.ref('stock.stock_location_stock').id,
                'location_dest_id': self.env.ref('stock.stock_location_customers').id,
            })]
        })
        
        picking._compute_is_cold_chain()
        self.assertTrue(picking.is_cold_chain)

    def test_02_temperature_logging(self):
        """ 测试运输温度记录逻辑 """
        picking = self.Picking.create({'picking_type_id': self.env.ref('stock.picking_type_out').id})
        log = self.TempLog.create({
            'picking_id': picking.id,
            'temperature': 4.5,
            'location_name': 'Loading Dock'
        })
        self.assertEqual(picking.temperature_log_ids[0].temperature, 4.5)
