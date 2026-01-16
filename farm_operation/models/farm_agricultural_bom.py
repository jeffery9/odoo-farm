from odoo import models, fields


class FarmAgriculturalBom(models.Model):
    """
    Concrete ISL model for Agricultural BOMs using _inherits.
    This model inherits from the base mrp.bom model and includes the shared logic from the mixin.
    """
    _name = 'farm.agricultural.bom'
    _description = 'Agricultural BOM (ISL Layer)'
    _inherits = {'mrp.bom': 'bom_id'}  # Inherit from base Odoo model
    _inherit = ['farm.agricultural.bom.mixin']  # Include shared logic

    # Link to the base model (this field is required for _inherits)
    bom_id = fields.Many2one(
        'mrp.bom',
        string="Base BOM",
        required=True,
        ondelete="cascade"
    )

    # Additional agricultural-specific fields can be added here
    # The mixin provides the core agricultural BOM functionality


class FarmAgricultulturalBomLine(models.Model):
    """
    Concrete ISL model for Agricultural BOM Lines using _inherits.
    """
    _name = 'farm.agricultural.bom.line'
    _description = 'Agricultural BOM Line (ISL Layer)'
    _inherits = {'mrp.bom.line': 'bom_line_id'}  # Inherit from base Odoo model
    _inherit = ['farm.agricultural.bom.line.mixin']  # Include shared logic

    # Link to the base model (this field is required for _inherits)
    bom_line_id = fields.Many2one(
        'mrp.bom.line',
        string="Base BOM Line",
        required=True,
        ondelete="cascade"
    )