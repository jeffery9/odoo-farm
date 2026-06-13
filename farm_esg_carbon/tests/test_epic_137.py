# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo import fields

class TestEpic137(TransactionCase):
    """ BDD Test for Epic 137 Granular Carbon Allocation """

    def setUp(self):
        super(TestEpic137, self).setUp()
        self.uom_unit = self.env.ref('uom.product_uom_unit', raise_if_not_found=False) or \
                        self.env['uom.uom'].search([('name', '=', 'Units')], limit=1)
        
        self.product = self.env['product.product'].create({
            'name': 'Low Carbon Flour',
            'type': 'product',
            'uom_id': self.uom_unit.id,
        })
        self.workcenter = self.env['mrp.workcenter'].create({
            'name': 'Electric Mill',
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
            'name': 'Milling',
            'bom_id': self.bom.id,
            'workcenter_id': self.workcenter.id,
            'time_cycle': 60,
            'sequence': 1,
        })

    def test_01_workorder_direct_integration_with_iot_smart_meters(self):
        """
        Scenario: Workorder direct integration with IoT smart meters
        """
        mo = self.env['mrp.production'].create({
            'product_id': self.product.id,
            'bom_id': self.bom.id,
            'product_qty': 1.0,
        })
        mo.action_confirm()
        wo = mo.workorder_ids[0]
        
        # Simulate IoT smart meter reading
        wo.write({'power_consumption_kwh': 45.5})
        
        wo.button_start()
        wo.button_finish()
        
        self.assertEqual(wo.power_consumption_kwh, 45.5)

    def test_02_granular_landed_cost_calculation_for_manufacturing_energy(self):
        """
        Scenario: Granular landed cost calculation for manufacturing energy
        """
        mo = self.env['mrp.production'].create({
            'product_id': self.product.id,
            'bom_id': self.bom.id,
            'product_qty': 1.0,
        })
        mo.action_confirm()
        wo = mo.workorder_ids[0]
        
        # 100 kWh * $0.15 = $15.0 financial cost
        wo.write({'power_consumption_kwh': 100.0})
        
        wo.button_start()
        wo.button_finish()
        
        # Check stock valuation layer for energy cost allocation
        svl = self.env['stock.valuation.layer'].search([
            ('stock_move_id', 'in', mo.move_finished_ids.ids),
            ('description', 'ilike', 'Energy Cost Allocation')
        ])
        self.assertTrue(svl, "Stock valuation layer for energy cost should be created.")
        self.assertAlmostEqual(sum(svl.mapped('value')), 15.0)

    def test_03_lot_level_scope_2_carbon_footprint_calculation_and_display(self):
        """
        Scenario: Lot-level Scope 2 carbon footprint calculation and display
        """
        mo = self.env['mrp.production'].create({
            'product_id': self.product.id,
            'bom_id': self.bom.id,
            'product_qty': 1.0,
        })
        mo.action_confirm()
        
        # Assign lot
        lot = self.env['stock.lot'].create({
            'name': 'LOT137',
            'product_id': self.product.id,
            'company_id': self.env.company.id,
        })
        mo.lot_producing_id = lot
        
        # 50 kWh * 0.5 kg CO2e/kWh = 25.0 kg CO2e
        wo = mo.workorder_ids[0]
        wo.write({'power_consumption_kwh': 50.0})
        
        wo.button_start()
        wo.button_finish()
        
        # Check agri.carbon.ledger creation
        ledger = self.env['agri.carbon.ledger'].search([
            ('lot_id', '=', lot.id),
        ], limit=1)
        self.assertTrue(ledger, "Carbon ledger entry for Scope 2 should be created.")
        self.assertEqual(ledger.total_co2e, 25.0)
