from odoo.tests.common import TransactionCase

class TestQualityAlert(TransactionCase):

    def setUp(self):
        super(TestQualityAlert, self).setUp()
        self.Check = self.env['farm.quality.check']
        self.Alert = self.env['farm.quality.alert']
        self.Lot = self.env['stock.lot']
        self.Product = self.env['product.product']
        
        self.product = self.Product.create({'name': 'Test Crop', 'type': 'product'})
        self.lot = self.Lot.create({'name': 'LOT-QC-001', 'product_id': self.product.id})
        self.point = self.env['farm.quality.point'].create({'name': 'Standard Test'})

    def test_01_create_alert_from_failed_check(self):
        """ 测试从失败的检查中触发质量告警 [US-15] """
        check = self.Check.create({
            'point_id': self.point.id,
            'lot_id': self.lot.id,
        })
        check.action_fail()
        
        # 触发创建告警
        alert = check.action_open_quality_alert()
        self.assertEqual(alert.lot_id.id, self.lot.id)
        self.assertEqual(alert.state, 'new')
        
        # 模拟处理：标记为报废
        alert.action_close_scrapped()
        self.assertEqual(alert.state, 'closed')
