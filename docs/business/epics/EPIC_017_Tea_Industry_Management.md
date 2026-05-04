# EPIC 017:茶叶生产与精制管理 (Tea Industry Management)
*目标：建立从茶园采摘轮次到精制工艺控制的全链路闭环，通过数字化手段锁定“明前/雨前”等关键价值指纹。*

## 1. 用户故事 (User Stories)

1. **[US-017-01] 茶季与采摘轮次管理 (Seasonal Flush Tracking)**：💡 待实现
    - **描述**：作为茶园经理，我希望记录每一批鲜叶的采摘轮次（如明前、雨前）及其对应的海拔坐标。
    - **验收条件**：
        - **(DNA-Inheritance)** 采收批次自动继承地块的海拔与坡度指纹。
        - **(Logic)** 支持“茶季（Tea Season）”属性，作为品质分级的核心维度。

2. **[US-017-02] 茶叶精制工艺 Recipe 建模 (Processing Recipe)**：💡 待实现
    - **描述**：作为评茶师，我希望在配方中定义不同茶类（绿、红、乌龙）的工艺参数（如发酵时长、揉捻次数）。
    - **验收条件**：
        - **(ISL-Proxy)** `farm.tea.recipe` 代理 `mrp.bom`。
        - **(Parameters)** 包含 `fermentation_temp`, `rolling_pressure`, `moisture_target` 等参数。

3. **[US-017-03] 鲜叶到成品的多级溯源 (Multi-stage Traceability)**：💡 待实现
    - **描述**：作为消费者，我希望扫码后能看到该茶叶从哪片茶园采摘、由哪位工艺师揉捻、以及其生化指标。
    - **验收条件**：
        - **(Traceability)** 继承 `AgriTraceabilityMixin`，实现鲜叶批次到毛茶批次的 Hash 链式传递。

4. **[US-017-04] 茶叶等级与感官评审存证 (Sensory Evaluation)**：💡 待实现
    - **描述**：作为质检员，我希望记录干茶外形、汤色、香气、滋味及叶底的评分。
    - **验收条件**：
        - **(Mixin)** 继承 `AgriQualityGateMixin`，强制在入库前进行感官指标录入。

## 2. 业务价值
- **品牌背书**: 100% 的道地性与茶季存证可支撑高端地理标志（GI）茶叶价值。
- **工艺优化**: 通过关联工艺参数与最终口感得分，实现配方的 AI 辅助优化。

---
*最后更新：2026-02-01*
