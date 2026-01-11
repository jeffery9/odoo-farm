from odoo.tests.common import TransactionCase

class TestHarvestGrading(TransactionCase):

    def setUp(self):
        super(TestHarvestGrading, self).setUp()
        self.Intervention = self.env['mrp.production']
        self.Product = self.env['product.product']
        self.Lot = self.env['stock.lot']
        
        # 创建农产品
        self.apple = self.Product.create({
            'name': 'Fuji Apple',
            'type': 'product',
            'tracking': 'lot'
        })

    def test_01_harvest_multiple_grades(self):
        """ 测试收获作业的多级产出 [US-08] """
        # 创建收获干预
        harvest_op = self.Intervention.create({
            'product_id': self.apple.id,
            'product_qty': 100.0,
            'intervention_type': 'harvesting',
        })
        
        # 模拟分级产出记录
        # 在 Odoo 中，收获通常对应 move_finished_ids
        # 我们假设用户录入了两个等级的果实
        move_a = self.env['stock.move'].create({
            'name': 'Grade A Apples',
            'product_id': self.apple.id,
            'product_uom_qty': 60.0,
            'product_uom': self.apple.uom_id.id,
            'location_id': self.apple.property_stock_production.id,
            'location_dest_id': self.env.ref('stock.stock_location_stock').id,
            'production_id': harvest_op.id,
            'quality_grade': 'grade_a'
        })
        
        move_b = self.env['stock.move'].create({
            'name': 'Grade B Apples',
            'product_id': self.apple.id,
            'product_uom_qty': 40.0,
            'product_uom': self.apple.uom_id.id,
            'location_id': self.apple.property_stock_production.id,
            'location_dest_id': self.env.ref('stock.stock_location_stock').id,
            'production_id': harvest_op.id,
            'quality_grade': 'grade_b'
        })
        
        self.assertEqual(harvest_op.move_finished_ids.mapped('quality_grade'), ['grade_a', 'grade_b'])
