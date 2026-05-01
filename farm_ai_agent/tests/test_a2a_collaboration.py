from odoo.tests.common import TransactionCase
import json

class TestA2ACollaboration(TransactionCase):

    def setUp(self):
        super(TestA2ACollaboration, self).setUp()
        self.Intervention = self.env['mrp.production']
        self.A2A = self.env['agri.a2a.message']
        
        # Setup test data
        self.product = self.env['product.product'].create({'name': 'Organic Tomato', 'type': 'consu'})
        self.intervention = self.Intervention.create({
            'product_id': self.product.id,
            'product_qty': 100.0,
            'geo_point': '120.456,30.789', # Level 1 Spatial evidence
            'carbon_intensity': 2.5,       # Level 0 Sustainability evidence
            'nitrogen_qty': 50.0,          # Level 1 Target Nitrogen
        })

    def test_01_plan_payload_construction(self):
        """Test Agent A constructing a PlanAPI payload with evidence."""
        # Ensure quality fingerprint exists
        self.intervention.action_finalize_clearing()
        
        payload = self.A2A.construct_plan_payload(
            agent_id='agent_a_producer',
            intent_type='SUBMIT_PROVISION',
            business_object=self.intervention
        )
        
        self.assertEqual(payload['intent']['type'], 'SUBMIT_PROVISION')
        self.assertEqual(payload['context_memory']['spatial_grid'], 'G_120.456_30.789')
        self.assertIn('quality_fingerprint', payload['evidence_bundle'])
        self.assertEqual(payload['evidence_bundle']['quality_fingerprint']['model'], 'mrp.production')

    def test_02_agent_b_audit_flow(self):
        """Test Agent B parsing payload and triggering EvidenceAnalyzer."""
        # 1. Simulate Agent A sending message
        payload = self.A2A.construct_plan_payload(
            agent_id='agent_a_producer',
            intent_type='REQUEST_AUDIT',
            business_object=self.intervention
        )
        payload_json = json.dumps(payload)
        
        # 2. Simulate Agent B receiving and parsing
        result = self.A2A.parse_and_validate_plan(payload_json)
        self.assertEqual(result['status'], 'accepted')
        
        # 3. Simulate Agent B triggering EvidenceAnalyzer on the related object
        audit_results = self.intervention.perform_evidence_audit()
        
        # If GPS matches (which our stub returns True), positive confidence should be high
        self.assertGreater(audit_results['positive_confidence'], 0.4)
        self.assertEqual(audit_results['status'], 'verified')

    def test_03_nutrient_feedback_actuation(self):
        """
        Test Level 1+: Physical Feedback Loop.
        Sensor Data -> Suggestion -> Actuation.
        """
        # 1. Mock sensor data: Soil nitrogen is high (45kg), target was 50kg.
        # Threshold in mixin: if soil > 80% of target (40kg), reduce input.
        sensor_data = {'n_soil_level': 45.0}
        
        # 2. Get suggested correction from NutrientMixin
        corrections = self.intervention.suggest_nutrient_correction(sensor_data)
        self.assertEqual(corrections.get('nitrogen_qty'), -0.2, "Decision engine failed to suggest 20% reduction")
        
        # 3. Apply actuation via ActuatorMixin
        # We need to mock some moves to see the effect
        nitrogen_product = self.env['product.product'].create({'name': 'Pure Nitrogen Fertilizer'})
        move = self.env['stock.move'].create({
            'name': 'Nitrogen Input',
            'product_id': nitrogen_product.id,
            'product_uom_qty': 100.0,
            'product_uom': self.env.ref('uom.product_uom_kgrm').id,
            'location_id': self.env.ref('stock.stock_location_stock').id,
            'location_dest_id': self.env.ref('stock.stock_location_customers').id,
            'raw_material_production_id': self.intervention.id,
        })
        
        # Trigger actuation
        self.intervention.apply_feedback_correction(corrections)
        
        # 4. Verify physical update: 100kg -> 80kg (20% reduction)
        self.assertEqual(move.product_uom_qty, 80.0, "Actuator failed to update physical stock move quantity")