# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

class TestLivestockMatterBridge(TransactionCase):

    def setUp(self):
        super(TestLivestockMatterBridge, self).setUp()
        self.livestock_asset = self.env['farm.livestock.asset'].create({
            'ear_tag_code': 'Sow #A102 (母猪 #A012)',
            'species': 'duroc'
        })
        self.tracking = self.env['stock.matter.tracking'].create({
            'name': 'EAR-TAG-GATE (物理耳标网口载体)'
        })

    def test_bridge_livestock_binding(self):
        """ Verify livestock asset can be late-bound to a physical tracking node """
        self.tracking.write({'livestock_asset_id': self.livestock_asset.id})
        self.assertEqual(self.tracking.livestock_asset_id.id, self.livestock_asset.id)

    def test_graceful_degradation_on_delete_livestock(self):
        """ Verify ondelete set null safety prevents cascading deletions on livestock """
        self.tracking.write({'livestock_asset_id': self.livestock_asset.id})
        self.livestock_asset.unlink()
        self.assertFalse(self.tracking.livestock_asset_id)
        self.assertTrue(self.tracking.exists(), "Physical carrier must survive livestock deletion")
