# Dual-Axis Traceability Decoupling Specification (Phase 1 & 2)
**Version:** 1.0  
**Date:** 2026-08-09  
**Status:** Approved  
**Subsystem:** Stock / Manufacturing / Industry Specialized Layer (ISL)

---

## 1. Introduction & Objectives

This specification details the structural and programmatic decoupling of the **static genetic pedigree axis** from the **dynamic physical carrier axis**. 

In historical implementations, `stock.lot` was overloaded with physical state attributes (such as dynamic weights, GPS coordinates, packaging status, and dynamic lifecycle stages). Under high-concurrency operations, high-frequency physical state mutations caused massive record locking on `stock.lot`, and made it impossible to split a single genetic batch across multiple vessels or package carriers while tracking distinct dynamic weights or coordinates.

### Objectives of Phase 1 & 2 Decoupling:
1. **Physical Property Migration:** Move all dynamic physical attributes (`current_weight`, `life_stage`, `last_gps_lat`, `last_gps_lng`, GPS-to-location plot ray-casting logic) to `stock.matter.tracking`.
2. **Genetic Purification:** Refactor `stock.lot` to focus purely on static genetics, certifications, and ancestral pedigrees.
3. **Downward Compatibility Bridge:** Implement compute/inverse properties and write-locks on `stock.lot` to guarantee zero breakage for legacy third-party views, reports, and API integrations.

---

## 2. Structural Coupling Architecture

The diagram below shows how the two axes bind transparently through Odoo's native `stock.quant` and `stock.package` mechanisms:

```
+─────────────────────────────────────────────────────────────────────────────+
|                         DUAL-AXIS STRUCTURAL BOUNDARY                       |
+─────────────────────────────────────────────────────────────────────────────+
|                                                                             |
|      [ LOT AXIS (Static / DNA) ]                                            |
|          - stock.lot                                                        |
|          - variety_id, is_organic, active_content, pedigree tree            |
|                                                                             |
|                               ▲                                             |
|                               │ (Linked via stock.quant / packaging)        |
|                               ▼                                             |
|                                                                             |
|      [ MATTER TRACKING AXIS (Dynamic / Physical Carrier) ]                  |
|          - stock.matter.tracking (extends stock.package)                    |
|          - current_weight, life_stage, GPS positioning, Ray-Casting         |
|                                                                             |
+─────────────────────────────────────────────────────────────────────────────+
```

---

## 3. Detailed Schema Mapping & Attributes Migration

### 3.1 Migrated Fields & Methods

| Attribute / Method | Source Model (`stock.lot`) | Destination Model (`stock.matter.tracking`) | Data Type / Definition |
|:---|:---|:---|:---|
| `current_weight` | Overloaded (Dynamic) | Active Physical Weight | `Float` (Digits: 'Stock Weight') |
| `life_stage` | Overloaded (Dynamic) | Active Maturity Stage | `Selection` (juvenile, growing, mature, harvested) |
| `last_gps_lat` | Overloaded (Spatial) | Current Vessel Latitude | `Float` (Digits: (10, 7)) |
| `last_gps_lng` | Overloaded (Spatial) | Current Vessel Longitude | `Float` (Digits: (10, 7)) |
| `last_location_update`| Overloaded (Spatial) | Latitude Sync Timestamp | `Datetime` |
| `_is_point_in_plot` | Geofence Check | Geofence Area Calculator| Method (Ray-casting Containment Algorithm) |
| `action_update_location_by_gps` | Geographic Sync | Vessel-to-Plot Matcher | Method (Dynamic Parcel Matching) |

### 3.2 Purified `stock.lot` (Static Attributes Only)
* `variety_id` (`Many2one` targeting `agri.industry.variety`): Static genetic code.
* `is_organic` (`Boolean`): Inherent agricultural crop or soil certification status.
* `is_gmo` (`Boolean`): Inherent genetic classification.
* `active_content` (`Float`): Inherent genetic sweetness, starch, or potency ratio.
* `parent_lot_ids` (`Many2many` to `stock.lot`): Immutable pedigree ancestry.

---

## 4. Phase 1 & 2 Execution Implementation Details

### 4.1 Phase 1: Physical Model Enrichment (`stock.matter.tracking`)
Implement migrated spatial, weight, and lifecycle properties directly inside `stock.matter.tracking` base model:

```python
class StockMatterTracking(models.Model):
    _inherit = 'stock.matter.tracking'

    current_weight = fields.Float(
        string="Current Weight (kg)",
        digits='Stock Weight',
        tracking=True,
        help="The active weight of material in this container/LPN."
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
```

### 4.2 Phase 2: Downward Compatibility Bridge (`stock.lot` Wrappers)
To support existing legacy modules and print reports that read weights or coordinates directly from `stock.lot`, the fields on `stock.lot` will be converted to stored or unstored computed fields linking back to the associated `stock.matter.tracking` (via active quants):

```python
class StockLot(models.Model):
    _inherit = 'stock.lot'

    # Compute Weight from Quants in active Matter Tracking packages
    current_weight = fields.Float(
        string="Current Weight (kg)",
        compute='_compute_physical_properties',
        inverse='_inverse_current_weight',
        store=False,
        help="Compatibility Bridge: Computes weight from active matter tracking containers."
    )

    last_gps_lat = fields.Float(
        string="Last Latitude",
        compute='_compute_physical_properties',
        inverse='_inverse_gps_coordinates',
        store=False
    )

    last_gps_lng = fields.Float(
        string="Last Longitude",
        compute='_compute_physical_properties',
        inverse='_inverse_gps_coordinates',
        store=False
    )

    @api.depends('quant_ids.package_id')
    def _compute_physical_properties(self):
        for lot in self:
            # Find the active package that implements matter tracking
            quants = lot.quant_ids.filtered(lambda q: q.package_id and q.package_id.is_matter_tracking)
            if quants:
                # Resolve attributes from the active tracking container
                package = quants[0].package_id
                lot.current_weight = getattr(package, 'current_weight', 0.0)
                lot.last_gps_lat = getattr(package, 'last_gps_lat', 0.0)
                lot.last_gps_lng = getattr(package, 'last_gps_lng', 0.0)
            else:
                lot.current_weight = 0.0
                lot.last_gps_lat = 0.0
                lot.last_gps_lng = 0.0

    # Prevent direct legacy write operations on physical properties
    def _inverse_current_weight(self):
        raise UserError(_(
            "Legacy Write Block: Weight is now managed dynamically by Matter Tracking (LPN/Vessel). "
            "Please update the weight on the active Matter Tracking container directly."
        ))

    def _inverse_gps_coordinates(self):
        raise UserError(_(
            "Legacy Write Block: GPS positioning is now managed dynamically by Matter Tracking (LPN/Vessel). "
            "Please sync coordinates via the active Matter Tracking container."
        ))
```

---

## 5. Verification & Acceptance Gherkin Contract

```gherkin
Feature: Dual-Axis Traceability Decoupling & Compatibility Bridge

  Scenario: Legacy write block prevents modification of physical properties on Lot
    Given a purified stock lot "LOT-GEN-001" with no direct physical state attributes
    And an active Matter Tracking container "MAT-CONT-01" containing "LOT-GEN-001" with weight 150.0 kg
    When the system reads "LOT-GEN-001"'s current_weight
    Then the compatibility bridge should return 150.0 kg
    And when a legacy API attempts to write current_weight as 200.0 kg on "LOT-GEN-001"
    Then the transaction should rollback with a UserError warning explaining that physical state is managed by the Matter container
```

---

## 6. Implementation Checklist & Phase Gate

- [ ] **Task 1: Schema Ingestion on Matter Tracking**
  - Add `current_weight`, `life_stage`, `last_gps_lat`, `last_gps_lng`, `last_location_update` to `stock.matter.tracking` model in `farm_core`.
  - Migrate ray-casting containment helper methods to `stock.matter.tracking`.
- [ ] **Task 2: UI Expansion for Physical Carrier Cockpit**
  - Enrich Matter Tracking views in `farm_core` to display migrated positioning and physical properties.
- [ ] **Task 3: Refactor & Clean `stock.lot` (Pure Genetics)**
  - Transition Lot fields in `farm_processing` and `farm_livestock` to computed properties.
  - Implement Write-Block warnings (`_inverse_current_weight`, `_inverse_gps_coordinates`) with explicit GxP instructions.
- [ ] **Task 4: Run Targeted Regression Validation Suite**
  - Verify zero-breakage on existing tests in `farm_core` and `farm_mrp` by executing clean database initializations.
