# Dual-Axis Consolidation Strategy & Jidoka Interlocks Specification
# 双轨合并策略与 Jidoka 物理安全防错连锁技术规范

**Document ID:** `SPEC-2026-08-09-DUAL-AXIS-CONSOLIDATION`  
**Status:** Approved (已批准)  
**Date:** 2026-08-09  
**Author:** Gemini CLI (Execution Agent)  
**Collaborative Partner:** ChatGPT (Principal Architect)  

---

## 1. Executive Summary / 执行摘要

This specification defines the architectural and mathematical rules for the **Dual-Axis Consolidation Strategy Engine** and **Jidoka Interlocks** in the Odoo Farm Workspace. 
To preserve the logical boundary between the **Static Genotype Axis (`stock.lot`)** and the **Dynamic Physical Axis (`stock.matter.tracking`)**, this engine dynamically resolves material mixing, DNA heritage decay, and physical/safety constraints during inventory movement and processing.

本规范定义了 Odoo Farm 空间下**双轨合并策略引擎**与 **Jidoka 物理防错连锁**的架构与数学计算规则。
为了维护**静态基因轨 (`stock.lot`)**与**动态物理轨 (`stock.matter.tracking`)**的逻辑边界，本引擎在底层库存流转与生产加工时，动态解析物料并箱混合、基因完整性衰减，以及物理/安全连锁约束。

---

## 2. Traceability Alignment Matrix / 追溯对齐矩阵

```
  +───────────────────────────────────────────────────────────+
  │                      STATIC GENOTYPE                      │
  │                 (静态基因轴 - Identity Track)              │
  │                  Represented by: stock.lot                │
  │                                                           │
  │   - DNA Pedigree (亲缘谱系)                                │
  │   - Compliance Credentials (认证资质)                     │
  │   - Quality Grade (质量等级)                              │
  +──────────────────────────────┬────────────────────────────+
                                 │
                     (Linked via Active Quants)
                                 │
  +──────────────────────────────▼────────────────────────────+
  │                     DYNAMIC Carrier                       │
  │                 (动态物质轴 - Carrier Track)               │
  │             Represented by: stock.matter.tracking         │
  │                                                           │
  │   - Live Weight / Bulk Tonnage (实时重/均重)                │
  │   - Life Stage / Biological Stage (生命/生物阶段)          │
  │   - GPS Real-time Coordinates (空间地理围栏)               │
  │   - CIP Sanitization Phase (洗消状态)                     │
  +───────────────────────────────────────────────────────────+
```

---

## 3. Product Category Metadata Extensions / 产品类别元数据扩展

The merging behavior of physical carriers (Matter Tracking) is fully driven by metadata stored at the **Product Category (`product.category`)** level. This respects Odoo’s native ORM-first hierarchy.

物理载体（Matter Tracking）的合并并箱行为完全由**产品类别（`product.category`）**上存储的元数据进行声明式驱动，这高度契合 Odoo 原生 ORM 继承树。

### 3.1 Field Declarations / 字段声明

```python
class ProductCategory(models.Model):
    _inherit = 'product.category'

    consolidation_strategy = fields.Selection([
        ('strict_isolation', 'Strict Isolation (Single-Lot Only)'),
        ('weighted_average', 'Weighted Average (Bulk & Liquid Mixing)'),
        ('multi_lot_package', 'Multi-Lot Pack (Co-existence in Package)')
    ], string="Consolidation Strategy", default='strict_isolation', required=True,
       help="Defines how physical carriers (Matter Tracking) handle multiple batches (Lots) entering the same container.")

    allow_cross_quality_mix = fields.Boolean(
        string="Allow Cross-Quality Mixing", default=False,
        help="If False, lots with different Quality Grades (e.g. Grade A & Grade B) cannot be consolidated, even under weighted average.")
```

### 3.2 Consolidation Strategies / 合并策略定义

1.  **`strict_isolation` (严格物理隔离 - 适用于高价值种苗、种猪、特定医药原材料)：**
    *   One physical carrier (`stock.matter.tracking`) can contain at most ONE lot.
    *   Any attempt to consolidate multiple lots triggers a `ValidationError` and blocks the transaction.
2.  **`weighted_average` (权重均值合并 - 适用于散装、液态及初级农产品，如苹果汁、谷物、饲料)：**
    *   Weights and physical counts are accumulated automatically.
    *   Chemical and nutrient attributes are computed via weighted averages based on input lot weights.
3.  **`multi_lot_package` (多批次混装包裹 - 适用于托盘、集装周转箱、成品包装货架)：**
    *   Lots co-exist independently within the same parent Matter package.
    *   They maintain distinct weights, but share the GPS positioning and biological stage of the outer carrier.

---

## 4. Mathematical Consolidation Logic / 数学合并逻辑

When two or more lots are consolidated under the **`weighted_average`** strategy, the physical attributes accumulate, and the genetic pedigree undergoes a decay penalty to account for mixing entropy.

当两个及以上批次在 `weighted_average` 策略下合并时，物理属性发生物理累加，而基因谱系因“混合熵（Mixing Entropy）”发生衰减：

### 4.1 Weight & Item Accumulation / 重量与数量累加

$$\text{New Weight} = \sum_{i=1}^{n} \text{Weight}_i$$
$$\text{New Item Count} = \sum_{i=1}^{n} \text{Count}_i$$

### 4.2 DNA Integrity Score Decay Formula / DNA 完整性衰减公式

To represent the trace degradation caused by blending different sources, the new DNA integrity score is calculated using a weighted average of the original lots, multiplied by a **10% Mixing Entropy Penalty (10% 混合熵惩罚)**:

为了表达混合不同源头造成的追溯力损耗，新 DNA 完整性评分由合并前各批次的原重量占比加权计算，并扣减 **10% 的物理合并熵惩罚**：

$$\text{DNA}_{\text{new}} = \left( \frac{\sum_{i=1}^{n} (\text{Weight}_i \times \text{DNA}_i)}{\sum_{i=1}^{n} \text{Weight}_i} \right) \times 0.90$$

---

## 5. Jidoka Physical Safety Interlocks / Jidoka 物理防错连锁

The Matter Tracking container acts as the physical gatekeeper. If the container is in an unsafe state, all inventory moves (`stock.move` or `stock.quant` writes) of the contained materials are locked.

物质跟踪容器充当物理网关。若容器处于不安全状态，其装载物料的所有库存变动（`stock.move` 或 `stock.quant` 写入）将被锁死。

```
                       [ Inventory Transaction / Stock Move ]
                                         │
                         (Reads Jidoka Interlock States)
                                         │
                 ┌───────────────────────┼───────────────────────┐
                 ▼                       ▼                       ▼
         [Vessel Locked?]        [Clean-Hold Active?]    [Moisture Target Met?]
                 │                       │                       │
           - Is True               - Within 24h of CIP     - Sensor < Target %
                 │                       │                       │
                 ▼                       ▼                       ▼
           【BLOCK & ERROR】       【BLOCK & ERROR】       【BLOCK & ERROR】
```

1.  **Vessel Mechanical Lock (罐体物理锁)**:
    If `is_vessel_locked` is `True`, all writes and transfers targeting its linked package are rejected with a `UserError`.
2.  **Clean-Hold Window Guard (洗消时效锁)**:
    After a CIP cleaning cycle completes (`action_complete_cleaning`), the vessel enters a mandatory 24-hour clean-hold window. During this window, any raw material input or mixing is blocked to prevent residue contamination.
3.  **MSL Moisture Interlock (水分安全锁)**:
    During drying or dehydration stages, the material can only be transferred or packaged once the IoT telemetry moisture percentage falls below the target parameter threshold.

---

## 6. Three-Second Visual Management / 3秒目视化管理控制台

To ensure high-signal visual awareness for workshop operators, the Matter Tracking Cockpit features an adaptive header banner:

为了确保车间操作员的高信号状态感知，Matter Tracking 控制台配备了自适应的 Banner 顶栏：

*   🔴 **Critical / Locked (红色 - 物理锁死)**: Vessel is locked (`is_vessel_locked = True`) or quarantined by a crisis incident (`is_crisis_locked = True`). Move/Transformation actions are physically disabled in the UI.
*   🟡 **Warning / Active (黄色 - 处理中/过渡态)**: Material undergoes a `weighted_average` calculation, or the vessel is currently in the 24-hour Clean-Hold phase.
*   🟢 **Normal / Ready (绿色 - 空闲就绪)**: Vessel is sanitarily clean, open, and ready to accept compliant lot registration or physical transfer.
