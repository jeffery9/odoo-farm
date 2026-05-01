from odoo.tests.common import TransactionCase

class TestEquipmentIntegration(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Equipment = self.env['maintenance.equipment']

    def test_01_equipment_creation_and_fields(self):
        """ Test Agricultural Equipment creation and specific fields [Integration] """
        tractor = self.Equipment.create({
            'name': 'Heavy Tractor',
            'is_agri_machinery': True,
            'horsepower': 150.0,
            'fuel_type': 'diesel'
        })
        self.assertTrue(tractor.is_agri_machinery)
        self.assertEqual(tractor.horsepower, 150.0)
        self.assertEqual(tractor.fuel_type, 'diesel')

    def test_02_drone_creation(self):
        """ Test Drone creation """
        drone = self.Equipment.create({
            'name': 'Spraying Drone X1',
            'is_drone': True,
            'working_width': 5.5,
            'max_flight_time': 30,
            'fuel_type': 'electric'
        })
        self.assertTrue(drone.is_drone)
        self.assertEqual(drone.max_flight_time, 30)

