# Universal Matter-Driven Cockpit & Genealogy Engine Spec

## 1. Context & Business Vision
In traditional ERP systems, manufacturing and field execution are strictly order-driven. Operators navigate through a static list of Work Orders (WOs) or Missions and manually assign raw materials or assets. 

This specification refactors the paradigm into a **Matter-Driven (物质驱动)** model. The physical Matter (tracked via `stock.matter.tracking`, representing containers, vessels, hoppers, or individual agricultural biological assets like livestock and trees) acts as the primary cockpit (Mission Control Center). All work orders, agricultural interventions, and GxP recipes are subordinate instructions dynamically pulled and rendered when the Matter is scanned or loaded.

Additionally, this specification introduces **Adaptive GxP Enforcement Levels** (Strict validation vs. Lightweight guidance) configured dynamically based on the product category risk, and **Lineage Fission Tracing** to track bulk splitting, cutting, and slaughtering processes.

---

## 2. Technical Architecture & Data Model

```
                ┌─────────────────────────────────┐
                │        product.category         │
                │   [ matter_enforcement_level ]  │
                └────────────────┬────────────────┘
                                 │ Adapts
                                 ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        stock.matter.tracking                           │
├────────────────────────────────────────────────────────────────────────┤
│  [ Header: Vessel Phase, Lock Status, Active Enforcement Mode ]       │
├────────────────────────────────┬───────────────────────────────────────┤
│    Physical Identification     │         GxP & Quality Metrics         │
│  - package_id (delegated)      │  - gxp_open_time / gxp_expiry_time    │
│  - biological_asset_id         │  - dna_integrity_score                │
│  - parent_tracking_id (fission)│                                       │
├────────────────────────────────┴───────────────────────────────────────┤
│                              Tabs / Pages                              │
│  ┌───────────────────────┬─────────────────────────┬─────────────────┐ │
│  │    Contained Matter   │    Genealogy (Lots)     │ GxP Snapshots   │ │
│  │    (stock.quant list) │    (stock.lot list)     │ (snapshots list)│ │
│  └───────────────────────┴─────────────────────────┴─────────────────┘ │
└────────────────────────────────────────────────────────────────────────┘
```

### 2.1 Schema Extensions (`farm_core` & `farm_mrp`)

#### Model: `product.category`
To support risk-adjusted compliance:
*   `matter_enforcement_level`: `Selection([('guidance', 'Lightweight Guidance / 选项2轻量指引'), ('strict', 'Strict GxP Enforcement / 选项1强卡控')], string="Matter Enforcement Level", default="guidance")`

#### Model: `stock.matter.tracking`
The central physical-logical twin representing the matter carrier:
*   `parent_tracking_id`: `Many2one('stock.matter.tracking', string="Parent Ancestor / 来源物质", help="Source vessel/matter this record split or was harvested from.")`
*   `child_tracking_ids`: `One2many('stock.matter.tracking', 'parent_tracking_id', string="Child Offspring / 分解物质")`
*   `fission_type`: `Selection([('none', 'None'), ('split', 'Division (分包/分切)'), ('slaughter', 'Slaughter (屠宰)')], string="Lineage Fission Type", default="none")`
*   `active_enforcement_level`: `Selection([('guidance', 'Guidance'), ('strict', 'Strict')], compute='_compute_active_enforcement', store=True, string="Active Enforcement Mode")`

#### Model: `stock.matter.tracking.snapshot`
Auditing tracker:
*   `parent_tracking_id`: `Many2one('stock.matter.tracking', string="Parent Vessel at Transition")`
*   `fission_type`: `Selection([('none', 'None'), ('split', 'Division'), ('slaughter', 'Slaughter')])`

---

## 3. Dynamic Business Logic & Algorithms

### 3.1 Adaptive GxP Enforcement Level Calculation
For any active `stock.matter.tracking` record, the enforcement level determines whether the operator can simply click "Confirm Completion" (Guidance) or must undergo strict verification (Strict):
1.  If the tracked `biological_asset_id` (or product) category on `stock.matter.tracking` is set to `strict` (such as veterinary medical applications or biological vaccine dosing), `active_enforcement_level` is resolved as `strict`.
2.  If the level is `strict`, the UI hides the basic completion action. The operator must scan the input lot or barcode, matching against the GxP recipe boundaries, before completion is authorized.
3.  If the level is `guidance`, the operator is presented with visual instruction steps and a simple manual "Complete Step" confirmation button.

```python
@api.depends('biological_asset_id', 'quant_ids', 'quant_ids.product_id')
def _compute_active_enforcement(self):
    for rec in self:
        level = 'guidance'
        if rec.biological_asset_id:
            # Check biological asset's category
            asset_cat = rec.biological_asset_id.growth_stage_id.category_id or rec.biological_asset_id.owner_id.industry_type
            if getattr(asset_cat, 'matter_enforcement_level', False) == 'strict':
                level = 'strict'
        elif rec.quant_ids:
            # Check products inside the carrier
            categories = rec.quant_ids.mapped('product_id.categ_id')
            if any(cat.matter_enforcement_level == 'strict' for cat in categories):
                level = 'strict'
        rec.active_enforcement_level = level
```

### 3.2 Fission & Genealogy Propagation (Slaughtering / Splitting)
When a biological asset is split or slaughtered (e.g., cow $\rightarrow$ meat pieces), the genealogy network propagates the maternal lot and DNA information downstream:

```python
def action_execute_fission(self, target_products_data):
    """
    Executes physical-logical fission of Matter.
    target_products_data: list of dicts [{'product_id': id, 'quantity': qty, 'lot_name': name}]
    """
    self.ensure_one()
    child_records = self.env['stock.matter.tracking']
    
    # 1. Capture Before-State snapshot
    self.action_capture_snapshot()
    
    # 2. Iterate and create child tracking packages
    for data in target_products_data:
        # Generate child delegated package
        child_package = self.env['stock.quant.package'].create({
            'name': data.get('lot_name') or self.env['ir.sequence'].next_by_code('stock.matter.tracking')
        })
        
        # Inherit genetic attributes and quality markings
        child_tracking = self.create({
            'package_id': child_package.id,
            'parent_tracking_id': self.id,
            'fission_type': 'split' if self.vessel_phase != 'dirty' else 'slaughter',
            'dna_integrity_score': self.dna_integrity_score * 0.95, # 5% entropy loss during division/processing
            'vessel_phase': 'idle'
        })
        child_records |= child_tracking
        
        # 3. Create stock move to balance mass conservation mathematically
        self.env['stock.move'].create({
            'name': _('Fission Division from %s') % self.name,
            'product_id': data['product_id'],
            'product_uom_qty': data['quantity'],
            'location_id': self.location_id.id,
            'location_dest_id': self.location_id.id, # Stays in-place, package changes
            'restrict_partner_id': self.company_id.partner_id.id,
        })
        
    # 4. Set parent vessel as dirty/depleted
    self.write({
        'vessel_phase': 'dirty',
        'biological_asset_id': False
    })
    
    return child_records
```

---

## 4. UI/UX: The Universal Operator Cockpit

### 4.1 "3-Second Visual Management" Responsive Form
The primary form view utilizes adaptive, highly stylized widgets for instant state assessment:
*   **Ready/Optimal State**: Rendered with **Green CSS badges** when `vessel_phase == 'ready'`.
*   **Hazardous/Non-Compliant State**: Rendered with **Red warning bars** if GxP timers are expired (`gxp_expiry_time < now`).
*   **Enforcement Dynamic Interface**: Under `strict` mode, the action panel highlights scanning input fields with a glowing amber border to direct the operator's eye.

---

## 5. TDD Verification Plan
Comprehensive coverage is maintained by writing explicit test scenarios targeting the custom models:
1.  **Test GxP Adaptive UI Rendering**: Validate that setting a Category to `strict` updates the Matter's `active_enforcement_level` dynamically.
2.  **Test Fission Mass Balance**: Verify parent-to-child division executes `stock.move` and correctly propagates `parent_tracking_id` links.
3.  **Test Genealogy Heritage Decay**: Ensure downstream offspring decay calculation (`dna_integrity_score` loss) is mathematical and deterministic.
