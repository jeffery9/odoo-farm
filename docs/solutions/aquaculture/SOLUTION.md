# 🐟 水产业解决方案：实时环境驱动的隐形资产管理 (Real-time Water-Driven Arena)

## 1. 行业概览
*   **科学独特性**：水产养殖是三维空间的管理。资产处于水面之下，无法直接观测，必须高度依赖物理环境数据（水质）来间接评估生物状态。
*   **核心痛点**：溶解氧（DO）波动迅速，极易发生大规模死亡；饲料转化率（FCR）由于投喂过量难以优化。

## 2. 匹配模块与实施路径 (Capability Matching)

| 目标能力 | 匹配的已实现模块 | 实施路径 / 逻辑 |
| :--- | :--- | :--- |
| **水体建模** | `farm_core` | `farm.lot.aquaculture` 代理 `stock.lot`，持有水体体积属性。 |
| **环境防御** | `farm_iot` | `handle_aquaculture_telemetry` 处理溶氧数据流，触发 `on_damaged` 风格防御。 |
| **生物量预测** | `farm_livestock` | 复用 `AgriBiologicalInventoryMixin` 进行均重抽样与 Biomass 聚合。 |
| **智能增氧** | `farm_ai_agent` | 通过 `AgriAgentInstructionMixin` 下达增氧机开关指令。 |

## 3. DNA 基因注入清单
*   [x] **Level 1 (物理)**：`AgriBiologicalInventoryMixin` (池塘载荷计算)
*   [x] **Level 2 (决策)**：`AgriIncidentAlertMixin` (溶氧红线报警)
*   [x] **Level 4 (编排)**：`AgriAgentInstructionMixin` (结构化设备控制指令)

## 4. 去工业化语义定义
*   `Manufacturing Order` -> **Growth Order (养殖周期单)**
*   `BOM` -> **Stocking Recipe (放养与投喂方案)**
*   `Work Center` -> **Pond / Cage (池塘/网箱)**

---
*最后更新：2026-02-01*
