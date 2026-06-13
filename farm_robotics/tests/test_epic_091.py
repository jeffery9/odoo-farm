# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo import fields

class TestEpic091(TransactionCase):
    """ BDD Test for Epic 091: Agricultural Robotics Automation """

    def setUp(self):
        super(TestEpic091, self).setUp()
        self.Robot = self.env['farm.robot']
        self.Mission = self.env['farm.robot.mission']
        self.Location = self.env['farm.location'].create({'name': 'Robotics Test Field'})
        
        self.robot = self.Robot.create({
            'name': 'Robo-Harvester-01',
            'robot_type': 'harvester',
        })

    def test_01_automated_device_integration_and_real_time_status_sync(self):
        """ Verify IIoT status sync (Battery, Position) """
        # Trigger compute
        self.robot._compute_iot_status()
        
        self.assertEqual(self.robot.battery_level, 85.0, "Battery level should be synced from IIoT")
        self.assertEqual(self.robot.robot_status, 'idle', "Robot status should be synced from IIoT")
        self.assertTrue(self.robot.agent_id.startswith('robot:harvester:'), "Agent ID should be correctly formatted")

    def test_02_robotic_mission_scheduling_and_path_execution(self):
        """ Verify GeoJSON path generation and mission start """
        mission = self.Mission.create({
            'robot_id': self.robot.id,
            'location_id': self.Location.id,
            'planned_path_geojson': '{"type": "LineString", "coordinates": [[0,0], [1,1]]}'
        })
        
        mission.action_start_mission()
        self.assertEqual(mission.state, 'in_progress', "Mission should transition to in_progress")
        self.assertEqual(self.robot.current_mission_id.id, mission.id, "Robot current mission should be updated")

    def test_04_robotic_neighborhood_discovery_and_a2a_negotiation(self):
        """ Verify A2A energy-aware quotes """
        # Case 1: Low Battery rejection
        self.robot.battery_level = 15.0
        proposal = {'proposed_credits': 20.0}
        result = self.robot.evaluate_a2a_proposal(proposal)
        self.assertEqual(result['decision'], 'reject', "Robot should reject missions when battery is low")
        
        # Case 2: Medium Battery surcharge
        self.robot.battery_level = 45.0
        proposal = {'proposed_credits': 11.0} # Market avg is 10.0, surcharge factor is 1.3 -> 13.0 expected
        result = self.robot.evaluate_a2a_proposal(proposal)
        self.assertEqual(result['decision'], 'counter', "Robot should counter-propose with energy surcharge")
        self.assertGreater(result['price'], 12.0, "Counter price should include surcharge")

    def test_05_automated_robotic_evidence_package_and_path_verification(self):
        """ Verify GeoJSON trajectory evidence """
        mission = self.Mission.create({
            'robot_id': self.robot.id,
            'location_id': self.Location.id,
            'actual_path_geojson': '{"type": "LineString", "coordinates": [[0,0], [0.1, 0.1]]}'
        })
        
        # Complete mission triggers evidence loop
        mission.action_complete_mission()
        self.assertEqual(mission.state, 'completed', "Mission should be completed")
        # Check if message is posted (Level 2: Automated Evidence Loop)
        messages = self.env['mail.message'].search([('model', '=', 'farm.robot.mission'), ('res_id', '=', mission.id)])
        self.assertTrue(any("Physical trajectory data packaged" in m.body for m in messages), "Evidence package should be logged")
