from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError

class TestCrisisLockdown(TransactionCase):

    def setUp(self):
        super(TestCrisisLockdown, self).setUp()
        self.Incident = self.env['farm.crisis.incident']
        self.Protocol = self.env['farm.emergency.protocol']
        self.Lot = self.env['stock.lot']
        self.Location = self.env['stock.location']
        
        # 1. 创建协议和受影响的地块
        self.protocol = self.Protocol.create({'name': 'Quarantine', 'crisis_type': 'disease', 'required_asset_lockdown': True})
        self.parcel = self.Location.create({'name': 'Infected Zone', 'is_land_parcel': True})
        
        # 2. 创建一个在地块内的批次
        self.lot = self.Lot.create({
            'name': 'SICK-LOT',
            'product_id': 1, # Placeholder
            'location_id': self.parcel.id
        })

    def test_01_automatic_lockdown(self):
        """ 测试地块危机自动锁定该区域内的所有批次 [US-17-03] """
        # 初始应未锁定
        self.assertFalse(self.lot.is_crisis_locked)
        
        # 触发危机
        incident = self.Incident.create({
            'protocol_id': self.protocol.id,
            'affected_location_ids': [(4, self.parcel.id)],
            'state': 'active'
        })
        
        # 再次检查锁定状态
        self.lot._compute_crisis_lock()
        self.assertTrue(self.lot.is_crisis_locked)

    def test_02_sale_blockage(self):
        """ 测试处于锁定状态的批次无法确认销售订单 """
        incident = self.Incident.create({
            'protocol_id': self.protocol.id,
            'affected_location_ids': [(4, self.parcel.id)],
            'state': 'active'
        })
        
        so = self.env['sale.order'].create({
            'partner_id': self.env['res.partner'].create({'name': 'Customer'}).id,
            'order_line': [(0, 0, {
                'product_id': self.lot.product_id.id,
                'lot_id': self.lot.id
            })]
        })
        
        with self.assertRaises(UserError):
            so.action_confirm()
