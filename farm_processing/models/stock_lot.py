from odoo import models, fields, api, _
from datetime import timedelta
import logging

_logger = logging.getLogger(__name__)

class StockLot(models.Model):
    _inherit = 'stock.lot'

    # --- Industry Context ---
    lot_purpose = fields.Selection([
        ('harvest', 'Land Harvest'),
        ('production', 'Manufacturing Output'),
        ('biological_asset', 'Biological Asset (Livestock/Aqua)'),
        ('lab_sample', 'Laboratory Sample'),
        ('commercial', 'Commercial / Resale')
    ], string="Lot Purpose", default='production', help="Business context of this specific lot.")

    # --- Biological Asset Details (US-03-01) ---
    birth_date = fields.Date("Birth/Hatch Date")
    life_stage = fields.Selection([
        ('juvenile', 'Juvenile / Seedling'),
        ('growing', 'Growing / Fattening'),
        ('mature', 'Mature / Breeding'),
        ('harvested', 'Harvested / Culled')
    ], string="Life Stage", default='juvenile')
    current_weight = fields.Float("Current Weight (kg)", digits='Stock Weight')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('neutral', 'Neutral/Mixed')], string="Gender")

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
    last_gps_lat = fields.Float("Last Latitude", digits=(10, 7))
    last_gps_lng = fields.Float("Last Longitude", digits=(10, 7))
    last_location_update = fields.Datetime("Last Location Sync")

    def action_update_location_by_gps(self, lat=None, lng=None):
        """ US-TECH-04-02: Spatial algorithm to find and set plot based on GPS. """
        self.ensure_one()
        target_lat = lat or self.last_gps_lat
        target_lng = lng or self.last_gps_lng
        
        if not target_lat or not target_lng:
            return False

        # Find all land parcels with defined boundaries
        plots = self.env['stock.location'].search([
            ('is_land_parcel', '=', True),
            ('boundary_geojson', '!=', False)
        ])

        for plot in plots:
            if self._is_point_in_plot(target_lat, target_lng, plot):
                self.write({
                    'location_id': plot.id,
                    'last_location_update': fields.Datetime.now()
                })
                return plot
        return False

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

    # 批次溯源 [US-14-03, US-04-02]
    parent_lot_ids = fields.Many2many('stock.lot', 'stock_lot_parent_lot_rel', 'child_lot_id', 'parent_id', string="Parent Lots/Origins", help="Trace back to the raw material lots consumed.")
    child_lot_ids = fields.One2many('stock.lot', 'parent_lot_ids', string="Derived Products")
    
    # 性能优化：写入时预计算的全路径 [Pre-calculated Path]
    full_traceability_path = fields.Text("Full Traceability Path", readonly=True, 
                                       help="Flattened upstream lot IDs for instant lookup.")

    # 分级与元数据 [US-14-05]
    quality_grade = fields.Selection([
        ('a', 'Grade A / Premium'),
        ('b', 'Grade B / Standard'),
        ('c', 'Grade C / Processing'),
        ('loss', 'Loss/Waste')
    ], string='Quality Grade')
    
    harvest_date = fields.Date('Harvest Date')
    plot_id = fields.Many2one('farm.land', string='Origin Plot')

    # Potency & Attributes [US-14-11, US-14-15, US-14-17]
    active_content = fields.Float("Active Content (%)", help="Actual potency/active ingredient percentage.")
    is_organic = fields.Boolean("Is Organic", default=False)
    is_gmo = fields.Boolean("Is GMO", default=False)
    functional_tags = fields.Char("Functional Tags", help="e.g. Selenium-enriched, Low-temp pressed")
    terroir_attributes_json = fields.Text("Terroir Attributes (JSON)", help="JSON string of weighted terroir attributes from source lots [US-14-06].")
    package_id = fields.Many2one('farm.package', string="Contained in Package", help="The physical package this lot belongs to.")

    @api.constrains('lot_purpose', 'plot_id')
    def _check_harvest_data(self):
        """ US-TECH-02-04: Ensure harvest lots have origin plot info. """
        for lot in self:
            if lot.lot_purpose == 'harvest' and not lot.plot_id:
                raise ValidationError(_("Land Harvest lots must have an associated Origin Plot for full traceability."))

    def action_get_full_ancestry(self, collected_ids=None):
        """ US-14-22: Recursive algorithm to get all upstream lots. """
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
        """ US-04-04: Check for expiring lots and create activity reminders. """
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
        return True

