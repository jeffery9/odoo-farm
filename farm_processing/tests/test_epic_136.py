# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo import fields
from datetime import timedelta

class TestEpic136(TransactionCase):
    """ BDD Test for Epic 136 WIP Shelf Life Degradation """

    def setUp(self):
        super(TestEpic136, self).setUp()
        self.uom_unit = self.env.ref('uom.product_uom_unit', raise_if_not_found=False) or \
                        self.env['uom.uom'].search([('name', '=', 'Units')], limit=1)
        
        self.product = self.env['product.product'].create({
            'name': 'Temp Sensitive Juice',
            'type': 'product',
            'uom_id': self.uom_unit.id,
            'uom_po_id': self.uom_unit.id,
            'tracking': 'lot',
            'use_expiration_date': True,
            'expiration_time': 7,
        })
        self.workcenter = self.env['mrp.workcenter'].create({
            'name': 'Cold Press Room',
            'capacity': 1,
            'time_start': 0,
            'time_stop': 0,
        })
        self.bom = self.env['mrp.bom'].create({
            'product_tmpl_id': self.product.product_tmpl_id.id,
            'product_qty': 1.0,
            'type': 'normal',
        })
        self.env['mrp.routing.workcenter'].create({
            'name': 'Pressing',
            'bom_id': self.bom.id,
            'workcenter_id': self.workcenter.id,
            'time_cycle': 60,
            'sequence': 1,
        })

    def test_01_capture_wip_time_temperature_indicator__tti__during_processing(self):
        """
        Scenario: Capture WIP Time-Temperature Indicator (TTI) during processing
        """
        mo = self.env['mrp.production'].create({
            'product_id': self.product.id,
            'bom_id': self.bom.id,
            'product_qty': 1.0,
        })
        mo.action_confirm()
        wo = mo.workorder_ids[0]
        
        # Simulate IoT Capture
        wo.write({
            'wip_exposure_hours': 2.5,
            'avg_env_temperature': 25.0
        })
        
        wo.button_start()
        wo.button_finish()
        
        self.assertEqual(wo.wip_exposure_hours, 2.5)
        self.assertEqual(wo.avg_env_temperature, 25.0)

    def test_02_dynamic_expiration_date_penalty_for_prolonged_wip_exposure(self):
        """
        Scenario: Dynamic expiration date penalty for prolonged WIP exposure
        """
        mo = self.env['mrp.production'].create({
            'product_id': self.product.id,
            'bom_id': self.bom.id,
            'product_qty': 1.0,
        })
        mo.action_confirm()
        
        # Produce the lot
        lot = self.env['stock.lot'].create({
            'name': 'LOT136',
            'product_id': self.product.id,
            'company_id': self.env.company.id,
        })
        mo.lot_producing_id = lot
        
        # Set initial expiration date
        initial_exp = fields.Datetime.now() + timedelta(days=7)
        lot.expiration_date = initial_exp
        
        wo = mo.workorder_ids[0]
        wo.write({
            'wip_exposure_hours': 5.0, # Penalty trigger: > 1.0
            'avg_env_temperature': 26.0 # Penalty trigger: > 20.0
        })
        
        # Mock calculation: penalty_hours = (5.0 - 1.0) * 12 = 48 hours
        wo.button_start()
        wo.button_finish()
        
        expected_exp = initial_exp - timedelta(hours=48)
        # Using timestamp comparison to avoid minor millisecond differences
        self.assertAlmostEqual(lot.expiration_date.timestamp(), expected_exp.timestamp(), delta=2)

    def test_03_wip_exposure_dashboard_alerts_and_meltdown_warnings(self):
        """
        Scenario: WIP exposure dashboard alerts and meltdown warnings
        """
        mo = self.env['mrp.production'].create({
            'product_id': self.product.id,
            'bom_id': self.bom.id,
            'product_qty': 1.0,
        })
        mo.action_confirm()
        wo = mo.workorder_ids[0]
        
        # Threshold is 10.0. 80% is 8.0.
        wo.wip_exposure_hours = 8.5
        self.assertEqual(wo.wip_exposure_status, 'orange')
        
        wo.wip_exposure_hours = 11.0
        self.assertEqual(wo.wip_exposure_status, 'red')
