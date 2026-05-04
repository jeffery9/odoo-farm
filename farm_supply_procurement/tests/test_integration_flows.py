# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from datetime import date, timedelta

class TestFarmSupplyProcurement(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Product = cls.env['product.product']
        cls.SaleOrder = cls.env['sale.order']
        cls.Partner = cls.env['res.partner'].create({'name': 'Test Supplier / Customer'})

        cls.seed = cls.Product.create({
            'name': 'Tomato Seeds v2',
            'type': 'consu',
            'is_agri_input': True,
            'input_type': 'seed',
            'growth_cycle_days': 90,
        })
        
        cls.pesticide = cls.Product.create({
            'name': 'Organic Pest Control',
            'type': 'consu',
            'is_agri_input': True,
            'input_type': 'pesticide',
            'withdrawal_period_days': 15,
            'is_safety_approved': True
        })

    def test_01_agri_input_attributes(self):
        """ Test basic agricultural input properties """
        self.assertTrue(self.seed.is_agri_input)
        self.assertEqual(self.seed.input_type, 'seed')
        self.assertEqual(self.seed.growth_cycle_days, 90)
        
        self.assertTrue(self.pesticide.is_agri_input)
        self.assertEqual(self.pesticide.withdrawal_period_days, 15)
        self.assertTrue(self.pesticide.is_safety_approved)

    def test_02_growth_cycle_warning_on_sale(self):
        """ Test that growth cycle logic does not crash sale order confirmation """
        # Sale orders for seeds that take 90 days
        order = self.SaleOrder.create({
            'partner_id': self.Partner.id,
            'order_line': [(0, 0, {
                'product_id': self.seed.id,
                'product_uom_qty': 10,
                'price_unit': 5.0,
            })]
        })
        # Try to confirm. The logic in farm_input.py intercepts this
        order.action_confirm()
        self.assertEqual(order.state, 'sale')

class TestIntegrationFarmSupplyProcurement(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.PurchaseOrder = cls.env['purchase.order']
        cls.Partner = cls.env['res.partner'].create({'name': 'Agri Supplier Inc'})
        cls.Product = cls.env['product.product'].create({
            'name': 'Bulk Fertilizer',
            'type': 'consu',
            'is_agri_input': True,
            'input_type': 'fertilizer',
            'n_content': 20.0,
            'p_content': 10.0,
            'k_content': 10.0,
        })

    def test_01_purchase_agri_input(self):
        """ Test PO integration with agri inputs """
        po = self.PurchaseOrder.create({
            'partner_id': self.Partner.id,
            'order_line': [(0, 0, {
                'product_id': self.Product.id,
                'product_qty': 1000.0,
                'price_unit': 1.2,
            })]
        })
        po.button_confirm()
        self.assertEqual(po.state, 'purchase')
