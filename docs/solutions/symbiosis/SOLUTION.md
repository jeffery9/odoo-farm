# 🌾🐟 稻渔共生解决方案：生态协同竞技场 (The Symbiosis Arena)

## 1. 行业概览
*   **科学独特性**：稻渔系统是一个“双维耦合”系统。水产提供了肥力与除草能力，水稻提供了遮蔽与水质净化。系统的核心是“平衡”——任何偏向一方的过度干预（如重肥重药）都会导致另一方的系统崩溃。
*   **核心痛点**：施药风险难控、共生价值无法量化。

## 2. 匹配模块与实施路径 (Capability Matching)

| 目标能力 | 匹配的已实现模块 | 实施路径 / 逻辑 |
| :--- | :--- | :--- |
| **共生地块** | `farm_core` | `farm.symbiotic.plot` 代理 `farm.location`，集成地块与环沟。 |
| **共生配方** | `farm_isl` | `farm.symbiotic.recipe` 代理 `mrp.bom`，核算循环养分。 |
| **药害拦截** | `farm_safety` | 在 `FarmSymbioticOrder` 中注入 `AgriQualityGateMixin`。 |
| **复合收获** | `farm_operation` | 复用 `multi_output` 逻辑分别产生稻米与鱼虾批次。 |

## 3. DNA 基因注入清单
*   [x] **Level 1 (物理)**：`NutrientMixin` (鱼粪换算肥力)
*   [x] **Level 2 (审计)**：`AgriQualityGateMixin` (高毒农药硬拦截)
*   [x] **Level 1 (物理)**：`AgriTraceabilityMixin` (双物种互链哈希)
*   [x] **Level 2 (决策)**：`AgriWeatherSensitiveMixin` (高温缺氧对共生系统的威胁)

## 4. 去工业化语义定义
*   `Manufacturing Order` -> **Symbiotic Cycle (共生周期单)**
*   `BOM` -> **Co-culture Recipe (共生方案)**
*   `Work Center` -> **Symbiotic Field (稻渔田)**

---
*最后更新：2026-02-01*
