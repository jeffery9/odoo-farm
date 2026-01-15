from odoo import fields, models, api, _
from odoo.exceptions import UserError

class FarmSubstituteWizard(models.TransientModel):
    _name = 'farm.substitute.wizard'
    _description = 'Substitute Product Suggestion Wizard'

    mrp_production_id = fields.Many2one('mrp.production', string='Manufacturing Order', required=True)
    original_product_id = fields.Many2one('product.product', string='Original Product (Out of Stock)', required=True)
    original_quantity = fields.Float(string='Original Quantity Needed', required=True)

    substitute_line_ids = fields.One2many('farm.substitute.line', 'wizard_id', string='Suggested Substitutes')

    def action_confirm_substitute(self):
        self.ensure_one()
        selected_substitute = self.substitute_line_ids.filtered(lambda l: l.is_selected)
        if not selected_substitute:
            raise UserError(_("Please select a substitute product."))
        if len(selected_substitute) > 1:
            raise UserError(_("You can only select one substitute product at a time."))
        
        selected_substitute = selected_substitute[0]

        # Find the original raw material move
        original_move = self.env['stock.move'].search([
            ('raw_material_production_id', '=', self.mrp_production_id.id),
            ('product_id', '=', self.original_product_id.id),
            ('state', 'in', ['draft', 'waiting', 'confirmed', 'assigned']),
        ], limit=1)

        if not original_move:
            raise UserError(_("Could not find the original raw material move for product '%s'.") % self.original_product_id.name)

        # Update the original move to use the substitute product and calculated quantity
        original_move.write({
            'product_id': selected_substitute.substitute_product_id.id,
            'product_uom_qty': selected_substitute.suggested_quantity,
        })
        
        self.mrp_production_id.message_post(body=_("Raw material '%s' substituted with '%s' (Quantity: %s).") % (
            self.original_product_id.name, selected_substitute.substitute_product_id.name, selected_substitute.suggested_quantity
        ))
        
        return {'type': 'ir.actions.act_window_close'}


class FarmSubstituteLine(models.TransientModel):
    _name = 'farm.substitute.line'
    _description = 'Substitute Product Suggestion Line'

    wizard_id = fields.Many2one('farm.substitute.wizard', string='Substitute Wizard', required=True, ondelete='cascade')
    substitute_product_id = fields.Many2one('product.product', string='Substitute Product', required=True)
    suggested_quantity = fields.Float(string='Suggested Quantity', required=True)
    is_selected = fields.Boolean(string='Select', default=False)

    # 显示养分含量，帮助用户决策
    n_content = fields.Float("Nitrogen (N) Content (%)", related='substitute_product_id.n_content', readonly=True)
    p_content = fields.Float("Phosphorus (P) Content (%)", related='substitute_product_id.p_content', readonly=True)
    k_content = fields.Float("Potassium (K) Content (%)", related='substitute_product_id.k_content', readonly=True)
