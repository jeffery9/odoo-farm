# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestFefoLogistics(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.local_partner = cls.env['res.partner'].create({'name': 'FastMarket'})
        cls.export_partner = cls.env['res.partner'].create({'name': 'OverseasMarket'})

        cls.picking_type = cls.env['stock.picking.type'].search([], limit=1)
        cls.location = cls.env['stock.location'].search([('usage', '=', 'internal')], limit=1)
        cls.dest_location = cls.env['stock.location'].search([('usage', '=', 'customer')], limit=1)

    def test_01_dynamic_fefo_routing(self):
        """ Scenario 40: Dynamic FEFO Smart Logistics """
        pick_fast = self.env['stock.picking'].create({
            'partner_id': self.local_partner.id,
            'picking_type_id': self.picking_type.id,
            'location_id': self.location.id,
            'location_dest_id': self.dest_location.id,
        })
        
        pick_hardy = self.env['stock.picking'].create({
            'partner_id': self.export_partner.id,
            'picking_type_id': self.picking_type.id,
            'location_id': self.location.id,
            'location_dest_id': self.dest_location.id,
        })
        
        pick_fast._compute_ripeness()
        pick_hardy._compute_ripeness()
        
        pick_fast.action_fefo_routing()
        pick_hardy.action_fefo_routing()
        
        self.assertEqual(pick_fast.routing_strategy, 'local', "Ripe produce must stay local.")
        self.assertEqual(pick_hardy.routing_strategy, 'export', "Hardy produce cleared for export.")

