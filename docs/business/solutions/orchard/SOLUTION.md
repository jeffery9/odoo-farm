# 🍎 果园与园艺解决方案：数字孪生果园 (Digital Twin Orchard)

## 1. 行业概览
*   **科学独特性**：果园是高价值、长周期的生物工厂。单株树木的健康状况、历年产量趋势及精确的采收时间（Maturity Window）决定了最终收益。
*   **核心痛点**：单株精细化管理成本高，采收期预测不准导致货架期缩短。
*   **数字化目标**：建立“一树一码”的空间档案，实现基于积温的成熟度自动预警。

## 2. 匹配模块与实施路径

| 目标能力 | 匹配的已实现模块 | 实施路径 / 逻辑 |
| :--- | :--- | :--- |
| **树木资产化** | `farm_core` | `farm.orchard.asset` 代理 `stock.lot`，持有品种 DNA。 |
| **单株 GIS** | `farm_core` | 注入 `GeoSpatialMixin` 实现树位的厘米级高精度定位。 |
| **培育路线** | `farm_operation` | `farm.orchard.cycle` 代理 `mrp.production`，执行年度修剪计划。 |
| **成熟度预测** | `farm_core` | 注入 `AgriGrowthCycleMixin`，基于积温驱动转色期预测。 |
| **资产估值** | `farm_financial_valuation` | 注入 `AgriBiologicalValuationMixin`，随树龄增长动态重估资产价值。 |

## 3. 核心用户故事 (User Stories)

*   **[US-ORCH-01] 一树一码空间档案**：在地图上可视化每一株果树，记录品种、定植日期及健康评分。
*   **[US-ORCH-02] 积温驱动采收预警**：系统根据实时气象数据自动更新积温进度，提前 7 天发出采收通知。
*   **[US-ORCH-03] 年度修剪与干预闭环**：记录冬季修剪、夏季疏果动作，并自动关联至该树位的产量分析。
*   **[US-ORCH-04] 多年生资产动态估值**：根据树龄（幼龄期、初果期、盛果期、衰老期）自动调整财务估值。

## 4. DNA 基因注入清单
*   [x] **Level 1 (物理)**：`GeoSpatialMixin` (高精度树位)
*   [x] **Level 1 (物理)**：`AgriGrowthCycleMixin` (生长进度与积温)
*   [x] **Level 2 (决策)**：`AgriWeatherSensitiveMixin` (花期防霜冻拦截)
*   [x] **Level 3 (价值)**：`AgriBiologicalValuationMixin` (多年生资产价值重估)

## 5. 去工业化语义定义
*   `Manufacturing Order` -> **Nurturing Cycle (培育周期)**
*   `BOM` -> **Cultural Itinerary (技术路线)**
*   `Work Center` -> **Orchard Row/Slot (果园行/位)**

---
*最后更新：2026-02-01*
