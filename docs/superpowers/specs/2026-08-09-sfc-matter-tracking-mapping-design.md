# Design Specification: SFC to Matter-Tracking Architectural Mapping & Traceability Algorithms

This document defines the semantic conversion of the SFC (Shop Floor Container) model into the `farm` Matter-Tracking system. It describes the runtime tracking pipeline, DNA pedigree decay propagation, spatial ray-casting routing, zero-latency snapshot ledgers, and decoupled process control patterns.

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
    *   *Specification:* Inherits standard Odoo `stock.package` via delegation (`_inherits`). Represents the physical container/carrier and coordinates logistics and material mutations.
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

### 2.3 SFC-Core Genealogy Transition Logic
Following the Gherkin & SFC design specifications, the physical genealogy is tracked via three native transactional transitions:
*   **Sequential (顺序流转):** The carrier retains its primary identifier and package name (e.g., `MAT-00001` remains `MAT-00001` as it moves from one physical node/stage to the next), seamlessly propagating its ancestral DNA metadata.
*   **Split (裂变/分流):** Spawns new, uniquely named offspring containers (e.g., splitting `MAT-00001` into children `MAT-00001-1` and `MAT-00001-2`), dividing physical mass proportionally and applying the 5% fission decay penalty.
*   **Merge (并合/混合):** Consolidates multiple source carriers into a unified target container. The unified carrier inherits the primary container's name (or adopts the target vessel LPN code) and calculates combined DNA purity according to Section 2.1.

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

### 3.3 M1-to-M2 Multi-Tier Workflow Routing
The routing process transitions continuously from static system definition to physical runtime execution:
*   **M1 Static Processes (`workflow.template`):** Employs static nodes (step definitions) and directed edges (allowable routing paths) to configure agricultural campaign constraints.
*   **M2 Runtime Execution (`execution.sfc` / `workflow` instance):** Tracks active carriers dynamically as they move through runtime node instances (`workflow.node`), auditing transit duration and updating current phase parameters.
*   **Missions (`mission`):** Mapped directly to HMI/POP execution cards (modeled as de-industrialized `agri.intervention` records). Confirming a mission triggers the state transit and moves the carrier to the next node.
*   **Process Parameter Snapshot (JSON):** At each step transition, the system captures a comprehensive state snapshot. Alongside lots and quantities, it records custom sensor readings or operator logs in a structured JSON schema (`process_parameters`).

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
                                   - Process Parameters (JSON)
```

### Snapshot Database Schema Table
*   `tracking_id`: Many2one reference pointing to the source `stock.matter.tracking`.
*   `vessel_phase`: State selection (`empty`, `ready`, `dirty`).
*   `quantity`: Numeric total matter volume/weight at snap-point.
*   `location_id`: Active `stock.location` reference.
*   `lot_ids`: Associated genetic ancestry lot records.
*   `gxp_open_time` & `gxp_expiry_time`: GxP temporal validation stamps.
*   `gps_lat` & `gps_lng`: Spatial geo-stamps.
*   `process_parameters`: Text field containing step JSON parameters.

---

## 5. Device and Container Decoupling & Batch Processing Patterns

To model complex chemical/biological processes, the system strictly enforces the principle: **"Equipment is Equipment, Material is Material."** Equipment/Workstations (`mrp.workcenter`) manage process execution capacity, whereas SFC Carriers (`stock.matter.tracking`) track material states.

```
  PATTERN 1: HEAT TREATMENT FURNACE               PATTERN 2: REACTION TANK
  (Physical coexistence, Individual identity)     (Material fusion, Morphic change)
  
   +------------------------------------+         +------------------------------------+
   |     sfc.process.batch (炉次)       |         |       Raw Carrier A (100 kg)       |
   |     - Equipment: Heat Furnace       |         |       Raw Carrier B (200 kg)       |
   +──────────────────┬─────────────────+         +──────────────────┬─────────────────+
                      │                                              │
         ┌────────────┴────────────┐                                 ▼ (Merge)
         ▼                         ▼                       +───────────────────+
  Carrier A (Weight)        Carrier B (Weight)             | Bulk Carrier Tank |
  - Enter: State "In Charge"                               | - Volume: 300 kg  |
  - Exit: Preserve original individual identity            | - State: Reacting |
                                                           +───────────────────+
                                                                     │
                                                                     ▼ (Split/Fission)
                                                           +─────────┴─────────+
                                                           ▼                   ▼
                                                   Product C (150kg)   Product D (150kg)
```

### 5.1 Heat Treatment Furnace (物理共存，个体独立)
*   **Core Architecture:** Models physical coexistence without physical fusion. Multiple SFC carriers are loaded into a single equipment workstation sharing process recipes (e.g., temperature curves).
*   **Data Aggregation:** Handled via `sfc.process.batch` (Process Batch/炉次). The batch contains `workcenter_id` and a `sfc_ids` One2many relation pointing to active carriers.
*   **State Machine:**
    *   **On Entry:** Carriers transition to the `in_charge` state and are bound to the current batch.
    *   **On Exit:** Carriers unbind from the batch and transition to `pending` or `qc` status, preserving their individual quantities and genetic names.

### 5.2 Reaction Tank (物质融合，形态转化)
*   **Core Architecture:** Models chemical/biological fusion where multiple raw materials fully integrate into a new compound substance.
*   **Data Flow:**
    *   **Merge Hook:** Multiple input carriers (SFC_A, SFC_B) are validated and emptied. Their underlying `stock.quant` records are transferred to a new, temporary **Bulk SFC Carrier** (e.g., SFC_Tank) representative of the vessel itself. Parent carriers are marked as `consumed`.
    *   **Reaction Node:** SFC_Tank represents the active physical reaction, recording real-time process indicators (pH, temperature, pressure, stirrer speed) in its JSON snapshot.
    *   **Split Hook:** Upon reaction completion, the bulk material is dispensed into multiple finished/offspring packaging containers (SFC_C, SFC_D), calling `action_execute_fission` to distribute the output quants, apply decay penalties, and mark the SFC_Tank as `scrapped/empty`.

---

## 6. Safety & Rule Engines: Admission & Transition Whitelists

To secure the material execution path from operator errors or unauthorized steps, the system establishes a strict, dual-layer validation checkpoint pipeline.

### 6.1 SFC Transition Rule Engine (状态流转规则)
Prevents process-skipping and enforces strict state machine evolution. The system overrides database write operations to assert validation against a state-transition whitelist matrix.

```
                      SFC TRANSITION ALLOWED MATRIX
                      
  FROM STATE \ TO STATE │ IDLE │ LOADING │ PROCESSING │ QC │ DONE │ CONSUMED │
  ──────────────────────┼──────┼─────────┼────────────┼────┼──────┼──────────┼
  IDLE                  │  --  │   Yes   │     No     │ No │  No  │    No    │
  LOADING               │  No  │   --    │    Yes     │ No │  No  │    No    │
  PROCESSING            │  No  │   No    │     --     │Yes │  No  │    No    │
  QC                    │  No  │   No    │     No     │ -- │ Yes  │    No    │
  DONE                  │  No  │   No    │     No     │ No │  --  │   Yes    │
  CONSUMED              │  --  │   --    │     --     │ -- │  --  │    --    │
```

*   **Implementation Guardrail:** If an update attempt bypasses the allowed transition path (e.g., writing `idle` $\rightarrow$ `qc`), the Odoo layer blocks execution and throws a `UserError("SFC State Transition Violation")`.

### 6.2 SFC Admission Rule Engine (工序准入校验)
Gates physical entry into any operational workcenter or geographic plot location. Before a scanned carrier is assigned to a process batch or location move line, the system verifies its physical properties.

```
  Carrier scan at Workcenter input ──► [ RUN ADMISSION CHECKS ]
                                              │
                                              ├─► Check: Temp >= Target Temp? (Yes/No)
                                              ├─► Check: Purity >= Target? (Yes/No)
                                              └─► Check: Pre-state == "done"? (Yes/No)
                                              │
                                              ▼ (All Pass)
                                      [ Assign to Batch & Process ]
```

*   **Property Validation:** Verifies factors such as temperature, composition, density, and previous GxP status. Any failed parameter throws a `ValidationError` block, physically halting material routing.

---

## 7. SFC Graph: Directed Acyclic Graph (DAG) Traceability Engine

To handle complex Many-to-Many processes (such as dynamic batch mergers and proportional splitting), the system implements a strict DAG-based genealogy engine, storing physical lineage connections as edges in a dedicated model.

```
                       SFC GENEALOGY GRAPH (DAG EDGES)
                       
     Source Carrier A (SFC_01) ───────┐
                                      ├─► [ Link Edge: Merge ] ──► Target Carrier (SFC_Tank)
     Source Carrier B (SFC_02) ───────┘                                │
                                                                       ├─► [ Link Edge: Split ] ──► offspring C (SFC_03)
                                                                       └─► [ Link Edge: Split ] ──► offspring D (SFC_04)
```

### 7.1 Lineage Edge Model Schema (`stock.matter.tracking.link`)
Each record in the `stock.matter.tracking.link` model represents a directed edge flowing from an ancestral parent carrier to a descendant child carrier:
*   `parent_id`: Many2one reference pointing to the source `stock.matter.tracking` (Ancestor/原料容器).
*   `child_id`: Many2one reference pointing to the target `stock.matter.tracking` (Descendant/产出容器).
*   `transition_type`: Selection field (`merge` / `split` / `sequential`).
*   `quantity_transferred`: Float field logging the physical mass transferred across the edge.
*   `timestamp`: Datetime field recording the precise execution point.

### 7.2 Bidirectional Tracing Recursive CTE Algorithms

#### A. Upstream Ancestry Search (逆向/追溯原料)
Given a specific descendant carrier ID `X`, this algorithm recursively walks the DAG edges backward to resolve all source parent carriers and ancestral material lots.

```sql
WITH RECURSIVE upstream_trace AS (
    -- Anchor Member: Start with the target carrier
    SELECT parent_id, child_id, transition_type, quantity_transferred, 1 AS depth
    FROM stock_matter_tracking_link
    WHERE child_id = X
    
    UNION ALL
    
    -- Recursive Member: Join backward on parent
    SELECT l.parent_id, l.child_id, l.transition_type, l.quantity_transferred, ut.depth + 1
    FROM stock_matter_tracking_link l
    INNER JOIN upstream_trace ut ON l.child_id = ut.parent_id
)
SELECT parent_id, transition_type, quantity_transferred, depth 
FROM upstream_trace;
```

#### B. Downstream Shipment Search (正向/跟踪流向)
Given an ancestral carrier ID `Y` (e.g., initial raw ingredient), this algorithm recursively walks the DAG edges forward to find all downstream intermediate vessels, finished packaging units, and customer shipping packages.

```sql
WITH RECURSIVE downstream_trace AS (
    -- Anchor Member: Start with the initial source carrier
    SELECT parent_id, child_id, transition_type, quantity_transferred, 1 AS depth
    FROM stock_matter_tracking_link
    WHERE parent_id = Y
    
    UNION ALL
    
    -- Recursive Member: Join forward on child
    SELECT l.parent_id, l.child_id, l.transition_type, l.quantity_transferred, dt.depth + 1
    FROM stock_matter_tracking_link l
    INNER JOIN downstream_trace dt ON l.parent_id = dt.child_id
)
SELECT child_id, transition_type, quantity_transferred, depth 
FROM downstream_trace;
```

---
**Document Status: Approved | Architecture Converged | Core Algorithms Enforced**
