from odoo.tests.common import TransactionCase

class TestParcelGIS(TransactionCase):

    def setUp(self):
        super(TestParcelGIS, self).setUp()
        self.Location = self.env['agri.location']

    def test_01_gis_map_url(self):
        """ 测试根据坐标自动生成网格 [US-TECH-04-02] """
        parcel = self.Location.create({
            'name': 'Pond 1',
            'location_type': 'pond',
            'geo_point': '121.4737,31.2304'
        })
        # Verifying compute grid
        parcel._compute_spatial_grid()
        self.assertTrue(parcel.spatial_grid_id.startswith('G_'))
        self.assertEqual(parcel.spatial_grid_id, 'G_121.4737_31.2304')

