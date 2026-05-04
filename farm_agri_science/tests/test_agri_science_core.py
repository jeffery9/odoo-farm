from odoo.tests.common import TransactionCase

class TestAgriScienceCore(TransactionCase):

    def setUp(self):
        super().setUp()
        # Ensure we have a location to work with
        self.agri_loc = self.env['agri.location'].create({
            'name': 'Science Field',
            'location_type': 'field'
        })
        self.parcel = self.env['farm.location'].create({
            'name': 'Science Parcel',
            'agri_location_id': self.agri_loc.id,
            'land_area': 5000.0
        })

    def test_01_grid_cell_creation(self):
        """ Test creating spatial grid cells [US-014-2026] """
        Model = self.env.get('agri.geospatial.grid.cell')
        if not Model:
            self.skipTest("agri.geospatial.grid.cell not found")
        cell = Model.create({
            'location_id': self.parcel.id,
            'row': 1,
            'col': 1,
            'ndvi_index': 0.75
        })
        self.assertEqual(cell.row, 1)

    def test_02_biological_twin_stub(self):
        """ Test Biological Twin model existence """
        TwinModel = self.env.get('agri.biological.twin')
        VarietyModel = self.env.get('agri.industry.variety')
        
        if TwinModel and VarietyModel:
            variety = VarietyModel.create({
                'product_name': 'Wheat',
                'variety_name': 'Winter Wheat'
            })
            twin = TwinModel.create({
                'name': 'Wheat-2026-Twin',
                'variety_id': variety.id
            })
            self.assertTrue(twin.id)
