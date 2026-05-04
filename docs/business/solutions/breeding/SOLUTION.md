# 🧪 育种与苗圃解决方案：农业芯片工厂 (Breeding & Nursery Engine)

## 1. 行业概览
*   **科学独特性**：育种是高价值、高风险的起始环节。核心价值在于遗传谱系的纯正度以及苗圃阶段对生理状态（苗龄、壮苗指数）的精准控制。
*   **核心痛点**：遗传档案断裂导致品种退化，以及移栽环节由于苗龄不匹配导致的规模化死亡。
*   **数字化目标**：建立“亲本 -> 种子 -> 种苗”的全链路溯源，并实现基于成活率的供给侧自动转换计算。

## 2. 匹配模块与实施路径

| 目标能力 | 匹配的已实现模块 | 实施路径 / 逻辑 |
| :--- | :--- | :--- |
| **谱系追踪** | `farm_core` | 注入 `AgriTraceabilityMixin`，基于父/母本哈希生成子代指纹。 |
| **苗圃管理** | `farm_breeding` | `farm.nursery.batch` 代理 `stock.lot`，记录苗龄与成活率。 |
| **性状打分** | `farm_ai_core` | 注入 `EvidenceAnalyzerMixin` 对表型性状（Phenotype）进行双重置信度评估。 |
| **移栽联动** | `farm_operation` | 通过 `action_create_transplant_task` 自动生成大田干预任务。 |
| **自动核销** | `farm_core` | 注入 `AgriBiologicalInventoryMixin` 实时核销损耗与死苗。 |

## 3. 核心用户故事 (User Stories)

*   **[US-BREED-01] 亲本溯源指纹**：每一批种苗必须持有父本与母本的溯源 Hash，确保遗传链条完整。
*   **[US-BREED-02] 壮苗指数与苗龄监控**：基于积温（GDD）实时计算种苗生理状态，自动预警最佳移栽窗口。
*   **[US-BREED-03] 供给转换预测**：根据当前苗圃存活率，动态预测可覆盖的大田面积（mu/ha）。
*   **[US-BREED-04] 性状实验室联动**：记录实验室检测数据（发芽率、抗性测试），作为批次入库的质量门控（QCP）。

## 4. DNA 基因注入清单
*   [x] **Level 1 (物理)**：`AgriGrowthCycleMixin` (苗龄与生理阶段)
*   [x] **Level 1 (物理)**：`AgriBiologicalInventoryMixin` (数量与成活率)
*   [x] **Level 1 (物理)**：`AgriTraceabilityMixin` (遗传谱系哈希)
*   [x] **Level 2 (审计)**：`AgriQualityGateMixin` (实验室准入拦截)

## 5. 去工业化语义定义
*   `Manufacturing Order` -> **Nursery Order (育苗指令)**
*   `BOM` -> **Variety Recipe (品种配方)**
*   `Work Center` -> **Nursery Bed / Shelf (苗床/育苗架)**

---
*最后更新：2026-02-01*
