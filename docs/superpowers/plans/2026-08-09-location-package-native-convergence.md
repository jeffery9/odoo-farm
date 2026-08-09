# Location & Package Native Convergence Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Clean up master data layers by converging overlapping agricultural locations directly into standard Odoo `stock.location` records and segregating dynamic logistics containers from static commercial packaging.

**Architecture:** Extend standard Odoo `stock.location` using class inheritance (`_inherit = 'stock.location'`) with GIS, terroir, and safety limits. Retain `farm.package` as an independent static, serialized commercial packaging registry with location synchronization hooks linked to standard move validations.

**Tech Stack:** Odoo 19 CE, Python 3.12, PostgreSQL.

## Global Constraints
* **Odoo 19 Compliance:** Extend native models using class inheritance (`_inherit`) without duplicate table structures.
* **Dual-Layer Segregation:** Dynamic logistics are handled exclusively by `stock.package` and standard `stock.quant` balances. Commercial structures use `farm.package`.
* **Zero Suppressions:** Never suppress warnings or bypass registry assertions.

---

### Task 1: Direct Agricultural Extension of `stock.location`

**Files:**
- Modify: `farm_core/models/land_location.py`
- Modify: `farm_core/models/__init__.py`
- Test: `farm_core/tests/test_converged_location.py`

**Interfaces:**
- Consumes: Native `stock.location` model.
- Produces: Merged agricultural, GIS, terroir, and capacity fields directly on the native Odoo `stock.location` record.

- [ ] **Step 1: Write the failing test**

Write `/Users/jeffery/odoo-farm-workspace/odoo-farm-dev/farm_core/tests/test_converged_location.py`:
```python
# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestConvergedLocation(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(TestConvergedLocation, cls).setUpClass()
        cls.Location = cls.env['stock.location']

    def test_agricultural_and_gis_fields_exist_on_native_location(self):
        """ Verify that standard Odoo stock.location records support GIS and agricultural fields directly """
        loc = self.Location.create({
            'name': 'Test Converged Plot',
            'is_land_parcel': True,
            'land_nature': 'basic_farmland',
            'gps_lat': 31.2304,
            'gps_lng': 121.4737,
            'max_capacity_volume_m3': 500.0,
            'max_stocking_density': 12.5
        })
        self.assertTrue(loc.is_land_parcel)
        self.assertEqual(loc.land_nature, 'basic_farmland')
        self.assertEqual(loc.gps_lat, 31.2304)
        self.assertEqual(loc.gps_lng, 121.4737)
        self.assertEqual(loc.max_capacity_volume_m3, 500.0)
        self.assertEqual(loc.max_stocking_density, 12.5)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `docker compose run --rm web odoo -d test_clean_db -i farm_core --test-enable --test-tags=TestConvergedLocation --stop-after-init --log-level=warn`
Expected: FAIL with `AttributeError` on missing attributes on `stock.location`.

- [ ] **Step 3: Write minimal implementation**

Modify `/Users/jeffery/odoo-farm-workspace/odoo-farm-dev/farm_core/models/land_location.py` to extend `stock.location` directly, merging GIS, terroir, and safety limits:
```python
# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class StockLocation(models.Model):
    """
    Direct Agricultural, GIS, and GxP Capacity extension of the native Odoo stock.location model.
    Enforces 'Location Scheme A' Convergence.
    """
    _inherit = 'stock.location'

    # --- Agricultural Identification ---
    is_land_parcel = fields.Boolean("Is Land Parcel", default=False, tracking=True)
    land_nature = fields.Selection([
        ('basic_farmland', 'Permanent Basic Farmland (永久基本农田)'),
        ('general_farmland', 'General Farmland (一般耕地)'),
        ('garden_land', 'Garden Land (园地)'),
        ('forest_land', 'Forest Land (林地)'),
        ('other_agri_land', 'Other Agricultural Land (其他农用地)'),
        ('construction_land', 'Construction Land (建设用地)'),
    ], string="Land Nature")

    land_area = fields.Float("Area (sqm/mu)", digits=(16, 2))
    land_area_uom_id = fields.Many2one('uom.uom', string="Area Unit")

    # --- Core GIS Fields ---
    gps_lat = fields.Float("Latitude", digits=(10, 7), tracking=True)
    gps_lng = fields.Float("Longitude", digits=(10, 7), tracking=True)
    boundary_geojson = fields.Text("Boundary Coordinates (GeoJSON)")
    calculated_area_ha = fields.Float("Calculated Area (Ha)", digits=(16, 4), readonly=True)

    # --- Terroir Profiling ---
    soil_type = fields.Selection([
        ('clay', 'Clay'),
        ('silt', 'Silt'),
        ('sand', 'Sand'),
        ('loam', 'Loam'),
    ], string="Soil Type")
    slope = fields.Float("Slope Gradient (%)")
    aspect = fields.Selection([
        ('n', 'North'), ('ne', 'North-East'), ('e', 'East'), ('se', 'South-East'),
        ('s', 'South'), ('sw', 'South-West'), ('w', 'West'), ('nw', 'North-West')
    ], string="Aspect / Orientation")
    water_source = fields.Selection([
        ('river', 'River/Stream'),
        ('well', 'Groundwater Well'),
        ('reservoir', 'Reservoir'),
        ('rain', 'Rain-fed')
    ], string="Primary Water Source")

    # --- Vertical Farming & CEA ---
    is_vertical_location = fields.Boolean("Is Vertical / Shelf", default=False)
    shelf_id = fields.Char("Shelf ID")
    shelf_level = fields.Integer("Level / Row")
    shelf_slot = fields.Char("Slot / Position")

    # --- Physical Capacity and Stocking Density Limits ---
    max_capacity_volume_m3 = fields.Float(string='Max Capacity Volume (m³)', default=0.0)
    max_stocking_density = fields.Float(string='Max Stocking Density (units/m²)', default=0.0)
```

Also, maintain `farm.location` as a lightweight compatibility alias pointing to `stock.location` to prevent compilation errors across downstream modules:
```python
class FarmLocation(models.Model):
    """ Lightweight backward compatibility wrapper model for farm.location """
    _name = 'farm.location'
    _description = 'Farm Location Compatibility Wrapper'
    _inherit = 'stock.location'
```

Ensure `test_converged_location.py` is registered in `farm_core/tests/__init__.py`:
```python
from . import test_converged_location
```

- [ ] **Step 4: Run test to verify it passes**

Run: `docker compose run --rm web odoo -d test_clean_db -i farm_core --test-enable --test-tags=TestConvergedLocation --stop-after-init --log-level=warn`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add farm_core/models/land_location.py farm_core/tests/test_converged_location.py farm_core/tests/__init__.py
git commit -m "feat(core): converge agricultural locations directly into stock.location [US-082-06]"
```

---

### Task 2: Refactor `farm.package` as a Static Commercial Packaging Registry

**Files:**
- Modify: `farm_processing/models/package_management.py`
- Test: `farm_processing/tests/test_commercial_packaging.py`
- Create: `farm_processing/tests/__init__.py` (if missing)

**Interfaces:**
- Consumes: Native `stock.location` model.
- Produces: `farm.package` model strictly tracking commercial filling data, specific lots, serial QR barcodes, and current location.

- [ ] **Step 1: Write the failing test**

Write `/Users/jeffery/odoo-farm-workspace/odoo-farm-dev/farm_processing/tests/test_commercial_packaging.py`:
```python
# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestCommercialPackaging(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(TestCommercialPackaging, cls).setUpClass()
        cls.Product = cls.env['product.product']
        cls.Lot = cls.env['stock.lot']
        cls.Location = cls.env['stock.location']
        cls.PackageLevel = cls.env['farm.package.level']
        cls.Package = cls.env['farm.package']

        cls.product_wine = cls.Product.create({
            'name': 'Reserve Cabernet',
            'type': 'consu',
            'is_storable': True
        })

        cls.lot_wine = cls.Lot.create({
            'name': 'LOT-CABERNET-01',
            'product_id': cls.product_wine.id
        })

        cls.bottle_level = cls.PackageLevel.create({
            'name': 'Single Bottle (750ml)',
            'code': 'BTL'
        })

        cls.cellar_location = cls.Location.create({
            'name': 'Aging Cellar A',
            'usage': 'internal'
        })

    def test_commercial_packaging_creation_and_nesting(self):
        """ Verify that commercial packages hold static fill quant, lot genetics, and parent case links """
        bottle = self.Package.create({
            'package_level_id': self.bottle_level.id,
            'product_id': self.product_wine.id,
            'lot_id': self.lot_wine.id,
            'quantity': 0.75,
            'barcode': 'QR-CAB-BTL-999',
            'location_id': self.cellar_location.id
        })

        self.assertEqual(bottle.product_id, self.product_wine)
        self.assertEqual(bottle.lot_id, self.lot_wine)
        self.assertEqual(bottle.quantity, 0.75)
        self.assertEqual(bottle.barcode, 'QR-CAB-BTL-999')
        self.assertEqual(bottle.location_id, self.cellar_location)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `docker compose run --rm web odoo -d test_clean_db -i farm_processing --test-enable --test-tags=TestCommercialPackaging --stop-after-init --log-level=warn`
Expected: FAIL due to missing fields or model compilation.

- [ ] **Step 3: Write minimal implementation**

Modify `/Users/jeffery/odoo-farm-workspace/odoo-farm-dev/farm_processing/models/package_management.py` to match the exact approved `farm.package` schema:
```python
# -*- coding: utf-8 -*-
from odoo import fields, models, api, _

class FarmPackageLevel(models.Model):
    _name = 'farm.package.level'
    _description = 'Commercial Product Package Level (e.g., Bottle, Box, Case)'

    name = fields.Char(string='Level Name', required=True, translate=True)
    code = fields.Char(string='Level Code', required=True) # e.g., BTL, CTN, CSE

class FarmPackage(models.Model):
    _name = 'farm.package'
    _description = 'Commercial Product Packaging Traceability'

    name = fields.Char(string='Unique Package Reference', default=lambda self: _('New'))
    package_level_id = fields.Many2one('farm.package.level', string='Package Level', required=True)
    
    # Static Commercial DNA
    product_id = fields.Many2one('product.product', string='Commercial Product', required=True)
    lot_id = fields.Many2one('stock.lot', string='Contained Lot/Serial', required=True)
    quantity = fields.Float(string='Net Fill Quantity', required=True)
    
    # Lineage / Packing nesting (Static)
    parent_package_id = fields.Many2one('farm.package', string='Parent Case')
    child_package_ids = fields.One2many('farm.package', 'parent_package_id', string='Contained Packages')

    # Logistics Synchronization
    barcode = fields.Char(string='Unique QR/Barcode', help="Unique QR serial number for anti-counterfeiting.")
    location_id = fields.Many2one('stock.location', string='Physical Current Location')

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('farm.package') or _('New')
        return super().create(vals)
```

Ensure tests are imported in `farm_processing/tests/__init__.py`:
```python
from . import test_commercial_packaging
```

- [ ] **Step 4: Run test to verify it passes**

Run: `docker compose run --rm web odoo -d test_clean_db -i farm_processing --test-enable --test-tags=TestCommercialPackaging --stop-after-init --log-level=warn`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add farm_processing/models/package_management.py farm_processing/tests/test_commercial_packaging.py farm_processing/tests/__init__.py
git commit -m "feat(processing): establish static commercial package registry with clean packaging hierarchy [US-082-06]"
```

---

### Task 3: Establish Location-Sync Hooks on Inventory Moves

**Files:**
- Modify: `farm_processing/models/package_management.py`
- Test: `farm_processing/tests/test_commercial_packaging.py`

**Interfaces:**
- Consumes: Odoo `stock.move` and `stock.picking` validations.
- Produces: Automated location alignment hook synchronizing the static `farm.package` instances' `location_id` fields to target `stock.location` upon inventory movement.

- [ ] **Step 1: Write the failing test**

Add `test_commercial_package_location_synchronization` to `/Users/jeffery/odoo-farm-workspace/odoo-farm-dev/farm_processing/tests/test_commercial_packaging.py`:
```python
    def test_commercial_package_location_synchronization(self):
        """ Verify that validating a stock move for a commercial lot automatically aligns associated farm.package coordinates """
        # Setup location destination
        shipping_dock = self.Location.create({
            'name': 'Shipping Dock Block B',
            'usage': 'internal'
        })

        # Create commercial package in cellar
        bottle = self.Package.create({
            'package_level_id': self.bottle_level.id,
            'product_id': self.product_wine.id,
            'lot_id': self.lot_wine.id,
            'quantity': 0.75,
            'barcode': 'QR-CAB-BTL-100',
            'location_id': self.cellar_location.id
        })

        # Simulate a stock move validation for this lot
        move = self.env['stock.move'].create({
            'name': 'Transfer Cabernet Bottles',
            'product_id': self.product_wine.id,
            'product_uom': self.product_wine.uom_id.id,
            'product_uom_qty': 1.0,
            'location_id': self.cellar_location.id,
            'location_dest_id': shipping_dock.id,
        })
        move._action_confirm()
        move._action_assign()
        
        # Write move line with exact lot
        move_line = move.move_line_ids[0]
        move_line.lot_id = self.lot_wine.id
        move_line.qty_done = 1.0
        
        # Execute standard Odoo move validation
        move._action_done()

        # Check that the location of the bottle has been auto-aligned
        self.assertEqual(bottle.location_id, shipping_dock, "Commercial package location must auto-align with move destination.")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `docker compose run --rm web odoo -d test_clean_db -i farm_processing --test-enable --test-tags=TestCommercialPackaging --stop-after-init --log-level=warn`
Expected: FAIL (bottle location remains in aging cellar instead of aligning to shipping dock).

- [ ] **Step 3: Write minimal implementation**

Surgically append the `stock.move` write override hook to `/Users/jeffery/odoo-farm-workspace/odoo-farm-dev/farm_processing/models/package_management.py` to catch validated lot lines and align corresponding `farm.package` records:
```python
class StockMove(models.Model):
    _inherit = 'stock.move'

    def _action_done(self, cancel_backorder=False):
        res = super(StockMove, self)._action_done(cancel_backorder=cancel_backorder)
        
        # Location synchronization hook for commercial packages
        for move in self:
            if move.state == 'done':
                for line in move.move_line_ids:
                    if line.lot_id:
                        # Find all static commercial packages associated with this lot
                        packages = self.env['farm.package'].search([
                            ('lot_id', '=', line.lot_id.id),
                            ('product_id', '=', line.product_id.id)
                        ])
                        if packages:
                            # Align package coordinates with inventory destination
                            packages.write({
                                'location_id': move.location_dest_id.id
                            })
        return res
```

- [ ] **Step 4: Run test to verify it passes**

Run: `docker compose run --rm web odoo -d test_clean_db -i farm_processing --test-enable --test-tags=TestCommercialPackaging --stop-after-init --log-level=warn`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add farm_processing/models/package_management.py farm_processing/tests/test_commercial_packaging.py
git commit -m "feat(processing): implement location synchronization hooks on stock.move validation [US-082-06]"
```
