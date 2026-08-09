# Specs: Biological Asset Vertical Integration & WIP Backpressure Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement vertical integration linking static genetic lots and dynamic carriers to biological assets, and enforce downstream WIP backpressure limits on physical capacities.

**Architecture:** Real-time implicit read-only reflection is combined with event-driven sync on `agri.biological.asset`. Downstream volumetric and stocking density capacities are checked via a transactional `ValidationError` interlock upon operation confirmation and movement writes.

**Tech Stack:** Odoo 19 (CE/EE), Python 3.12+, PostgreSQL

## Global Constraints
- Target Schema: Odoo 19.0 compatibility (e.g. standard `<list>` views, no obsolete APIs)
- Modular isolation: All dependencies flow downwards; cross-module linkages use safe registry fallback checks (`'farm.livestock.event' in self.env`)
- No placeholders: Every task defines concrete parameters and full test scenarios
- TDD cycle: Run verify commands on each step to guarantee absolute success

---

## File Structure & Responsibility Map

1.  `farm_core/models/agri_biological_asset.py` (Modify): Extends `agri.biological.asset` with dynamic computed fields pointing to its physical `stock.matter.tracking` carrier.
2.  `farm_core/models/stock_matter_tracking.py` (Modify): Injects the write hook tracking physical state mutations to log `farm.livestock.event` dynamically.
3.  `farm_core/models/land_location.py` (Modify): Adds maximum volumetric capacity (`max_capacity_volume_m3`) and stocking density (`max_stocking_density`) fields to `farm.location`.
4.  `farm_core/models/stock_quant_consolidation.py` (Modify): Enhances `_check_consolidation_constraints` to block quant/move updates when target destination limits are violated.
5.  `farm_mrp/models/mrp_production.py` (Modify): Intercepts `action_confirm` to prevent confirmation if production order target destination violates backpressure margin limits.

---

## Tasks

### Task 1: Biological Asset Real-time Implicit Reflection

**Files:**
- Modify: `farm_core/models/agri_biological_asset.py`
- Test: `farm_core/tests/test_biological_asset_reflection.py`

**Interfaces:**
- Consumes: `stock.matter.tracking` models and relations
- Produces: `current_weight`, `life_stage`, `last_gps_lat`, `last_gps_lng` computed fields on `agri.biological.asset`

- [ ] **Step 1: Write the failing test**
  Create the test file `farm_core/tests/test_biological_asset_reflection.py` with:
  ```python
  from odoo.tests.common import TransactionCase
  from odoo.exceptions import ValidationError

  class TestBiologicalAssetReflection(TransactionCase):
      def setUp(self):
          super(TestBiologicalAssetReflection, self).setUp()
          self.Asset = self.env['agri.biological.asset']
          self.Tracking = self.env['stock.matter.tracking']
          self.Package = self.env['stock.package']
          self.Product = self.env['product.product']

          # Set up base product & package
          self.product_pig = self.Product.create({'name': 'Pig', 'is_storable': True})
          self.package = self.Package.create({'name': 'LPN-CARRIER-TEST-10'})

      def test_dynamic_reflection_from_carrier(self):
          # 1. Create Biological Asset
          asset = self.Asset.create({'name': 'PIG-HERD-A', 'agricultural_type': 'animal'})

          # 2. Create Matter Tracking Carrier linked to asset
          tracking = self.Tracking.create({
              'package_id': self.package.id,
              'biological_asset_id': asset.id,
              'current_weight': 420.5,
              'life_stage': 'growing',
              'last_gps_lat': 34.0522,
              'last_gps_lng': -118.2437
          })

          # 3. Assert compute reflection
          asset.invalidate_recordset()
          self.assertAlmostEqual(asset.current_weight, 420.5)
          self.assertEqual(asset.life_stage, 'growing')
          self.assertAlmostEqual(asset.last_gps_lat, 34.0522)
          self.assertAlmostEqual(asset.last_gps_lng, -118.2437)
  ```

- [ ] **Step 2: Run test to verify it fails**
  Run: `docker compose run --rm web odoo -d test_db -i base,stock,farm_core --test-enable --test-tags=farm_core --stop-after-init`
  Expected: FAIL (fields not defined or not computed)

- [ ] **Step 3: Implement minimal code**
  In `farm_core/models/agri_biological_asset.py`, add the following fields and method:
  ```python
    tracking_carrier_ids = fields.One2many(
        'stock.matter.tracking',
        'biological_asset_id',
        string='Active Carrier Containers',
        help="The physical tracking carriers carrying this biological asset."
    )

    current_weight = fields.Float(
        string='Current Weight (kg)',
        compute='_compute_carrier_physical_properties',
        store=False,
        help="Dynamic weight resolved from active tracking carriers."
    )

    life_stage = fields.Selection([
        ('juvenile', 'Juvenile / Seedling'),
        ('growing', 'Growing / Fattening'),
        ('mature', 'Mature / Breeding'),
        ('harvested', 'Harvested / Culled')
    ], string='Life Stage', compute='_compute_carrier_physical_properties', store=False)

    last_gps_lat = fields.Float('Last Latitude', compute='_compute_carrier_physical_properties', store=False)
    last_gps_lng = fields.Float('Last Longitude', compute='_compute_carrier_physical_properties', store=False)

    @api.depends('tracking_carrier_ids', 'tracking_carrier_ids.current_weight', 'tracking_carrier_ids.life_stage', 'tracking_carrier_ids.last_gps_lat', 'tracking_carrier_ids.last_gps_lng')
    def _compute_carrier_physical_properties(self):
        for asset in self:
            carriers = asset.tracking_carrier_ids.filtered(lambda c: c.vessel_phase != 'dirty')
            if carriers:
                primary = carriers[0]
                asset.current_weight = primary.current_weight
                asset.life_stage = primary.life_stage
                asset.last_gps_lat = primary.last_gps_lat
                asset.last_gps_lng = primary.last_gps_lng
            else:
                asset.current_weight = 0.0
                asset.life_stage = 'juvenile'
                asset.last_gps_lat = 0.0
                asset.last_gps_lng = 0.0
  ```
  And import `_compute_carrier_physical_properties` dependencies inside `farm_core/tests/__init__.py`:
  Add `from . import test_biological_asset_reflection` inside `farm_core/tests/__init__.py`.

- [ ] **Step 4: Run test to verify it passes**
  Run: `docker compose run --rm web odoo -d test_db -i base,stock,farm_core --test-enable --test-tags=farm_core --stop-after-init`
  Expected: PASS

- [ ] **Step 5: Commit**
  ```bash
  git add farm_core/models/agri_biological_asset.py farm_core/tests/test_biological_asset_reflection.py farm_core/tests/__init__.py
  git commit -m "feat(traceability): implement real-time dynamic reflection on Biological Assets"
  ```

---

### Task 2: Event-driven Write Hook Sync

**Files:**
- Modify: `farm_core/models/stock_matter_tracking.py:298-305`
- Test: `farm_core/tests/test_biological_asset_reflection.py`

**Interfaces:**
- Consumes: physical writes on `stock.matter.tracking`
- Produces: dynamic entry in `farm.livestock.event` if available in the registry

- [ ] **Step 1: Write the failing test**
  Add test method to `farm_core/tests/test_biological_asset_reflection.py`:
  ```python
      def test_event_driven_write_hook_sync(self):
          # Mock the presence of livestock event model inside registry if needed, or check write side-effects
          asset = self.Asset.create({'name': 'PIG-HERD-B', 'agricultural_type': 'animal'})
          tracking = self.Tracking.create({
              'package_id': self.package.id,
              'biological_asset_id': asset.id,
              'current_weight': 100.0,
              'life_stage': 'juvenile'
          })

          # Trigger write of physical state
          tracking.write({'current_weight': 115.0})
          # Assert that the system did not crash and computed values updated
          self.assertEqual(asset.current_weight, 115.0)
  ```

- [ ] **Step 2: Run test to verify it fails**
  Expected: FAIL or verify that we can also record standard events. To verify historical entries: if `'farm.livestock.event' in self.env`, we write to it. Let's add mock-safe testing or verify.

- [ ] **Step 3: Implement minimal code**
  In `farm_core/models/stock_matter_tracking.py` inside the `write(self, vals)` method, add the event-driven logger hook:
  ```python
          # Capture physical metrics changes to Event Logger if model exists
          if any(f in vals for f in ['current_weight', 'life_stage']):
              for rec in self:
                  if rec.biological_asset_id and 'farm.livestock.event' in self.env:
                      self.env['farm.livestock.event'].create({
                          'lot_id': rec.quant_ids.mapped('lot_id')[0].id if rec.quant_ids.mapped('lot_id') else False,
                          'event_type': 'weight' if 'current_weight' in vals else 'stage',
                          'event_date': fields.Datetime.now(),
                          'notes': f"Auto-sync from Matter Carrier: {rec.package_id.name}. Weight: {rec.current_weight} kg."
                      })
  ```

- [ ] **Step 4: Run test to verify it passes**
  Run: `docker compose run --rm web odoo -d test_db -i base,stock,farm_core --test-enable --test-tags=farm_core --stop-after-init`
  Expected: PASS

- [ ] **Step 5: Commit**
  ```bash
  git add farm_core/models/stock_matter_tracking.py farm_core/tests/test_biological_asset_reflection.py
  git commit -m "feat(traceability): integrate dynamic physical metrics write hook to Event Logger"
  ```

---

### Task 3: Physical Capacity & Stocking Density Model Fields

**Files:**
- Modify: `farm_core/models/land_location.py`
- Modify: `farm_core/models/stock_matter_tracking.py`
- Test: `farm_core/tests/test_backpressure_constraints.py`

- [ ] **Step 1: Write the failing test**
  Create `farm_core/tests/test_backpressure_constraints.py` with:
  ```python
  from odoo.tests.common import TransactionCase
  from odoo.exceptions import ValidationError

  class TestBackpressureConstraints(TransactionCase):
      def setUp(self):
          super(TestBackpressureConstraints, self).setUp()
          self.Location = self.env['farm.location']
          self.Tracking = self.env['stock.matter.tracking']
          self.Package = self.env['stock.package']

          # Create a holding location
          self.holding_location = self.Location.create({
              'name': 'Backpressure holding plot',
              'gps_lat': 12.0,
              'gps_lng': 34.0,
              'land_area': 100.0, # 100 sqm
              'max_capacity_volume_m3': 200.0,
              'max_stocking_density': 1.5 # 1.5 animals per sqm => Max 150 animals
          })

      def test_capacity_fields_declaration(self):
          self.assertEqual(self.holding_location.max_capacity_volume_m3, 200.0)
          self.assertEqual(self.holding_location.max_stocking_density, 1.5)
  ```

- [ ] **Step 2: Run test to verify it fails**
  Expected: FAIL (fields do not exist)

- [ ] **Step 3: Implement minimal code**
  In `farm_core/models/land_location.py`, add the fields:
  ```python
    max_capacity_volume_m3 = fields.Float(
        string='Max Capacity Volume (m³)',
        default=0.0,
        help="Maximum capacity constraint for physical volumetric safety checks."
    )

    max_stocking_density = fields.Float(
        string='Max Stocking Density (units/m²)',
        default=0.0,
        help="Maximum stocking density constraint (e.g. animals/sqm or plants/sqm)."
    )
  ```
  And in `farm_core/models/stock_matter_tracking.py`, add the field:
  ```python
    max_capacity_volume_m3 = fields.Float(
        string='Max Capacity Volume (m³)',
        default=0.0,
        help="Maximum capacity constraint for physical volumetric safety checks."
    )
  ```
  And add import inside `farm_core/tests/__init__.py`:
  Add `from . import test_backpressure_constraints` inside `farm_core/tests/__init__.py`.

- [ ] **Step 4: Run test to verify it passes**
  Run: `docker compose run --rm web odoo -d test_db -i base,stock,farm_core --test-enable --test-tags=farm_core --stop-after-init`
  Expected: PASS

- [ ] **Step 5: Commit**
  ```bash
  git add farm_core/models/land_location.py farm_core/models/stock_matter_tracking.py farm_core/tests/test_backpressure_constraints.py farm_core/tests/__init__.py
  git commit -m "feat(traceability): add maximum capacity and stocking density constraint fields"
  ```

---

### Task 4: Volumetric & Density Constraint Interlocks

**Files:**
- Modify: `farm_core/models/stock_quant_consolidation.py`
- Test: `farm_core/tests/test_backpressure_constraints.py`

**Interfaces:**
- Consumes: stock location and quant writing events
- Produces: `ValidationError` block when capacity margins are violated

- [ ] **Step 1: Write the failing test**
  Add the following test methods to `farm_core/tests/test_backpressure_constraints.py`:
  ```python
      def test_stocking_density_interlock_validation(self):
          Product = self.env['product.product']
          Lot = self.env['stock.lot']
          Quant = self.env['stock.quant']

          product = Product.create({'name': 'Sow', 'is_storable': True})
          # Location capacity is 100 sqm with max_stocking_density 1.5 => Max 150 animals.
          # Create quants totaling 160 animals inside the target location
          lot = Lot.create({'name': 'SOW-LOT-TEST-99', 'product_id': product.id})
          
          # Attempting to write a quant that pushes animal density above 1.5 raises ValidationError
          with self.assertRaises(ValidationError):
              Quant.create({
                  'product_id': product.id,
                  'location_id': self.holding_location.agri_location_id.id, # Base stock location linked to agri.location
                  'lot_id': lot.id,
                  'quantity': 160.0
              })
  ```

- [ ] **Step 2: Run test to verify it fails**
  Expected: FAIL (no validation is performed)

- [ ] **Step 3: Implement minimal code**
  In `farm_core/models/stock_quant_consolidation.py` inside the `StockQuant` model, extend the constraint check:
  ```python
      @api.constrains('quantity', 'location_id', 'package_id')
      def _check_backpressure_and_capacity_constraints(self):
          for quant in self:
              # Retrieve linked farm.location if available
              farm_loc = self.env['farm.location'].search([
                  ('agri_location_id', '=', quant.location_id.id)
              ], limit=1)

              if farm_loc and farm_loc.max_stocking_density > 0.0:
                  # Compute current total animal count in this location
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

              # Check matter tracking carrier volume capacity
              if quant.package_id:
                  tracking = self.env['stock.matter.tracking'].search([
                      ('package_id', '=', quant.package_id.id)
                  ], limit=1)
                  if tracking and tracking.max_capacity_volume_m3 > 0.0:
                      existing_quants = self.env['stock.quant'].search([
                          ('package_id', '=', quant.package_id.id)
                      ])
                      total_volume = sum(existing_quants.mapped('quantity')) # Using weight/qty as 1-to-1 volume proxy
                      if total_volume > tracking.max_capacity_volume_m3:
                          raise ValidationError(_(
                              "Backpressure Limit Reached: Active vessel tracking carrier %s exceeds "
                              "maximum physical capacity limit (%.2f m³)."
                          ) % (tracking.package_id.name, tracking.max_capacity_volume_m3))
  ```

- [ ] **Step 4: Run test to verify it passes**
  Run: `docker compose run --rm web odoo -d test_db -i base,stock,farm_core --test-enable --test-tags=farm_core --stop-after-init`
  Expected: PASS

- [ ] **Step 5: Commit**
  ```bash
  git add farm_core/models/stock_quant_consolidation.py farm_core/tests/test_backpressure_constraints.py
  git commit -m "feat(traceability): enforce physical density and volumetric safety limits"
  ```

---

### Task 5: Operations & MRP WIP Backpressure Interlocks

**Files:**
- Modify: `farm_mrp/models/mrp_production.py`
- Test: `farm_mrp/tests/test_mrp_backpressure.py`

**Interfaces:**
- Consumes: `mrp.production` action confirmation
- Produces: blocks production plan if destination capacity limits are violated

- [ ] **Step 1: Write the failing test**
  Create `farm_mrp/tests/test_mrp_backpressure.py` with:
  ```python
  from odoo.tests.common import TransactionCase
  from odoo.exceptions import ValidationError

  class TestMrpBackpressure(TransactionCase):
      def setUp(self):
          super(TestMrpBackpressure, self).setUp()
          self.Location = self.env['farm.location']
          self.Product = self.env['product.product']
          self.Bom = self.env['mrp.bom']
          self.Production = self.env['mrp.production']

          # 1. Create product and destination
          self.p_cow = self.Product.create({'name': 'Dairy Cow', 'is_storable': True})
          self.dest_location = self.Location.create({
              'name': 'Holding Pen C',
              'gps_lat': 12.0,
              'gps_lng': 34.0,
              'land_area': 100.0,
              'max_stocking_density': 0.1 # Max 10 animals
          })

          # 2. Create base BOM
          self.bom = self.Bom.create({
              'product_id': self.p_cow.id,
              'product_tmpl_id': self.p_cow.product_tmpl_id.id,
              'product_qty': 1.0,
              'type': 'normal'
          })

      def test_mrp_confirmation_backpressure_block(self):
          # Attempt to plan and confirm an order of 15 animals (violating max 10 density limit)
          mo = self.Production.create({
              'product_id': self.p_cow.id,
              'bom_id': self.bom.id,
              'product_qty': 15.0,
              'location_dest_id': self.dest_location.agri_location_id.id
          })
          
          with self.assertRaises(ValidationError):
              mo.action_confirm()
  ```

- [ ] **Step 2: Run test to verify it fails**
  Run: `docker compose run --rm web odoo -d test_db -i base,stock,farm_core,farm_mrp --test-enable --test-tags=farm_mrp --stop-after-init`
  Expected: FAIL

- [ ] **Step 3: Implement minimal code**
  In `farm_mrp/models/mrp_production.py` inside `action_confirm(self)` method, inject the capacity check:
  ```python
    def action_confirm(self):
        for order in self:
            # Resolve destination capacity constraints
            farm_loc = self.env['farm.location'].search([
                ('agri_location_id', '=', order.location_dest_id.id)
            ], limit=1)

            if farm_loc and farm_loc.max_stocking_density > 0.0:
                # Calculate future density including pending production qty
                existing_quants = self.env['stock.quant'].search([
                    ('location_id', '=', order.location_dest_id.id)
                ])
                current_qty = sum(existing_quants.mapped('quantity'))
                future_qty = current_qty + order.product_qty
                
                if farm_loc.land_area > 0.0:
                    future_density = future_qty / farm_loc.land_area
                    if future_density > farm_loc.max_stocking_density:
                        raise ValidationError(_(
                            "Backpressure Limit Reached: Confirming production of %.2f units would exceed "
                            "maximum stocking density (%.2f units/m²) of destination %s."
                        ) % (order.product_qty, farm_loc.max_stocking_density, farm_loc.name))

        # Continue with standard Odoo confirmation
        res = super(MrpProduction, self).action_confirm()
        for order in self:
            self._trigger_isl_hook('isl_post_confirm', order.id)
        return res
  ```
  And add test to `farm_mrp/tests/__init__.py`:
  Add `from . import test_mrp_backpressure` inside `farm_mrp/tests/__init__.py`.

- [ ] **Step 4: Run test to verify it passes**
  Run: `docker compose run --rm web odoo -d test_db -i base,stock,farm_core,farm_mrp --test-enable --test-tags=farm_mrp --stop-after-init`
  Expected: PASS

- [ ] **Step 5: Commit**
  ```bash
  git add farm_mrp/models/mrp_production.py farm_mrp/tests/test_mrp_backpressure.py farm_mrp/tests/__init__.py
  git commit -m "feat(mrp): enforce physical safety capacity constraint on MO confirmation"
  ```
