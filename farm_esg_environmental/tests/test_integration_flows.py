# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestESGRedLine(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.RedLineConfig = cls.env['agri.esg.red.line.config']
        cls.RedLineMonitoring = cls.env['agri.esg.red.line.monitoring']

    def test_01_red_line_config_creation(self):
        """ Test creating an ESG Red Line configuration """
        config = self.RedLineConfig.create({
            'name': 'Max Deforestation Limit',
            'red_line_type': 'deforestation',
            'threshold_value': 0.0,
            'threshold_unit': 'ha',
        })
        self.assertTrue(config.exists())
        self.assertEqual(config.red_line_type, 'deforestation')

    def test_ac_01_compliance_defense(self):
        """ [AC 评审映射] AC1 (合规防御): 必须拦截任何违反预设环境/安全红线（Red Line）的操作 """
        """ Test ESG Red Line Monitoring evaluation """
        config = self.RedLineConfig.create({
            'name': 'Water Extraction Limit',
            'red_line_type': 'water_extraction',
            'threshold_value': 1000.0,
            'threshold_unit': 'm3',
        })
        
        # Test under threshold
        monitor_safe = self.RedLineMonitoring.create({
            'red_line_config_id': config.id,
            'current_value': 500.0,
        })
        self.assertEqual(monitor_safe.compliance_status, 'compliant')

        # Test breach (exceeds threshold * 1.3 buffer, resulting in 'critical')
        monitor_breach = self.RedLineMonitoring.create({
            'red_line_config_id': config.id,
            'current_value': 1500.0,
        })
        self.assertEqual(monitor_breach.compliance_status, 'critical')
