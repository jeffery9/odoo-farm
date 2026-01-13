from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError, ValidationError

class TestRegulationSync(TransactionCase):

    def setUp(self):
        super(TestRegulationSync, self).setUp()
        self.Product = self.env['product.product']
        self.Intervention = self.env['mrp.production']
        
        # 1. 创建受监管投入品 (农药)
        self.pesticide = self.Product.create({
            'name': 'Restricted Pesticide A',
            'is_regulated_input': True,
            'reg_cert_no': 'PD20230001',
            'type': 'product'
        })

    def test_01_real_name_validation(self):
        """ 测试受监管投入品必须有操作人身份证号 [US-18-02] """
        mo = self.Intervention.create({
            'product_id': self.env.ref('product.product_delivery_01', raise_if_not_found=False).id or 1,
            'product_qty': 1.0,
            'move_raw_ids': [(0, 0, {
                'product_id': self.pesticide.id,
                'product_uom_qty': 10.0,
            })]
        })
        
        # 没有身份证号，确认应报错
        with self.assertRaises(UserError):
            mo.action_confirm()
            
        # 录入非法的身份证号格式
        with self.assertRaises(ValidationError):
            mo.operator_id_card = '12345'
            mo._check_operator_id_card()

    def test_02_json_payload_generation(self):
        """ 测试生成的“肥药两制” JSON 报文格式 """
        mo = self.Intervention.create({
            'name': 'MO/2026/0001',
            'product_id': 1,
            'product_qty': 1.0,
            'operator_id_card': '330101199001011234',
            'move_raw_ids': [(0, 0, {
                'product_id': self.pesticide.id,
                'product_uom_qty': 5.5,
            })]
        })
        
        payload = mo._generate_regulation_payload()
        self.assertEqual(payload['operator']['id_card'], '330101199001011234')
        self.assertEqual(payload['items'][0]['reg_no'], 'PD20230001')
        self.assertEqual(payload['items'][0]['dosage'], 5.5)
