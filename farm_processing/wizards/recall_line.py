from odoo import fields, models, api, _

class FarmRecallLine(models.TransientModel):
    _name = 'farm.recall.line'
    _description = 'Recall Simulation Line'
    _order = 'level, sequence'

    wizard_id = fields.Many2one('farm.recall.wizard', string='Recall Wizard', ondelete='cascade')
    sequence = fields.Integer(string='Sequence', default=10)
    level = fields.Integer(string='Level', default=0, help="Indicates the depth of the trace")
    product_id = fields.Many2one('product.product', string='Product')
    lot_id = fields.Many2one('stock.lot', string='Lot/Serial Number')
    quantity = fields.Float(string='Quantity')
    uom_id = fields.Many2one('uom.uom', string='Unit of Measure')
    
    move_type = fields.Selection([
        ('input', 'Input (Consumed)'),
        ('output', 'Output (Produced/Sold)'),
        ('transfer', 'Internal Transfer')
    ], string='Movement Type')
    
    reference = fields.Char(string='Reference', help="Related document (MO, PO, SO, Picking)")
    partner_id = fields.Many2one('res.partner', string='Partner (Customer/Vendor)')
    date = fields.Datetime(string='Date')

    # For displaying indented structure
    display_name_indented = fields.Char(compute='_compute_display_name_indented', string='Trace Item')

    @api.depends('level', 'product_id', 'lot_id', 'move_type', 'reference', 'partner_id')
    def _compute_display_name_indented(self):
        for rec in self:
            indent = "  " * rec.level
            name_parts = [indent]
            if rec.move_type == 'input':
                name_parts.append("<- Input:")
            elif rec.move_type == 'output':
                name_parts.append("-> Output:")
            elif rec.move_type == 'transfer':
                name_parts.append("<> Transfer:")
            
            if rec.product_id:
                name_parts.append(f"Product: {rec.product_id.display_name}")
            if rec.lot_id:
                name_parts.append(f"Lot: {rec.lot_id.name}")
            if rec.quantity:
                name_parts.append(f"Qty: {rec.quantity} {rec.uom_id.name if rec.uom_id else ''}")
            if rec.reference:
                name_parts.append(f"Ref: {rec.reference}")
            if rec.partner_id:
                name_parts.append(f"Partner: {rec.partner_id.display_name}")
            if rec.date:
                name_parts.append(f"Date: {rec.date.strftime('%Y-%m-%d')}")
            
            rec.display_name_indented = " ".join(name_parts)
