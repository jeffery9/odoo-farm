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
        cls.strawberry = cls.Product.create({'name': 'Raw Strawberry', 'type': 'product'})
        cls.sugar = cls.Product.create({'name': 'White Sugar', 'type': 'product'})
        cls.jam = cls.Product.create({'name': 'Strawberry Jam', 'type': 'product'})

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

    def test_03_toll_manufacturing_mass_balance_epic_135(self):
        """
        US-135-01: Test Subcontracting Mass Balance validation.
        Ensure that receiving products below the minimum yield tolerance raises an error.
        """
        from odoo.exceptions import ValidationError

        # 1. Setup a BOM with a strict 25% minimum yield tolerance
        bom = self.Bom.create({
            'product_tmpl_id': self.jam.product_tmpl_id.id,
            'product_qty': 100.0,
            'type': 'subcontract',
            'min_yield_tolerance_pct': 25.0,
        })
        
        # 2. Mock an incoming picking (Subcontractor sending finished goods back)
        partner = self.env['res.partner'].create({'name': 'Shady Co-Packer Inc.'})
        picking_type = self.env['stock.picking.type'].search([('code', '=', 'incoming')], limit=1)
        location_dest = self.env['stock.location'].search([('usage', '=', 'internal')], limit=1)
        location_supplier = self.env['stock.location'].search([('usage', '=', 'supplier')], limit=1)

        picking = self.env['stock.picking'].create({
            'partner_id': partner.id,
            'picking_type_id': picking_type.id,
            'location_id': location_supplier.id,
            'location_dest_id': location_dest.id,
        })

        move = self.env['stock.move'].create({
            'name': 'Receive Jam from Co-packer',
            'product_id': self.jam.id,
            'product_uom_qty': 200.0, # Attempting to receive only 200kg (20% yield based on mock 1000kg sent)
            'product_uom': self.jam.uom_id.id,
            'picking_id': picking.id,
            'location_id': location_supplier.id,
            'location_dest_id': location_dest.id,
            'bom_id': bom.id,
        })
        
        # Mock the subcontracting flag which would normally be set by Odoo's native subcontracting module
        move.is_subcontract = True
        
        picking.action_confirm()
        picking.action_assign()
        move.quantity = 200.0 # Force the done quantity
        
        # 3. The Validation should fail because 200 / 1000 = 20%, which is less than 25% min yield
        with self.assertRaises(ValidationError) as error_catcher:
            picking.button_validate()
            
        self.assertIn("Mass Balance Anomaly", str(error_catcher.exception), "The system failed to block a fraudulent toll manufacturing receipt.")
