# Dual-Axis Traceability Decoupling Implementation Plan (Phase 1 & 2)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Decouple physical dynamic carrier states from genetic DNA attributes by migrating weight, life stage, GPS tracking, and geofencing to `stock.matter.tracking`, while purifying `stock.lot` and providing a computed backward compatibility bridge with transactional write-locks.

**Architecture:** Extend the Odoo 19 `stock.matter.tracking` model to handle active weights, lifecycle stages, and ray-casting geolocation boundaries. Transform existing lot physical fields in `farm_processing` to read-only computed properties resolving from associated active packaging quants.

**Tech Stack:** Odoo 19 CE / Python 3.12 / PostgreSQL 16 / pytest-bdd (represented via standard unittest)

## Global Constraints
* **Odoo 19 Compliance:** Use `stock.package` instead of `stock.quant.package`. Define storable products as `type: 'consu'` with `is_storable: True`.
* **Surgical Integrity:** Modify files minimally using precise `replace` operations without modifying neighboring logic or formatting.
* **No Suppressions:** Do not use `warnings.suppress` or bypass Odoo registry/ORM structures. Follow explicit composition.

---

### Task 1: Physical Model Enrichment in `farm_core`

**Files:**
- Modify: `farm_core/models/stock_matter_tracking.py`
- Test: `farm_core/tests/test_stock_matter_tracking.py`

**Interfaces:**
- Consumes: None (Extends existing base `stock.matter.tracking` model)
- Produces: `current_weight` (Float), `life_stage` (Selection), `last_gps_lat` (Float), `last_gps_lng` (Float), `last_location_update` (Datetime), and geographic containment methods on the tracking model.

- [ ] **Step 1: Define physical fields and geographic methods inside `farm_core/models/stock_matter_tracking.py`**

Surgically append physical/spatial definitions and geofence verification logic to the `stock.matter.tracking` model in `farm_core/models/stock_matter_tracking.py`.

```python
    current_weight = fields.Float(
        string="Current Weight (kg)",
        digits='Stock Weight',
        tracking=True,
        help="Dynamic weight of the material inside this vessel or package container."
    )
    last_gps_lat = fields.Float("Last Latitude", digits=(10, 7), tracking=True)
    last_gps_lng = fields.Float("Last Longitude", digits=(10, 7), tracking=True)
    last_location_update = fields.Datetime("Last Location Sync")
    life_stage = fields.Selection([
        ('juvenile', 'Juvenile / Seedling'),
        ('growing', 'Growing / Fattening'),
        ('mature', 'Mature / Breeding'),
        ('harvested', 'Harvested / Culled')
    ], string="Dynamic Life Stage", default='juvenile', tracking=True)

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
                    'location_id': plot.id,
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
```

- [ ] **Step 2: Append Unit Test to verify new physical attributes and geofencing on Matter Tracking**

Add `test_04_matter_physical_properties_and_geofencing` inside `farm_core/tests/test_stock_matter_tracking.py`:

```python
    def test_04_matter_physical_properties_and_geofencing(self):
        """ Test weight tracking, GPS alignment, and Ray-casting Plot geofencing inside Matter Tracking """
        tracking = self.Tracking.create({
            'vessel_phase': 'idle',
            'current_weight': 450.5,
            'life_stage': 'growing'
        })
        self.assertEqual(tracking.current_weight, 450.5)
        self.assertEqual(tracking.life_stage, 'growing')

        # Create land parcel with geojson polygon
        import json
        boundary = {
            "type": "Polygon",
            "coordinates": [[
                [120.0, 30.0],
                [121.0, 30.0],
                [121.0, 31.0],
                [120.0, 31.0],
                [120.0, 30.0]
            ]]
        }
        plot = self.env['farm.location'].create({
            'name': 'Greenhouse Poly Block A',
            'is_land_parcel': True,
            'boundary_geojson': json.dumps(boundary)
        })

        # Test GPS outside boundary
        matched_plot = tracking.action_update_location_by_gps(lat=29.5, lng=120.5)
        self.assertFalse(matched_plot)

        # Test GPS inside boundary
        matched_plot = tracking.action_update_location_by_gps(lat=30.5, lng=120.5)
        self.assertEqual(matched_plot, plot)
        self.assertEqual(tracking.location_id, plot)
        self.assertEqual(tracking.last_gps_lat, 30.5)
```

- [ ] **Step 3: Run the test suite on a clean database**

Run: `docker compose run --rm web odoo -d test_clean_db_plan_t1 -i base,stock,farm_core --test-enable --test-tags=/farm_core --stop-after-init --log-level=warn`  
Expected: PASS

- [ ] **Step 4: Commit**

```bash
git add farm_core/models/stock_matter_tracking.py farm_core/tests/test_stock_matter_tracking.py
git commit -m "feat(core): enrich stock.matter.tracking with weight, spatial positioning, and geofencing [US-082-04]"
```

---

### Task 2: Operator UI Expansion in `farm_core`

**Files:**
- Modify: `farm_core/views/stock_matter_tracking_views.xml`

- [ ] **Step 1: Add spatial and physical properties to Matter Tracking form view**

Modify `farm_core/views/stock_matter_tracking_views.xml` to include a group for "Physical & Spatial Profile":

```xml
                            <group string="Physical Profile">
                                <field name="current_weight" />
                                <field name="life_stage" />
                            </group>
                            <group string="Spatial Profile">
                                <field name="last_gps_lat" readonly="1" />
                                <field name="last_gps_lng" readonly="1" />
                                <field name="last_location_update" readonly="1" />
                            </group>
```

- [ ] **Step 2: Verify XML validation and load the views cleanly**

Run: `docker compose run --rm web odoo -d test_clean_db_plan_t2 -i base,stock,farm_core --stop-after-init --log-level=warn`  
Expected: SUCCESS

- [ ] **Step 3: Commit**

```bash
git add farm_core/views/stock_matter_tracking_views.xml
git commit -m "style(core): enrich operator UI view layouts with physical and spatial sections [US-082-04]"
```

---

### Task 3: Purification and Downward Compatibility Bridge on `stock.lot`

**Files:**
- Modify: `farm_processing/models/stock_lot.py`
- Test: `farm_core/tests/test_stock_matter_tracking.py`

**Interfaces:**
- Consumes: `stock.matter.tracking` fields from Task 1.
- Produces: Stored or dynamic computed properties on `stock.lot` representing `current_weight`, `life_stage`, `last_gps_lat`, `last_gps_lng`, and their corresponding write-lock inverses.

- [ ] **Step 1: Refactor `farm_processing/models/stock_lot.py` to bridge physical fields**

Find the definitions of `current_weight`, `life_stage`, `last_gps_lat`, `last_gps_lng` inside `farm_processing/models/stock_lot.py` and convert them into computed properties pointing to the active tracking container.

```python
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

    @api.depends('quant_ids.package_id')
    def _compute_matter_physical_properties(self):
        for lot in self:
            # Locate an active packaging quant with matter tracking enabled
            quants = lot.quant_ids.filtered(lambda q: q.package_id and q.package_id.is_matter_tracking)
            if quants:
                package = quants[0].package_id
                lot.current_weight = getattr(package, 'current_weight', 0.0)
                lot.last_gps_lat = getattr(package, 'last_gps_lat', 0.0)
                lot.last_gps_lng = getattr(package, 'last_gps_lng', 0.0)
                lot.life_stage = getattr(package, 'life_stage', 'juvenile')
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
```

- [ ] **Step 2: Append BDD Unit Test inside `test_stock_matter_tracking.py` to verify computed properties and write-locks**

```python
    def test_05_decoupled_compatibility_bridge_and_write_locks(self):
        """ Verify Lot physical properties are computed from Matter Tracking, and legacy writes are blocked """
        from odoo.exceptions import UserError

        # Create tracking vessel with physical profile
        tracking = self.Tracking.create({
            'vessel_phase': 'idle',
            'current_weight': 120.5,
            'life_stage': 'mature',
            'last_gps_lat': 41.25,
            'last_gps_lng': -73.98
        })

        # Put grapes lot into the tracking container
        self.env['stock.quant'].create({
            'product_id': self.product_apple.id,
            'location_id': self.location_vessel.id,
            'lot_id': self.lot_a.id,
            'quantity': 1.0,
            'package_id': tracking.id
        })

        # Test read bridge
        self.assertEqual(self.lot_a.current_weight, 120.5)
        self.assertEqual(self.lot_a.life_stage, 'mature')
        self.assertEqual(self.lot_a.last_gps_lat, 41.25)

        # Test legacy write blocks
        with self.assertRaisesRegex(UserError, "Weight is now managed dynamically by Matter Tracking"):
            self.lot_a.write({'current_weight': 250.0})

        with self.assertRaisesRegex(UserError, "GPS positioning is now managed dynamically by Matter Tracking"):
            self.lot_a.write({'last_gps_lat': 42.0})
```

- [ ] **Step 3: Run full integration regression test suite on a clean database**

Run: `docker compose run --rm web odoo -d test_clean_db_plan_t3 -i base,stock,farm_core,farm_mrp --test-enable --test-tags=/farm_core,/farm_mrp --stop-after-init --log-level=warn`  
Expected: PASS with 100% success on all base and manufacturing matter-tracking/bridge test classes.

- [ ] **Step 4: Commit**

```bash
git add farm_processing/models/stock_lot.py farm_core/tests/test_stock_matter_tracking.py
git commit -m "feat(processing): purify stock.lot and implement compatibility bridge write-locks [US-082-04]"
```
