from odoo.tests.common import TransactionCase
from datetime import date, timedelta

class TestLivestockLogic(TransactionCase):

    def setUp(self):
        super(TestLivestockLogic, self).setUp()
        self.Lot = self.env['stock.lot']
        self.Product = self.env['product.product']
        self.Bom = self.env['mrp.bom']
        
        # 1. Create animal product
        self.pig = self.Product.create({'name': 'Pig', 'type': 'product'})
        self.feed = self.Product.create({'name': 'Pig Feed', 'type': 'product'})
        
        # 2. Create feeding recipe
        self.bom = self.Bom.create({
            'product_id': self.pig.id,
            'product_tmpl_id': self.pig.product_tmpl_id.id,
            'product_qty': 1.0,
            'type': 'normal',
            'intervention_type': 'feeding',
            'bom_line_ids': [(0, 0, {'product_id': self.feed.id, 'product_qty': 2.5})]
        })

    def test_01_adg_prediction(self):
        """ Test weight prediction based on ADG [US-03-01] """
        # Create a lot born 10 days ago
        ten_days_ago = date.today() - timedelta(days=10)
        lot = self.Lot.create({
            'name': 'PIG-001',
            'product_id': self.pig.id,
            'start_weight': 20.0,
            'average_daily_gain': 0.8,
            'create_date': ten_days_ago,
            'biological_stage': 'growing'
        })
        
        lot._compute_predicted_weight()
        # 20kg + (10 days * 0.8 ADG) = 28kg
        self.assertEqual(lot.current_predicted_weight, 28.0)

    def test_02_daily_depletion_cron(self):
        """ Test the cron job for daily feeding [US-03-01] """
        lot = self.Lot.create({
            'name': 'PIG-DEP-01',
            'product_id': self.pig.id,
            'animal_count': 50,
            'biological_stage': 'growing',
            'active_feeding_bom_id': self.bom.id
        })
        
        # Run cron manually
        self.Lot._cron_daily_feed_depletion()
        
        # Check if an intervention was created and finished
        interventions = self.env['mrp.production'].search([
            ('lot_producing_id', '=', lot.id),
            ('intervention_type', '=', 'feeding')
        ])
        self.assertTrue(interventions)
        self.assertEqual(interventions[0].state, 'done')
        # Qty should match animal count
        self.assertEqual(interventions[0].product_qty, 50.0)
