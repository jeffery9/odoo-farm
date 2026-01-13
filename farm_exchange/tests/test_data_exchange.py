from odoo.tests.common import TransactionCase
import base64

class TestDataExchange(TransactionCase):

    def setUp(self):
        super(TestDataExchange, self).setUp()
        self.Exchanger = self.env['farm.data.exchanger']
        
        # 创建一个测试地块
        self.env['stock.location'].create({
            'name': 'Exchange Plot 1',
            'is_land_parcel': True,
            'land_area': 50.5,
            'gps_lat': 30.0
        })

    def test_01_daplos_export(self):
        """ 测试 DAPLOS XML 导出格式 [US-20-02] """
        ex = self.Exchanger.create({
            'name': 'DAPLOS Export Test',
            'format_type': 'daplos',
            'exchange_type': 'export'
        })
        ex.action_perform_exchange()
        
        self.assertEqual(ex.state, 'done')
        content = base64.b64decode(ex.data_file).decode()
        # 验证 XML 结构中是否包含地块信息
        self.assertTrue('ISO11783_TaskData' in content)
        self.assertTrue('Exchange Plot 1' in content)
        self.assertTrue('50.5' in content)

    def test_02_telepac_export(self):
        """ 测试 TELEPAC CSV 导出格式 """
        ex = self.Exchanger.create({
            'name': 'TELEPAC Export Test',
            'format_type': 'telepac',
            'exchange_type': 'export'
        })
        ex.action_perform_exchange()
        
        content = base64.b64decode(ex.data_file).decode()
        # 验证 CSV 分隔符和内容
        self.assertTrue('ParcelName;Area;CertLevel' in content)
        self.assertTrue('Exchange Plot 1;50.5' in content)
