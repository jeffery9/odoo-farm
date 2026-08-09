# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime, timedelta

class StockMatterTracking(models.Model):
    _name = 'stock.matter.tracking'
    _description = 'Stock Matter Tracking (Individual Agricultural Tracking / LPN / SFC)'
    _inherits = {'stock.package': 'package_id'}
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    package_id = fields.Many2one(
        'stock.package',
        string='Associated Stock Package',
        required=True,
        ondelete='cascade',
        index=True,
        help="The physical stock package delegated by this Individual Agricultural Tracking record."
    )

    biological_asset_id = fields.Many2one(
        'agri.biological.asset',
        string='Tracked Biological Asset / 个体资产',
        index=True,
        tracking=True,
        help="The specific individual biological/living asset (animal/plant/tree) physically tracked by this matter container."
    )

    vessel_phase = fields.Selection([
        ('idle', 'Idle / 空闲'),
        ('ready', 'Ready / 待命'),
        ('dirty', 'Dirty / 待清洗'),
        ('cleaning', 'Cleaning / 清洗中')
    ], string='Vessel/Individual Phase / 阶段状态', default='idle', required=True, index=True, tracking=True, help="GxP container or agricultural individual physical phase.")

    gxp_open_time = fields.Datetime(
        string='GxP Opened Time',
        tracking=True,
        help="Timestamp when the vessel's GxP environmental barrier was opened/sealed."
    )

    gxp_expiry_time = fields.Datetime(
        string='GxP Expiry Time',
        tracking=True,
        help="Timestamp when the current clean-hold validation expires."
    )

    dna_integrity_score = fields.Float(
        string='DNA Integrity Score',
        default=100.0,
        tracking=True,
        help="The genealogical purity and integrity score propagated from ancestral material lots."
    )

    current_weight = fields.Float(
        string="Current Weight (kg)",
        digits='Stock Weight',
        tracking=True,
        help="Dynamic weight of the material inside this vessel or package container."
    )
    farm_location_id = fields.Many2one('farm.location', string="Agricultural Plot / 农事地块", tracking=True)
    last_gps_lat = fields.Float("Last Latitude", digits=(10, 7), tracking=True)
    last_gps_lng = fields.Float("Last Longitude", digits=(10, 7), tracking=True)
    last_location_update = fields.Datetime("Last Location Sync")
    life_stage = fields.Selection([
        ('juvenile', 'Juvenile / Seedling'),
        ('growing', 'Growing / Fattening'),
        ('mature', 'Mature / Breeding'),
        ('harvested', 'Harvested / Culled')
    ], string="Dynamic Life Stage", default='juvenile', tracking=True)

    biological_stage = fields.Selection([
        ('born', 'Born / Started'),
        ('growing', 'Growing / Fattening'),
        ('mature', 'Mature / Breeding'),
        ('harvested', 'Harvested / Culled')
    ], string="Biological Stage", default='born', tracking=True)

    animal_count = fields.Integer("Physical Item Count", default=1, tracking=True)
    water_volume_m3 = fields.Float("Contained Water Volume (m3)", tracking=True)

    is_consolidated = fields.Boolean("Has Consolidated Batches", default=False)
    consolidation_history = fields.Text("Consolidation Audit Log")

    active_enforcement_level = fields.Selection([
        ('guidance', 'Guidance'),
        ('strict', 'Strict')
    ], string="Active Enforcement Level", compute='_compute_active_enforcement', store=True, default='guidance')

    parent_tracking_id = fields.Many2one(
        'stock.matter.tracking',
        string='Parent Source Vessel / 来源容器',
        ondelete='restrict',
        index=True,
        help="The ancestor vessel/individual this matter split from."
    )
    child_tracking_ids = fields.One2many(
        'stock.matter.tracking',
        'parent_tracking_id',
        string='Child Vessels / 拆分容器'
    )
    fission_type = fields.Selection([
        ('none', 'None'),
        ('split', 'Division (分包/分切)'),
        ('slaughter', 'Slaughter (屠宰)')
    ], string='Lineage Fission Type', default='none', help="Lineage division operation classification.")

    lot_ids = fields.Many2many(
        'stock.lot',
        string='Genealogical Lots',
        compute='_compute_lot_ids',
        store=True,
        help="The genealogical material lots currently contained in this vessel/individual."
    )

    snapshot_ids = fields.One2many(
        'stock.matter.tracking.snapshot',
        'tracking_id',
        string='GxP Stage Snapshots',
        help="Historical Before-State snapshots captured during process transitions."
    )

    @api.depends('quant_ids', 'quant_ids.lot_id')
    def _compute_lot_ids(self):
        for rec in self:
            if rec.quant_ids:
                rec.lot_ids = rec.quant_ids.mapped('lot_id')
            else:
                rec.lot_ids = [(5, 0, 0)]

    @api.depends('biological_asset_id', 'quant_ids', 'quant_ids.product_id', 'quant_ids.product_id.categ_id')
    def _compute_active_enforcement(self):
        for rec in self:
            level = 'guidance'
            if rec.biological_asset_id:
                # Resolve biological asset industry category or growth stage settings
                asset_cat = rec.biological_asset_id.growth_stage_id.category_id if rec.biological_asset_id.growth_stage_id else False
                if asset_cat and getattr(asset_cat, 'matter_enforcement_level', False) == 'strict':
                    level = 'strict'
            else:
                # Direct search as fallback to bypass delegation cache delays in transaction tests
                quants = rec.quant_ids or self.env['stock.quant'].search([('package_id', '=', rec.package_id.id)])
                if quants:
                    categories = quants.mapped('product_id.categ_id')
                    if any(cat.matter_enforcement_level == 'strict' for cat in categories):
                        level = 'strict'
            rec.active_enforcement_level = level

    def action_seal_vessel(self):
        self.ensure_one()
        now = fields.Datetime.now()
        self.write({
            'gxp_open_time': now,
            'gxp_expiry_time': now + timedelta(hours=24), # Standard 24h clean-hold limit
            'vessel_phase': 'ready'
        })
        return True

    def action_clean_vessel(self):
        self.ensure_one()
        # Custom safety check: check if locked. This is extended in farm_mrp but we check standard flag here.
        if self.env.context.get('check_vessel_lock') or getattr(self, 'is_vessel_locked', False):
            raise UserError(_("Cannot clean a vessel that is physically locked to a workcenter."))
        self.write({
            'vessel_phase': 'cleaning',
            'gxp_open_time': False,
            'gxp_expiry_time': False
        })
        return True

    def action_complete_cleaning(self):
        self.ensure_one()
        self.write({
            'vessel_phase': 'idle'
        })
        return True

    def action_update_location_by_gps(self, lat=None, lng=None):
        self.ensure_one()
        target_lat = lat or self.last_gps_lat
        target_lng = lng or self.last_gps_lng
        if not target_lat or not target_lng:
            return False

        plots = self.env['farm.location'].search([
            ('is_land_parcel', '=', True),
            ('boundary_geojson', '!=', False)
        ])
        for plot in plots:
            if self._is_point_in_plot(target_lat, target_lng, plot):
                self.write({
                    'farm_location_id': plot.id,
                    'last_location_update': fields.Datetime.now(),
                    'last_gps_lat': target_lat,
                    'last_gps_lng': target_lng,
                })
                return plot
        return False

    def _is_point_in_plot(self, lat, lng, plot):
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

            inside = False
            n = len(coords)
            p1x, p1y = coords[0][0], coords[0][1]  # lng, lat
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

    def action_execute_fission(self, target_products_data):
        """
        Executes physical-logical fission of Matter.
        target_products_data: list of dicts [{'product_id': id, 'quantity': qty, 'lot_name': name}]
        """
        self.ensure_one()
        child_records = self.env['stock.matter.tracking']
        
        # 1. Capture Before-State snapshot
        self.action_capture_snapshot()
        
        # 2. Iterate and create child tracking packages
        for data in target_products_data:
            # Generate child delegated package
            child_package = self.env['stock.package'].create({
                'name': data.get('lot_name') or self.env['ir.sequence'].next_by_code('stock.matter.tracking')
            })
            
            # Inherit genetic attributes and quality markings
            child_tracking = self.create({
                'package_id': child_package.id,
                'parent_tracking_id': self.id,
                'fission_type': 'slaughter' if self.vessel_phase == 'dirty' else 'split',
                'dna_integrity_score': self.dna_integrity_score * 0.95, # 5% entropy decay during split
                'vessel_phase': 'idle'
            })
            child_records |= child_tracking
            
            # Create standard Odoo quant to hold the split matter inside the child package
            self.env['stock.quant'].create({
                'product_id': data['product_id'],
                'quantity': data['quantity'],
                'location_id': self.location_id.id,
                'package_id': child_package.id
            })
            
        # 3. Mark parent vessel as dirty and deplete biological assets
        self.write({
            'vessel_phase': 'dirty',
            'biological_asset_id': False
        })
        
        return child_records

    def action_capture_snapshot(self):
        self.ensure_one()
        snapshot_model = self.env['stock.matter.tracking.snapshot']
        
        # Calculate total matter quantity
        total_qty = sum(self.quant_ids.mapped('quantity')) if self.quant_ids else 0.0
        
        snapshot_vals = {
            'tracking_id': self.id,
            'vessel_phase': self.vessel_phase,
            'biological_asset_id': self.biological_asset_id.id if self.biological_asset_id else False,
            'quantity': total_qty,
            'location_id': self.location_id.id if self.location_id else False,
            'lot_ids': [(6, 0, self.lot_ids.ids)] if self.lot_ids else False,
            'gxp_open_time': self.gxp_open_time,
            'gxp_expiry_time': self.gxp_expiry_time,
        }
        
        # If there's an MRP extension containing phase_id, we populate it
        if 'phase_id' in snapshot_model._fields and getattr(self, 'current_phase_id', False):
            snapshot_vals['phase_id'] = self.current_phase_id.id
            
        return snapshot_model.create(snapshot_vals)

    def write(self, vals):
        # Before-State Snapshot Capture: Catch process transitions
        state_changing_fields = ['current_phase_id', 'vessel_phase', 'location_id', 'biological_asset_id']
        if any(f in vals for f in state_changing_fields):
            for rec in self:
                rec.action_capture_snapshot()

        res = super(StockMatterTracking, self).write(vals)

        # Capture physical metrics changes to Event Logger if model exists
        if any(f in vals for f in ['current_weight', 'life_stage']):
            for rec in self:
                if rec.biological_asset_id and 'farm.livestock.event' in self.env:
                    lots = rec.quant_ids.mapped('lot_id') or rec.lot_ids
                    if lots:
                        self.env['farm.livestock.event'].create({
                            'lot_id': lots[0].id,
                            'event_type': 'weight' if 'current_weight' in vals else 'stage',
                            'event_date': fields.Datetime.now(),
                            'notes': f"Auto-sync from Matter Carrier: {rec.package_id.name}. Weight: {rec.current_weight} kg."
                        })

        return res

    def _recalculate_consolidation_properties(self):
        """ Recalculates total container weights and handles DNA decay calculations """
        import json
        for tracking in self:
            quants = self.env['stock.quant'].search([('package_id', '=', tracking.package_id.id)])
            if quants:
                total_weight = sum(quants.mapped('quantity'))
                tracking.current_weight = total_weight

                # Multi-lot checks
                unique_lots = quants.mapped('lot_id')
                if len(unique_lots) > 1:
                    tracking.is_consolidated = True
                    
                    # Compute DNA Decay if category allows mixing
                    category = unique_lots[0].product_id.categ_id
                    if category and category.consolidation_strategy == 'weighted_average':
                        weighted_sum = sum(q.quantity * (q.lot_id.dna_integrity_score or 100.0) for q in quants)
                        weighted_avg = weighted_sum / total_weight if total_weight else 0.0
                        # Apply 10% mixing entropy penalty
                        tracking.dna_integrity_score = weighted_avg * 0.90
                        
                        # Write JSON audit trail log
                        history = []
                        for q in quants:
                            history.append({
                                'lot': q.lot_id.name,
                                'qty': q.quantity,
                                'dna': q.lot_id.dna_integrity_score or 100.0
                            })
                        tracking.consolidation_history = json.dumps(history)
            else:
                tracking.write({
                    'current_weight': 0.0,
                    'is_consolidated': False,
                    'consolidation_history': False
                })

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            # Generate clean sequence name if name is missing or '/'
            if not vals.get('name') or vals.get('name') == '/':
                vals['name'] = self.env['ir.sequence'].next_by_code('stock.matter.tracking') or '/'
        return super(StockMatterTracking, self).create(vals_list)


class StockMatterTrackingSnapshot(models.Model):
    _name = 'stock.matter.tracking.snapshot'
    _description = 'Stock Matter Tracking GxP Process Stage Snapshot'
    _order = 'timestamp desc'

    tracking_id = fields.Many2one('stock.matter.tracking', string='Matter Tracking Source', required=True, ondelete='cascade', index=True)
    vessel_phase = fields.Selection([
        ('idle', 'Idle / 空闲'),
        ('ready', 'Ready / 待命'),
        ('dirty', 'Dirty / 待清洗'),
        ('cleaning', 'Cleaning / 清洗中')
    ], string='Vessel Phase', required=True)

    biological_asset_id = fields.Many2one('agri.biological.asset', string='Biological Asset / 个体资产')
    quantity = fields.Float(string='Contained Quantity', digits='Product Unit of Measure')
    location_id = fields.Many2one('stock.location', string='Physical Location')
    lot_ids = fields.Many2many('stock.lot', string='Lots Inside')
    timestamp = fields.Datetime(string='Snapshot Timestamp', default=fields.Datetime.now, required=True)
    
    gxp_open_time = fields.Datetime(string='GxP Opened Time')
    gxp_expiry_time = fields.Datetime(string='GxP Expiry Time')
