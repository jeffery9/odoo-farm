from odoo.tests.common import TransactionCase

class TestESGCore(TransactionCase):
    def test_01_esg_registry(self):
        """ Test ESG model existence """
        self.assertIn('esg.indicator', self.env)
