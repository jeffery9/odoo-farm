# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError

class TestA2ACollaboration(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Coordination = cls.env['agri.ai.coordination.layer']
        
    def test_01_coordination_layer_creation(self):
        """ Test basic coordination layer setup """
        coord = self.Coordination.create({
            'name': 'Pest-Irrigation Sync',
            'coordination_type': 'vision_decision_integration',
            'result_aggregation_method': 'weighted_average',
        })
        self.assertTrue(coord.exists())
        self.assertEqual(coord.status, 'draft')
        
    def test_02_multi_service_linkage(self):
        """ Test linking multiple AI services to the coordination layer """
        coord = self.Coordination.create({
            'name': 'Full Automation Loop',
            'coordination_type': 'cross_module_workflow',
        })
        
        # Link a decision agent if available
        agent = self.env['agri.ai.agent'].create({
            'name': 'Planner Agent',
            'agent_type': 'planning',
        })
        coord.ai_decision_ids = [(4, agent.id)]
        
        # Link a vision service if available
        vision = self.env['agri.ai.pest.disease.detection'].create({
            'name': 'Pest Detector',
            'detection_type': 'pest',
        })
        coord.ai_vision_ids = [(4, vision.id)]
        
        self.assertEqual(len(coord.ai_decision_ids), 1)
        self.assertEqual(len(coord.ai_vision_ids), 1)

    def test_03_coordination_execution_workflow(self):
        """ Test coordination execution state changes """
        coord = self.Coordination.create({
            'name': 'Workflow Test',
            'coordination_type': 'cross_module_workflow',
        })
        
        if hasattr(coord, 'action_execute_coordination'):
            coord.action_execute_coordination()
            self.assertEqual(coord.status, 'completed')

    def test_04_native_vector_cosine_similarity(self):
        """ Verify native cosine similarity vector math for RAG memory """
        # Create a product and a stock lot with ISL proxy
        product = self.env['product.product'].create({
            'name': 'Organic Soybean',
            'type': 'consu',
            'is_storable': True,
        })
        lot = self.env['stock.lot'].create({
            'name': 'LOT-VEC-01',
            'product_id': product.id,
            'company_id': self.env.company.id,
        })
        isl_lot = self.env['agri.isl.stock.lot'].create({
            'stock_lot_id': lot.id,
            'industry_type': 'field_crop',
            'vector_embedding': '[1.0, 0.0, 0.0]', # 3D vector representing soybean traits
        })
        
        # Test cosine similarity calculation
        similarity_exact = isl_lot.calculate_cosine_similarity([1.0, 0.0, 0.0])
        self.assertAlmostEqual(similarity_exact, 1.0)
        
        similarity_ortho = isl_lot.calculate_cosine_similarity([0.0, 1.0, 0.0])
        self.assertAlmostEqual(similarity_ortho, 0.0)

    def test_05_autonomous_resource_auction(self):
        """ Verify autonomous resource auction and credit bidding mechanism """
        # Create a workcenter (physical resource)
        workcenter = self.env['mrp.workcenter'].create({
            'name': 'Smart Irrigation Valve #3',
            'code': 'SIV3',
        })
        
        # Open an autonomous resource auction for this workcenter
        auction = self.env['agri.a2a.resource.auction'].create({
            'name': 'AUC-SIV3-TIMESLOT',
            'resource_ref': f'mrp.workcenter:{workcenter.id}',
        })
        self.assertEqual(auction.state, 'open')
        
        # Submitting competitive bids autonomously from different agents
        bid1 = self.env['agri.a2a.resource.bid'].create({
            'auction_id': auction.id,
            'agent_id': 'agent:crop:irrigation',
            'amount': 25.5,
            'bid_type': 'water',
        })
        bid2 = self.env['agri.a2a.resource.bid'].create({
            'auction_id': auction.id,
            'agent_id': 'agent:livestock:drinking',
            'amount': 42.0,
            'bid_type': 'water',
        })
        
        # Close auction - Livestock agent wins the resource allocation because 42.0 > 25.5
        auction.action_close_auction()
        self.assertEqual(auction.state, 'allocated')
        self.assertEqual(auction.winner_agent_id, 'agent:livestock:drinking')
        self.assertEqual(auction.current_highest_bid, 42.0)
