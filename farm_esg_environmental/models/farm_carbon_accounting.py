from odoo import models, fields, api, _

class FarmCarbonFactor(models.Model):
    _name = 'farm.carbon.factor'
    _description = 'Agricultural Carbon Emission Factors'

    name = fields.Char("Factor Name", required=True)
    product_id = fields.Many2one('product.template', string="Related Product", help="Product like Diesel, Urea, etc.")
    category = fields.Selection([
        ('input', 'Agricultural Inputs (Fertilizer/Pesticide)'),
        ('energy', 'Energy (Diesel/Electricity)'),
        ('land', 'Land Use (Soil/Sequestration)'),
        ('waste', 'Waste/Residue')
    ], string="Category", required=True)
    
    emission_factor = fields.Float("Emission Factor (kg CO2e / unit)", digits=(12, 4), required=True)
    uom_id = fields.Many2one('uom.uom', string="Unit", required=True)
    
    source = fields.Char("Data Source", help="e.g., IPCC, FAO, Local Research")

class FarmCarbonLedger(models.Model):
    _name = 'farm.carbon.ledger'
    _description = 'Agricultural Carbon Transaction Ledger'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Transaction Ref", required=True, readonly=True, default=lambda self: _('New'))
    date = fields.Date("Transaction Date", default=fields.Date.today)
    
    # Links
    location_id = fields.Many2one('farm.location', string="Farm Location")
    lot_id = fields.Many2one('stock.lot', string="Production Lot")
    operation_id = fields.Many2one('mrp.workorder', string="Source Operation") # Link to actual task
    
    # Values
    factor_id = fields.Many2one('farm.carbon.factor', string="Carbon Factor", required=True)
    quantity = fields.Float("Quantity Used")
    uom_id = fields.Many2one('uom.uom', string="Unit")
    
    total_co2e = fields.Float("Total CO2e (kg)", compute='_compute_total_co2e', store=True)
    
    impact_type = fields.Selection([
        ('emission', 'Emission (+)'),
        ('sequestration', 'Sequestration (-)')
    ], string="Impact Type", default='emission')

    @api.depends('quantity', 'factor_id')
    def _compute_total_co2e(self):
        for rec in self:
            val = rec.quantity * rec.factor_id.emission_factor
            rec.total_co2e = val if rec.impact_type == 'emission' else -val

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('farm.carbon.ledger') or _('CO2-NEW')
        return super().create(vals_list)

class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    def button_finish(self):
        """
        Extending Odoo MRP Workorder to trigger carbon accounting on completion.
        """
        res = super(MrpWorkorder, self).button_finish()
        self._action_calculate_carbon_footprint()
        return res

    def _action_calculate_carbon_footprint(self):
        """
        LCA Logic: Iterate through consumed inputs and fuel to record carbon entries.
        """
        Ledger = self.env['farm.carbon.ledger']
        Factor = self.env['farm.carbon.factor']
        
        for wo in self:
            # 1. Input-based Emissions (Fertilizers/Pesticides)
            # Find raw material moves associated with this workorder/production
            moves = wo.production_id.move_raw_ids.filtered(lambda m: m.state == 'done')
            for move in moves:
                factor = Factor.search([('product_id', '=', move.product_id.product_tmpl_id.id)], limit=1)
                if factor:
                    Ledger.create({
                        'operation_id': wo.id,
                        'location_id': wo.production_id.location_src_id.id,
                        'lot_id': wo.production_id.lot_producing_id.id,
                        'factor_id': factor.id,
                        'quantity': move.quantity_done,
                        'uom_id': move.product_uom.id,
                    })

            # 2. Machinery/Energy Emissions
            # If a tractor was used, calculate based on duration or fuel consumed
            # This requires integration with farm_equipment or fleet
            if wo.duration > 0:
                diesel_factor = Factor.search([('category', '=', 'energy'), ('name', 'ilike', 'Diesel')], limit=1)
                if diesel_factor:
                    # Mock calculation: 5 Liters per hour
                    fuel_qty = (wo.duration / 60.0) * 5.0
                    Ledger.create({
                        'operation_id': wo.id,
                        'factor_id': diesel_factor.id,
                        'quantity': fuel_qty,
                        'uom_id': diesel_factor.uom_id.id,
                        'description': _("Machinery energy consumption for %s") % wo.name
                    })

