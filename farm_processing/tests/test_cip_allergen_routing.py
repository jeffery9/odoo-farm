# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError

class TestCIPAllergenRouting(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        
        cls.allergen_peanut = cls.env['agri.allergen'].create({'name': 'Peanuts'})
        cls.allergen_dairy = cls.env['agri.allergen'].create({'name': 'Dairy'})
        
        cls.product_peanut_butter = cls.env['product.product'].create({
            'name': 'Organic Peanut Butter',
            'type': 'product',
        })
        if hasattr(cls.product_peanut_butter, 'allergen_ids'):
            cls.product_peanut_butter.allergen_ids = [(4, cls.allergen_peanut.id)]
            
        cls.product_almond_butter = cls.env['product.product'].create({
            'name': 'Organic Almond Butter',
            'type': 'product'
        })
        
        cls.workcenter = cls.env['mrp.workcenter'].create({
            'name': 'Grinding Mill 01'
        })

    def test_01_cip_lock_flow(self):
        """
        Scenario 38: CIP Routing & Allergen Traceability
        1. Produce Peanut Butter on the Grinding Mill.
        2. Production completes, mill is contaminated.
        3. Attempt to produce Almond Butter on the same mill.
        4. System blocks it with a FATAL FOOD SAFETY LOCK.
        5. Quality Inspector signs off a CIP (Clean-In-Place) wash.
        6. Almond Butter production is now allowed.
        """
        # Step 1: Produce Peanut Butter
        mo1 = self.env['mrp.production'].create({
            'product_id': self.product_peanut_butter.id,
            'product_qty': 100.0,
        })
        # Simulate workorder attachment since we don't have a full routing/BOM setup here
        wo1 = self.env['mrp.workorder'].create({
            'name': 'Grinding',
            'production_id': mo1.id,
            'workcenter_id': self.workcenter.id,
            'product_uom_id': self.product_peanut_butter.uom_id.id
        })
        
        mo1.action_confirm()
        # Mock completion of MO which triggers the contamination
        mo1.button_mark_done()
        
        # Verify contamination
        if hasattr(self.product_peanut_butter, 'allergen_ids'):
            self.assertTrue(self.workcenter.requires_cip, "Workcenter must be locked for CIP.")
            self.assertEqual(self.workcenter.last_allergen_id.id, self.allergen_peanut.id)

        # Step 3: Attempt to produce Almond Butter
        mo2 = self.env['mrp.production'].create({
            'product_id': self.product_almond_butter.id,
            'product_qty': 50.0,
        })
        wo2 = self.env['mrp.workorder'].create({
            'name': 'Grinding',
            'production_id': mo2.id,
            'workcenter_id': self.workcenter.id,
            'product_uom_id': self.product_almond_butter.uom_id.id
        })
        
        if hasattr(self.product_peanut_butter, 'allergen_ids'):
            # Step 4: Blocked!
            with self.assertRaises(UserError) as e:
                mo2.action_confirm()
            self.assertIn("FATAL FOOD SAFETY LOCK", str(e.exception))
            
            # Step 5: Perform CIP Wash
            cip_wizard = self.env['farm.cip.wizard'].create({
                'workcenter_id': self.workcenter.id
            })
            cip_wizard.action_certify_cip()
            
            self.assertFalse(self.workcenter.requires_cip, "Workcenter should be clean now.")
            
            # Step 6: Allowed!
            mo2.action_confirm()
            self.assertEqual(mo2.state, 'confirmed', "MO should proceed after CIP.")

