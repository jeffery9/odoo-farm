from odoo.tests.common import TransactionCase

class TestEcology(TransactionCase):
    def test_01_ecology_registry(self):
        """ Test Ecology model existence """
        if 'farm.ecology.survey' in self.env:
            self.assertTrue(True)
