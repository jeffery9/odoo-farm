from odoo.tests.common import TransactionCase

class TestParcelGIS(TransactionCase):

    def setUp(self):
        super(TestParcelGIS, self).setUp()
        self.Location = self.env['stock.location']

    def test_01_gis_map_url(self):
        """ 测试根据坐标自动生成地图链接 """
        parcel = self.Location.create({
            'name': 'Pond 1',
            'is_land_parcel': True,
            'gps_lat': 31.2304,
            'gps_lng': 121.4737
        })
        self.assertTrue('openstreetmap.org' in parcel.gis_map_url)
        self.assertTrue('31.2304' in parcel.gis_map_url)

    def test_02_water_depth_conversion(self):
        """ 测试单位换算逻辑 [US-01-02] """
        pond = self.Location.create({
            'name': 'Fish Tank',
            'water_depth': 1.5 # 1.5 meters
        })
        # 自动计算分米
        self.assertEqual(pond.water_depth_dm, 15.0)
        
        # 反向计算
        pond.water_depth_dm = 20.0
        self.assertEqual(pond.water_depth, 2.0)
