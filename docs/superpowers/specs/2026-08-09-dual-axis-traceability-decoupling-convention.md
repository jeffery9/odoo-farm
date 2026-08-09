# Dual-Axis Traceability Decoupling Convention
**Version:** 1.0  
**Date:** 2026-08-09  
**Category:** Architectural Standards  
**Status:** Enforced  

---

## 1. Architectural Mandate

To prevent database locks, ensure transactional performance at scale, and support material fission (splitting) and consolidation (mixing), the agricultural traceability system is strictly decoupled into two separate,正交 (orthogonal) axes of traceability:

1.  **Static Genetic Axis (The Gene):** Managed strictly by `stock.lot`.
2.  **Dynamic Carrier Axis (The Carrier):** Managed strictly by `stock.matter.tracking`.

```
                    ┌──────────────────────────────┐
                    │     stock.lot (静态基因轴)   │
                    │  - 纯净 DNA (Genotype)        │
                    │  - 谱系树 (immutable Pedigree)│
                    │  - 认证状态、有机、活性成分    │
                    └──────────────┬───────────────┘
                                   │
                                   │ (动态绑定 via Odoo 19 stock.quant)
                                   ▼
                    ┌──────────────────────────────┐
                    │ stock.matter.tracking (载体)  │
                    │  - 物理实体 (Carrier / LPN)  │
                    │  - 动态重量、GPS、地理围栏    │
                    │  - 机械锁 (Jidoka Lock)       │
                    └──────────────────────────────┘
```

---

## 2. Axis Classification & Responsibility Matrix

### 2.1 Static Genetic Axis (`stock.lot` - DNA)
The Lot represents the **immutable genetic identity** and immutable heritage of the agricultural substance.
*   **Permitted Fields:**
    *   Genetic variety and breed info (`variety_id`).
    *   Immutable certifications (e.g. `is_organic`, certification grades).
    *   Potency levels and static attributes (`is_gmo`, `active_content`).
    *   Pedigree ancestry and sibling lists (`parent_lot_ids`, `child_lot_ids`).
*   **Prohibited Fields & Behaviors:**
    *   NO physical weight storage (e.g. `current_weight`).
    *   NO physical location or GPS storage (e.g. `last_gps_lat`, `last_gps_lng`).
    *   NO physical lifecycle/maturity stage tracking (e.g. `life_stage`).
    *   Direct physical property modifications are strictly **blocked** with a transaction-rolling `UserError` (Write-Block mechanism).

### 2.2 Dynamic Carrier Axis (`stock.matter.tracking` - Carrier)
The Matter Tracking entity represents the **physical carrier vessel (LPN, Silo, Tank, Lot-Package)**.
*   **Permitted Fields:**
    *   Physical active weights (`current_weight`).
    *   Vessel phase & lifecycle states (`life_stage`, `vessel_phase`, `current_phase_id`).
    *   Spatial positioning coordinates (`last_gps_lat`, `last_gps_lng`, `last_location_update`).
    *   Sustainability mixins (e.g. `carbon_footprint`).
    *   Dynamic calculations (e.g. geofence ray-casting polygon checks).
    *   Safety interlocks (`is_vessel_locked`).
*   **Prohibited Fields & Behaviors:**
    *   NO primary gene/pedigree tree declarations.
    *   NO static quality grading settings (grades must be inherited dynamically from contained lots).

---

## 3. The Downward Compatibility Bridge

To maintain backwards compatibility with third-party apps, reports, and standard Odoo views, the purified `stock.lot` implements read-only computed properties that dynamically reflect states from the active tracking containers:

### 3.1 Dynamic Resolution via Quants
Physical properties on `stock.lot` are computed on-the-fly by querying standard Odoo quants residing in active packaging:
```python
@api.depends('quant_ids.package_id')
def _compute_matter_physical_properties(self):
    for lot in self:
        quants = lot.quant_ids.filtered(lambda q: q.package_id and getattr(q.package_id, 'is_matter_tracking', False))
        if quants:
            package = quants[0].package_id
            lot.current_weight = getattr(package, 'current_weight', 0.0)
            lot.last_gps_lat = getattr(package, 'last_gps_lat', 0.0)
            lot.last_gps_lng = getattr(package, 'last_gps_lng', 0.0)
            lot.life_stage = getattr(package, 'life_stage', 'juvenile')
```

### 3.2 Legacy Write-Block Mechanism
Writing directly to physical properties of `stock.lot` is intercepted and rolled back to enforce physical carrier integrity:
```python
def _inverse_current_weight(self):
    raise UserError(_(
        "Legacy Write Block: Weight is now managed dynamically by Matter Tracking (LPN/Vessel). "
        "Please update the weight on the active Matter Tracking container directly."
    ))
```

---

## 4. Development & Extension Checklist
When extending the traceability system in vertical industry modules (e.g. Livestock, Orchard, Winery):
1.  **Never** add dynamic physical storage fields directly to `stock.lot`.
2.  All location and GPS properties **must** inherit from `agri.geospatial.mixin` or `agri.sustainability.mixin` on `stock.matter.tracking`.
3.  Ensure all write tests for physical properties target `stock.matter.tracking` instead of `stock.lot`.
