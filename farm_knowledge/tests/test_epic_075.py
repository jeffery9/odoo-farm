# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError

class TestEpic075(TransactionCase):
    """ BDD Test for Epic 075 Agricultural Knowledge Management """

    def setUp(self):
        super(TestEpic075, self).setUp()
        self.knowledge_base = self.env['agricultural.knowledge']

    def test_01_structured_agricultural_knowledge_base_construction(self):
        """
        Scenario: Structured agricultural knowledge base construction
        """
        article = self.knowledge_base.create({
            'name': 'Rice Blast Management',
            'content': '<p>Prevention measures for rice blast...</p>',
            'category': 'pest_disease',
            'tags': 'Rice, Blast, Fungus',
            'knowledge_type': 'article'
        })
        
        self.assertTrue(article.id)
        results = self.knowledge_base.smart_search('Rice Blast')
        self.assertIn(article, results)

    def test_02_context_aware_ai_farming_recommendations(self):
        """
        Scenario: Context-aware AI farming recommendations
        """
        # Create a pest/disease entry
        pest = self.env['agri.pest.disease'].create({
            'name': 'Late Blight',
            'category': 'disease',
            'symptoms': 'Water-soaked spots on leaves',
            'integrated_treatment': '<p>Apply copper-based fungicides and improve drainage.</p>'
        })
        
        # Link a knowledge article
        self.knowledge_base.create({
            'name': 'Managing Late Blight in Potatoes',
            'pest_disease_id': pest.id,
            'category': 'pest_disease'
        })
        
        # Search by symptoms
        matches = self.knowledge_base.search_pest_disease_by_symptoms('water-soaked spots')
        self.assertIn(pest, matches)
        
        # Get recommendations
        rec = pest.get_treatment_recommendations('integrated')
        self.assertIn('copper-based fungicides', rec['treatment'])

    def test_03_multi_lingual_agricultural_q_a_via_natural_language(self):
        """
        Scenario: Multi-lingual agricultural Q&A via natural language
        """
        # Mandarin entry
        article_cn = self.knowledge_base.create({
            'name': '水稻纹枯病防治',
            'content': '<p>水稻纹枯病的防治方法包括...</p>',
            'tags': '水稻, 纹枯病',
        })
        
        # Search using Mandarin keywords
        results_cn = self.knowledge_base.smart_search('水稻')
        self.assertIn(article_cn, results_cn)
        
        # English entry
        article_en = self.knowledge_base.create({
            'name': 'Rice Sheath Blight',
            'content': '<p>Control methods for Rice Sheath Blight...</p>',
            'tags': 'Rice, Sheath Blight',
        })
        
        results_en = self.knowledge_base.smart_search('Sheath Blight')
        self.assertIn(article_en, results_en)
