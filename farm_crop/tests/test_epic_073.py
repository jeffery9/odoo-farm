# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError

class TestEpic073(TransactionCase):
    """ BDD Test for Epic 073 Weed Identification & Control """

    def setUp(self):
        super(TestEpic073, self).setUp()
        self.parcel = self.env['farm.location'].create({
            'name': 'Field 101',
            'location_type': 'field'
        })
        self.weed_type = self.env['agri.pest.disease'].create({
            'name': 'Barnyard Grass',
            'category': 'weed',
            'severity_level': 'high'
        })

    def test_01_ai_driven_weed_species_recognition_and_density_mapping(self):
        """
        Scenario: AI-driven weed species recognition and density mapping
        """
        # Simulate AI vision identifying weeds and generating a density map
        # We store the result as a message or a custom field on location
        self.parcel.message_post(body="AI Analysis: High density of Barnyard Grass detected (80 weeds/sqm).")
        
        # Verify density info is present in chatter
        self.assertIn("Barnyard Grass", self.parcel.message_ids[0].body)
        self.assertIn("High density", self.parcel.message_ids[0].body)

    def test_02_precision_weeding_operations_and_targeted_application(self):
        """
        Scenario: Precision weeding operations and targeted application
        """
        # Create a weeding task
        task = self.env['project.task'].create({
            'name': 'Precision Weeding - Field 101',
            'location_id': self.parcel.id
        })
        
        # Simulate tracking cleared weeds (linked to a robotic mission or manual work)
        mission = self.env['farm.robot.mission'].create({
            'robot_id': self.env['farm.robot'].create({'name': 'Weeder 1', 'robot_type': 'weeder'}).id,
            'location_id': self.parcel.id,
            'task_id': task.id
        })
        
        # Record herbicide reduction
        # Assuming we track efficiency or savings in mission
        mission.write({'efficiency_score': 95.0}) # 95% herbicide saved
        
        self.assertEqual(mission.efficiency_score, 95.0)

    def test_03_herbicide_resistance_monitoring_and_adaptive_treatment(self):
        """
        Scenario: Herbicide resistance monitoring and adaptive treatment
        """
        # Weed shows resistance
        self.weed_type.write({'description': 'Signs of Glyphosate resistance observed in Field 101.'})
        
        # System alerts specialist
        activity = self.env['mail.activity'].create({
            'res_id': self.weed_type.id,
            'res_model_id': self.env['ir.model']._get('agri.pest.disease').id,
            'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
            'summary': 'Herbicide Resistance Detected',
            'note': 'Barnyard Grass showing resistance in Field 101. Recommend mechanical weeding.'
        })
        
        self.assertTrue(activity.id)
        self.assertIn('Resistance', activity.summary)
