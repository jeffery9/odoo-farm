# 🧪 精油行业解决方案：高价值提取动力学 (High-Value Extraction Arena)

## 1. 行业概览
*   **科学独特性**：精油是生物质能的极致浓缩。生产过程是一个复杂的相变与分离过程。其价值完全由“成分指纹”和“提取合规性”定义。
*   **核心痛点**：大规模原材料投入与微量产出之间的核销对账极难、工艺参数波动导致的成分降解。

## 2. 匹配模块与实施路径 (Capability Matching)

| 目标能力 | 匹配的已实现模块 | 实施路径 / 逻辑 |
| :--- | :--- | :--- |
| **精制 Recipe** | `farm_agricultural_processing` | `farm.essential_oil.recipe` 代理 `mrp.bom`，锁定温压参数。 |
| **提取率审计** | `farm_operation` | 在 `FarmEssentialOilProduction` 中实现投入产出自动核销。 |
| **DNA 链式继承** | `farm_core` | 利用 `AgriTraceabilityMixin` 实现多来源批次哈希聚合。 |
| **品质门控** | `farm_core` | 注入 `AgriQualityGateMixin` 进行 GC-MS 成分合规性拦截。 |

## 3. DNA 基因注入清单
*   [x] **Level 1 (物理)**：`AgriTraceabilityMixin` (从大宗植物到微量精油的溯源)
*   [x] **Level 1 (物理)**：`NutrientMixin` (原材料干物质/水分核算)
*   [x] **Level 2 (审计)**：`AgriQualityGateMixin` (化学成分阈值门控)
*   [x] **Level 3 (价值)**：`AgriBiologicalValuationMixin` (基于提取率与成分的资产重估)

## 4. 去工业化语义定义
*   `Manufacturing Order` -> **Distillation Order (蒸馏指令)**
*   `BOM` -> **Extraction Protocol (提取规范)**
*   `Work Center` -> **Extraction Station / Still (提取位/蒸馏釜)**

---
*最后更新：2026-02-01*
