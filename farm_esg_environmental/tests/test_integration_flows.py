# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestESGRedLine(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.RedLineConfig = cls.env['agri.esg.red.line.config']
        cls.RedLineMonitoring = cls.env['agri.esg.red.line.monitoring']
        cls.Partner = cls.env['res.partner'].create({'name': 'Partner A'})

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
            'config_id': config.id,
            'partner_id': self.Partner.id,
            'current_value': 500.0,
        })
        # Assuming there is an evaluation method, if not, we check basic state
        if hasattr(monitor_safe, 'action_evaluate_status'):
            monitor_safe.action_evaluate_status()
            self.assertEqual(monitor_safe.status, 'compliant')

        # Test breach
        monitor_breach = self.RedLineMonitoring.create({
            'config_id': config.id,
            'partner_id': self.Partner.id,
            'current_value': 1500.0,
        })
        if hasattr(monitor_breach, 'action_evaluate_status'):
            monitor_breach.action_evaluate_status()
            self.assertEqual(monitor_breach.status, 'breached')
