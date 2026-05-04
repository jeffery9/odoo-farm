# 🥗 净菜行业解决方案：极速转化与安全透明 (Net Veg Speed & Safety)

## 1. 行业概览
*   **科学独特性**：净菜加工是一个“高频、低毛利、高风险”的过程。重点在于将分散的农业产出快速标准化为确定性的商品单元。
*   **核心痛点**：损耗对账混乱、短保质期带来的库存风险、多级包装关联断裂。

## 2. 匹配模块与实施路径 (Capability Matching)

| 目标能力 | 匹配的已实现模块 | 实施路径 / 逻辑 |
| :--- | :--- | :--- |
| **损耗核销** | `farm_agricultural_processing` | 在 `FarmNetVegProduction` 中实现 `yield_analysis.py` 逻辑。 |
| **多级包装** | `farm_agricultural_processing` | 利用 `packaging_hierarchy.py` 实现“袋-筐-托”代理关系。 |
| **洗消门控** | `farm_core` | 注入 `AgriQualityGateMixin` 进行消毒液浓度红线校验。 |
| **全链路溯源** | `farm_core` | 继承 `AgriTraceabilityMixin` 实现从地块到包装袋的哈希传递。 |

## 3. DNA 基因注入清单
*   [x] **Level 1 (物理)**：`AgriTraceabilityMixin` (批次指纹继承)
*   [x] **Level 1 (物理)**：`AgriResourceConsumptionMixin` (清洗用水/预冷能耗)
*   [x] **Level 2 (审计)**：`AgriQualityGateMixin` (食品安全红线拦截)

## 4. 去工业化语义定义
*   `Manufacturing Order` -> **Preparation Order (净菜加工单)**
*   `BOM` -> **Processing Standard (加工标准)**
*   `Work Center` -> **Prep Station / Packaging Line (切配台/包装线)**

---
*最后更新：2026-02-01*
