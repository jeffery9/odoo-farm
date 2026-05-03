# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError, UserError

class TestISLRedirection(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Ensure we have the base models
        cls.Redirector = cls.env['agri.isl.model.redirector']
        
    def test_get_isl_record_not_found(self):
        """Test looking up a record that doesn't exist returns None."""
        res = self.Redirector.get_isl_record('mrp.production', 999999)
        self.assertFalse(res)
        
    def test_auto_redirect_to_isl(self):
        """Test the auto redirect utility."""
        class MockRecord:
            _name = 'mrp.production'
            id = 999999
            
        mock = MockRecord()
        res = self.Redirector._auto_redirect_to_isl(mock)
        self.assertEqual(res, mock, "Should return base record if no ISL record found")
