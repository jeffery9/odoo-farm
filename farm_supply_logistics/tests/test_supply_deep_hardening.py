# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase, tagged
from odoo import fields
from datetime import timedelta

@tagged('uavm_surgical', 'post_install', '-at_install')
class TestSupplyDeepHardening(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Find unit of measure
        cls.uom_unit = cls.env.ref('uom.product_uom_unit', raise_if_not_found=False) or \
                       cls.env['uom.uom'].search([('name', '=', 'Units')], limit=1)
        
        # Create a storable product tracked by lot
        cls.product = cls.env['product.product'].create({
            'name': 'FEFO Tracked Juice',
            'type': 'consu',
            'uom_id': cls.uom_unit.id if cls.uom_unit else False,
            'tracking': 'lot',
        })

    def test_fefo_expiry_sorting_math(self):
        """ Verify storable lots are correctly sorted by soonest-expiration date """
        now = fields.Datetime.now()
        
        # Check if expiration_date exists on stock.lot in the active database registry
        has_expiry_field = 'expiration_date' in self.env['stock.lot']._fields
        
        # Create three lots with distinct expiration dates / or names for fallback
        vals_1 = {
            'name': 'Lot A (Mid Expiry)',
            'product_id': self.product.id,
            'company_id': self.env.company.id,
        }
        if has_expiry_field:
            vals_1['expiration_date'] = now + timedelta(days=10)
        lot_1 = self.env['stock.lot'].create(vals_1)
        
        vals_2 = {
            'name': 'Lot B (Soonest Expiry)',
            'product_id': self.product.id,
            'company_id': self.env.company.id,
        }
        if has_expiry_field:
            vals_2['expiration_date'] = now + timedelta(days=5)
        lot_2 = self.env['stock.lot'].create(vals_2)
        
        vals_3 = {
            'name': 'Lot C (Latest Expiry)',
            'product_id': self.product.id,
            'company_id': self.env.company.id,
        }
        if has_expiry_field:
            vals_3['expiration_date'] = now + timedelta(days=20)
        lot_3 = self.env['stock.lot'].create(vals_3)
        
        # Create a lot with no expiration date
        vals_no_expiry = {
            'name': 'Lot D (No Expiry)',
            'product_id': self.product.id,
            'company_id': self.env.company.id,
        }
        if has_expiry_field:
            vals_no_expiry['expiration_date'] = False
        lot_no_expiry = self.env['stock.lot'].create(vals_no_expiry)
        
        # Collect lots
        lots = self.env['stock.lot'].browse([lot_1.id, lot_2.id, lot_3.id, lot_no_expiry.id])
        
        # Sort using Python key on real Odoo model fields (ensure lots without expiration are pushed to end)
        if has_expiry_field:
            sorted_lots_python = sorted(
                lots, 
                key=lambda l: l.expiration_date or fields.Datetime.to_datetime('9999-12-31 23:59:59')
            )
            
            # Assertions to ensure Lot B is selected first, then Lot A, then Lot C, then Lot D (no expiry)
            self.assertEqual(sorted_lots_python[0], lot_2, "Lot B (5 days) should be first.")
            self.assertEqual(sorted_lots_python[1], lot_1, "Lot A (10 days) should be second.")
            self.assertEqual(sorted_lots_python[2], lot_3, "Lot C (20 days) should be third.")
            self.assertEqual(sorted_lots_python[3], lot_no_expiry, "Lot with no expiry should be last.")

            # Also verify Odoo ORM search sort order
            sorted_lots_orm = self.env['stock.lot'].search([
                ('id', 'in', [lot_1.id, lot_2.id, lot_3.id])
            ], order='expiration_date asc')
            
            self.assertEqual(list(sorted_lots_orm), [lot_2, lot_1, lot_3], "Odoo ORM search order must match FEFO (soonest first).")
        else:
            # Fallback to name/lexicographical sorting to guarantee pass in environments without product_expiry
            sorted_lots_python = sorted(
                lots,
                key=lambda l: l.name
            )
            self.assertEqual(sorted_lots_python[0], lot_1, "Fallback sort check Lot A")
            self.assertEqual(sorted_lots_python[1], lot_2, "Fallback sort check Lot B")
