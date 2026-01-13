from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from datetime import date, timedelta

class TestNutrientLeadtime(TransactionCase):

    def setUp(self):
        super(TestNutrientLeadtime, self).setUp()
        self.Product = self.env['product.product']
        self.Intervention = self.env['mrp.production']
        self.SaleOrder = self.env['sale.order']
        
        # 1. Create Fertilizer
        self.fertilizer = self.Product.create({
            'name': 'Urea',
            'agricultural_type': 'input',
            'n_content': 46.0,
            'standard_price': 2.0,
            'type': 'product'
        })
        
        # 2. Create Crop with growth duration
        self.crop = self.Product.create({
            'name': 'Wheat',
            'agricultural_type': 'output',
            'growth_duration': 120,
            'type': 'product'
        })

    def test_01_nutrient_calculation(self):
        """ Test that pure N/P/K is correctly calculated in interventions [US-02-03] """
        # Create an intervention (MO)
        mo = self.Intervention.create({
            'product_id': self.crop.id,
            'product_qty': 1.0,
            'bom_id': False, # Manual components
            'intervention_type': 'fertilizing',
            'move_raw_ids': [(0, 0, {
                'product_id': self.fertilizer.id,
                'product_uom_qty': 100.0,
                'product_uom': self.fertilizer.uom_id.id,
                'location_id': self.env.ref('stock.stock_location_stock').id,
                'location_dest_id': self.env.ref('stock.stock_location_stock').id, # Placeholder
            })]
        })
        
        # Check calculation: 100kg * 46% = 46kg pure N
        self.assertEqual(mo.pure_n_qty, 46.0)
        self.assertEqual(mo.pure_p_qty, 0.0)
        
        # Mark as done to trigger accumulation
        mo.button_mark_done()
        
        # 3. Check Land Parcel accumulation [US-02-03]
        parcel = self.env['stock.location'].create({
            'name': 'Parcel A',
            'is_land_parcel': True,
            'land_area': 10.0
        })
        # Link intervention to parcel via task
        task = self.env['project.task'].create({
            'name': 'Fertilizing Task',
            'project_id': self.env['project.project'].search([], limit=1).id,
            'land_parcel_id': parcel.id
        })
        mo.agri_task_id = task.id
        
        # Verify compute
        parcel._compute_nutrient_balance()
        self.assertEqual(parcel.total_n_input, 46.0)

    def test_02_leadtime_warning(self):
        """ Test that Sale Order raises error if lead-time is insufficient [US-09-01] """
        partner = self.env['res.partner'].create({'name': 'Test Customer'})
        
        # Create Sale Order with a delivery date only 30 days away (needs 120 days)
        so = self.SaleOrder.create({
            'partner_id': partner.id,
            'commitment_date': date.today() + timedelta(days=30),
            'order_line': [(0, 0, {
                'product_id': self.crop.id,
                'product_uom_qty': 10.0,
            })]
        })
        
        with self.assertRaises(UserError):
            so.action_confirm()
