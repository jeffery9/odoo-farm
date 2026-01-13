from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError

class TestProcessingLogic(TransactionCase):

    def setUp(self):
        super(TestProcessingLogic, self).setUp()
        self.Production = self.env['mrp.production']
        self.Product = self.env['product.product']
        self.Bom = self.env['mrp.bom']
        
        # Create products
        self.raw_material = self.Product.create({'name': 'Raw Apple', 'type': 'product'})
        self.finished_good = self.Product.create({'name': 'Apple Juice', 'type': 'product'})
        
        # Create BOM
        self.bom = self.Bom.create({
            'product_id': self.finished_good.id,
            'product_tmpl_id': self.finished_good.product_tmpl_id.id,
            'product_qty': 1.0,
            'type': 'normal',
            'bom_line_ids': [(0, 0, {'product_id': self.raw_material.id, 'product_qty': 1.2})]
        })

    def test_mass_balance_validation(self):
        """ Test that MO cannot be done if mass balance is off [US-04-02] """
        mo = self.Production.create({
            'product_id': self.finished_good.id,
            'bom_id': self.bom.id,
            'product_qty': 100.0,
            'scrap_qty': 5.0, # 100 finished + 5 scrap = 105 total output
        })
        mo.action_confirm()
        
        # Total raw needed: 120 (100 * 1.2)
        # Output: 105 (100 + 5)
        # Balanced: False (105 != 120)
        
        with self.assertRaises(UserError):
            mo.button_mark_done()

    def test_traceability_linkage(self):
        """ Test that finished lot links to raw lot and calculates full path [US-14-03] """
        # 1. Create a root lot (Harvest)
        root_lot = self.env['stock.lot'].create({
            'name': 'ROOT-LOT',
            'product_id': self.raw_material.id,
            'company_id': self.env.company.id,
        })
        
        # 2. Create MO to process root lot into finished good
        mo = self.Production.create({
            'product_id': self.finished_good.id,
            'bom_id': self.bom.id,
            'product_qty': 1.0,
            'harvest_lot_ids': [(4, root_lot.id)]
        })
        mo.action_confirm()
        
        # Create output lot
        finished_lot = self.env['stock.lot'].create({
            'name': 'JUICE-LOT',
            'product_id': self.finished_good.id,
            'company_id': self.env.company.id,
        })
        
        # Simulate finishing
        mo.lot_producing_id = finished_lot.id
        mo.button_mark_done()
        
        # 3. Verify linkage
        self.assertEqual(finished_lot.parent_lot_id.id, root_lot.id)
        # Verify pre-calculated path
        self.assertEqual(finished_lot.full_traceability_path, str(root_lot.id))
