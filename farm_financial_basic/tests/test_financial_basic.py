from odoo.tests.common import TransactionCase, tagged

@tagged('post_install', '-at_install')
class TestFinancialBasic(TransactionCase):
    def setUp(self):
        super().setUp()
        self.Product = self.env['product.product']
        self.product = self.Product.create({'name': 'Seed Cost', 'type': 'consu'})

    def test_01_cost_template_creation(self):
        """ Test creating a cost template """
        Model = self.env.get('agri.cost.template')
        if not Model:
            self.skipTest("agri.cost.template model not found")
        template = Model.create({
            'name': 'Standard Planting Cost',
            'product_id': self.product.id,
            'standard_amount': 500.0
        })
        self.assertEqual(template.standard_amount, 500.0)
