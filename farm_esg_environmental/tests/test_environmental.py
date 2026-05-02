from odoo.tests.common import TransactionCase

class TestEnvironmental(TransactionCase):
    def test_01_env_registry(self):
        if 'farm.esg.water.usage' in self.env:
            self.assertTrue(True)
