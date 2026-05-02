from odoo.tests.common import TransactionCase

class TestFarmSubsidy(TransactionCase):
    def test_01_subsidy_application(self):
        """ Test subsidy application model """
        if 'farm.subsidy.application' not in self.env:
            self.skipTest("farm.subsidy.application model not found")
        app = self.env['farm.subsidy.application'].create({
            'name': 'Wheat Subsidy 2026',
            'subsidy_type': 'crop',
            'requested_amount': 5000.0
        })
        self.assertEqual(app.requested_amount, 5000.0)
