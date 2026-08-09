# Design Specification: SFC to Matter-Tracking Architectural Mapping & Traceability Algorithms

This document defines the semantic conversion of the SFC (Shop Floor Container) model into the `farm` Matter-Tracking system. It describes the runtime tracking pipeline, DNA pedigree decay propagation, spatial ray-casting routing, and zero-latency snapshot ledgers.

---

## 1. Structural Model Conversion Directory

The agricultural ERP transitions from rigid industrial work-order flows to a material-centric, dynamic-carrier paradigm.

```
+-----------------------------------------------------------------------+
|                       STATIC BLUEPRINT SPACE (M1)                     |
|                                                                       |
|  [ agri.bom.mixin ]                      [ agri.intervention.mixin ]  |
|  Defines static Recipes                  Defines static Mission       |
|  and ingredient formulas                 procedure & safety criteria  |
+-----------------------------------┬────────────────────────────────---+
                                    │
                                    ▼ (Instantiation)
+-----------------------------------------------------------------------+
|                       PHYSICAL RUNTIME COCKPIT (M2)                    |
|                                                                       |
|  [ stock.matter.tracking ]               [ stock.location ]           |
|  Inherits stock.package (LPN)            Extended native warehouse    |
|  Tracks current_weight, life_stage       with gps_lat, gps_lng, area  |
+-----------------------------------┬────────────────────────────────---+
                                    │
                                    ▼ (Execution & Verification)
+-----------------------------------------------------------------------+
|                    ZERO-LATENCY FORENSIC SNAPSHOTS                    |
|                                                                       |
|  [ stock.matter.tracking.snapshot ]                                   |
|  Atomic digital twin ledger. Captures timestamp, spatial location,   |
|  lot mixing ratio, and GxP compliance boundaries upon state change.   |
+-----------------------------------------------------------------------+
```

### Mapping Matrix
*   **Shop Floor Container (SFC)** -> `stock.matter.tracking`
    *   *Specification:* Inherits standard Odoo `stock.package` via delegation. Represents the physical container/carrier and coordinates logistics and material mutations.
*   **M1 Templates (Workflow / Node / Edge)** -> `agri.bom.mixin` & `agri.intervention.mixin`
    *   *Specification:* Custom abstract templates defining static campaign routes, processing recipes, and step connections.
*   **M2 Execution (Workflow Node Runtime)** -> `agri.intervention`
    *   *Specification:* Runtime instances representing physical operations (Missions) mapped to active carriers.
*   **SFC Snapshot System** -> `stock.matter.tracking.snapshot`
    *   *Specification:* Independent database journal logging high-fidelity digital twin snapshots at each transactional boundary.

---

## 2. Genealogy & Tracking Algorithms

The material tracking system enforces genetic preservation and measures DNA degeneration during material mixing (consolidation) and cutting/slaughtering (fission).

```
                      GENEALOGICAL PURITY & LINEAGE TREE
                      
      [ Ancestral Lot A ]                      [ Ancestral Lot B ]
      (DNA Purity: 100.0)                      (DNA Purity: 90.0)
         (Quantity: 200)                          (Quantity: 100)
                │                                        │
                └───────────────┬────────────────────────┘
                                │
                                ▼ (Consolidation Merge)
                    [ stock.matter.tracking ]
                    - Total Weight: 300.0 kg
                    - Calculated DNA Purity: 87.0
                      (Includes 10% Mixing Penalty)
                                │
                ┌───────────────┴───────────────┐
                ▼ (Fission Split offspring 1)   ▼ (Fission Split offspring 2)
       [ offspring Tracking ]          [ offspring Tracking ]
       - Weight: 150.0 kg              - Weight: 150.0 kg
       - DNA Purity: 82.65             - DNA Purity: 82.65
         (5% Fission Penalty Applied)    (5% Fission Penalty Applied)
```

### 2.1 Consolidation DNA Mixing & Decay Algorithm
When multiple material lots are consolidated into a single container tracking record, the cumulative DNA integrity score decays due to mixing entropy.

```
Consolidation Mixing Entropy Formula:

                      ( SUM( Q_i * DNA_i ) )
  [ Consolidated DNA ] = ────────────────────── * 0.90
                            (  SUM( Q_i )  )
  
  Where:
    - Q_i   : Quantity of Quant_i in the container.
    - DNA_i : DNA integrity score of the associated Lot_i.
    - 0.90  : 10% mixing entropy penalty representing loss of lineage purity.
```

### 2.2 Fission Mass & Pedigree Preservation Algorithm
When a parent container is divided (e.g., slaughtering or carcass splitting), mass conservation is preserved, and a 5% fission pedigree decay penalty is applied to offspring lineages.

```
Fission Pedigree Decay Formula:

  [ offspring DNA ] = [ Parent DNA ] * 0.95
  
  Where:
    - 0.95  : 5% biological fission penalty representing lineage fragmentation.
    
Mass Balance Constraint:

  [ Parent Weight ] = SUM( [ offspring_i Weight ] )
```

---

## 3. Dynamic Terrain & Spatial Routing Algorithms

The system automatically manages location synchronization and checks terroir containment using GIS coordinates.

```
                        TERROIR GEOFENCING CONTAINMENT
                        
   (GPS: 11.0, 31.0)                      (GPS: 13.0, 35.0)
   Land Parcel Vertex 1 ─────────────────── Land Parcel Vertex 2
            │                                       │
            │          * (Inside)                   │
            │          Carrier (GPS: 12.0, 34.0)    │
            │                                       │
   Land Parcel Vertex 4 ─────────────────── Land Parcel Vertex 3
   (GPS: 11.0, 35.0)                      (GPS: 13.0, 31.0)
```

### 3.1 Terroir GPS Boundary Containment (Ray-Casting Router)
To verify if a dynamic carrier (`stock.matter.tracking`) is physically inside the spatial boundaries of a native `stock.location` parcel, the system executes a geographic point-in-polygon containment test.

```
Algorithm: Geographic Ray-Casting Containment

  Given Carrier Point P = ( gps_lat, gps_lng )
  And Land Parcel Polygon Vertices V = [ V_1, V_2, ... V_n ]

  Initialize intersect_count = 0

  For each Edge E_i from V_i to V_(i+1):
    If (E_i.lng_start > P.lng) != (E_i.lng_end > P.lng):
      Calculate intersection latitude on the edge:
      
                            (E_i.lat_end - E_i.lat_start) * (P.lng - E_i.lng_start)
      intersect_lat = lat_start + ─────────────────────────────────────────────────────────────
                                              (E_i.lng_end - E_i.lng_start)
                                              
      If P.lat < intersect_lat:
        intersect_count = intersect_count + 1

  If (intersect_count % 2) == 1:
    Result = True  --> [ Carrier is INSIDE the land parcel ]
  Else:
    Result = False --> [ Carrier is OUTSIDE the land parcel (Raises Geofence Warning) ]
```

### 3.2 Volumetric & Density Backpressure Interlocks
Downstream location capacity constraints prevent over-saturation by asserting capacity checks upon transaction validation or production order confirmation.

```
Capacity Evaluation Formulas:

  [ Current Volume ] = SUM( [ Active Quant Volumes ] )
  [ Future Volume  ] = [ Current Volume ] + [ Pending Volume ]
  
  Safety Interlock Constraint:
  
  [ Future Volume ] <= [ Max Volumetric Capacity ]
  
  -------------------------------------------------------------
  
  [ Location Density ] = [ Current Quantity ] / [ Land Area ]
  [ Future Density  ] = ( [ Current Quantity ] + [ Order Quantity ] ) / [ Land Area ]
  
  Safety Interlock Constraint:
  
  [ Future Density ] <= [ Max Stocking Density ]
```

---

## 4. Zero-Latency Forensic Snapshot Ledger

The Snapshot Ledger serves as the immutable evidentiary audit trail, recording complete state profiles upon any operational write activity.

```
                     STATE CAPTURE PIPELINE (TRANSACTION GATE)
                     
   Operation: Carrier.write(vals) ──► [ DB UPDATE ]
                                           │
                                           ▼ (Triggers Hook)
                                   [ Captures current state ]
                                           │
                                           ▼
                                   [ Create Snapshot ]
                                   - ID / Timestamp / GPS Lat & Lng
                                   - Quant Lot Composition (IDs, DNA)
                                   - Active GxP Enforcement Levels
```

### Snapshot Database Schema Table
*   `tracking_id`: Many2one reference pointing to the source `stock.matter.tracking`.
*   `vessel_phase`: State selection (`empty`, `ready`, `dirty`).
*   `quantity`: Numeric total matter volume/weight at snap-point.
*   `location_id`: Active `stock.location` reference.
*   `lot_ids`: Associated genetic ancestry lot records.
*   `gxp_open_time` & `gxp_expiry_time`: GxP temporal validation stamps.
*   `gps_lat` & `gps_lng`: Spatial geo-stamps.

---
**Document Status: Approved | Architecture Converged | Core Algorithms Enforced**
