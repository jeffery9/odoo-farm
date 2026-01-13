from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

class TestLandUsage(TransactionCase):

    def setUp(self):
        super(TestLandUsage, self).setUp()
        self.Location = self.env['stock.location']
        self.Project = self.env['project.project']

    def test_01_prime_farmland_restriction(self):
        """ 测试基本农田用途管制校验 [US-18-01] """
        # 创建一个基本农田地块
        prime_field = self.Location.create({
            'name': 'Prime Field 101',
            'is_land_parcel': True,
            'land_usage_type': 'prime_farmland', # 基本农田
            'contract_no': 'CERT-12345'
        })
        
        # 尝试在该地块上创建“观光设施”项目
        with self.assertRaises(ValidationError):
            self.Project.create({
                'name': 'New Tourist Cafe',
                'is_agri_activity': True,
                'activity_family': 'agritourism',
                'land_parcel_id': prime_field.id
            })
            
        # 允许在该地块上进行“种植”活动
        planting_project = self.Project.create({
            'name': 'Wheat Production',
            'is_agri_activity': True,
            'activity_family': 'planting',
            'land_parcel_id': prime_field.id
        })
        self.assertTrue(planting_project)
