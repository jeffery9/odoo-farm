# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class StockQuant(models.Model):
    _inherit = 'stock.quant'

    def _check_consolidation_constraints(self, package_id, lot_id, product_id):
        if not package_id or not lot_id or not product_id:
            return
        tracking = self.env['stock.matter.tracking'].search([('package_id', '=', package_id)], limit=1)
        if not tracking:
            return
            
        new_lot = self.env['stock.lot'].browse(lot_id)
        product = self.env['product.product'].browse(product_id)
        category = product.categ_id
        if not category:
            return

        # Find existing quants in container
        existing_quants = self.search([('package_id', '=', package_id)])
        if existing_quants:
            # Quality Grade restriction check
            if not category.allow_cross_quality_mix:
                existing_lots = existing_quants.mapped('lot_id')
                if any(l.quality_grade != new_lot.quality_grade for l in existing_lots if l.quality_grade and l != new_lot):
                    raise ValidationError(_("Mixing Blocked: Cross-quality mixing is disabled for category %s.") % category.name)

            # Strict Isolation check
            if category.consolidation_strategy == 'strict_isolation':
                if any(q.lot_id != new_lot for q in existing_quants):
                    raise ValidationError(_("Strict Isolation: Container %s enforces single-lot isolation.") % tracking.name)

    @api.constrains('quantity', 'package_id', 'location_id')
    def _check_jidoka_locks(self):
        for quant in self:
            if quant.package_id:
                tracking = self.env['stock.matter.tracking'].search([('package_id', '=', quant.package_id.id)], limit=1)
                if tracking:
                    # Mechanical Vessel Lock Interlock
                    if 'is_vessel_locked' in tracking._fields and tracking.is_vessel_locked:
                        raise ValidationError(_("Jidoka Interlock Blocked: Vessel Lock is active on container %s. All movements and operations locked.") % tracking.name)

                    # Check matter tracking carrier volume capacity
                    if tracking.max_capacity_volume_m3 > 0.0:
                        existing_quants = self.env['stock.quant'].search([
                            ('package_id', '=', quant.package_id.id)
                        ])
                        total_volume = sum(existing_quants.mapped('quantity'))
                        if total_volume > tracking.max_capacity_volume_m3:
                            raise ValidationError(_(
                                "Backpressure Limit Reached: Active vessel tracking carrier %s exceeds "
                                "maximum physical capacity limit (%.2f m³)."
                            ) % (tracking.package_id.name, tracking.max_capacity_volume_m3))

            # Stocking Density Interlock Validation
            if quant.location_id:
                farm_loc = self.env['farm.location'].search([
                    '|', ('id', '=', quant.location_id.id),
                    ('agri_location_id', '=', quant.location_id.id)
                ], limit=1)

                if farm_loc and farm_loc.max_stocking_density > 0.0:
                    existing_quants = self.env['stock.quant'].search([
                        ('location_id', '=', quant.location_id.id)
                    ])
                    total_count = sum(existing_quants.mapped('quantity'))
                    
                    if farm_loc.land_area > 0.0:
                        density = total_count / farm_loc.land_area
                        if density > farm_loc.max_stocking_density:
                            raise ValidationError(_(
                                "Backpressure Limit Reached: Relocation of quantity %.2f would exceed "
                                "maximum stocking density (%.2f units/m²) of target destination %s."
                            ) % (quant.quantity, farm_loc.max_stocking_density, farm_loc.name))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            package_id = vals.get('package_id')
            lot_id = vals.get('lot_id')
            product_id = vals.get('product_id')
            if package_id and lot_id and product_id:
                self._check_consolidation_constraints(package_id, lot_id, product_id)
        res = super(StockQuant, self).create(vals_list)
        tracking_to_recalc = self.env['stock.matter.tracking']
        for quant in res:
            if quant.package_id:
                tracking = self.env['stock.matter.tracking'].search([('package_id', '=', quant.package_id.id)], limit=1)
                if tracking:
                    tracking_to_recalc |= tracking
        if tracking_to_recalc:
            tracking_to_recalc._recalculate_consolidation_properties()
        return res

    def write(self, vals):
        if 'package_id' in vals or 'lot_id' in vals or 'quantity' in vals:
            for quant in self:
                package_id = vals.get('package_id', quant.package_id.id)
                lot_id = vals.get('lot_id', quant.lot_id.id)
                product_id = quant.product_id.id
                if package_id and lot_id and product_id:
                    self._check_consolidation_constraints(package_id, lot_id, product_id)
        res = super(StockQuant, self).write(vals)
        if 'package_id' in vals or 'lot_id' in vals or 'quantity' in vals:
            tracking_to_recalc = self.env['stock.matter.tracking']
            for quant in self:
                if quant.package_id:
                    tracking = self.env['stock.matter.tracking'].search([('package_id', '=', quant.package_id.id)], limit=1)
                    if tracking:
                        tracking_to_recalc |= tracking
            if tracking_to_recalc:
                tracking_to_recalc._recalculate_consolidation_properties()
        return res
