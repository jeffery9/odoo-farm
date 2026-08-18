# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError

class TestTraceabilityQualityBlock(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))

        # Check if mrp.production exists and contains the necessary fields
        if 'mrp.production' not in cls.env or 'lot_producing_id' not in cls.env['mrp.production']._fields:
            cls.skip_mrp_tests = True
            return

        cls.skip_mrp_tests = False

        # 1. Create a forbidden chemical
        cls.chemical_product = cls.env['product.product'].create({
            'name': 'Banned Pesticide X',
            'type': 'consu',
            'is_agricultural_chemical': True,
            'is_forbidden': True, # We need to add these fields
        })

        # 2. Create the crop product
        cls.crop_product = cls.env['product.product'].create({
            'name': 'Organic Apples',
            'type': 'consu',
            'is_storable': True,
            'tracking': 'lot',
        })

        # 3. Create a location and operation
        cls.location = cls.env['stock.location'].create({
            'name': 'Orchard A1',
            'usage': 'internal'
        })
        
        # We need a picking type
        cls.picking_type = cls.env['stock.picking.type'].search([('code', '=', 'mrp_operation')], limit=1)

    def test_01_forbidden_chemical_blocks_shipping(self):
        """
        Scenario:
        1. An intervention (Spraying) uses a forbidden chemical.
        2. A harvesting intervention yields a Lot of Apples.
        3. The system links the Harvested Lot to the field's history (or direct BOM).
        4. When attempting to ship this Lot, a Quality Alert is raised and shipment is blocked.
        """
        if getattr(self, 'skip_mrp_tests', False):
            self.skipTest("mrp.production or lot_producing_id field not available")

        # We'll use a direct approach: The Harvest Intervention consumes the chemical directly for simplicity,
        # or we create a stock.lot and manually link its origin.
        
        lot = self.env['stock.lot'].create({
            'name': 'LOT-APPLE-001',
            'product_id': self.crop_product.id,
            'company_id': self.env.company.id
        })
        
        # Create an intervention that produced this lot
        intervention = self.env['mrp.production'].create({
            'product_id': self.crop_product.id,
            'product_qty': 100.0,
            'intervention_type': 'harvesting',
            'lot_producing_id': lot.id,
            'picking_type_id': self.picking_type.id,
        })
        
        # Inject the forbidden chemical into the intervention's consumed materials
        self.env['stock.move'].create({
            'product_id': self.chemical_product.id,
            'product_uom_qty': 1.0,
            'product_uom': self.chemical_product.uom_id.id,
            'location_id': self.location.id,
            'location_dest_id': self.location.id,
            'raw_material_production_id': intervention.id,
        })
        
        intervention.action_confirm()
        # intervention.button_mark_done() # Simplified
        
        # Attempt to create an outgoing shipment for this lot
        out_picking_type = self.env['stock.picking.type'].search([('code', '=', 'outgoing')], limit=1)
        customer_loc = self.env.ref('stock.stock_location_customers')
        
        picking = self.env['stock.picking'].create({
            'picking_type_id': out_picking_type.id,
            'location_id': self.location.id,
            'location_dest_id': customer_loc.id,
        })
        
        move = self.env['stock.move'].create({
            'product_id': self.crop_product.id,
            'product_uom_qty': 10.0,
            'product_uom': self.crop_product.uom_id.id,
            'picking_id': picking.id,
            'location_id': self.location.id,
            'location_dest_id': customer_loc.id,
        })
        
        picking.action_confirm()
        
        # Assign the lot
        move_line = self.env['stock.move.line'].create({
            'move_id': move.id,
            'product_id': self.crop_product.id,
            'lot_id': lot.id,
            'quantity': 10.0,
        })
        
        # Validating the picking should trigger the Traceability Quality Block
        with self.assertRaises(UserError) as e:
            picking.button_validate()
            
        self.assertIn("Safety Violation", str(e.exception))
        self.assertIn("Banned Pesticide X", str(e.exception))

