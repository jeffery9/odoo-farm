# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class FarmCropBom(models.Model):
    """
    Crop Farming Recipe (ISL Layer)
    Implements ISL standards using _inherits mechanism for proper ownership
    and industry specialization while maintaining base functionality.
    """
    _name = 'farm.crop.bom'
    _description = 'Crop Farming Recipe (ISL Layer)'
    _inherits = {'mrp.bom': 'bom_id'}
    _inherit = ['farm.agri.bom.mixin']

    bom_id = fields.Many2one('mrp.bom', string='Base BOM', required=True, ondelete='cascade')

    # Crop Specifics
    growing_season = fields.Selection([
        ('spring', 'Spring'),
        ('summer', 'Summer'),
        ('autumn', 'Autumn'),
        ('winter', 'Winter')
    ], string="Growing Season")

    phi_days = fields.Integer("Pre-Harvest Interval (PHI) Days", help="Safe days to wait after last treatment before harvest.")

    def write(self, vals):
        # Ensure industry type is set to crop agriculture
        if 'industry_type' not in vals and not self.industry_type:
            vals['industry_type'] = 'crop'
        return super().write(vals)

    @api.model_create_multi
    def create(self, vals_list):
        # Ensure industry type is set to crop agriculture
        for vals in vals_list:
            if 'industry_type' not in vals or not vals.get('industry_type'):
                vals['industry_type'] = 'crop'
        return super().create(vals_list)

class FarmCropProduction(models.Model):
    """
    Crop Farming Task (ISL Layer)
    Implements ISL standards using _inherits mechanism for proper ownership
    and industry specialization while maintaining base functionality.
    """
    _name = 'farm.crop.production'
    _description = 'Crop Farming Task (ISL Layer)'
    _inherits = {'mrp.production': 'production_id'}
    _inherit = ['farm.agri.production.mixin']

    production_id = fields.Many2one('mrp.production', string='Base MO', required=True, ondelete='cascade')

    # Crop Specific Fields
    area_to_treat = fields.Float("Operational Area (Ha)", digits='Product Unit of Measure')

    # --- Polymorphic Link (US-TECH-06-26) ---
    crop_bom_id = fields.Many2one('farm.crop.bom', string='Crop Recipe', compute='_compute_crop_bom_id')

    def _compute_crop_bom_id(self):
        for rec in self:
            if rec.bom_id:
                rec.crop_bom_id = self.env['farm.crop.bom'].search([('bom_id', '=', rec.bom_id.id)], limit=1)
            else:
                rec.crop_bom_id = False

    # Moved & Enhanced GIS Validation (US-GIS-01)
    @api.constrains('area_to_treat', 'production_id')
    def _check_spatial_limit(self):
        """ ISL-level spatial validation. """
        for rec in self:
            # Logic: Access the base production's linked location/task
            plot = rec.production_id.location_src_id # Simplified plot link
            if plot and plot.is_land_parcel and plot.calculated_area_ha > 0:
                if rec.area_to_treat > plot.calculated_area_ha * 1.05:
                    raise UserError(_("ISL SPATIAL BLOCK: Declared area exceeds physical plot boundary of %s.") % plot.name)

    def write(self, vals):
        # Ensure industry type is set to crop agriculture
        if 'industry_type' not in vals and not self.industry_type:
            vals['industry_type'] = 'crop'
        return super().write(vals)

    @api.model_create_multi
    def create(self, vals_list):
        # Ensure industry type is set to crop agriculture
        for vals in vals_list:
            if 'industry_type' not in vals or not vals.get('industry_type'):
                vals['industry_type'] = 'crop'
        return super().create(vals_list)

class FarmCropLot(models.Model):
    """
    Crop Harvest Batch (ISL Layer)
    Implements ISL standards using _inherits mechanism for proper ownership
    and industry specialization while maintaining base functionality.
    """
    _name = 'farm.crop.lot'
    _description = 'Crop Harvest Batch (ISL Layer)'
    _inherits = {'stock.lot': 'lot_id'}

    lot_id = fields.Many2one('stock.lot', string='Base Lot', required=True, ondelete='cascade')

    # Terroir Metadata (Moved from Base)
    plot_origin_id = fields.Many2one('farm.location', string='Origin Plot', domain="[('is_land_parcel', '=', True)]")
    terroir_json = fields.Text("Weighted Terroir Attributes")

    def write(self, vals):
        # Ensure industry type is set to crop agriculture
        if 'industry_type' not in vals and not self.industry_type:
            vals['industry_type'] = 'crop'
        return super().write(vals)

    @api.model_create_multi
    def create(self, vals_list):
        # Ensure industry type is set to crop agriculture
        for vals in vals_list:
            if 'industry_type' not in vals or not vals.get('industry_type'):
                vals['industry_type'] = 'crop'
        return super().create(vals_list)
