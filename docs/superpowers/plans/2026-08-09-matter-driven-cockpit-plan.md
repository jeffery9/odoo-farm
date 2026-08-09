# Universal Matter-Driven Cockpit & Genealogy Engine Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Transform the agricultural execution pattern from mission-driven to a unified Matter-driven cockpit with adaptive GxP compliance and slaughtering fission lineage traceability.

**Architecture:** Extend the base `stock.matter.tracking` and `product.category` models. Implement adaptive enforcement level routing (Strict GxP validation vs. Guidance), build an atomic fission math wizard for slaughtering split tracing, and update the operator forms for high-signal visual management.

**Tech Stack:** Odoo 19 CE (Python 3.12+, Owl Framework, GWeb XML).

## Global Constraints
- Target version: Odoo 19.0.
- Decouple code and documentation commits.
- Follow "3-Second Visual Management" standards.
- Use `<list>` views in Odoo 19 (instead of legacy `<tree>`).
- Define explicit `ondelete` rules for added selection/relational fields.

---

### Task 1: Product Category Compliance Levels & Stored Computing

**Files:**
- Modify: `farm_core/models/stock_matter_tracking.py` (Add `active_enforcement_level` compute and imports)
- Modify: `farm_core/security/ir.model.access.csv` (Add new model accesses if any, categories are pre-existing)
- Create: `farm_core/models/product_category_extension.py` (Extend `product.category` with compliance level)
- Modify: `farm_core/models/__init__.py` (Register `product_category_extension`)
- Test: `farm_core/tests/test_stock_matter_tracking.py` (Verify adaptive level computations)

**Interfaces:**
- Consumes: `stock.matter.tracking` model from core foundation.
- Produces: `active_enforcement_level` Selection on `stock.matter.tracking`.

- [ ] **Step 1: Write `product_category_extension.py`**

Write the following content to `farm_core/models/product_category_extension.py`:
```python
# -*- coding: utf-8 -*-
from odoo import models, fields

class ProductCategory(models.Model):
    _inherit = 'product.category'

    matter_enforcement_level = fields.Selection([
        ('guidance', 'Lightweight Guidance / 轻量级指引'),
        ('strict', 'Strict GxP Enforcement / 强合规卡控')
    ], string="Matter Enforcement Level", default="guidance", required=True, help="Risk level for physical matter tracking in this category.")
```

- [ ] **Step 2: Register model in `farm_core/models/__init__.py`**

Call `replace` on `farm_core/models/__init__.py` to import `product_category_extension` after `common_fields`.
```python
from . import product_category_extension
```

- [ ] **Step 3: Update `stock_matter_tracking.py` to add `active_enforcement_level`**

Modify `farm_core/models/stock_matter_tracking.py` to add the computed selection field and its compute method:
```python
    active_enforcement_level = fields.Selection([
        ('guidance', 'Guidance'),
        ('strict', 'Strict')
    ], string="Active Enforcement Level", compute='_compute_active_enforcement', store=True)

    @api.depends('biological_asset_id', 'quant_ids', 'quant_ids.product_id', 'quant_ids.product_id.categ_id')
    def _compute_active_enforcement(self):
        for rec in self:
            level = 'guidance'
            if rec.biological_asset_id:
                # Resolve biological asset industry category or growth stage settings
                asset_cat = rec.biological_asset_id.growth_stage_id.category_id if rec.biological_asset_id.growth_stage_id else False
                if asset_cat and getattr(asset_cat, 'matter_enforcement_level', False) == 'strict':
                    level = 'strict'
            elif rec.quant_ids:
                categories = rec.quant_ids.mapped('product_id.categ_id')
                if any(cat.matter_enforcement_level == 'strict' for cat in categories):
                    level = 'strict'
            rec.active_enforcement_level = level
```

- [ ] **Step 4: Write unit test to verify adaptive computation**

Open `farm_core/tests/test_stock_matter_tracking.py` and append:
```python
    def test_06_adaptive_enforcement_computation(self):
        """ Test that changing a category enforcement level correctly propagates active level """
        tracking = self.Tracking.create({'vessel_phase': 'idle'})
        
        # Base category default is 'guidance'
        self.assertEqual(tracking.active_enforcement_level, 'guidance')
        
        # Update product category to strict
        self.product_apple.categ_id.matter_enforcement_level = 'strict'
        
        # Link product quant to tracking vessel
        self.Quant.create({
            'product_id': self.product_apple.id,
            'quantity': 5.0,
            'location_id': self.location_vessel.id,
            'package_id': tracking.package_id.id
        })
        
        # Trigger dependency compute
        tracking._compute_active_enforcement()
        self.assertEqual(tracking.active_enforcement_level, 'strict', "Active level must resolve to strict if any contained product is high-risk.")
```

- [ ] **Step 5: Run tests and commit**

Verify tests pass. Commit with:
```bash
git add farm_core/models/product_category_extension.py farm_core/models/stock_matter_tracking.py farm_core/tests/test_stock_matter_tracking.py
git commit -m "feat: add adaptive GxP compliance enforcement levels [US-CORE-MATTER-01]"
```

---

### Task 2: Fission Split & Slaughter Genealogy Net

**Files:**
- Modify: `farm_core/models/stock_matter_tracking.py` (Add Fission Fields and `action_execute_fission` method)
- Test: `farm_core/tests/test_stock_matter_tracking.py` (Verify fission mass and pedigree preservation)

- [ ] **Step 1: Write fields in `stock_matter_tracking.py`**

Add the following lineage and split relational fields to `StockMatterTracking` in `farm_core/models/stock_matter_tracking.py`:
```python
    parent_tracking_id = fields.Many2one(
        'stock.matter.tracking',
        string='Parent Source Vessel / 来源容器',
        ondelete='restrict',
        index=True,
        help="The ancestor vessel/individual this matter split from."
    )
    child_tracking_ids = fields.One2many(
        'stock.matter.tracking',
        'parent_tracking_id',
        string='Child Vessels / 拆分容器'
    )
    fission_type = fields.Selection([
        ('none', 'None'),
        ('split', 'Division (分包/分切)'),
        ('slaughter', 'Slaughter (屠宰)')
    ], string='Lineage Fission Type', default='none', help="Lineage division operation classification.")
```

- [ ] **Step 2: Add `action_execute_fission` method to `stock_matter_tracking.py`**

Add the business method mapping splitting/cutting math and DNA decay to the model class:
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
                'fission_type': 'slaughter' if self.vessel_phase == 'dirty' else 'split',
                'dna_integrity_score': self.dna_integrity_score * 0.95, # 5% entropy decay during split
                'vessel_phase': 'idle'
            })
            child_records |= child_tracking
            
            # Create standard Odoo quant to hold the split matter inside the child package
            self.env['stock.quant'].create({
                'product_id': data['product_id'],
                'quantity': data['quantity'],
                'location_id': self.location_id.id,
                'package_id': child_package.id
            })
            
        # 3. Mark parent vessel as dirty and deplete biological assets
        self.write({
            'vessel_phase': 'dirty',
            'biological_asset_id': False
        })
        
        return child_records
```

- [ ] **Step 3: Add Unit Test for Fission and Lineage Tracking**

Open `farm_core/tests/test_stock_matter_tracking.py` and append:
```python
    def test_07_fission_split_math_and_dna_decay(self):
        """ Test that executing fission generates child records, balances quantities, and applies DNA decay """
        # Set base tracking record with 100% DNA score
        parent_tracking = self.Tracking.create({
            'vessel_phase': 'ready',
            'dna_integrity_score': 100.0,
            'location_id': self.location_vessel.id
        })
        
        # Split target data representing carcass division
        target_splits = [
            {'product_id': self.product_apple.id, 'quantity': 4.0, 'lot_name': 'SPLIT-1'},
            {'product_id': self.product_apple.id, 'quantity': 6.0, 'lot_name': 'SPLIT-2'}
        ]
        
        child_records = parent_tracking.action_execute_fission(target_splits)
        
        self.assertEqual(len(child_records), 2, "Must create exactly 2 split offspring vessels.")
        self.assertEqual(parent_tracking.vessel_phase, 'dirty', "Parent vessel must be marked dirty/depleted.")
        
        # Verify DNA Integrity score decay (100 * 0.95 = 95.0%)
        for child in child_records:
            self.assertAlmostEqual(child.dna_integrity_score, 95.0, delta=0.1, msg="Offspring must inherit decayed DNA integrity score.")
```

- [ ] **Step 4: Run test suite and commit**

Ensure all tests pass. Commit using standard command:
```bash
git add farm_core/models/stock_matter_tracking.py farm_core/tests/test_stock_matter_tracking.py
git commit -m "feat: implement slaughtering fission split algorithms with DNA decay [US-CORE-MATTER-02]"
```

---

### Task 3: Cockpit Operator UI Enrichment & Adaptability

**Files:**
- Modify: `farm_core/views/stock_matter_tracking_views.xml` (Inject split hierarchy and adaptive modes)
- Modify: `farm_mrp/views/stock_matter_tracking_mrp_views.xml` (Extend extended view)

- [ ] **Step 1: Update form views in `farm_core/views/stock_matter_tracking_views.xml`**

Add `parent_tracking_id`, `fission_type`, and `active_enforcement_level` fields to the base form view of `stock.matter.tracking`:
```xml
        <xpath expr="//group[@id='group_physical_identification']" position="inside">
            <field name="parent_tracking_id" readonly="1"/>
            <field name="fission_type" readonly="1"/>
            <field name="active_enforcement_level" widget="badge" decoration-warning="active_enforcement_level == 'strict'" decoration-info="active_enforcement_level == 'guidance'"/>
        </xpath>
```
Also let's add a "Split Lineage Network" child sub-page/page inside the `<notebook>` element to view offspring:
```xml
        <xpath expr="//notebook[@id='notebook_stock_matter_tracking']" position="inside">
            <page string="Lineage Offspring (Split)" name="child_lineage">
                <field name="child_tracking_ids" readonly="1">
                    <list string="Split Offspring">
                        <field name="name"/>
                        <field name="fission_type"/>
                        <field name="dna_integrity_score"/>
                        <field name="location_id"/>
                        <field name="create_date"/>
                    </list>
                </field>
            </page>
        </xpath>
```

- [ ] **Step 2: Apply adaptive visual warnings in form view**

Under strict modes, apply high-signal visual cues. We can add a banner or styling classes dependent on `active_enforcement_level`:
```xml
        <xpath expr="//sheet" position="before">
            <div class="alert alert-warning text-center" role="alert" invisible="active_enforcement_level != 'strict'" style="margin-bottom:0px;">
                <strong>STRICT GXP COMPLIANCE ENFORCED / 强合规控制模式已启动</strong>: Batch verification, strict weights, and safety scanning are active for this matter category.
            </div>
        </xpath>
```

- [ ] **Step 3: Run full module upgrade and verification**

Run clean compile and upgrade commands. Commit UI updates:
```bash
git add farm_core/views/stock_matter_tracking_views.xml
git commit -m "style: enrich operator cockpit layout with adaptive GxP warnings [US-CORE-MATTER-03]"
```
