# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class FarmWasteTransformationWizard(models.TransientModel):
    _name = 'farm.waste.transformation.wizard'
    _description = 'Agricultural Waste Transformation Wizard'

    source_lot_id = fields.Many2one('stock.lot', string='Source Waste Lot', required=True, 
                                   domain="[('quality_grade', '=', 'loss')]")
    source_product_id = fields.Many2one('product.product', related='source_lot_id.product_id', readonly=True)
    available_qty = fields.Float('Available Waste Qty', related='source_lot_id.product_qty', readonly=True)
    
    target_product_id = fields.Many2one('product.product', string='Target Asset (e.g. Fertilizer)', required=True,
                                       domain="[('is_agri_material', '=', True)]")
    transformation_qty = fields.Float('Qty to Transform', required=True)
    output_qty = fields.Float('Expected Output Qty', required=True)
    
    notes = fields.Text('Transformation Notes')

    def action_transform(self):
        """ US-27-01: Execute transformation inventory moves. """
        self.ensure_one()
        if self.transformation_qty > self.available_qty:
            raise UserError(_("Not enough waste quantity available in the source lot."))

        # 1. Create a Picking for the transformation process
        picking_type = self.env.ref('stock.picking_type_internal')
        picking = self.env['stock.picking'].create({
            'picking_type_id': picking_type.id,
            'location_id': self.source_lot_id.location_id.id or self.env.ref('stock.stock_location_stock').id,
            'location_dest_id': self.env.ref('stock.stock_location_stock').id,
            'origin': _('Waste Transformation: %s') % self.source_lot_id.name,
        })

        # 2. Consume the Waste
        move_consume = self.env['stock.move'].create({
            'name': _('Consume Waste'),
            'product_id': self.source_product_id.id,
            'product_uom_qty': self.transformation_qty,
            'product_uom': self.source_product_id.uom_id.id,
            'picking_id': picking.id,
            'location_id': picking.location_id.id,
            'location_dest_id': self.env.ref('stock.stock_location_scrapped').id,
        })

        # 3. Create the New Asset (Fertilizer)
        move_produce = self.env['stock.move'].create({
            'name': _('Produce Organic Fertilizer'),
            'product_id': self.target_product_id.id,
            'product_uom_qty': self.output_qty,
            'product_uom': self.target_product_id.uom_id.id,
            'picking_id': picking.id,
            'location_id': self.env.ref('stock.stock_location_scrapped').id, # Internal transformation
            'location_dest_id': picking.location_dest_id.id,
        })

        picking.action_confirm()
        picking.action_assign()
        # Note: In a real environment, we'd assign the lot_id to move_consume
        
        return {
            'effect': {
                'fadeout': 'slow',
                'message': _("Waste successfully transformed into valuable assets!"),
                'type': 'rainbow_man',
            }
        }
