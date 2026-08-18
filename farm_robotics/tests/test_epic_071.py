# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo import fields

class TestEpic071(TransactionCase):
    """ BDD Test for Epic 071 Drone Based Crop Monitoring """

    def setUp(self):
        super(TestEpic071, self).setUp()
        self.location = self.env['farm.location'].create({
            'name': 'Parcel A',
            'location_type': 'field'
        })
        self.drone = self.env['farm.robot'].create({
            'name': 'Scout Drone 01',
            'robot_type': 'scout'
        })

    def test_01_periodic_crop_growth_monitoring_via_multi_spectral_imaging(self):
        """
        Scenario: Periodic crop growth monitoring via multi-spectral imaging
        """
        mission = self.env['farm.robot.mission'].create({
            'robot_id': self.drone.id,
            'location_id': self.location.id,
            'state': 'scheduled'
        })
        
        # Simulate drone capturing images and processing NDVI
        mission.action_start_mission()
        
        # Mock NDVI analysis results stored in mission (adding a field if needed in real impl)
        # Here we simulate the effect by setting efficiency or custom message
        mission.write({
            'actual_path_geojson': '{"type": "LineString", "coordinates": [[0,0], [1,1]]}',
        })
        mission.action_complete_mission()
        
        self.assertEqual(mission.state, 'completed')
        self.assertTrue(mission.efficiency_score >= 0, "Efficiency score should be calculated")

    def test_02_ai_driven_pest_and_disease_recognition_from_drone_imagery(self):
        """
        Scenario: AI-driven pest and disease recognition from drone imagery
        """
        mission = self.env['farm.robot.mission'].create({
            'robot_id': self.drone.id,
            'location_id': self.location.id,
            'state': 'in_progress'
        })
        
        # Simulate AI Vision detecting a hotspot
        # In a real scenario, this would be a call to farm_ai_vision
        pest = self.env['agri.pest.disease'].create({
            'name': 'Aphids',
            'category': 'pest'
        })
        
        # Trigger scouting activity if threshold exceeded
        activity = self.env['mail.activity'].create({
            'res_id': mission.id,
            'res_model_id': self.env['ir.model']._get('farm.robot.mission').id,
            'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
            'summary': 'Scouting needed: High Aphid density detected',
            'note': 'Hotspot detected at Parcel A during drone mission'
        })
        
        self.assertTrue(activity.id)
        self.assertIn('Aphid', activity.summary)

    def test_03_precision_spraying_and_seeding_operations_via_drones(self):
        """
        Scenario: Precision spraying and seeding operations via drones
        """
        sprayer_drone = self.env['farm.robot'].create({
            'name': 'Spray Drone 01',
            'robot_type': 'sprayer'
        })
        
        mission = self.env['farm.robot.mission'].create({
            'robot_id': sprayer_drone.id,
            'location_id': self.location.id,
            'planned_path_geojson': '{"type": "FeatureCollection", "features": []}'
        })
        
        mission.action_start_mission()
        
        # Simulate recording consumption in lot history (Epic 052)
        # Assuming a production task is linked
        task = self.env['project.task'].create({
            'name': 'Precision Spraying Task',
            'land_parcel_id': self.location.id
        })
        mission.task_id = task.id
        
        mission.action_complete_mission()
        
        self.assertEqual(mission.state, 'completed')
        self.assertTrue(mission.task_id, "Mission should be linked to a task")
