# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
import logging

_logger = logging.getLogger(__name__)

class TestDroneDispatchFlow(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))

        # 1. Create a Location (Land Parcel)
        cls.location = cls.env['farm.location'].create({
            'name': 'Test Grid A1'
        })

        # Create a dummy profile
        cls.profile = cls.env['iiot.device.profile'].create({
            'name': 'Drone Profile',
            'code': 'DRONE-PROF',
            'telemetry_topic_template': 't/{device}',
            'command_topic_template': 'c/{device}'
        })
        # 2. Create a Scout Drone (Robotic Asset)
        cls.drone_device = cls.env['iiot.device'].create({
            'name': 'Scout Drone D1',
            'serial_number': 'SN-DRONE-001',
            'profile_id': cls.profile.id,
            'physical_level': 'controller'
        })
        
        cls.drone = cls.env['farm.robot'].create({
            'name': 'AgriScout 5000',
            'robot_type': 'scout', # Bridge expects 'scout'
            'device_id': cls.drone_device.id
        })

        # 3. Create a Biological Twin for the location
        cls.twin = cls.env['agri.biological.twin'].create({
            'name': 'Wheat Crop A1 Twin',
            'location_id': cls.location.id,
            'health_score': 100.0
        })

        # 4. Create an AI Autonomous Orchestrator
        cls.orchestrator = cls.env['ai.autonomous.orchestrator'].create({
            'name': 'L5 Regional Dispatcher',
            'auto_dispatch_threshold': 60.0
        })
        
        # Ensure project exists for the task creation
        try:
            cls.project = cls.env.ref('farm_operation.project_farm_operations')
        except ValueError:
            cls.project = cls.env['project.project'].create({
                'name': 'Farm Operations Project'
            })
            cls.env['ir.model.data'].create({
                'name': 'project_farm_operations',
                'module': 'farm_operation',
                'model': 'project.project',
                'res_id': cls.project.id
            })

    def test_01_end_to_end_drone_dispatch(self):
        """
        Simulates:
        1. IoT Telemetry indicates critical crop stress.
        2. Biological Twin health score drops below threshold.
        3. AI Orchestrator detects low health and dispatches a Drone.
        4. Mission is created and robot is engaged.
        """
        _logger.info("Simulating IoT Telemetry triggering health score drop...")
        self.twin.write({'health_score': 45.0}) 
        
        _logger.info("Running AI Autonomous Scan...")
        self.orchestrator.action_run_autonomous_scan()
        
        logs = self.env['ai.autonomous.mission.log'].search([
            ('orchestrator_id', '=', self.orchestrator.id),
            ('twin_id', '=', self.twin.id)
        ])
        
        self.assertTrue(logs, "AI Orchestrator should have generated a mission log.")
        self.assertEqual(logs[0].status, 'dispatched', "Mission log status should be 'dispatched'.")
        
        mission = logs[0].mission_id
        self.assertTrue(mission, "A physical robotic mission must be created.")
        self.assertEqual(mission.robot_id.id, self.drone.id, "The idle scout drone should have been assigned.")
        self.assertEqual(mission.location_id.id, self.location.id, "Drone must be dispatched to the exact twin location.")
        
        _logger.info("Drone dispatch flow successfully validated.")
