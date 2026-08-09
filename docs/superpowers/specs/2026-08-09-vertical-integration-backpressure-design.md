# Specs: Biological Asset Vertical Integration & Downstream WIP Backpressure Control
**Version:** 1.0  
**Date:** 2026-08-09  
**Status:** Approved  
**Subsystems:** Stock / Core / Manufacturing / Industry Specialized Layer (ISL)

---

## 1. Executive Summary

This specification outlines the technical design for:
1.  **Vertical Integration:** Linking the decoupled **Static Genetic Axis** (`stock.lot` / DNA) and **Dynamic Carrier Axis** (`stock.matter.tracking`) to the high-level biological asset entity (`agri.biological.asset`).
2.  **Downstream WIP Backpressure Control:** Restricting the confirmation of manufacturing operations (Missions, Recipes) and physical inventory transfers when downstream storage containers (silos, pens, holding tanks) reach volumetric or stocking density capacity.

---

## 2. Part A: Biological Asset Vertical Integration

We implement a hybrid architecture that guarantees real-time computational truth while maintaining a durable, query-optimized historical event ledger.

```
                  [ stock.matter.tracking (Physical Carrier) ]
                             │
            ┌────────────────┴────────────────┐
            ▼ (Implicit Read-only Reflection)  ▼ (Write Sync Hook)
    [ agri.biological.asset ]            [ farm.livestock.event ]
     - current_weight (computed)          - event_type = 'weight'
     - life_stage (computed)              - event_date = datetime.now()
     - last_gps_lat/lng (computed)        - notes = 'Sync'
```

### 2.1 Schema Mapping Extensions

#### `agri.biological.asset`
*   `tracking_carrier_ids` (`One2many` to `stock.matter.tracking` matching on `biological_asset_id`): Locates active physical containers.
*   `current_weight` (`Float`, Computed): Read-only, dynamically pulls weight from the primary active tracking carrier.
*   `life_stage` (`Selection`, Computed): Read-only, pulls active growth stage from the primary active tracking carrier.
*   `last_gps_lat` / `last_gps_lng` (`Float`, Computed): Read-only spatial position pulled from active carriers.

#### `stock.matter.tracking`
*   `biological_asset_id` (`Many2one` targeting `agri.biological.asset`): Establishes active physical tracking link.
*   A write hook is established on physical state changes (weight, GPS, life stage). When these values are written to `stock.matter.tracking`, the write hook automatically writes to `farm.livestock.event` to record the physical measurement event.

---

## 3. Part B: Downstream WIP Backpressure Control

To enforce industrial safety limits and prevent biological or raw-material downstream overflow, we implement a **Physical Capacity Interlock** on physical locations (`farm.location`) and vessels (`stock.matter.tracking`).

### 3.1 Mathematical Constraint Model

For any target destination (either a `farm.location` or a container `stock.matter.tracking`), the backpressure safety margin is evaluated as:

$$\text{Pending Volume} + \text{Active Volume} \le \text{Max Volumetric Capacity}$$

Where:
*   $$\text{Active Volume}$$ is calculated dynamically by summing the volumes or counting the biological entities currently situated in the target location/vessel.
*   $$\text{Pending Volume}$$ represents the scheduled incoming production or transfer quantity.

If the constraint is violated, the system blocks operation confirmation with a transactional rollback and a `ValidationError`.

### 3.2 Schema Extensions

#### `farm.location` (Silos / Pens / Parcels)
*   `max_capacity_volume_m3` (`Float`): Maximum volume limit.
*   `max_stocking_density` (`Float`): Maximum animals or plant units per square meter.

#### `stock.matter.tracking` (Vessels / Tanks)
*   `max_capacity_volume_m3` (`Float`): Volumetric limit.

### 3.3 The Visual Management Widget (3-Second Rule)
An adaptive visual banner is displayed on the location and carrier views, indicating queue saturation:
*   **Green (< 80% Capacity):** Safe status.
*   **Yellow (80% - 100% Capacity):** Approaching limit.
*   **Red (> 100% Capacity):** Over-saturated / Backpressure Triggered.

---

## 4. Verification & Acceptance Gherkin Contract

```gherkin
Feature: Vertical Integration & WIP Backpressure Control

  Scenario: Physical properties reflect on Biological Asset dynamically
    Given an agri.biological.asset "COW-GROUP-45"
    And an active stock.matter.tracking "VESSEL-04" linked to "COW-GROUP-45"
    When the weight on "VESSEL-04" is updated to 620.0 kg
    Then the computed field current_weight on "COW-GROUP-45" should return 620.0 kg
    And a farm.livestock.event of type 'weight' should be recorded in the ledger

  Scenario: Manufacturing order fails when downstream destination is over-capacity
    Given a farm.location "Holding Pen B" with max_stocking_density 2.0 per m2 and area 100 m2 (Max count = 200)
    And "Holding Pen B" currently contains 190 active animals
    When an operator attempts to confirm a manufacturing order for 20 additional animals destined for "Holding Pen B"
    Then the system should trigger a ValidationError "Backpressure Limit Reached: Holding Pen B would exceed stocking density limits"
```
