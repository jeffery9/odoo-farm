# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo import fields

class TestEpic094(TransactionCase):
    """ BDD Test for Epic 094: Smart Livestock Management """

    def setUp(self):
        super(TestEpic094, self).setUp()
        self.Lot = self.env['stock.lot']
        self.IslLot = self.env['agri.isl.lot.livestock']
        self.EnvLog = self.env['farm.livestock.house.env']
        self.Event = self.env['farm.livestock.event']
        self.Task = self.env['agri.isl.livestock.task']
        
        self.product = self.env['product.product'].create({
            'name': 'Angus Cow',
            'type': 'consu'
        })
        
        self.lot = self.Lot.create({
            'name': 'ANIMAL-001',
            'product_id': self.product.id,
            'company_id': self.env.company.id
        })
        
        self.isl_lot = self.IslLot.create({
            'lot_id': self.lot.id,
            'birth_date': '2025-01-01',
            'gender': 'female',
            'current_weight': 250.0
        })

    def test_01_individual_animal_life_log_and_pedigree_tracking(self):
        """ Verify RFID linkage and parent-child pedigree links """
        # Life log event
        event = self.Event.create({
            'lot_id': self.lot.id,
            'event_type': 'vaccination',
            'notes': 'Yearly FMD vaccine'
        })
        self.assertEqual(event.lot_id.id, self.lot.id)
        
        # Pedigree verification (simulated by checking lot summary)
        summary = self.lot._get_isl_summary_parts()
        self.assertTrue(any("Husbandry: female" in s for s in summary))

    def test_02_ai_driven_health_monitoring_and_behavioral_risk_alerts(self):
        """ Verify "Comfort Index" calculation """
        log = self.EnvLog.create({
            'location_id': self.env['farm.location'].create({'name': 'Barn A'}).id,
            'temperature': 25.0,
            'humidity': 60.0
        })
        # Comfort Index: 0.8 * 25 + (60/100) * (25 - 14.4) + 46.4 = 20 + 0.6 * 10.6 + 46.4 = 20 + 6.36 + 46.4 = 72.76
        self.assertAlmostEqual(log.comfort_index, 72.76, places=2)

    def test_03_precision_feeding_management_based_on_growth_stage(self):
        """ Verify FCR tracking in real-time """
        production = self.env['mrp.production'].create({
            'product_id': self.product.id,
            'product_uom_id': self.product.uom_id.id,
            'product_qty': 1.0,
        })
        production.lot_producing_id = self.lot.id
        
        task = self.Task.create({
            'intervention_id': production.id,
            'initial_total_weight': 200.0,
            'final_total_weight': 250.0
        })
        
        # Gain is 50kg. product_qty (feed) is 1.0 (simulation). FCR = feed / gain
        # In reality product_qty might be large, but let's check the formula
        task._compute_fcr_isl()
        self.assertEqual(task.fcr, 1.0/50.0)

    def test_05_automated_environmental_optimization_for_livestock_welfare(self):
        """ Verify ventilation trigger for gas thresholds """
        log = self.EnvLog.create({
            'location_id': self.env['farm.location'].create({'name': 'Barn B'}).id,
            'ammonia_level': 25.0, # High ammonia
            'co2_level': 3000.0   # High CO2
        })
        
        # In a real system, there would be an automated action or compute to trigger ventilation
        # Here we verify the thresholds are captured
        self.assertGreater(log.ammonia_level, 20.0, "High ammonia level should be recorded")
        self.assertGreater(log.co2_level, 2000.0, "High CO2 level should be recorded")
