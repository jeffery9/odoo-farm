# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestCircularEconomy(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Flow = cls.env['agri.sustainability.circular.flow']
        cls.ProductRaw = cls.env['product.product'].create({'name': 'Wheat Straw'})
        cls.ProductOut = cls.env['product.product'].create({'name': 'Organic Fertilizer'})
        
    def test_01_flow_creation(self):
        """ Test basic circular flow record creation """
        flow = self.Flow.create({
            'name': 'Straw to Fertilizer',
            'code': 'FLOW-001',
            'flow_type': 'composting',
            'input_product_id': self.ProductRaw.id,
            'output_product_id': self.ProductOut.id,
            'input_quantity': 1000.0,
            'output_quantity': 500.0,
        })
        self.assertTrue(flow.exists())
        
    def test_02_net_benefit_calculation(self):
        """ Test net benefit computation """
        flow = self.Flow.create({
            'name': 'Straw to Fertilizer Benefit',
            'code': 'FLOW-002',
            'flow_type': 'composting',
            'input_product_id': self.ProductRaw.id,
            'output_product_id': self.ProductOut.id,
            'input_quantity': 100.0,
            'output_quantity': 50.0,
            'processing_cost': 200.0,
            'revenue': 500.0,
        })
        self.assertEqual(flow.net_benefit, 300.0)
        
    def test_03_duration_calculation(self):
        """ Test duration computation """
        from datetime import date, timedelta
        start = date.today()
        end = start + timedelta(days=30)
        flow = self.Flow.create({
            'name': 'Straw to Fertilizer Duration',
            'code': 'FLOW-003',
            'input_product_id': self.ProductRaw.id,
            'output_product_id': self.ProductOut.id,
            'input_quantity': 100.0,
            'output_quantity': 50.0,
            'start_date': start,
            'end_date': end,
        })
        self.assertEqual(flow.duration_days, 30)
        
    def test_04_analysis_view_exists(self):
        """ Test if analysis view model exists """
        analysis_model = self.env['agri.sustainability.circular.flow.analysis']
        self.assertTrue(analysis_model)
