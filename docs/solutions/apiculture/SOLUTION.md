# 🐝 养蜂业解决方案：移动的授粉与能量采集引擎 (Mobile Foraging Arena)

## 1. 行业概览
*   **科学独特性**：养蜂是高度“动态”的农业。蜂箱位置随花期全球移动，且资产（蜜蜂）处于半开放状态。其价值核心在于“蜂群强度”与“蜜源环境”的匹配。
*   **核心痛点**：转场路径规划难、蜂群健康黑盒（分蜂/疾病）、蜂蜜蜜源掺假。

## 2. 匹配模块与实施路径 (Capability Matching)

| 目标能力 | 匹配的已实现模块 | 实施路径 / 逻辑 |
| :--- | :--- | :--- |
| **蜂群资产化** | `farm_core` | `farm.lot.hive` 代理 `stock.lot`，持有蜂群 DNA。 |
| **蜜源空间追踪** | `farm_core` | 注入 `GeoSpatialMixin` 实现蜂场坐标与采集半径分析。 |
| **转场调度** | `farm_operation` | 复用 `stock.transfer` 逻辑管理蜂箱跨地块迁徙。 |
| **品质门控** | `farm_processing` | 注入 `AgriQualityGateMixin` 核验蜂蜜波美度与理化指标。 |

## 3. DNA 基因注入清单
*   [x] **Level 1 (物理)**：`AgriBiologicalInventoryMixin` (蜂群数、死亡率)
*   [x] **Level 1 (物理)**：`GeoSpatialMixin` (蜂场 GIS 缓冲区)
*   [x] **Level 2 (审计)**：`AgriQualityGateMixin` (分级与理化门控)
*   [x] **Level 4 (编排)**：`AgriAgentInstructionMixin` (转场 GPS 路由指令)

## 4. 去工业化语义定义
*   `Manufacturing Order` -> **Honey Flow Order (采蜜周期单)**
*   `BOM` -> **Foraging Strategy (蜜源与补饲策略)**
*   `Work Center` -> **Apiary/Site (蜂场/场地位)**
*   `Work Order` -> **Hive Inspection (开箱检查)**

---
*最后更新：2026-02-01*
