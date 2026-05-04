# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestIntegrationFarmAgriScience(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Profile = cls.env['agri.physiology.profile']
        cls.Stage = cls.env['agri.growth.stage']
        cls.VraStrategy = cls.env['agri.intervention.vra.strategy']
        
        cls.wheat_profile = cls.Profile.create({
            'name': 'Winter Wheat X1',
            'temp_base': 0.0,
            'temp_opt': 20.0,
            'temp_max': 30.0,
            'logistic_l': 1000.0,
            'response_max_yield': 900.0
        })
        
        cls.stage_v1 = cls.Stage.create({
            'name': 'Vegetative 1',
            'stage_code': 'V1',
            'profile_id': cls.wheat_profile.id,
            'gdd_threshold': 150.0
        })

    def test_01_physiology_profile_creation(self):
        """ Test physiology profile and stages integration """
        self.assertTrue(self.wheat_profile.exists())
        self.assertEqual(len(self.wheat_profile.stage_ids), 1)
        self.assertEqual(self.wheat_profile.stage_ids[0].stage_code, 'V1')

    def test_02_vra_strategy_integration(self):
        """ Test VRA (Variable Rate Application) Strategy properties """
        vra = self.VraStrategy.create({
            'name': 'Wheat N Application',
            'type': 'inverse_ndvi',
            'is_stage_aware': True,
            'target_yield': 800.0
        })
        self.assertTrue(vra.exists())
        self.assertEqual(vra.type, 'inverse_ndvi')
        self.assertTrue(vra.is_stage_aware)
        self.assertEqual(vra.target_yield, 800.0)
