# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
import logging

_logger = logging.getLogger(__name__)

class TestAdvancedProcessingEpics(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super(TestAdvancedProcessingEpics, cls).setUpClass()
        # Disable tracking to speed up tests
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        
        # Models
        cls.Product = cls.env['product.product']
        cls.Bom = cls.env['mrp.bom']
        cls.BomLine = cls.env['mrp.bom.line']
        cls.Production = cls.env['mrp.production']
        cls.Workorder = cls.env['mrp.workorder']

        # Setup basic mock products
        cls.strawberry = cls.Product.create({'name': 'Raw Strawberry', 'type': 'consu', 'is_storable': True})
        cls.sugar = cls.Product.create({'name': 'White Sugar', 'type': 'consu', 'is_storable': True})
        cls.jam = cls.Product.create({'name': 'Strawberry Jam', 'type': 'consu', 'is_storable': True})

    def test_01_dynamic_recipe_formulation_epic_134(self):
        """
        US-134-01 & US-134-02: Test AST-based dynamic formula calculation.
        """
        bom = self.Bom.create({
            'product_tmpl_id': self.jam.product_tmpl_id.id,
            'product_qty': 10.0,
            'type': 'normal',
        })
        
        # Primary ingredient
        self.BomLine.create({
            'bom_id': bom.id,
            'product_id': self.strawberry.id,
            'product_qty': 8.0,
        })
        
        # Dynamic excipient (Sugar)
        sugar_line = self.BomLine.create({
            'bom_id': bom.id,
            'product_id': self.sugar.id,
            'product_qty': 2.0,
            'is_dynamic_formulation': True,
            'dynamic_formula': 'base_qty + (12 - brix) * 0.5',
            'min_qty': 1.0,
            'max_qty': 5.0,
        })

        production = self.Production.create({
            'product_id': self.jam.id,
            'bom_id': bom.id,
            'product_qty': 10.0,
        })
        
        # Call the dynamic formula engine (in a real scenario, mock_brix=9.0 is hardcoded in our model for testing)
        production.action_apply_dynamic_formula()
        
        # Calculation: base_qty(2.0) + (12 - 9.0)*0.5 = 2.0 + 1.5 = 3.5
        sugar_move = production.move_raw_ids.filtered(lambda m: m.product_id == self.sugar)
        self.assertEqual(sugar_move.product_uom_qty, 3.5, "Dynamic formulation failed to adjust sugar qty based on Brix deficit.")

    def test_02_wip_shelf_life_and_carbon_allocation_epics_136_137(self):
        """
        US-136 & US-137: Test WIP Shelf-Life penalty and granular Carbon/Cost allocation on workorder completion.
        """
        production = self.Production.create({
            'product_id': self.jam.id,
            'product_qty': 10.0,
        })
        
        # Create a mock workorder
        workorder = self.Workorder.create({
            'name': 'Cooking and Pasteurization',
            'production_id': production.id,
            'product_id': self.jam.id,
            'workcenter_id': self.env['mrp.workcenter'].create({'name': 'Cooker A'}).id,
            'wip_exposure_hours': 3.0,     # Exceeds 1h tolerance
            'avg_env_temperature': 25.0,   # Exceeds 20C tolerance
            'power_consumption_kwh': 100.0 # Huge energy spike
        })
        
        # Trigger the finish hook
        workorder.button_finish()
        
        # Verify Messages were posted to the Production chatter
        messages = self.env['mail.message'].search([
            ('res_id', '=', production.id),
            ('model', '=', 'mrp.production')
        ])
        
        message_bodies = [m.body for m in messages]
        
        # EPIC-136 Check
        penalty_found = any("WIP Shelf-Life Penalty Applied" in b for b in message_bodies)
        self.assertTrue(penalty_found, "WIP Shelf-Life degradation logic failed to trigger warning.")
        
        # EPIC-137 Check
        carbon_found = any("ESG & Cost Allocation (Scope 2)" in b for b in message_bodies)
        self.assertTrue(carbon_found, "Granular Carbon/Energy allocation failed to log to chatter.")
