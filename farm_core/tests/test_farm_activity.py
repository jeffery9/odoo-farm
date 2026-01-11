from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

class TestFarmActivity(TransactionCase):

    def setUp(self):
        super(TestFarmActivity, self).setUp()
        # 初始化测试数据
        self.Project = self.env['project.project']

    def test_01_create_agri_activity(self):
        """ 测试创建不同家族的农业活动 [US-01] """
        project_planting = self.Project.create({
            'name': 'Organic Wheat 2026',
            'is_agri_activity': True,
            'activity_family': 'planting'
        })
        self.assertTrue(project_planting.is_agri_activity, "应该是农业活动")
        self.assertEqual(project_planting.activity_family, 'planting', "活动家族应该是种植业")

    def test_02_default_non_agri(self):
        """ 测试默认情况下不是农业活动 """
        project_normal = self.Project.create({
            'name': 'Normal Office Project'
        })
        self.assertFalse(project_normal.is_agri_activity, "普通项目默认不应是农业活动")

class TestFarmLocation(TransactionCase):

    def setUp(self):
        super(TestFarmLocation, self).setUp()
        self.Location = self.env['stock.location']

    def test_03_create_land_parcel(self):
        """ 测试创建地块 [US-03] """
        parcel = self.Location.create({
            'name': 'North Field A1',
            'is_land_parcel': True,
            'land_area': 50.5,
            'gps_coordinates': '{"type": "Point", "coordinates": [116.4, 39.9]}'
        })
        self.assertTrue(parcel.is_land_parcel, "应该是地块")
        self.assertEqual(parcel.land_area, 50.5, "面积应为 50.5")
