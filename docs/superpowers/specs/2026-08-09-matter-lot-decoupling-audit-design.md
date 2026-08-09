# Architectural Convergence & Audit Design Specification: Matter/Lot Decoupling and ISL Alignment

This document outlines the comprehensive project-wide architectural audit and convergence design to align the entire Odoo Farm ecosystem with the **Matter/Lot Decoupling** paradigm and the de-industrialized **ISA-88 Agricultural Process Routing** standards.

---

## 1. Executive Summary & Core Paradigm

The **Matter-Driven Paradigm** enforces a strict physical and logical separation between the genetic/batch blueprint (**Genotype**) and its real-world physical carrier representation (**Phenotype**). 

### 1.1 The Decoupling Hierarchy

*   **stock.lot (Genotype Layer):** Defines static genetic lineage, parent pedigree, species, breed, birth date, certification types (e.g. Organic, Demeter), and legal withdrawal indicators. Crucially, direct writes to physical state fields on this model are blocked at the database level using a **Write-Block mechanism** to maintain data integrity.
*   **stock.matter.tracking (Phenotype/Carrier Layer):** Serves as the actual digital twin. It tracks real-world state mutations including live weight, volume, geographic GIS coordinates (GPS), life stage transitions, and carrier flow states.
*   **Compatibility Bridge:** Allows standard Odoo views to query physical properties (such as current weight or location) as read-only computed fields on `stock.lot` that dynamically resolve from the active `stock.matter.tracking` carrier.

### 1.2 Unified Decoupling Diagram (ASCII)

```
                       +---------------------------------------------+
                       |                 stock.lot                   |
                       |    (Genotype / Genetic & Batch Baseline)    |
                       +----------------------+----------------------+
                                              ^
                                              | (Delegation Inheritance _inherits)
                       +----------------------+----------------------+
                       |         agri.isl.lot.livestock              |
                       |     (also FarmCropLot, FarmLotAquaculture)  |
                       +---------------------------------------------+
                                              ^
                                              | (Computed / Read-only Bridge)
                                              v
                       +---------------------------------------------+
                       |          stock.matter.tracking              |
                       |      (Phenotype / Physical Digital Twin)     |
                       |  * Live Weight, Life Stage, Carrier State   |
                       +---------------------------------------------+
                                              ^
                                              | (Logs transitions)
                                              v
                       +---------------------------------------------+
                       |       stock.matter.tracking.snapshot        |
                       |  (SFC Snapshot / GxP state / Cleaning state) |
                       +---------------------------------------------+
```

---

## 2. Project-Wide Audit Findings: Industry-Specific Layers (ISL)

An extensive audit of all Industry-Specific Layers was conducted to verify compliance with the delegation-inheritance lot mapping and the Write-Block safety protocols:

### 2.1 Compliant ISL Lots (Already Aligned)
The following models correctly use Odoo delegation inheritance (`_inherits`) on `stock.lot` via their bridge fields, which automatically inherits and enforces the write-block security validations and compatibility bridges of the parent `stock.lot`:
*   `agri.isl.lot.livestock` (Livestock) -> Aligned and fully verified green.
*   `farm.crop.lot` (Field Crops) -> Aligned and verified.
*   `agri.isl.lot.aquaculture` (Aquaculture) -> Aligned and verified.
*   `farm.lot.hive` (Apiculture) -> Aligned.
*   `farm.lot.wine` (Winery) -> Aligned.
*   `farm.lot.grape` (Viticulture) -> Aligned.
*   `farm.lot.flower` (Floriculture) -> Aligned.
*   `farm.lot.brew` (Fermentation) -> Aligned.
*   `farm.lot.harvest` (Processing) -> Aligned.
*   `farm.lot.medicinal` (Medicinal Plants) -> Aligned.

---

## 3. Targeted Audit Findings & Proposed Refactoring

The audit identified two key areas in `farm_processing` requiring architectural alignment:

### 3.1 Gap A: `farm.industry.operation` (In `farm_processing/models/mrp_operation_isl.py`)

*   **The Issue:**
    Currently, `farm.industry.operation` extends `mrp.routing.workcenter` via delegation, but it explicitly duplicates physical fields: `technical_manual`, `param_monitoring_required`, `target_value`, and `tolerance_range`. 
    Since `mrp.routing.workcenter` now inherits from `agri.operation.mixin` (which contains these exact fields with localized help text, localized labels, and GxP status support), the duplicate declarations in the ISL layer mask the parent's mixin fields. This causes MRO field resolution warnings and breaks synchronization with ISA-88 agricultural process steps.
*   **The Solution (To-Be):**
    Remove the redundant field declarations from `farm.industry.operation`. The delegation engine automatically exposes the fields on the parent model `mrp.routing.workcenter` (inherited from `agri.operation.mixin`), which simplifies the codebase, resolves registry duplication warnings, and fully aligns the model with the de-industrialized ISA-88 process step routing standard.

### 3.2 Gap B: `farm.seasonal.bom` (In `farm_processing/models/missing_models.py`)

*   **The Issue:**
    `farm.seasonal.bom` exists as a mock/fallback structure within `missing_models.py`. In contrast, `farm_agricultural_processing` implements the modern, de-industrialized, and GxP-compatible `agri.seasonal.recipe` model, which handles versioned, time-bound recipe adjustments.
*   **The Solution (To-Be):**
    Acknowledge `farm.seasonal.bom` as a deprecated legacy representation. To maintain backwards compatibility with existing legacy integration flows and tests, `farm.seasonal.bom` will remain as a legacy wrapper. Any active manufacturing checks inside `farm_mrp` or `farm_processing` must prioritize the `agri.seasonal.recipe` checks, ensuring that real-world material compatibility and GxP validations are performed against the active, seasonally adjusted version.

---

## 4. Implementation Plan & Checklist

### [Task 1] Refactor `farm.industry.operation` in `farm_processing`
*   **Action:** Modify `/Users/jeffery/odoo-farm-workspace/odoo-farm-dev/farm_processing/models/mrp_operation_isl.py` to remove the duplicated fields.
*   **Verification:** Run the `farm_processing` tests to verify that workcenters and routing form views still successfully resolve technical SOPs and monitoring variables via the delegation relation.

### [Task 2] Audit and Validate Project-Wide Test Compliance
*   **Action:** Execute the complete `farm_processing` test suite to ensure that removing duplicate fields introduces no regressions and that the model is fully integrated.
*   **Verification:** Verify 100% green pass with 0 failures on Odoo 19.

---

## 5. Architectural Self-Review

*   **Placeholder Scan:** No placeholders are present.
*   **Internal Consistency:** The delegation mapping matches Odoo 19 registry standards and respects `agri.operation.mixin`.
*   **Scope Check:** Extremely focused on removing redundancy and unifying routing step specifications.
*   **Ambiguity Check:** All field mappings and parent delegations are explicitly specified.
