# 🏭 工厂化渔业解决方案：维生系统竞技场 (The RAS LSS Arena)

## 1. 行业概览
*   **科学独特性**：RAS 是脱离自然环境的“孤立系统”。鱼类的排泄（Ammonia）与系统的清除（Bio-filter）必须实时平衡。电力是该系统的“氧气”，能效是该系统的“生命线”。
*   **核心痛点**：生化过滤器的崩溃具有滞后性、高频度的用电峰值导致运营成本极高。

## 2. 匹配模块与实施路径 (Capability Matching)

| 目标能力 | 匹配的已实现模块 | 实施路径 / 逻辑 |
| :--- | :--- | :--- |
| **维生系统建模** | `farm_core` | `farm.aquaculture.lss` 代理 `mrp.workcenter`，管理过滤组件。 |
| **代谢物门控** | `farm_quality` | 注入 `AgriQualityGateMixin`，将氨氮/亚硝酸盐设为 CCP。 |
| **能效分析** | `farm_core` | 注入 `AgriResourceConsumptionMixin` 计算单罐 kWh/kg。 |
| **生存模式防御** | `farm_ai_agent` | 通过 `AgriAgentInstructionMixin` 执行紧急降载与强制增氧。 |

## 3. DNA 基因注入清单
*   [x] **Level 1 (物理)**：`AgriResourceConsumptionMixin` (电力/水循环计量)
*   [x] **Level 2 (审计)**：`AgriQualityGateMixin` (水处理关键参数拦截)
*   [x] **Level 2 (决策)**：`AgriIncidentAlertMixin` (设备失效即时预警)
*   [x] **Level 4 (编排)**：`AgriAgentInstructionMixin` (变频泵与执行器联动)

## 4. 去工业化语义定义
*   `Work Center` -> **Life Support System (维生系统/机组)**
*   `Manufacturing Order` -> **Culture Batch Order (养殖批次单)**
*   `BOM` -> **RAS Technical Protocol (RAS 工艺规程)**
*   `Scrap` -> **Mortality / Sludge (死亡/污泥损耗)**

---
*最后更新：2026-02-01*
