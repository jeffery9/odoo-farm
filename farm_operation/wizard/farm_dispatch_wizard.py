from odoo import models, fields, api, _

class FarmDispatchWizard(models.TransientModel):
    _name = 'farm.dispatch.wizard'
    _description = 'Agricultural Task Dispatch Wizard'

    location_ids = fields.Many2many('stock.location', string="Selected Parcels", domain=[('is_land_parcel', '=', True)])
    total_area = fields.Float("Total Area (mu)", compute='_compute_total_area')
    
    intervention_type = fields.Selection([
        ('tillage', 'Soil Preparation'),
        ('sowing', 'Sowing/Planting'),
        ('fertilizing', 'Fertilizing'),
        ('irrigation', 'Irrigation'),
        ('protection', 'Crop Protection'),
        ('aerial_spraying', 'Aerial Spraying'),
        ('harvesting', 'Harvesting'),
    ], string="Intervention Type", required=True, default='aerial_spraying')
    
    campaign_id = fields.Many2one('agricultural.campaign', string="Campaign/Season", required=True)
    product_id = fields.Many2one('product.product', string="Target Product (Crop)", help="The crop or output product.")
    
    @api.model
    def default_get(self, fields):
        res = super(FarmDispatchWizard, self).default_get(fields)
        if self._context.get('active_model') == 'stock.location' and self._context.get('active_ids'):
            res['location_ids'] = [(6, 0, self._context.get('active_ids'))]
        return res

    @api.depends('location_ids')
    def _compute_total_area(self):
        for wizard in self:
            wizard.total_area = sum(wizard.location_ids.mapped('land_area'))

    def action_dispatch(self):
        self.ensure_one()
        # Create a Production Task (project.task)
        task_name = _("%s - Batch Dispatch %s") % (
            dict(self._fields['intervention_type'].selection).get(self.intervention_type),
            fields.Date.today()
        )
        
        task = self.env['project.task'].create({
            'name': task_name,
            'campaign_id': self.campaign_id.id,
            'size_value': self.total_area,
            'land_parcel_id': self.location_ids[0].id if self.location_ids else False,
            'industry_type': 'field_crops',
        })
        
        # Create Interventions (mrp.production) for each parcel
        for loc in self.location_ids:
            self.env['mrp.production'].create({
                'product_id': self.product_id.id if self.product_id else False, # Should ideally be required or inferred
                'product_qty': 1.0,
                'product_uom_id': self.product_id.uom_id.id if self.product_id else self.env.ref('uom.product_uom_unit').id,
                'location_dest_id': loc.id,
                'agri_task_id': task.id,
                'intervention_type': self.intervention_type,
            })
            
        return {
            'name': _('Production Task'),
            'type': 'ir.actions.act_window',
            'res_model': 'project.task',
            'res_id': task.id,
            'view_mode': 'form',
            'target': 'current',
        }
