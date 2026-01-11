from odoo.tests.common import TransactionCase

class TestFarmProperties(TransactionCase):

    def setUp(self):
        super(TestFarmProperties, self).setUp()
        self.Location = self.env['stock.location']
        self.Lot = self.env['stock.lot']
        self.Product = self.env['product.product']

    def test_01_location_properties(self):
        """ 测试地块的动态属性 [US-02] """
        # 定义属性：酸碱度(PH)
        parcel = self.Location.create({
            'name': 'East Field B2',
            'is_land_parcel': True,
            'location_properties_definition': [{
                'name': 'ph_level',
                'string': 'PH Level',
                'type': 'integer',
            }]
        })
        
        # 设置属性值
        parcel.location_properties = {'ph_level': 7}
        self.assertEqual(parcel.location_properties.get('ph_level'), 7, "PH值应为7")

    def test_02_lot_properties(self):
        """ 测试生物资产的动态属性 [US-02] """
        product = self.Product.create({
            'name': 'Tilapia (罗非鱼)',
            'type': 'product',
            'tracking': 'lot'
        })
        
        # 在产品上定义批次属性：水温要求
        product.product_tmpl_id.lot_properties_definition = [{
            'name': 'temp_requirement',
            'string': 'Temperature Requirement',
            'type': 'integer',
        }]
        
        fish_lot = self.Lot.create({
            'name': 'FISH-2026-X',
            'product_id': product.id,
            'is_animal': True
        })
        
        # 设置批次属性值
        fish_lot.lot_properties = {'temp_requirement': 25}
        self.assertEqual(fish_lot.lot_properties.get('temp_requirement'), 25, "水温要求应为25")
