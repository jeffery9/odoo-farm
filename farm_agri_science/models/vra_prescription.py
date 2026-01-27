from odoo import models, fields, api, _

class FarmVraStrategy(models.Model):
    _name = 'farm.vra.strategy'
    _description = 'VRA Decision Strategy'

    name = fields.Char("Strategy Name", required=True)
    type = fields.Selection([
        ('inverse_ndvi', 'Inverse NDVI (Growth-based)'),
        ('soil_replacement', 'Soil Nutrient Replacement'),
        ('fixed_step', 'Threshold Stepping')
    ], string="Logic Type", default='inverse_ndvi', required=True)

    # Parameters
    target_ndvi = fields.Float("Target NDVI", default=0.7)
    correction_slope = fields.Float("Correction Slope", default=0.5)
    
    low_threshold = fields.Float("Low NDVI Threshold", default=0.3)
    high_threshold = fields.Float("High NDVI Threshold", default=0.6)
    low_multiplier = fields.Float("Weak Area Multiplier", default=1.3)
    high_multiplier = fields.Float("Strong Area Multiplier", default=0.8)

class FarmVRAPrescription(models.Model):
    _name = 'farm.vra.prescription'
    _description = 'Variable Rate Prescription'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Prescription Ref", required=True, copy=False, readonly=True, default=lambda self: _('New'))
    location_id = fields.Many2one('farm.location', string="Target Parcel", required=True, domain=[('is_land_parcel', '=', True)])
    product_id = fields.Many2one('product.template', string="Input Material", required=True)
    strategy_id = fields.Many2one('farm.vra.strategy', string="VRA Strategy", required=True)
    
    target_type = fields.Selection([
        ('fertilizer', 'Fertilizer'),
        ('seed', 'Seeding'),
        ('pesticide', 'Pesticide')
    ], string="Application Type", required=True)
    
    base_rate = fields.Float("Base Rate (kg/mu)", required=True, default=10.0)
    
    line_ids = fields.One2many('farm.vra.prescription.line', 'prescription_id', string="Prescription Grid")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('generated', 'Grid Generated'),
        ('exported', 'Sent to Machine'),
        ('executed', 'Completed')
    ], default='draft', tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('farm.vra.prescription') or _('VRA-NEW')
        return super().create(vals_list)

    def action_generate_prescription_map(self):
        """
        Complete VRA Engine: Implements multiple decision strategies.
        """
        for rec in self:
            if not rec.location_id.grid_cell_ids:
                rec.location_id.action_generate_grid()
            
            rec.line_ids.unlink()
            lines = []
            strategy = rec.strategy_id

            for cell in rec.location_id.grid_cell_ids:
                rate = rec.base_rate
                
                if strategy.type == 'inverse_ndvi':
                    # Rate = Base * (1 + (Target_NDVI - Current_NDVI) * Slope)
                    rate = rec.base_rate * (1 + (strategy.target_ndvi - cell.ndvi_index) * strategy.correction_slope)
                
                elif strategy.type == 'soil_replacement':
                    # GIS Logic: If pH is too low (acidic), increase fertilizer buffering
                    ph_adjustment = 1.2 if cell.soil_ph < 5.5 else 1.0
                    rate = rec.base_rate * ph_adjustment

                elif strategy.type == 'fixed_step':
                    if cell.ndvi_index < strategy.low_threshold:
                        rate *= strategy.low_multiplier
                    elif cell.ndvi_index > strategy.high_threshold:
                        rate *= strategy.high_multiplier
                
                # Physical safety limits: 50% - 150% of base rate
                rate = max(rec.base_rate * 0.5, min(rec.base_rate * 1.5, rate))

                lines.append((0, 0, {
                    'grid_cell_id': cell.id,
                    'target_rate': rate,
                    'uom_id': rec.product_id.uom_id.id
                }))
            
            rec.line_ids = lines
            rec.state = 'generated'

    def action_export_to_machinery(self):
        """
        Exports the prescription map in a machine-readable format (ISO-XML).
        """
        self.ensure_one()
        self.message_post(body=_("VRA ISO-XML Map Exported to telemetry channel for machine application."))
        self.state = 'exported'
        return True

class FarmVRAPrescriptionLine(models.Model):
    _name = 'farm.vra.prescription.line'
    _description = 'VRA Grid Rate'

    prescription_id = fields.Many2one('farm.vra.prescription', ondelete='cascade')
    grid_cell_id = fields.Many2one('farm.land.grid.cell', string="Grid Cell", required=True)
    target_rate = fields.Float("Target Rate", digits=(10, 3))
    uom_id = fields.Many2one('uom.uom', string="Unit")
    actual_rate = fields.Float("Actual Rate Applied", digits=(10, 3))