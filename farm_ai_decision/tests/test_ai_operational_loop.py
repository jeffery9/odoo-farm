# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
import json
from datetime import datetime

class TestAiOperationalLoop(TransactionCase):
    """
    Test the integrated "Sense-Decide-Act" loop:
    IoT Shadow -> AI Decision -> Intervention Engine
    """
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # 1. Setup Location and Device
        cls.parcel = cls.env['farm.location'].create({
            'name': 'AI Test Field',
            'isa95_level': 'area',
        })
        
        cls.profile = cls.env['iiot.device.profile'].create({
            'name': 'Soil Sensor Profile',
            'code': 'soil_sensor_profile',
        })
        
        # 2. Setup Device with Shadow State
        cls.moisture_sensor = cls.env['iiot.device'].create({
            'name': 'Soil Sensor 01',
            'serial_number': 'SN-SOIL-001',
            'device_id': 'soil_sensor_01_id',
            'profile_id': cls.profile.id,
            'location_id': cls.parcel.id,
            'connection_status': 'online',
            'shadow_state': json.dumps({'moisture': 25.0, 'temp': 22.0})
        })

        # 3. Setup Crop
        cls.crop = cls.env['product.product'].create({
            'name': 'AI Test Corn',
            'type': 'consu',
            'is_storable': True,
        })

    def test_01_irrigation_loop(self):
        """ Test IoT -> Irrigation Decision -> Intervention loop """
        # 1. Create Decision record
        decision = self.env['agri.ai.irrigation.decision'].create({
            'name': 'Low Moisture Correction',
            'land_location_id': self.parcel.id,
            'product_id': self.crop.product_tmpl_id.id,
        })

        # 2. SENSE: Fetch from IoT Shadow
        decision.action_fetch_iot_shadow()
        self.assertEqual(decision.current_soil_moisture, 25.0, "Should pull moisture from device shadow")

        # 3. DECIDE: Calculate needs
        decision.calculate_irrigation_needs()
        self.assertTrue(decision.recommended_water_amount > 0, "AI should recommend water for 25% moisture")
        self.assertEqual(decision.status, 'recommended')

        # 4. ACT: Apply recommendation
        decision.action_apply_recommendation()
        self.assertEqual(decision.status, 'applied')
        self.assertTrue(decision.result_intervention_id, "Should have triggered an intervention")
        
        # 5. Verify the created intervention
        intervention = decision.result_intervention_id
        self.assertEqual(intervention.intervention_type, 'irrigation')
        self.assertEqual(intervention.location_id, self.parcel)
        self.assertEqual(intervention.state, 'confirmed', "Correction intervention should be auto-confirmed")

    def test_02_fertilization_loop(self):
        """ Test IoT -> Fertilization Decision loop """
        # Update shadow with NPK data
        self.moisture_sensor.shadow_state = json.dumps({
            'n': 50.0, 'p': 10.0, 'k': 80.0, 'ph': 6.5
        })

        decision = self.env['agri.ai.fertilization.decision'].create({
            'name': 'Nutrient Gap Correction',
            'land_location_id': self.parcel.id,
            'product_id': self.crop.product_tmpl_id.id,
        })

        # 1. SENSE
        decision.action_fetch_iot_shadow()
        self.assertEqual(decision.soil_nitrogen, 50.0)

        # 2. DECIDE
        decision.calculate_fertilization_needs()
        self.assertTrue(decision.recommended_n > 0)

        # 3. ACT
        decision.action_apply_recommendation()
        intervention = decision.result_intervention_id
        self.assertEqual(intervention.intervention_type, 'fertilizing')

    def test_03_ai_engine_recovery_loop(self):
        """ Test the generalized AI Decision Engine loop """
        # Create an intervention with biological stress
        mo = self.env['mrp.production'].create({
            'product_id': self.crop.id,
            'product_qty': 1.0,
            'location_id': self.parcel.id,
        })
        # Simulate stress via field (assuming biological_stress_index exists)
        if hasattr(mo, 'biological_stress_index'):
            mo.biological_stress_index = 45.0

        decision = self.env['ai.decision.engine'].create({
            'name': 'Stress Recovery',
            'intervention_id': mo.id,
        })

        # 1. DECIDE
        decision.action_generate_recovery_plan()
        plan = json.loads(decision.active_skill_json)
        self.assertEqual(plan.get('action'), 'irrigation_boost')

        # 2. ACT
        decision.action_apply_recommendation()
        recovery_mo = decision.result_intervention_id
        self.assertEqual(recovery_mo.intervention_type, 'irrigation')
        self.assertIn("AI Recovery", recovery_mo.origin)

    def test_04_pest_disease_loop(self):
        """ Test AI Pest Detection -> Intervention loop """
        decision = self.env['agri.ai.pest.disease.decision'].create({
            'name': 'Aphid Outbreak Detection',
            'land_location_id': self.parcel.id,
            'product_id': self.crop.product_tmpl_id.id,
            'pest_disease_name': 'Aphids',
            'affected_area_percentage': 55.0, # High severity (>= 50%)
        })

        # 1. DECIDE: Analyze
        decision.analyze_pest_disease_decision()
        self.assertEqual(decision.severity_level, 'high')

        # 2. ACT: Apply
        decision.action_apply_recommendation()
        
        # 3. Verify
        intervention = decision.result_intervention_id
        self.assertEqual(intervention.intervention_type, 'protection')
        self.assertIn("Aphids", intervention.origin)

    def test_05_generic_agent_loop(self):
        """ Test Generic AI Agent -> Recommendation -> Intervention loop """
        agent = self.env['agri.ai.agent'].create({
            'name': 'Optimization Agent',
            'agent_type': 'optimization',
            'model_architecture': 'rule_based',
        })
        
        # 1. Execute Agent (Mocked result will set status to recommended)
        agent.action_execute_agent(input_data={'crop_type': 'corn'})
        self.assertEqual(agent.status, 'recommended')
        
        # 2. ACT: Apply (Requires manual stub for generic agent or specific implementation)
        # For this test, we verify the status change and base action trigger
        agent.action_apply_recommendation()
        self.assertEqual(agent.status, 'applied')
