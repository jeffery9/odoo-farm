from odoo import models, fields, api
from odoo.exceptions import ValidationError


class FieldCropOperation(models.Model):
    """
    Field Crop Operation model to manage specific operations for field crop farming
    """
    _name = 'farm.field.crop.operation'
    _description = 'Field Crop Operation'
    _inherits = {'project.task': 'operation_id'}
    _inherit = ['mail.thread', 'mail.activity.mixin']

    operation_id = fields.Many2one(
        'project.task',
        required=True,
        ondelete='cascade',
        string='Operation Task'
    )

    # Field crops specific fields
    seeding_rate = fields.Float(
        string='Seeding Rate',
        help='Amount of seeds planted per unit area (e.g., kg/ha or lbs/acre)'
    )
    fertilizer_application_rate = fields.Float(
        string='Fertilizer Application Rate',
        help='Amount of fertilizer applied per unit area'
    )
    irrigation_schedule = fields.Char(
        string='Irrigation Schedule',
        help='Schedule for irrigation activities'
    )
    crop_rotation_sequence = fields.Integer(
        string='Crop Rotation Sequence',
        help='Position in the crop rotation sequence'
    )
    planting_density = fields.Float(
        string='Planting Density',
        help='Number of plants per unit area'
    )

    # Linked to specific crops and fields
    crop_type_id = fields.Many2one(
        'product.template',
        domain=[('is_agricultural_product', '=', True)],
        string='Crop Type',
        help='Type of crop being cultivated'
    )
    field_parcel_id = fields.Many2one(
        'stock.location',
        domain=[('is_land_parcel', '=', True)],
        string='Field Parcel',
        help='Specific field parcel for this operation'
    )
    expected_yield = fields.Float(
        string='Expected Yield',
        help='Expected yield per unit area'
    )

    @api.model
    def create(self, vals):
        # Set default values based on crop type if available
        if vals.get('crop_type_id'):
            crop = self.env['product.template'].browse(vals['crop_type_id'])
            if crop.default_seeding_rate:
                vals.setdefault('seeding_rate', crop.default_seeding_rate)
            if crop.default_planting_density:
                vals.setdefault('planting_density', crop.default_planting_density)

        return super().create(vals)

    def action_view_field_details(self):
        """Action to view detailed field information"""
        self.ensure_one()
        if self.field_parcel_id:
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'stock.location',
                'res_id': self.field_parcel_id.id,
                'view_mode': 'form',
                'target': 'current',
            }
        return {'type': 'ir.actions.act_window.close'}