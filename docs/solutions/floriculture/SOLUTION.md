# 🌸 花卉行业解决方案：智能温室竞技场 (Smart Greenhouse Arena)

## 1. 行业概览 (Executive Summary)
*   **科学独特性**：花卉生产是极度“感光”与“感温”的。其价值高度依赖于花期的精准控制（通过 DIF）以及采收后瓶插寿命（Vase-life）的预测。
*   **核心痛点**：环境细微变化导致的错峰开花风险，以及物流环节冷链断裂导致的毁灭性贬值。
*   **数字化目标**：建立“环境输入 -> 生理响应 -> 价值评估”的全链路数字孪生。

## 2. 匹配模块与实施路径 (Capability Matching)

| 目标能力 | 匹配的已实现模块 | 实施路径 / 逻辑 |
| :--- | :--- | :--- |
| **种苗供给** | `farm_breeding` | 复用 `farm.nursery.batch` 逻辑，通过移栽任务进入 `FarmFlowerOrder`。 |
| **开花配方** | `farm_isl` + `farm_core` | `farm.flower.bom` 代理 `mrp.bom`，注入 `NutrientMixin` 进行养分锁定。 |
| **生长控制** | `farm_operation` | `farm.flower.order` 继承干预框架，集成气象与积温拦截。 |
| **品质评估** | `farm_esg_compliance` | 注入 `AgriSustainabilityMixin` 进行 TBL 评分，计算瓶插寿命。 |
| **极致溯源** | `farm_core` | 注入 `AgriTraceabilityMixin` 为每一束花生成 SHA-256 指纹。 |
| **智能补光** | `farm_ai_agent` | 通过 `AgriAgentInstructionMixin` 向温室下达补光 JSON 指令。 |
| **采后保鲜** | `farm_processing` | `farm.flower.bom` 扩展保鲜液配方，集成吸水时长控制与 QCP。 |

## 3. 核心用户故事 (User Stories)

*   **[US-FLOR-01] 供给 DNA 继承**：✅ 已实现。种苗批次的积温与品种属性自动流转至生长订单。
*   **[US-FLOR-02] DIF 动态补足**：✅ 已实现。实时计算昼夜温差，环境缺口自动触发补光/控温“技能”。
*   **[US-FLOR-03] 瓶插寿命 (Vase-life) 动态评估**：✅ 已实现。基于采收阶段与冷链历史自动计算剩余寿命。
*   **[US-FLOR-04] 冷链红线防御拦截**：✅ 已实现。温度超标触发 `AgriIncidentAlertMixin` 并冻结资产。
*   **[US-FLOR-06] 采后保鲜配方管控**：✅ 已实现。定义保鲜剂浓度、吸水时长（Pulse Treatment），强制执行质量门控。

## 4. ISL 技术映射 (Technical Mapping)
*   **顶层代理**：`farm.flower.order` -> 代理 `mrp.production` (涵盖培育与保鲜两种指令类型)
*   **资产代理**：`farm.lot.flower` -> 代理 `stock.lot` (持有 Vase-life、冷链指纹及保鲜状态)
*   **属性扩展**：`actual_light_hours` (实时光照), `hydration_duration` (吸水时长), `preservative_concentration` (保鲜剂浓度)。

## 5. DNA 基因注入清单 (Genome Injection)
*   [x] **Level 1 (物理)**：`AgriGrowthCycleMixin` (生理阶段自动迁移)
*   [x] **Level 1 (物理)**：`AgriTraceabilityMixin` (溯源哈希)
*   [x] **Level 2 (决策)**：`AgriWeatherSensitiveMixin` (气象安全拦截)
*   [x] **Level 2 (决策)**：`AgriIncidentAlertMixin` (异常实时报警)
*   [x] **Level 4 (编排)**：`AgriAgentInstructionMixin` (结构化指令派发)

## 6. 去工业化语义定义 (Semantics)
*   `Manufacturing Order` -> **Growing Order (培育订单)**
*   `BOM` -> **Bloom Recipe (开花配方)**
*   `Work Center` -> **Greenhouse Slot (温室库位)**
*   `Work Order` -> **Nurturing Activity (育花活动)**

---
*最后更新：2026-02-01*
