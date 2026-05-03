# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class AgriCarbonFactor(models.Model):
    """
    Agri Domain Level: Carbon Emission Factors. [US-104-2026]
    Standard factors for inputs, energy, and sequestration across the domain.
    """
    _name = 'agri.carbon.factor'
    _description = 'Agricultural Carbon Emission Factors'

    name = fields.Char("Factor Name", required=True, translate=True)
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

class AgriCarbonLedger(models.Model):
    """
    Agri Domain Level: Carbon Ledger. [US-104-2026]
    The universal transaction record for carbon impact.
    Refactored from farm.carbon.ledger with 100% logic retention.
    """
    _name = 'agri.carbon.ledger'
    _description = 'Agricultural Carbon Transaction Ledger'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'agri.evidence.mixin']

    name = fields.Char("Transaction Ref", required=True, readonly=True, default=lambda self: _('New'))
    date = fields.Date("Transaction Date", default=fields.Date.today)
    
    # Links
    location_id = fields.Many2one('farm.location', string="Physical Container")
    lot_id = fields.Many2one('stock.lot', string="Production Lot")
    operation_id = fields.Many2one('mrp.workorder', string="Source Operation")
    
    # Values
    factor_id = fields.Many2one('agri.carbon.factor', string="Carbon Factor", required=True)
    quantity = fields.Float("Quantity Used")
    uom_id = fields.Many2one('uom.uom', string="Unit")
    
    total_co2e = fields.Float("Total CO2e (kg)", compute='_compute_total_co2e', store=True)
    
    impact_type = fields.Selection([
        ('emission', 'Emission (+)'),
        ('sequestration', 'Sequestration (-)')
    ], string="Impact Type", default='emission')

    # --- 100% Original Logic Retention (RESTORED) ---
    @api.depends('quantity', 'factor_id')
    def _compute_total_co2e(self):
        """Standard domain logic for CO2e calculation."""
        for rec in self:
            if rec.factor_id:
                val = rec.quantity * rec.factor_id.emission_factor
                rec.total_co2e = val if rec.impact_type == 'emission' else -val
            else:
                rec.total_co2e = 0.0

    @api.model_create_multi
    def create(self, vals_list):
        """Auto-sequence for carbon transactions."""
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('agri.carbon.ledger') or _('CO2-NEW')
        return super(AgriCarbonLedger, self).create(vals_list)
    # --- End of Original Logic ---

class MrpWorkorder(models.Model):
    _name = 'mrp.workorder'
    _inherit = 'mrp.workorder'

    def button_finish(self):
        """
        Extending Odoo MRP Workorder to trigger carbon accounting on completion.
        100% Original Life Cycle Assessment (LCA) Logic.
        """
        res = super(MrpWorkorder, self).button_finish()
        self._action_calculate_carbon_footprint()
        return res

    def _action_calculate_carbon_footprint(self):
        """
        Standard LCA Algorithm: Iterates through consumed inputs and fuel to record domain carbon entries.
        Refactored to target the agri.carbon.* namespace.
        """
        Ledger = self.env['agri.carbon.ledger']
        Factor = self.env['agri.carbon.factor']
        
        for wo in self:
            # 1. Input-based Emissions (Fertilizers/Pesticides)
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
            if wo.duration > 0:
                diesel_factor = Factor.search([('category', '=', 'energy'), ('name', 'ilike', 'Diesel')], limit=1)
                if diesel_factor:
                    # Original Mock calculation: 5 Liters per hour
                    fuel_qty = (wo.duration / 60.0) * 5.0
                    Ledger.create({
                        'operation_id': wo.id,
                        'factor_id': diesel_factor.id,
                        'quantity': fuel_qty,
                        'uom_id': diesel_factor.uom_id.id,
                    })