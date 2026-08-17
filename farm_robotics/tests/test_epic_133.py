# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

class TestEpic133(TransactionCase):
    """ BDD Test Suite for Epic 133: Epic 133 Swarm Robotics Coordination (群控机器人协同) """

    def setUp(self):
        super(TestEpic133, self).setUp()
        self.coord = self.env['agri.swarm.coord'].create({
            'name': 'Test Swarm Coordination',
            'state': 'progress'
        })

    def test_01_swarm_robotics_collision_avoidance_checks(self):
        """ US-133-01 """
        self.coord.write({
            'speed_alpha': 850.0,
            'coordinates_beta': 1.2
        })
        self.assertFalse(self.coord.is_clear)
        self.assertEqual(self.coord.target_speed, 0.0)

    def test_02_realtime_tractor_sprayer_vra_valve_adjustment_vra(self):
        """ US-133-02 """
        self.coord.write({
            'gps_coordinates': 'Low-SOM'
        })
        self.assertEqual(self.coord.nozzle_flow_rate, 85.0)
        self.assertEqual(self.coord.state, 'progress')

    def test_03_sensor_offline_fallback_safe_mode_irrigation(self):
        """ US-133-03 """
        self.coord.write({
            'sensor_status': 'offline'
        })
        self.assertTrue(self.coord.safe_mode)

    def test_04_obstacle_sensor_collision_solenoid_spray_pause(self):
        """ US-133-04 """
        self.coord.write({
            'obstacle_distance': 2.5
        })
        self.assertTrue(self.coord.is_solenoid_closed)

    def test_05_high_wind_safety_sprayer_launch_block(self):
        """ US-133-05 """
        self.coord.write({
            'state': 'ready',
            'wind_limit': 4.0
        })
        with self.assertRaises(ValidationError) as e:
            self.coord.write({
                'wind_speed': 5.2
            })
        self.assertIn("Wind speed exceeds safety limits for swarm spray mission", str(e.exception))

    def test_06_swarm_drone_obstacle_detection_and_realtime_bypass(self):
        """ US-133-06 """
        self.coord.write({
            'coordination_state': 'optimal',
            'obstacle_distance': 4.5
        })
        self.assertTrue(self.coord.bypass_active)

    def test_07_swarm_drone_obstacle_detection_adaptive_mission_pause(self):
        """ US-133-07 """
        self.coord.write({
            'target_speed': 100.0,
        })
        with self.assertRaises(ValidationError) as e:
            self.coord.write({
                'obstacle_proximity': 2.9
            })
        self.assertIn("OBSTACLE_DETECTED_MISSION_PAUSED", str(e.exception))

