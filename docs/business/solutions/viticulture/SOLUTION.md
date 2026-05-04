# 🍇 葡萄行业解决方案：从风土到杯中的数字闭环 (Terroir-to-Glass Arena)

## 1. 行业概览
*   **科学独特性**：葡萄是“时间与空间的艺术”。核心在于地块微气候（风土）与工艺干预（修剪、发酵）的耦合。
*   **核心痛点**：采收决策滞后导致糖酸失衡、多级加工过程中的溯源断裂。

## 2. 匹配模块与实施路径 (Capability Matching)

| 目标能力 | 匹配的已实现模块 | 实施路径 / 逻辑 |
| :--- | :--- | :--- |
| **风土档案** | `farm_core` | `farm.viticulture.plot` 代理 `farm.location`，注入 `GeoSpatialMixin`。 |
| **修剪计划** | `farm_operation` | `farm.viticulture.cycle` 代理 `mrp.production`，执行年度技术路线。 |
| **成熟度预测** | `farm_core` | 注入 `AgriGrowthCycleMixin`，基于 GDD 曲线预测 Brix 峰值。 |
| **压榨核销** | `farm_processing` | 利用 `yield_analysis.py` 逻辑计算出汁率。 |
| **全链路溯源** | `farm_core` | 继承 `AgriTraceabilityMixin`，实现鲜果 Hash 向原酒 Hash 的转换。 |

## 3. DNA 基因注入清单
*   [x] **Level 1 (物理)**：`GeoSpatialMixin` (坡向与风土坐标)
*   [x] **Level 1 (物理)**：`AgriGrowthCycleMixin` (糖分累积算法)
*   [x] **Level 2 (审计)**：`AgriQualityGateMixin` (糖酸比入库拦截)
*   [x] **Level 3 (价值)**：`AgriBiologicalValuationMixin` (基于产区等级的资产估值)

## 4. 去工业化语义定义
*   `Manufacturing Order` -> **Viticulture Cycle (葡萄培育周期)**
*   `BOM` -> **Cultural Itinerary (技术方案/配方)**
*   `Work Center` -> **Vineyard Block / Row (地块/行位)**

---
*最后更新：2026-02-01*
