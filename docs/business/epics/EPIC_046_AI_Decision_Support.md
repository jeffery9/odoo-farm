# EPIC 046:AI 智能决策支持 (AI Decision Support)
*版本: V1.0 | 状态: DRAFT | 归口: farm_ai_decision*

## 1. 核心愿景 (Core Vision)
构建农场的“智能参谋部”。AI 决策模块通过聚合科学底座（生理压力、发育进度）与物联遥测数据，自动生成补救性指令或生产计划调整建议，实现从“被动报警”到“主动决策”的跨越。

---

## 2. 用户故事集 (User Stories)

### **[US-046-01] 压力驱动的主动补救决策 (Stress-Driven Recovery)**
- **描述**: 作为农技主管，我希望当生物压力指数 (Stress Index) 超过阈值时，AI 能自动创建“补救任务”，以便最大限度挽回产量。
- **验收标准 (AC)**:
    - **(Logic)** 监控 `mrp.production` 中的 `biological_stress_index`。
    - **(Logic)** 当单日压力增量 > X 时，自动触发 `ai.decision.engine`。
    - **(Science-Driven)** 建议指令需包含具体的补救措施（如：增加灌溉时长以抵消高温压力）。
    *   **验收标准 (Acceptance Criteria)**:
        *   **AC1 (算法容错)**: 【压力驱动的主动补救决策 (Stress-Driven Recovery)】的 AI 推理请求必须配置合理的超时限制（Timeout），在引擎不可用时优雅降级。
        *   **AC2 (置信度防御)**: 当 AI 返回的置信度得分 (Confidence Score) 低于阈值时，必须强制转为“需人工复核”状态。
        *   **AC3 (数据隔离)**: 模型执行产生的数据结果必须与原始样本数据建立强关联溯源（Traceability）。


### **[US-046-02] 采收期动态预测与预售联动 (Dynamic Harvest Window)**
- **描述**: 作为销售经理，我希望 AI 根据当前的生理进度 (GDD) 和受压情况，给出精确的采收窗口预测。
- **验收标准 (AC)**:
    - **(Logic)** 计算 `Expected Harvest Date = Base Date + Physiological Delay (from Stress)`。
    - **(Science-Driven)** 预测结果自动同步至 `farm_marketing` 模块。
    *   **验收标准 (Acceptance Criteria)**:
        *   **AC1 (算法容错)**: 【采收期动态预测与预售联动 (Dynamic Harvest Window)】的 AI 推理请求必须配置合理的超时限制（Timeout），在引擎不可用时优雅降级。
        *   **AC2 (置信度防御)**: 当 AI 返回的置信度得分 (Confidence Score) 低于阈值时，必须强制转为“需人工复核”状态。
        *   **AC3 (数据隔离)**: 模型执行产生的数据结果必须与原始样本数据建立强关联溯源（Traceability）。


### **[US-046-03] 决策存证与“人机博弈”闭环 (Decision Audit)**
- **描述**: 作为架构师，我希望所有的 AI 建议必须经过人工审核（或自动信任评分），并记录完整的决策依据。
- **验收标准 (AC)**:
    - **(Level 2 Evidence)** AI 建议必须关联具体的 `agri.intervention.basis`。
    - **(UX)** 提供“接受/拒绝”交互，拒绝理由反馈至 AI 学习模型。

---
    *   **验收标准 (Acceptance Criteria)**:
        *   **AC1 (算法容错)**: 【决策存证与“人机博弈”闭环 (Decision Audit)】的 AI 推理请求必须配置合理的超时限制（Timeout），在引擎不可用时优雅降级。
        *   **AC2 (置信度防御)**: 当 AI 返回的置信度得分 (Confidence Score) 低于阈值时，必须强制转为“需人工复核”状态。
        *   **AC3 (数据隔离)**: 模型执行产生的数据结果必须与原始样本数据建立强关联溯源（Traceability）。


## 3. 核心算法对标 (Algorithm Alignment)
- **决策编排**: 对标 `docs/algorithms/AI_DECISION_ALGORITHM.md`。
- **风险评估**: 对标 `docs/algorithms/WEATHER_IMPACT_ALGORITHM.md`。

---
*V1.0 - The Intelligence Hub | 2026-02-01*
