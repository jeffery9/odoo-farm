from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta

class TestAgritourismFlow(TransactionCase):

    def setUp(self):
        super(TestAgritourismFlow, self).setUp()
        self.Resource = self.env['farm.resource']
        self.Booking = self.env['farm.booking']
        
        self.spot = self.Resource.create({'name': 'Fishing Spot A', 'resource_type': 'fishing'})
        self.partner = self.env['res.partner'].create({'name': 'Tourist A'})

    def test_01_booking_conflict(self):
        """ 测试同一资源的预约冲突校验 [US-05-03] """
        start = datetime.now()
        end = start + timedelta(hours=2)
        
        # 创建第一个预约
        self.Booking.create({
            'name': 'B1',
            'partner_id': self.partner.id,
            'resource_id': self.spot.id,
            'date_start': start,
            'date_stop': end,
            'state': 'confirmed'
        })
        
        # 尝试创建一个重叠的预约
        with self.assertRaises(ValidationError):
            self.Booking.create({
                'name': 'B2',
                'partner_id': self.partner.id,
                'resource_id': self.spot.id,
                'date_start': start + timedelta(hours=1),
                'date_stop': end + timedelta(hours=1),
                'state': 'confirmed'
            })

    def test_02_sale_auto_booking(self):
        """ 测试销售订单确认后自动创建预约 [US-05-04] """
        # 创建一个体验套餐产品
        package = self.env['product.product'].create({
            'name': 'Family Day Package',
            'is_experience_package': True,
            'type': 'service'
        })
        
        so = self.env['sale.order'].create({
            'partner_id': self.partner.id,
            'order_line': [(0, 0, {'product_id': package.id, 'product_uom_qty': 1})]
        })
        so.action_confirm()
        
        # 检查是否自动生成了预约
        booking = self.Booking.search([('sale_order_id', '=', so.id)])
        self.assertTrue(booking)
        self.assertEqual(booking.booking_type, 'visit')
