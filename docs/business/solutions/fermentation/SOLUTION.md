# 🍶 传统发酵解决方案：时间、曲药与微生物的竞技场 (Fermentation Arena)

## 1. 行业概览
*   **科学独特性**：传统发酵（醋/酱/酒）是极其缓慢的生化过程。价值核心不在于生产速度，而在于“稳定性”与“时间溢价”。
*   **核心痛点**：由于曲药活性不均导致的烂窖风险、由于年份信息不透明导致的资产贬值。

## 2. 匹配模块与实施路径 (Capability Matching)

| 目标能力 | 匹配的已实现模块 | 实施路径 / 逻辑 |
| :--- | :--- | :--- |
| **窖池建模** | `farm_core` | `farm.fermentation.vessel` 代理 `mrp.workcenter`，注入空间 DNA。 |
| **发酵防御** | `farm_iot` | `handle_pit_telemetry` 处理品温数据，执行补偿动作。 |
| **年份增值** | `farm_core` | 注入 `AgriBiologicalValuationMixin` 实现时间杠杆估值。 |
| **全链路溯源** | `farm_core` | 继承 `AgriTraceabilityMixin` 实现从原粮到陶坛再到瓶装的哈希链。 |

## 3. DNA 基因注入清单
*   [x] **Level 1 (物理)**：`AgriTraceabilityMixin` (多轮次发酵链式哈希)
*   [x] **Level 2 (审计)**：`AgriQualityGateMixin` (氨基酸态氮/酒精度红线)
*   [x] **Level 3 (价值)**：`AgriBiologicalValuationMixin` (年份溢价模型)
*   [x] **Level 4 (编排)**：`AgriAgentInstructionMixin` (自动温控系统指令)

## 4. 去工业化语义定义
*   `Manufacturing Order` -> **Fermentation Job (发酵周期单)**
*   `BOM` -> **Brewing Protocol (酿造配方与工艺)**
*   `Work Center` -> **Fermentation Pit / Jar (窖池/陶坛)**
*   `Blending` -> **Goutiao (勾调)**

---
*最后更新：2026-02-01*
