# 🌾 大田作物解决方案：精准规模化农业 (Precision Field Crops)

## 1. 行业概览
*   **科学独特性**：大田作物是保障粮食安全的核心。其成功取决于对“水、肥、气、热”四大因子的规模化调度，以及基于变量算法（VRA）的投入品优化。
*   **核心痛点**：由于地块异质性导致的资源浪费，以及对极端气象灾害的响应迟缓。
*   **数字化目标**：通过生产季驱动的干预工作流，实现地块级养分平衡与作业合规审计。

## 2. 匹配模块与实施路径

| 目标能力 | 匹配的已实现模块 | 实施路径 / 逻辑 |
| :--- | :--- | :--- |
| **生产季管理** | `farm_operation` | 复用 `farm.agricultural.campaign` 逻辑，管理年度轮作。 |
| **地块养分核销** | `farm_core` | 注入 `NutrientMixin`，实现施肥量与土壤缺口的实时抵扣。 |
| **变量作业 (VRA)** | `farm_operation` | 结合 `AgriAgentInstructionMixin` 向农机派发精准施肥 JSON 指令。 |
| **作业红线监控** | `farm_core` | 注入 `AgriWeatherSensitiveMixin` 拦截风速超标时的喷洒作业。 |
| **碳足迹核算** | `farm_esg_carbon` | 基于 `AgriResourceConsumptionMixin` 记录的燃油量自动计算每吨粮食排放。 |

## 3. 核心用户故事 (User Stories)

*   **[US-CROP-01] 生产季任务自动排期**：根据品种积温需求，自动在日历上排布播种与采收窗口。
*   **[US-CROP-02] 变量施肥指令闭环**：基于土壤处方图生成的结构化指令，由农机执行并实时回传实际施用量。
*   **[US-CROP-03] 地块级品质指纹**：收获批次（Lot）自动继承地块的土质、施肥历程及气象历史。
*   **[US-CROP-04] 作业合规性空间审计**：通过 `GeoSpatialMixin` 自动计算农机作业的轨迹合规率。

## 4. DNA 基因注入清单
*   [x] **Level 1 (物理)**：`NutrientMixin` (养分平衡)
*   [x] **Level 1 (物理)**：`AgriResourceConsumptionMixin` (机械能耗)
*   [x] **Level 2 (决策)**：`AgriWeatherSensitiveMixin` (气象拦截)
*   [x] **Level 4 (编排)**：`AgriAgentInstructionMixin` (VRA 指令)

## 5. 去工业化语义定义
*   `Manufacturing Order` -> **Crop Production Order (种植订单)**
*   `BOM` -> **Input Recipe (投入品配方)**
*   `Work Center` -> **Field Plot / Zone (田块/分区)**

---
*最后更新：2026-02-01*
