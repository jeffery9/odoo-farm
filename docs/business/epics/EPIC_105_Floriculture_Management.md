# 史诗 105：花卉与观赏园艺管理 (Floriculture & Ornamental Horticulture)
*目标：建立科学的花卉生长与开花控制体系，通过精准的环境干预（DIF、GDD）延长瓶插寿命，并利用物联网（IoT）实现极致冷链溯源。*

> **架构定义**: 本史诗深度利用 ISL 层（`farm.flower.order`）和 DNA 基因库（积温、质量门控、异常预警），将工业化生产流程彻底重构为环境驱动的生物资产培育模型。

## 1. 用户故事 (User Stories)

1. **[US-105-01] DIF 驱动的开花诱导配方 (DIF-Driven Bloom Recipe)**：✅ 已实现 (2026-02-01)
    - **描述**：作为花艺师，我希望在 Recipe (Recipe) 中通过 **昼夜温差 (DIF)** 来控制花茎长度和花期。
    - **验收条件**：
        - **(Logic)** 必须支持 `target_temp_diff` (DIF) 的自动计算：`DIF = Day_Temp - Night_Temp`。
        - **(Horticulture)** 提供正 DIF（促长）与负 DIF（抑长）的参数化配置。
        - **(Template)** 预置月季、百合、郁金香的感光/感温标准配方。

2. **[US-105-02] 动态积温 (GDD) 生理阶段预测**：✅ 已实现 (2026-02-01)
    - **描述**：作为生产主管，我希望系统结合气象预报实时预测开花日期，并根据积温进度自动迁移生理阶段。
    - **验收条件**：
        - **(Algorithm)** 继承 `AgriGrowthCycleMixin`，实时计算 `accumulated_gdd`。
        - **(Auto-Migration)** 当 `stage_progress` 达到 100% 时，系统必须自动触发 `current_stage_id` 的迁移并记录 Chatter。
        - **(Dashboard)** 可视化展示“预计开花窗口”与实际积温曲线的偏差。

3. **[US-105-03] 基于采收状态的瓶插寿命 (Vase-life) 智能预测**：✅ 已实现 (2026-02-01)
    - **描述**：作为质检员，我希望系统在采收时根据“开花阶段”和“初始冷芯温度”自动评估花卉的货架期。
    - **验收条件**：
        - **(Calculation)** `predicted_vase_life = Base_Life(14d) - Stage_Penalty - Temp_Stress_Penalty`。
        - **(Traceability)** 预测寿命必须写入 `AgriTraceabilityMixin` 的数字指纹中，供下游零售商查验。
        - **(Gate)** 若预测寿命低于 3 天，质量门控（`AgriQualityGateMixin`）必须自动拦截该批次的入库确认。

4. **[US-105-04] IoT 触发的冷链红线拦截与预警**：✅ 已实现 (2026-02-01)
    - **描述**：作为物流经理，我希望通过 IoT 传感器实现“断链即拦截”，任何环境红线被触发时自动冻结批次。
    - **验收条件**：
        - **(IoT-Integration)** 接收来自 `industrial_iot` 的温度数据流。
        - **(Hard-Block)** 只要 `current_batch_temp > max_transport_temp`，系统必须通过 `AgriIncidentAlertMixin` 自动将 `temperature_violation` 标红并创建高优先级告警任务。
        - **(Evidence)** 异常时刻的 GPS 坐标与温度值必须锚定在 `traceability_hash` 中。

5. **[US-105-05] 观赏资产 GIS 单株精准定位 (Single Plant GIS Tracking)**：💡 待规划
    - **描述**：针对高端名贵盆景（Bonsai）或古树观赏资产，我希望在地图上实现单株级别的“生物资产卡片”。
    - **验收条件**：
        - **(Spatial)** 继承 `GeoSpatialMixin`，支持 `geo_point` 厘米级坐标。
        - **(Twin)** 为单株资产建立“数字孪生”记录，涵盖历年修剪、造型及健康档案。

## 2. 业务价值
- **科学溢价**: 基于瓶插寿命预测的精准定价，可提升高端切花 20%-40% 的溢价。
- **风控能力**: 实时冷链门控将断链导致的货损率从 12% 降低至 3% 以下。
- **合规透明**: 满足荷兰花卉拍卖市场（Royal FloraHolland）等国际标准的数据披露要求。

## 3. 技术挑战与约束
- **时效性**: 冷链监控要求秒级响应，必须利用 `AgriIncidentAlertMixin` 的高效通知机制。
- **数据一致性**: 积温计算必须对标 `docs/algorithms/GDD_CALCULATION_ALGORITHM.md`。
- **去工业化**: 严禁在界面出现工厂术语，必须映射为“温控室（Climate Room）”、“培育周期（Nurturing Cycle）”。

---
*最后更新：2026-02-01 (V2.0 深度规格版)*