from odoo.tests import HttpCase, tagged

@tagged('-at_install', 'post_install')
class TestUiTour(HttpCase):
    def test_01_aqua_tour(self):
        self.assertTrue(True)
