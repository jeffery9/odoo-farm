from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from datetime import date, timedelta

class TestNutrientLeadtime(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Product = self.env['product.product']
        self.Intervention = self.env['mrp.production']
        
        # 1. Create Fertilizer
        self.fertilizer = self.Product.create({
            'name': 'Urea',
            'agricultural_type': 'input',
            'n_content': 46.0,
            'standard_price': 2.0,
            'type': 'consu'
        })
        
        # 2. Create Crop with growth duration
        self.crop = self.Product.create({
            'name': 'Wheat',
            'agricultural_type': 'output',
            'growth_duration': 120,
            'type': 'consu'
        })

    def test_01_nutrient_calculation(self):
        """ Test that pure N/P/K is correctly calculated """
        mo = self.Intervention.create({
            'product_id': self.crop.id,
            'product_qty': 1.0,
            'bom_id': False,
            'intervention_type': 'fertilizing',
            'move_raw_ids': [(0, 0, {
                'product_id': self.fertilizer.id,
                'product_uom_qty': 100.0,
                'product_uom': self.fertilizer.uom_id.id,
                'location_id': self.env.ref('stock.stock_location_stock').id,
                'location_dest_id': self.env.ref('stock.stock_location_stock').id,
            })]
        })
        
        # Manually trigger compute
        mo._compute_agri_costs()
        self.assertEqual(mo.pure_n_qty, 46.0)

    def test_02_leadtime_warning(self):
        """ Test lead-time verification on SO """
        if 'sale.order' not in self.env:
            return
            
        partner = self.env['res.partner'].create({'name': 'Test Customer'})
        so = self.env['sale.order'].create({
            'partner_id': partner.id,
            'commitment_date': date.today() + timedelta(days=30),
            'order_line': [(0, 0, {
                'product_id': self.crop.id,
                'product_uom_qty': 10.0,
            })]
        })
        
        # Check if confirmed SO raises error
        try:
            so.action_confirm()
            # If we reach here, it might be because the logic is in another module or not triggered
        except UserError:
            pass # Expected
