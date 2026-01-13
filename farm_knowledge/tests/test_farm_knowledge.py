from odoo.tests.common import TransactionCase

class TestFarmKnowledge(TransactionCase):

    def setUp(self):
        super(TestFarmKnowledge, self).setUp()
        self.PestDisease = self.env['farm.pest.disease']
        self.Knowledge = self.env['agricultural.knowledge']
        self.FAQ = self.env['faq.entry']

    def test_smart_search(self):
        """Test the smart search functionality [US-16-06]"""
        self.Knowledge.create({
            'name': 'How to control Wheat Rust',
            'tags': 'wheat, rust, disease',
            'category': 'pest_disease',
            'content': 'Check for red spots on leaves.'
        })
        self.Knowledge.create({
            'name': 'Irrigation Best Practices',
            'tags': 'water, efficiency',
            'category': 'irrigation'
        })
        
        # Search by keyword
        results = self.Knowledge.smart_search('wheat')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, 'How to control Wheat Rust')
        
        # Search in content
        results = self.Knowledge.smart_search('spots')
        self.assertEqual(len(results), 1)

    def test_knowledge_stats(self):
        """Test counters"""
        k = self.Knowledge.create({'name': 'Test'})
        k.action_mark_helpful()
        self.assertEqual(k.helpful_count, 1)