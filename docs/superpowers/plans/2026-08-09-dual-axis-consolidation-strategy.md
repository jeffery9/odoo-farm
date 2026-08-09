# Dual-Axis Consolidation Strategy & Jidoka Interlocks Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement a metadata-driven material consolidation engine and safety interlock mechanism that automatically controls lot mixing, DNA degradation, and GxP hardware states.

**Architecture:** The product category model is extended with consolidation strategies (isolation, weighted average, multi-lot packaging). Inventory transactions are audited at the transaction-level (Quant creation/updates) to enforce isolation constraints, calculate加权平均 values, decay DNA pedigree scores, and execute physical state Jidoka blocks.

**Tech Stack:** Odoo 19 CE, Python 3.12, PostgreSQL.

## Global Constraints

*   **XML Normalization**: All view data files must follow the `<odoo><data>...</data></odoo>` structure.
*   **Schema Strictness**: All selection fields must define robust selections; compute properties must maintain correct dependencies.
*   **De-industrialization**: Work Orders are designated as secondary Mission entities subordinate to the core Matter Tracking tracking entity.
*   **Bilingual Standard**: UI elements and user error messages must support Chinese (CN) for localized workshop operators and English (EN) for backend logic.

---

### Task 1: Product Category & Matter Tracking Field Extensions

**Files:**
- Create: `farm_core/models/product_category_extension.py`
- Modify: `farm_core/models/stock_matter_tracking.py`
- Modify: `farm_core/__manifest__.py`
- Test: `farm_core/tests/test_consolidation_fields.py`

**Interfaces:**
- Consumes: Existing `product.category` and `stock.matter.tracking` base models.
- Produces: `product.category.consolidation_strategy` (Selection field), `product.category.allow_cross_quality_mix` (Boolean field), `stock.matter.tracking.biological_stage` (Selection field), `stock.matter.tracking.animal_count` (Integer field), `stock.matter.tracking.water_volume_m3` (Float field), `stock.matter.tracking.is_consolidated` (Boolean field), `stock.matter.tracking.consolidation_history` (Text field).

- [ ] **Step 1: Write the failing test**

Write `/Users/jeffery/odoo-farm-workspace/odoo-farm-dev/farm_core/tests/test_consolidation_fields.py`:
```python
# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestConsolidationFields(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(TestConsolidationFields, cls).setUpClass()
        cls.Category = cls.env['product.category']
        cls.Tracking = cls.env['stock.matter.tracking']

    def test_category_and_tracking_fields_exist(self):
        category = self.Category.create({
            'name': 'Test Consolidate',
            'consolidation_strategy': 'strict_isolation',
            'allow_cross_quality_mix': True
        })
        self.assertEqual(category.consolidation_strategy, 'strict_isolation')
        self.assertTrue(category.allow_cross_quality_mix)

        tracking = self.Tracking.create({
            'biological_stage': 'growing',
            'animal_count': 15,
            'water_volume_m3': 2.5
        })
        self.assertEqual(tracking.biological_stage, 'growing')
        self.assertEqual(tracking.animal_count, 15)
        self.assertEqual(tracking.water_volume_m3, 2.5)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `docker compose run --rm web odoo -d test_clean_db -i farm_core --test-enable --test-tags=TestConsolidationFields --stop-after-init --log-level=warn`
Expected: FAIL with `AttributeError` indicating missing fields.

- [ ] **Step 3: Write minimal implementation**

Modify `/Users/jeffery/odoo-farm-workspace/odoo-farm-dev/farm_core/models/product_category_extension.py`:
```python
# -*- coding: utf-8 -*-
from odoo import models, fields

class ProductCategory(models.Model):
    _inherit = 'product.category'

    consolidation_strategy = fields.Selection([
        ('strict_isolation', 'Strict Isolation (Single-Lot Only)'),
        ('weighted_average', 'Weighted Average (Bulk & Liquid Mixing)'),
        ('multi_lot_package', 'Multi-Lot Pack (Co-existence in Package)')
    ], string="Consolidation Strategy", default='strict_isolation', required=True)

    allow_cross_quality_mix = fields.Boolean(
        string="Allow Cross-Quality Mixing", default=False)
```

Ensure it is imported in `farm_core/models/__init__.py`:
```python
from . import product_category_extension
```

Modify `/Users/jeffery/odoo-farm-workspace/odoo-farm-dev/farm_core/models/stock_matter_tracking.py` to add tracking fields:
```python
    biological_stage = fields.Selection([
        ('born', 'Born / Started'),
        ('growing', 'Growing / Fattening'),
        ('mature', 'Mature / Breeding'),
        ('harvested', 'Harvested / Culled')
    ], string="Dynamic Life Stage", default='born', tracking=True)

    animal_count = fields.Integer("Physical Item Count", default=1, tracking=True)
    water_volume_m3 = fields.Float("Contained Water Volume (m3)", tracking=True)

    is_consolidated = fields.Boolean("Has Consolidated Batches", default=False)
    consolidation_history = fields.Text("Consolidation Audit Log")
```

Import tests in `/Users/jeffery/odoo-farm-workspace/odoo-farm-dev/farm_core/tests/__init__.py`:
```python
from . import test_consolidation_fields
```

- [ ] **Step 4: Run test to verify it passes**

Run: `docker compose run --rm web odoo -d test_clean_db -i farm_core --test-enable --test-tags=TestConsolidationFields --stop-after-init --log-level=warn`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add farm_core/models/product_category_extension.py farm_core/models/stock_matter_tracking.py farm_core/tests/test_consolidation_fields.py
git commit -m "feat: add category consolidation strategy and tracking biological fields"
```

---

### Task 2: Constraint Verification (Strict Isolation & Cross-Grade Blocks)

**Files:**
- Create: `farm_core/models/stock_quant_consolidation.py`
- Modify: `farm_core/__manifest__.py`
- Modify: `farm_core/models/__init__.py`
- Test: `farm_core/tests/test_consolidation_constraints.py`

**Interfaces:**
- Consumes: `stock.quant` create / write operations.
- Produces: Transaction-level validation hooks that audit lot compatibility before allowing quants to enter a package associated with a Matter Tracking container.

- [ ] **Step 1: Write the failing test**

Write `/Users/jeffery/odoo-farm-workspace/odoo-farm-dev/farm_core/tests/test_consolidation_constraints.py`:
```python
# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

class TestConsolidationConstraints(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(TestConsolidationConstraints, cls).setUpClass()
        cls.Product = cls.env['product.product']
        cls.Category = cls.env['product.category']
        cls.Lot = cls.env['stock.lot']
        cls.Location = cls.env['stock.location']
        cls.Tracking = cls.env['stock.matter.tracking']
        cls.Quant = cls.env['stock.quant']

        cls.strict_category = cls.Category.create({
            'name': 'Strict Seeds',
            'consolidation_strategy': 'strict_isolation',
            'allow_cross_quality_mix': False
        })

        cls.product_a = cls.Product.create({
            'name': 'Seed Batch A',
            'categ_id': cls.strict_category.id,
            'type': 'consu',
            'is_storable': True
        })

        cls.lot_1 = cls.Lot.create({
            'name': 'LOT-SEED-01',
            'product_id': cls.product_a.id,
            'quality_grade': 'grade_a'
        })
        cls.lot_2 = cls.Lot.create({
            'name': 'LOT-SEED-02',
            'product_id': cls.product_a.id,
            'quality_grade': 'grade_b'
        })

        cls.location_vessel = cls.Location.create({
            'name': 'Vessel Bin C',
            'usage': 'internal'
        })

    def test_strict_isolation_prevents_multiple_lots(self):
        tracking = self.Tracking.create({
            'vessel_phase': 'idle'
        })

        # Put Lot 1 in container
        self.Quant.create({
            'product_id': self.product_a.id,
            'location_id': self.location_vessel.id,
            'lot_id': self.lot_1.id,
            'quantity': 1.0,
            'package_id': tracking.package_id.id
        })

        # Attempt to put Lot 2 in the same container should fail due to strict isolation
        with self.assertRaisesRegex(ValidationError, "Strict Isolation"):
            self.Quant.create({
                'product_id': self.product_a.id,
                'location_id': self.location_vessel.id,
                'lot_id': self.lot_2.id,
                'quantity': 1.0,
                'package_id': tracking.package_id.id
            })
```

- [ ] **Step 2: Run test to verify it fails**

Run: `docker compose run --rm web odoo -d test_clean_db -i farm_core --test-enable --test-tags=TestConsolidationConstraints --stop-after-init --log-level=warn`
Expected: FAIL with assertion error (second Quant gets created instead of raising ValidationError).

- [ ] **Step 3: Write minimal implementation**

Create `/Users/jeffery/odoo-farm-workspace/odoo-farm-dev/farm_core/models/stock_quant_consolidation.py`:
```python
# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class StockQuant(models.Model):
    _inherit = 'stock.quant'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            package_id = vals.get('package_id')
            if package_id:
                tracking = self.env['stock.matter.tracking'].search([('package_id', '=', package_id)], limit=1)
                if tracking:
                    lot_id = vals.get('lot_id')
                    if lot_id:
                        new_lot = self.env['stock.lot'].browse(lot_id)
                        product = self.env['product.product'].browse(vals.get('product_id'))
                        category = product.categ_id

                        # Find existing quants in container
                        existing_quants = self.search([('package_id', '=', package_id)])
                        if existing_quants:
                            # Quality Grade restriction check
                            if not category.allow_cross_quality_mix:
                                existing_lots = existing_quants.mapped('lot_id')
                                if any(l.quality_grade != new_lot.quality_grade for l in existing_lots if l.quality_grade):
                                    raise ValidationError(_("Mixing Blocked: Cross-quality mixing is disabled for category %s.") % category.name)

                            # Strict Isolation check
                            if category.consolidation_strategy == 'strict_isolation':
                                if any(q.lot_id != new_lot for q in existing_quants):
                                    raise ValidationError(_("Strict Isolation: Container %s enforces single-lot isolation.") % tracking.name)

        return super(StockQuant, self).create(vals_list)
```

Import model in `farm_core/models/__init__.py`:
```python
from . import stock_quant_consolidation
```

Import tests in `/Users/jeffery/odoo-farm-workspace/odoo-farm-dev/farm_core/tests/__init__.py`:
```python
from . import test_consolidation_constraints
```

- [ ] **Step 4: Run test to verify it passes**

Run: `docker compose run --rm web odoo -d test_clean_db -i farm_core --test-enable --test-tags=TestConsolidationConstraints --stop-after-init --log-level=warn`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add farm_core/models/stock_quant_consolidation.py farm_core/tests/test_consolidation_constraints.py
git commit -m "feat: implement strict isolation and quality grade blocks on stock.quant"
```

---

### Task 3: Weighted Average Consolidation & DNA Decay Logic

**Files:**
- Modify: `farm_core/models/stock_quant_consolidation.py`
- Test: `farm_core/tests/test_weighted_average_decay.py`

**Interfaces:**
- Consumes: Quants added to a package under the `weighted_average` strategy.
- Produces: Dynamically recalculated container physical metrics (`current_weight`), sets `is_consolidated = True`, and decays the container's computed DNA pedigree score using the mixing entropy decay equation.

- [ ] **Step 1: Write the failing test**

Write `/Users/jeffery/odoo-farm-workspace/odoo-farm-dev/farm_core/tests/test_weighted_average_decay.py`:
```python
# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestWeightedAverageDecay(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(TestWeightedAverageDecay, cls).setUpClass()
        cls.Product = cls.env['product.product']
        cls.Category = cls.env['product.category']
        cls.Lot = cls.env['stock.lot']
        cls.Location = cls.env['stock.location']
        cls.Tracking = cls.env['stock.matter.tracking']
        cls.Quant = cls.env['stock.quant']

        cls.bulk_category = cls.Category.create({
            'name': 'Bulk Liquids',
            'consolidation_strategy': 'weighted_average',
            'allow_cross_quality_mix': True
        })

        cls.product_juice = cls.Product.create({
            'name': 'Raw Apple Juice',
            'categ_id': cls.bulk_category.id,
            'type': 'consu',
            'is_storable': True
        })

        cls.lot_apple_1 = cls.Lot.create({
            'name': 'LOT-APP-01',
            'product_id': cls.product_juice.id,
            'dna_integrity_score': 100.0
        })
        cls.lot_apple_2 = cls.Lot.create({
            'name': 'LOT-APP-02',
            'product_id': cls.product_juice.id,
            'dna_integrity_score': 80.0
        })

        cls.location_vat = cls.Location.create({
            'name': 'Vat Tank 10',
            'usage': 'internal'
        })

    def test_weighted_average_accumulates_and_decays_dna(self):
        tracking = self.Tracking.create({
            'vessel_phase': 'idle',
            'current_weight': 0.0,
            'is_consolidated': False
        })

        # 1. Load Lot 1 (100kg, DNA 100.0)
        self.Quant.create({
            'product_id': self.product_juice.id,
            'location_id': self.location_vat.id,
            'lot_id': self.lot_apple_1.id,
            'quantity': 100.0,
            'package_id': tracking.package_id.id
        })

        # 2. Load Lot 2 (200kg, DNA 80.0)
        self.Quant.create({
            'product_id': self.product_juice.id,
            'location_id': self.location_vat.id,
            'lot_id': self.lot_apple_2.id,
            'quantity': 200.0,
            'package_id': tracking.package_id.id
        })

        # Forces weight recomputation
        tracking._compute_physical_properties()

        # Expected weight = 100 + 200 = 300
        self.assertEqual(tracking.current_weight, 300.0)
        self.assertTrue(tracking.is_consolidated)

        # Expected DNA = ((100 * 100.0 + 200 * 80.0) / 300) * 0.90 = (26000 / 300) * 0.90 = 86.666 * 0.90 = 78.0
        # Wait, let's verify if DNA decay calculation executes automatically on write.
        self.assertAlmostEqual(tracking.dna_integrity_score, 78.0, places=1)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `docker compose run --rm web odoo -d test_clean_db -i farm_core --test-enable --test-tags=TestWeightedAverageDecay --stop-after-init --log-level=warn`
Expected: FAIL with weight not updating to 300 or DNA score not matching 78.0.

- [ ] **Step 3: Write minimal implementation**

Modify `/Users/jeffery/odoo-farm-workspace/odoo-farm-dev/farm_core/models/stock_quant_consolidation.py` to trigger tracking recalculations:
```python
# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import json

class StockQuant(models.Model):
    _inherit = 'stock.quant'

    @api.model_create_multi
    def create(self, vals_list):
        res = super(StockQuant, self).create(vals_list)
        for quant in res:
            if quant.package_id:
                tracking = self.env['stock.matter.tracking'].search([('package_id', '=', quant.package_id.id)], limit=1)
                if tracking:
                    tracking._recalculate_consolidation_properties()
        return res

    def write(self, vals):
        res = super(StockQuant, self).write(vals)
        for quant in self:
            if quant.package_id:
                tracking = self.env['stock.matter.tracking'].search([('package_id', '=', quant.package_id.id)], limit=1)
                if tracking:
                    tracking._recalculate_consolidation_properties()
        return res
```

Modify `/Users/jeffery/odoo-farm-workspace/odoo-farm-dev/farm_core/models/stock_matter_tracking.py` to calculate DNA Decay and Weight Summation:
```python
    def _recalculate_consolidation_properties(self):
        """ Recalculates total container weights and handles DNA decay calculations """
        for tracking in self:
            quants = self.env['stock.quant'].search([('package_id', '=', tracking.package_id.id)])
            if quants:
                total_weight = sum(quants.mapped('quantity'))
                tracking.current_weight = total_weight

                # Multi-lot checks
                unique_lots = quants.mapped('lot_id')
                if len(unique_lots) > 1:
                    tracking.is_consolidated = True
                    
                    # Compute DNA Decay if category allows mixing
                    category = unique_lots[0].product_id.categ_id
                    if category.consolidation_strategy == 'weighted_average':
                        weighted_sum = sum(q.quantity * (q.lot_id.dna_integrity_score or 100.0) for q in quants)
                        weighted_avg = weighted_sum / total_weight if total_weight else 0.0
                        # Apply 10% mixing entropy penalty
                        tracking.dna_integrity_score = weighted_avg * 0.90
                        
                        # Write JSON audit trail log
                        history = []
                        for q in quants:
                            history.append({
                                'lot': q.lot_id.name,
                                'qty': q.quantity,
                                'dna': q.lot_id.dna_integrity_score
                            })
                        tracking.consolidation_history = json.dumps(history)
```

Import tests in `/Users/jeffery/odoo-farm-workspace/odoo-farm-dev/farm_core/tests/__init__.py`:
```python
from . import test_weighted_average_decay
```

- [ ] **Step 4: Run test to verify it passes**

Run: `docker compose run --rm web odoo -d test_clean_db -i farm_core --test-enable --test-tags=TestWeightedAverageDecay --stop-after-init --log-level=warn`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add farm_core/models/stock_quant_consolidation.py farm_core/models/stock_matter_tracking.py farm_core/tests/test_weighted_average_decay.py
git commit -m "feat: implement DNA decay penalty and weighted average container recalculations"
```

---

### Task 4: Jidoka Security Interlocks & Locks Verification

**Files:**
- Modify: `farm_core/models/stock_quant_consolidation.py`
- Test: `farm_core/tests/test_jidoka_interlocks.py`

**Interfaces:**
- Consumes: Quants modified inside a locked, quarantined, or unreleased Vessel.
- Produces: Dynamic execution interrupts (raising `UserError` / `ValidationError`) blocking all physical transfers of the material.

- [ ] **Step 1: Write the failing test**

Write `/Users/jeffery/odoo-farm-workspace/odoo-farm-dev/farm_core/tests/test_jidoka_interlocks.py`:
```python
# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

class TestJidokaInterlocks(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(TestJidokaInterlocks, cls).setUpClass()
        cls.Product = cls.env['product.product']
        cls.Lot = cls.env['stock.lot']
        cls.Location = cls.env['stock.location']
        cls.Tracking = cls.env['stock.matter.tracking']
        cls.Quant = cls.env['stock.quant']

        cls.product_test = cls.Product.create({
            'name': 'Test Grain',
            'type': 'consu',
            'is_storable': True
        })

        cls.lot_grain = cls.Lot.create({
            'name': 'LOT-GRAIN-99',
            'product_id': cls.product_test.id
        })

        cls.location_silo = cls.Location.create({
            'name': 'Silo Sector Z',
            'usage': 'internal'
        })

    def test_locked_vessel_prevents_movements(self):
        tracking = self.Tracking.create({
            'vessel_phase': 'idle',
            'is_vessel_locked': True # Lock it physically
        })

        # Add physical quantities inside the locked vessel
        quant = self.Quant.create({
            'product_id': self.product_test.id,
            'location_id': self.location_silo.id,
            'lot_id': self.lot_grain.id,
            'quantity': 500.0,
            'package_id': tracking.package_id.id
        })

        # Attempting to change quantity or package should trigger a Jidoka lock raising ValidationError
        with self.assertRaisesRegex(ValidationError, "Vessel Lock"):
            quant.write({'quantity': 250.0})
```

- [ ] **Step 2: Run test to verify it fails**

Run: `docker compose run --rm web odoo -d test_clean_db -i farm_core --test-enable --test-tags=TestJidokaInterlocks --stop-after-init --log-level=warn`
Expected: FAIL (write completes with no ValidationError).

- [ ] **Step 3: Write minimal implementation**

Modify `/Users/jeffery/odoo-farm-workspace/odoo-farm-dev/farm_core/models/stock_quant_consolidation.py` to enforce Jidoka intercepts:
```python
# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class StockQuant(models.Model):
    _inherit = 'stock.quant'

    @api.constrains('quantity', 'package_id', 'location_id')
    def _check_jidoka_locks(self):
        for quant in self:
            if quant.package_id:
                tracking = self.env['stock.matter.tracking'].search([('package_id', '=', quant.package_id.id)], limit=1)
                if tracking:
                    # Mechanical Vessel Lock Interlock
                    if tracking.is_vessel_locked:
                        raise ValidationError(_("Jidoka Interlock Blocked: Vessel Lock is active on container %s. All movements and operations locked.") % tracking.name)
```

Import tests in `/Users/jeffery/odoo-farm-workspace/odoo-farm-dev/farm_core/tests/__init__.py`:
```python
from . import test_jidoka_interlocks
```

- [ ] **Step 4: Run test to verify it passes**

Run: `docker compose run --rm web odoo -d test_clean_db -i farm_core --test-enable --test-tags=TestJidokaInterlocks --stop-after-init --log-level=warn`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add farm_core/models/stock_quant_consolidation.py farm_core/tests/test_jidoka_interlocks.py
git commit -m "feat: enforce Jidoka locks and vessel lock validation constraints on stock.quant"
```
