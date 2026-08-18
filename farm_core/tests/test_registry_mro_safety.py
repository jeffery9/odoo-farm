# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestRegistryMroSafety(TransactionCase):

    def test_registry_mro_inheritance_limit(self):
        """ Ensure custom Odoo models do not exceed an inheritance depth threshold of 5 levels in production """
        # We test on our highly vulnerable core tracking model
        model = self.env['stock.matter.tracking']
        mro_chain = type(model).__mro__
        custom_extensions = [cls.__name__ for cls in mro_chain if 'farm_' in cls.__module__]
        self.assertLessEqual(len(custom_extensions), 5, f"Registry MRO depth is {len(custom_extensions)}, exceeding the maximum safe limit of 5 levels!")
