from odoo.tests.common import TransactionCase

class TestSocialImpact(TransactionCase):
    def test_01_social_registry(self):
        self.assertIn('farm.esg.social.diversity.metric', self.env)
