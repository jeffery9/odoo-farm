# 🍄 食用菌解决方案：基质驱动的精密环境竞技场 (Substrate-Driven Arena)

## 1. 行业概览
*   **科学独特性**：食用菌是“非光合作用”农业。其能量全部来源于基质。生长过程极度依赖对二氧化碳（呼吸作用）和空气湿度的精准干预。
*   **核心痛点**：杂菌污染难以早期识别、不同潮次采收逻辑混乱、环境参数偏差导致的“只长菌丝不开伞”。

## 2. 匹配模块与实施路径 (Capability Matching)

| 目标能力 | 匹配的已实现模块 | 实施路径 / 逻辑 |
| :--- | :--- | :--- |
| **菌包资产化** | `farm_core` | `farm.mushroom.batch` 代理 `stock.lot`，持有品种与发菌状态。 |
| **基质养分** | `farm_core` | 注入 `NutrientMixin` 核算 C/N 比。 |
| **潮次管理** | `farm_operation` | `farm.mushroom.production` 实现多潮次采收与生物转化率分析。 |
| **环境防御** | `farm_iot` | `handle_mushroom_telemetry` 处理 CO2/湿度流，触发主动通风。 |

## 3. DNA 基因注入清单
*   [x] **Level 1 (物理)**：`AgriGrowthCycleMixin` (菌丝定植进度)
*   [x] **Level 2 (审计)**：`AgriQualityGateMixin` (灭菌/杂菌率门控)
*   [x] **Level 4 (编排)**：`AgriAgentInstructionMixin` (通风/喷雾设备指令)

## 4. 去工业化语义定义
*   `Manufacturing Order` -> **Fruiting Cycle (出菇周期)**
*   `BOM` -> **Substrate Formula (基质配方)**
*   `Work Center` -> **Growing Room / Shelf (出菇房/架位)**

---
*最后更新：2026-02-01*
