from odoo.tests.common import TransactionCase

class TestFinancialCore(TransactionCase):
    def test_01_abstract_model_exists(self):
        """ Verify abstract financial model is in registry """
        self.assertIn('farm.financial.abstract', self.env)
