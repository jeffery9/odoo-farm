# EPIC 022:食用菌生产与环境精准控制管理 (Mushroom Smart Management)
*目标：建立基于基质配方优化与多潮次产量追踪的数字化菌类养殖体系，通过 IoT 联动实现对出菇环境的极致门控。*

## 1. 用户故事 (User Stories)

1. **[US-022-01] 菌包批次数字孪生 (Mushroom Batch Life-log)**：✅ 已实现 (2026-02-01)
    - **描述**：作为技术员，我希望记录每个菌包批次的品种、接种日期、发菌状态及杂菌污染记录。
    - **验收条件**：
        - **(ISL-Proxy)** `farm.mushroom.batch` 代理 `stock.lot`。
        - **(DNA-Injection)** 继承 `AgriGrowthCycleMixin` 追踪菌丝填充进度。
        - **(Sanity)** 记录 `contamination_rate` 并触发异常预警。

2. **[US-022-02] 基质配方与灭菌参数建模 (Substrate Recipe)**：✅ 已实现 (2026-02-01)
    - **描述**：作为工艺师，我希望在 Recipe 中定义培养料的 C/N 比、含水量及灭菌温度时长。
    - **验收条件**：
        - **(Logic)** 继承 `NutrientMixin` 核算基质养分。
        - **(ISL-Gate)** 继承 `AgriQualityGateMixin` 强制核验灭菌温度达标记录。

3. **[US-022-03] 出菇期多潮次产量核销 (Flush Yield Tracking)**：✅ 已实现 (2026-02-01)
    - **描述**：作为场长，我希望分别记录每一批次在不同潮次（1st, 2nd, 3rd Flush）的采收重量与品质。
    - **验收条件**：
        - **(Workflow)** `farm.mushroom.production` 代理 `mrp.production`。
        - **(Math)** 自动计算“生物转化率 (Biological Efficiency)”。

4. **[US-022-04] 环境因子（CO2/湿/温）主动防御**：✅ 已实现 (2026-02-01)
    - **描述**：作为运维人员，我希望当出菇房 CO2 浓度过高时，系统自动执行通风指令。
    - **验收条件**：
        - **(Skill)** 类似 `apply_aeration_skill`，触发通风设备 Agent 指令。
        - **(Alert)** 异常环境数据触发 `AgriIncidentAlertMixin`。

## 2. 业务价值
- **良品率提升**: 将发菌期杂菌报废率降低 15%。
- **产量优化**: 通过精确的潮次评估，将生物转化率（BE）提升 10% 以上。
- **能源节约**: 自动化的环境联动减少 20% 的不必要通风能耗。

---
*最后更新：2026-02-01*
