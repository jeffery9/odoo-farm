from odoo import models, fields, api, _
from datetime import timedelta
import logging

_logger = logging.getLogger(__name__)

class StockLot(models.Model):
    _name = 'stock.lot'
    _inherit = 'stock.lot'

    # --- Industry Context ---
    lot_purpose = fields.Selection([
        ('harvest', 'Land Harvest'),
        ('production', 'Manufacturing Output'),
        ('biological_asset', 'Biological Asset (Livestock/Aqua)'),
        ('lab_sample', 'Laboratory Sample'),
        ('commercial', 'Commercial / Resale')
    ], string="Lot Purpose", default='production', help="Business context of this specific lot.")

    # --- Biological Asset Details (US-003-01) ---
    birth_date = fields.Date("Birth/Hatch Date")
    
    current_weight = fields.Float(
        string="Current Weight (kg)",
        compute='_compute_matter_physical_properties',
        inverse='_inverse_current_weight',
        store=False,
        help="Compatibility Bridge: Resolves dynamic weight from active tracking containers."
    )
    last_gps_lat = fields.Float(
        string="Last Latitude",
        compute='_compute_matter_physical_properties',
        inverse='_inverse_spatial_properties',
        store=False
    )
    last_gps_lng = fields.Float(
        string="Last Longitude",
        compute='_compute_matter_physical_properties',
        inverse='_inverse_spatial_properties',
        store=False
    )
    life_stage = fields.Selection([
        ('juvenile', 'Juvenile / Seedling'),
        ('growing', 'Growing / Fattening'),
        ('mature', 'Mature / Breeding'),
        ('harvested', 'Harvested / Culled')
    ], string="Life Stage", compute='_compute_matter_physical_properties', inverse='_inverse_matter_life_stage', store=False)
    
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('neutral', 'Neutral/Mixed')], string="Gender")

    @api.depends('quant_ids.package_id')
    def _compute_matter_physical_properties(self):
        for lot in self:
            # Locate an active packaging quant and retrieve its associated matter tracking record
            quants = lot.quant_ids.filtered(lambda q: q.package_id)
            _logger.info("COMPUTE LOT BRIDGES: lot=%s, quants=%s, quant_packages=%s", lot.name, lot.quant_ids, lot.quant_ids.mapped('package_id'))
            tracking_record = False
            for q in quants:
                tracking_record = self.env['stock.matter.tracking'].search([('package_id', '=', q.package_id.id)], limit=1)
                if tracking_record:
                    break
                
            if tracking_record:
                _logger.info("COMPUTE LOT BRIDGES: Found tracking_record=%s, weight=%s", tracking_record.name, tracking_record.current_weight)
                lot.current_weight = tracking_record.current_weight or 0.0
                lot.last_gps_lat = tracking_record.last_gps_lat or 0.0
                lot.last_gps_lng = tracking_record.last_gps_lng or 0.0
                lot.life_stage = tracking_record.life_stage or 'juvenile'
            else:
                lot.current_weight = 0.0
                lot.last_gps_lat = 0.0
                lot.last_gps_lng = 0.0
                lot.life_stage = 'juvenile'

    def _inverse_current_weight(self):
        from odoo.exceptions import UserError
        raise UserError(_(
            "Legacy Write Block: Weight is now managed dynamically by Matter Tracking (LPN/Vessel). "
            "Please update the weight on the active Matter Tracking container directly."
        ))

    def _inverse_spatial_properties(self):
        from odoo.exceptions import UserError
        raise UserError(_(
            "Legacy Write Block: GPS positioning is now managed dynamically by Matter Tracking (LPN/Vessel). "
            "Please sync coordinates via the active Matter Tracking container."
        ))

    def _inverse_matter_life_stage(self):
        from odoo.exceptions import UserError
        raise UserError(_(
            "Legacy Write Block: Lifecycle stages are now managed dynamically by Matter Tracking (LPN/Vessel). "
            "Please update status on the active Matter Tracking container."
        ))

    # --- Polymorphic Data Reflection (US-TECH-06-20) ---
    def _get_isl_summary_parts(self):
        """ Reflexively pull info from ISL sub-models for display in Base Lookups. """
        res = super(StockLot, self)._get_isl_summary_parts()
        if self.lot_purpose == 'harvest':
            isl = self.env['farm.lot.harvest'].search([('lot_id', '=', self.id)], limit=1)
            if isl:
                res.append(_("Crop: Plot %s") % (isl.plot_id.name or 'Unknown'))
        return res

    # --- Spatial Positioning (US-TECH-04-02) ---
    last_location_update = fields.Datetime("Last Location Sync")

    def action_update_location_by_gps(self, lat=None, lng=None):
        from odoo.exceptions import UserError
        raise UserError(_(
            "Legacy Write Block: GPS positioning is now managed dynamically by Matter Tracking (LPN/Vessel). "
            "Please sync coordinates via the active Matter Tracking container."
        ))

    def _is_point_in_plot(self, lat, lng, plot):
        """ Ray-casting algorithm for GeoJSON Polygon containment. """
        import json
        try:
            data = json.loads(plot.boundary_geojson)
            coords = []
            if data.get('type') == 'Polygon':
                coords = data['coordinates'][0]
            elif data.get('type') == 'Feature' and data['geometry']['type'] == 'Polygon':
                coords = data['geometry']['coordinates'][0]
            
            if not coords:
                return False

            # Standard point-in-polygon logic
            inside = False
            n = len(coords)
            p1x, p1y = coords[0][0], coords[0][1] # lng, lat
            for i in range(n + 1):
                p2x, p2y = coords[i % n][0], coords[i % n][1]
                if lat > min(p1y, p2y):
                    if lat <= max(p1y, p2y):
                        if lng <= max(p1x, p2x):
                            if p1y != p2y:
                                xinters = (lat - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                            if p1x == p2x or lng <= xinters:
                                inside = not inside
                p1x, p1y = p2x, p2y
            return inside
        except Exception:
            return False

    # 批次溯源 [US-037-03, US-004-02]
    parent_lot_ids = fields.Many2many('stock.lot', 'farm_stock_lot_parent_rel_custom', 'child_lot_id', 'parent_id', string="Parent Lots/Origins", help="Trace back to the raw material lots consumed.")
    child_lot_ids = fields.One2many('stock.lot', 'parent_lot_ids', string="Derived Products")
    
    # 性能优化：写入时预计算的全路径 [Pre-calculated Path]
    full_traceability_path = fields.Text("Full Traceability Path", readonly=True, 
                                       help="Flattened upstream lot IDs for instant lookup.")

    # 分级与元数据 [US-037-05]
    quality_grade = fields.Selection([
        ('grade_a', 'Grade A'),
        ('grade_b', 'Grade B'),
        ('grade_c', 'Grade C'),
        ('ungraded', 'Not Graded'),
        ('a', 'Grade A / Premium'),
        ('b', 'Grade B / Standard'),
        ('c', 'Grade C / Processing'),
        ('loss', 'Loss/Waste')
    ], default='ungraded')
    
    harvest_date = fields.Date('Harvest Date')
    plot_id = fields.Many2one('farm.location', string='Origin Plot')

    # Potency & Attributes [US-037-11, US-037-15, US-037-17]
    active_content = fields.Float("Active Content (%)", help="Actual potency/active ingredient percentage.")
    is_organic = fields.Boolean("Is Organic", default=False)
    is_gmo = fields.Boolean("Is GMO", default=False)
    functional_tags = fields.Char("Functional Tags", help="e.g. Selenium-enriched, Low-temp pressed")
    terroir_attributes_json = fields.Text("Terroir Attributes (JSON)", help="JSON string of weighted terroir attributes from source lots [US-037-06].")
    package_id = fields.Many2one('farm.package', string="Contained in Package", help="The physical package this lot belongs to.")

    @api.constrains('lot_purpose', 'plot_id')
    def _check_harvest_data(self):
        """ US-TECH-02-04: Ensure harvest lots have origin plot info. """
        for lot in self:
            if lot.lot_purpose == 'harvest' and not lot.plot_id:
                raise ValidationError(_("Land Harvest lots must have an associated Origin Plot for full traceability."))

    def action_get_full_ancestry(self, collected_ids=None):
        """ US-037-22: Recursive algorithm to get all upstream lots. """
        self.ensure_one()
        if collected_ids is None:
            collected_ids = set()
        
        ancestors = self.env['stock.lot']
        for parent in self.parent_lot_ids:
            if parent.id not in collected_ids:
                collected_ids.add(parent.id)
                ancestors |= parent
                ancestors |= parent.action_get_full_ancestry(collected_ids)
        
        return ancestors

    def get_recall_report_data(self):
        """ Logic to structure the full supply chain report for this lot. """
        self.ensure_one()
        ancestors = self.action_get_full_ancestry()
        harvest_lots = ancestors.filtered(lambda l: l.lot_purpose == 'harvest')
        
        report_data = {
            'target_lot': self.name,
            'product': self.product_id.display_name,
            'ancestry_count': len(ancestors),
            'origin_plots': list(set(harvest_lots.mapped('plot_id.name'))),
            'harvest_dates': [d.strftime('%Y-%m-%d') for d in harvest_lots.mapped('harvest_date') if d],
            'full_chain': ancestors.mapped(lambda l: {
                'lot': l.name,
                'purpose': l.lot_purpose,
                'product': l.product_id.name
            })
        }
        return report_data

    def _check_expiring_lots(self):
        """ US-004-04: Check for expiring lots and create activity reminders. """
        _logger.info("Running _check_expiring_lots cron job...")
        today = fields.Date.today()
        # Find lots expiring within the next 30 days
        expiring_date = today + timedelta(days=30)
        expiring_lots = self.search([
            ('expiration_date', '!=', False),
            ('expiration_date', '>', today),
            ('expiration_date', '<=', expiring_date),
            ('product_id.type', '=', 'product'), # Only actual products
        ])

        for lot in expiring_lots:
            # Check if an activity for this lot already exists
            existing_activity = self.env['mail.activity'].search([
                ('res_model_id', '=', self.env['ir.model']._get_id(self._name)),
                ('res_id', '=', lot.id),
                ('activity_type_id.category', '=', 'reminder'), # Assuming a reminder category
                ('summary', 'like', _('Expiring Lot')),
                ('date_deadline', '=', lot.expiration_date),
                ('state', 'not in', ['done', 'canceled']) # Don't create if open activity exists
            ], limit=1)

            if not existing_activity:
                # Create a reminder activity for the warehouse manager
                self.env['mail.activity'].create({
                    'res_model_id': self.env['ir.model']._get_id(self._name),
                    'res_id': lot.id,
                    'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id, # Or a specific reminder activity type
                    'summary': _('Expiring Lot: %s (%s) expires on %s. Prioritize usage (FEFO).') % (lot.product_id.display_name, lot.name, lot.expiration_date),
                    'user_id': self.env.ref('stock.group_stock_user').users[0].id if self.env.ref('stock.group_stock_user').users else self.env.user.id, # Assign to a warehouse user or current user
                    'date_deadline': lot.expiration_date,
                    'note': _('This lot is expiring soon. Ensure it is used before the expiration date to avoid waste.'),
                })
                _logger.info("Created activity for expiring lot %s", lot.name)

        # Also check for expired lots (past expiration date) - additional functionality for US-004-04
        self._check_expired_lots()
        return True

    def _check_expired_lots(self):
        """ Check for expired lots and create urgent activity reminders. """
        _logger.info("Running _check_expired_lots cron job...")
        today = fields.Date.today()
        # Find lots that have expired (expiration date is in the past)
        expired_lots = self.search([
            ('expiration_date', '!=', False),
            ('expiration_date', '<', today),
            ('product_id.type', '=', 'product'), # Only actual products
        ])

        for lot in expired_lots:
            # Check if an urgent activity for this expired lot already exists
            existing_urgent_activity = self.env['mail.activity'].search([
                ('res_model_id', '=', self.env['ir.model']._get_id(self._name)),
                ('res_id', '=', lot.id),
                ('summary', 'ilike', _('Expired Lot')),
                ('state', 'not in', ['done', 'canceled']) # Don't create if open activity exists
            ], limit=1)

            if not existing_urgent_activity:
                # Create an urgent reminder activity for the warehouse manager to quarantine or dispose
                self.env['mail.activity'].create({
                    'res_model_id': self.env['ir.model']._get_id(self._name),
                    'res_id': lot.id,
                    'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                    'summary': _('URGENT: Expired Lot: %s (%s) expired on %s. Quarantine required.') % (lot.product_id.display_name, lot.name, lot.expiration_date),
                    'user_id': self.env.ref('stock.group_stock_user').users[0].id if self.env.ref('stock.group_stock_user').users else self.env.user.id,
                    'date_deadline': today,
                    'note': _('This lot has expired on %s. Immediate action required to quarantine or dispose of the expired inventory to prevent contamination or compliance issues.') % lot.expiration_date,
                })
                _logger.info("Created urgent activity for expired lot %s", lot.name)

        return True

    def _check_lot_expiry_before_use(self):
        """ US-004-04: Check if a lot is expired before it's used in operations. """
        today = fields.Date.today()
        if self.expiration_date and self.expiration_date < today:
            from odoo.exceptions import UserError
            raise UserError(_("The lot '%s' is expired (expired on %s). It cannot be used in operations.") % (self.name, self.expiration_date))
        return True


class StockMove(models.Model):
    _name = 'stock.move'
    _inherit = 'stock.move'

    is_subcontract = fields.Boolean("Is Subcontract Move", default=False)
    bom_id = fields.Many2one('mrp.bom', string="BOM")

