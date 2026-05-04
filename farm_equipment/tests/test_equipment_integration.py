# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestEquipmentIntegration(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Equipment = self.env['maintenance.equipment']
        self.Checklist = self.env['farm.equipment.checklist']

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

    def test_03_pre_op_checklist(self):
        """ Test Equipment Pre-op Checklist association """
        # Create a checklist
        checklist = self.Checklist.create({
            'name': 'Standard Drone Check',
            'equipment_type': 'drone',
            'line_ids': [
                (0, 0, {'name': 'Check Battery Level', 'is_mandatory': True}),
                (0, 0, {'name': 'Check Propellers', 'requires_photo': True})
            ]
        })
        
        # Assign to equipment
        drone = self.Equipment.create({
            'name': 'Scout Drone',
            'checklist_id': checklist.id
        })
        
        self.assertEqual(drone.checklist_id.id, checklist.id)
        self.assertEqual(len(drone.checklist_id.line_ids), 2)
        # Verify specific line flags
        propeller_check = drone.checklist_id.line_ids.filtered(lambda l: l.name == 'Check Propellers')
        self.assertTrue(propeller_check.requires_photo)
