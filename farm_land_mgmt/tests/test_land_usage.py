from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

class TestLandUsage(TransactionCase):

    def setUp(self):
        super().setUp()
        agri_loc = self.env['agri.location'].create({
            'name': 'Mgmt Field',
            'location_type': 'field'
        })
        self.parcel = self.env['farm.location'].create({
            'name': 'Mgmt Parcel',
            'agri_location_id': agri_loc.id,
            'land_nature': 'agriculture_land'
        })

    def test_01_land_nature_constraint(self):
        """ Test land usage constraints """
        # If construction land, is_land_parcel might be blocked by constraints in models
        if hasattr(self.parcel, 'land_nature'):
            with self.assertRaises(Exception):
                self.parcel.write({
                    'land_nature': 'construction_land',
                    'is_land_parcel': True
                })
