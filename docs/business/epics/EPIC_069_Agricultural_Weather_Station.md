# EPIC 069:农业气象站与环境监测 (Agricultural Weather Station & Environmental Monitoring)
*目标：建立跨实体的气象监测共识网络，通过多点物理校验提供高精度超本地（Hyper-local）气候服务。*

## 1. 用户故事 (User Stories)

1. **[US-069-01] 多参数环境数据采集 (Multi-parameter Environmental Data Collection)**：💡 待规划
    - **描述**：作为农技员，我希望收集全面的环境数据用于农业生产决策。
    - **验收条件**：
        - **(Weather-Parameters)** 实时监测温度、湿度、风速、风向、降雨量、光照强度等物理因子。
        - **(Soil-Conditions)** 深度集成土壤温度、湿度、pH 值、电导率等关键生长参数。
        - **(Air-Quality)** 监测空气中 CO2、气压等对作物光合作用有显著影响的物理指标。
        - **(IoT-Direct)** 数据 100% 透传映射至 Odoo 气象站模型，支持高频（15min）心跳上报。

2. **[US-069-02] 本地化天气预报 (Localized Weather Forecasting)**：💡 待规划
    - **描述**：作为农场主，我希望获得基于本地气象站数据的精准天气预报。
    - **验收条件**：
        - **(Micro-climate-Modeling)** 建立基于本地数据的微气候预测模型，提供 24h 内的精细化气压与降水概率。
        - **(Agricultural-Impact)** 预测天气对农业活动的具体影响（如：自动评估霜冻、暴雨对当前物候期的物理风险）。
        - **(Actionable-Insights)** 提供针对农业生产的天气应对建议（如：建议在降雨前 6h 完成某项 Intervention）。

3. **[US-069-03] 环境异常预警 (Environmental Anomaly Alert)**：💡 待规划
    - **描述**：作为风险管理员，我希望及时收到环境异常的预警信息。
    - **验收条件**：
        - **(Threshold-Monitoring)** 设置并监控环境参数的预警阈值。
        - **(Risk-Assessment)** 基于 `BasePPOCritic` 逻辑评估环境异常对农业生产的潜在损失等级。
        - **(Multi-channel-Alerts)** 通过多种渠道（钉钉/短信/A2A）发送环境预警信息。

4. **[US-069-04] 历史数据分析与趋势预测 (Historical Data Analysis & Trend Prediction)**：💡 待规划
    - **描述**：作为农业规划师，我希望分析历史环境数据以预测长期趋势。
    - **验收条件**：
        - **(Data-Aggregation)** 汇总和分析多年环境数据，识别长期气候变化趋势。
        - **(Planning-Support)** 为种植计划（Epic 070）和农业投资提供基于气候趋势的决策参考。

5. **[US-069-05] 跨农场气象数据共享与共识校验 (Cross-Farm Weather Consensus)**：💡 待规划
    - **描述**：即便没有 AI 代理，我也希望对比邻近气象站的数据，通过证据评价算法识别虚假告警。
    - **验收条件**：
        - **(Weather-Evidence-Extraction)** 对标 `extract_evidence` 逻辑：将站点读数（如：降雨量 > 50mm）视为一个 `Claim`。
        - **(Dual-Confidence-Scoring)** 实现多站点证据融合：当 5km 内 3 个以上站点确认同一事件，且综合 `confidence_score` > 0.8 时，升级灾害防御等级。
        - **(Sensor-Alibi)** 利用 `get_alibi` 逻辑进行位置偏置校验：若某站读数显著偏离物理邻近站点均值，触发“物理检修”任务。

6. **[US-069-06] 区域级灾害天气物理联动响应 (Joint Disaster Response)**：💡 待规划
    - **描述**：作为区域管理者，我希望根据气象共识自动指挥跨实体的防灾设施。
    - **验收条件**：
        - **(Logic)** 联动 Epic 013，证据确认为 `Positive` 时，自动调度物理泵站或加固设施。
        - **(Redundancy)** 通信链路支持跨农场路由，确保单场网络故障时的物理数据透传。

7. **[US-069-07] 微气候资产所有权与维护分摊 (Weather Asset Ownership)**：💡 待规划
    - **描述**：作为合作社经理，我希望多个农场共建高精度气象站。
    - **验收条件**：
        - **(Asset-Mapping)** 气象站关联 `account.asset`，支持基于 GIS Beneficiary Area（受益面积）的动态维护费分摊。

## 业务价值
- **核心价值**: 建立精准的农业气象监测网络，通过多点物理校验消除单点预警偏差，实现区域气象服务的“资产轻量化”与“精度极大化”。
- **目标用户**: 农技员、农场主、风险管理员、区域管理者。
- **量化收益**: 气象预警精度提升 30%，单场气象资产投入降低 50%，防灾响应延迟降低 200%。

## 技术挑战
- **复杂性**: 异构气象数据同步、基于证据论（D-S Evidence Theory）的置信度融合。
- **物理性**: 深度依赖 Epic 013 的物理资产分摊模型。

---
*最后更新：2026-01-31*
