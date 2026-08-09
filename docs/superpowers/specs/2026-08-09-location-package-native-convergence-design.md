# Location & Package Native Convergence Design Specification

> **Status:** APPROVED  
> **Architectural Paradigm:** 100% Odoo 19 Native Base Integration  
> **Date:** August 9, 2026  

---

## 1. Background & Structural Context

The Odoo Farm Workspace has evolved rapidly. While implementing advanced GxP safety gates, Jidoka interlocks, and volumetric backpressure controls, we identified a critical architectural redundancy in our underlying master data layers:
1. **Location Duplication:** Multiple overlapping models represent physical land parcels, CEA structures, and facility locations: `agri.location` (abstract domain container), `farm.location` (custom parcel and GIS database table), and `stock.location` (standard Odoo inventory table). This duplication causes data silos, prevents seamless standard stock transactions (since Odoo's stock moves exclusively reference `stock.location`), and complicates GIS coordinate synchronization.
2. **Packaging Overlap:** Standard logistics LPNs (`stock.package`) and custom packaging records (`farm.package`) competed for physical container representation. 

To address these redundancies and enforce maximum physical data consistency, we are executing **Schema Convergence (方案 A)**:
* We are retiring redundant database layers and merging all agricultural and geospatial properties directly into the native Odoo `stock.location` model.
* We are establishing a clean, orthogonal **Dual-Layer Packaging Separation**:
  * **Logistics Packaging Axis (`stock.package`)** represents dynamic warehouse shipping packages, pallets, and LPNs. GxP containers and reactors utilize `stock.matter.tracking` as an SFC-focused delegated extension of `stock.package`.
  * **Commercial Product Packaging Axis (`farm.package`)** represents static commercial product packing instances (bottles, cases, bags) created during processing, capturing irreversible fill quantities, specific lot genetics, and packing lineages.

---

## 2. Core Architecture

### 2.1 Part 1: Location Model Convergence (`stock.location` Direct Extension)

We are retiring the separate `farm.location` and `agri.location` models. All custom GIS, soil, terroir, vertical farming, and GxP volumetric limits are merged directly onto Odoo's standard `stock.location` model using single-table class inheritance (`_inherit = 'stock.location'`).

```
 [ Location Model Convergence Architecture ]

 +─────────────────────────────────────────────────────────────────────────────+
 |                              stock.location                                 |
 |  (Unified Database Table: stock_location)                                   |
 +─────────────────────────────────────────────────────────────────────────────+
 |  * NATIVE FIELDS:                                                           |
 |    - name, usage, parent_id, company_id                                     |
 |                                                                             |
 |  * AGRICULTURAL CORE:                                                       |
 |    - is_land_parcel (Boolean)                                               |
 |    - land_nature (Selection: basic_farmland, general_farmland, etc.)        |
 |    - land_area (Float), land_area_uom_id (Many2one)                         |
 |                                                                             |
 |  * GEOSPATIAL & GIS (Directly inherited from agri.geospatial.mixin):        |
 |    - gps_lat (Float), gps_lng (Float)                                       |
 |    - boundary_geojson (Text)                                                |
 |    - calculated_area_ha (Float)                                             |
 |                                                                             |
 |  * TERROIR PROFILE (US-062-01):                                             |
 |    - soil_type (Selection: clay, silt, sand, loam)                          |
 |    - slope (Float), aspect (Selection)                                      |
 |    - water_source (Selection)                                               |
 |                                                                             |
 |  * VERTICAL FARMING & STORAGE (US-063-01):                                  |
 |    - is_vertical_location (Boolean)                                         |
 |    - shelf_id (Char), shelf_level (Integer), shelf_slot (Char)              |
 |                                                                             |
 |  * VOLUMETRIC SAFETY & CAPACITY (US-082-05):                                |
 |    - max_capacity_volume_m3 (Float)                                         |
 |    - max_stocking_density (Float)                                           |
 +─────────────────────────────────────────────────────────────────────────────+
```

### 2.2 Part 2: Dual-Layer Packaging Axis

We separate logistics packaging from commercial packaging to prevent stock status discrepancies.

```
       [ 1. Dynamic Logistics Layer ]
       +───────────────────────────────────────────────────────────+
       |                      stock.package                        | <-- Logistics LPN
       |  - Represents standard pallets, bulk crates, bin boxes    |
       |  - Tracks temporary physical packages inside warehouse    |
       |  - Balances calculated dynamically via stock.quant        |
       +───────────────────────────────────────────────────────────+
                                     │
                                     │ [Contains / Transports]
                                     ▼
       [ 2. Static Commercial Packing & Pedigree Layer ]
       +───────────────────────────────────────────────────────────+
       |                      farm.package                         | <-- Commercial Product
       |  - Static commercial product packing instances            |
       |  - Permanent biological & processing pedigree tracking    |
       |  - Holds specific lot, product, and net fill weight       |
       +───────────────────────────────────────────────────────────+
```

#### 2.2.1 Logistics Package Layer (`stock.package` + GxP SFC Extensions)
* Standard logistics containers (crates, bins, carts) use the native `stock.package` LPN structure.
* GxP manufacturing reactors and vessels inherit `stock.package` via Odoo delegation (`_inherits = {'stock.package': 'package_id'}`) inside `stock.matter.tracking` to inject SFC phases, chemical/biological traits, and Jidoka locks without bloating standard inventory tables.
* Pieces, cartons, and pallets are defined using standard **`stock.package.type`** structures.

#### 2.2.2 Commercial Product Package Layer (`farm.package`)
* Dedicated to static commercial product nesting structures created at bottling/bagging/boxing lines.
* Captures net fill metrics, exact ingredient lot lineage, barcodes (serial QR codes for end-customers), and current warehouse location.

```python
class FarmPackageLevel(models.Model):
    _name = 'farm.package.level'
    _description = 'Commercial Product Package Level (e.g., Bottle, Box, Case)'

    name = fields.Char(string='Level Name', required=True, translate=True)
    code = fields.Char(string='Level Code', required=True) # BTL, CTN, CSE, PAL

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
```

---

## 3. Data Integrity & Sync Hooks

To prevent commercial packages (`farm.package`) from getting out of sync with actual physical logistics locations, we establish a **Location Synchronization Hook**:
* **Inventory Move Listener:** When a standard Odoo inventory move (`stock.move`) involving a commercial lot is validated, a listener checks for associated `farm.package` records.
* **Auto-alignment:** The listener automatically updates the `location_id` field on the corresponding `farm.package` instances to align with the move's `location_dest_id` (standard destination `stock.location`).

---

## 4. Verification & Validation Protocol

To prove that the converged database schema functions perfectly without regressions:
1. **Migration Integrity:** Ensure that the conversion of any existing test fixtures or models from `farm.location` and `agri.location` to `stock.location` preserves all GIS and terroir properties.
2. **Regression Assertions:** Execute the complete `farm_core`, `farm_mrp`, and `farm_operation` test suites to guarantee all 137+ test scenarios pass with the merged `stock.location` and converged packaging structures.
