# EPIC 019:水产养殖智能管理 (Aquaculture Smart Management)
*目标：建立基于水质感知的精准养殖体系，通过生物量动态预测与载荷门控，实现高密度养殖的风险控制与产量优化。*

## 1. 用户故事 (User Stories)

1. **[US-019-01] 池塘/网箱数字孪生 (Pond Digital Twin)**：✅ 已实现 (2026-02-01)
    - **描述**：作为场长，我希望在系统中定义每个水体的容量、水深及底质类型。
    - **验收条件**：
        - **(ISL-Proxy)** `farm.lot.aquaculture` 代理 `stock.lot`。
        - **(DNA-Injection)** 继承 `GeoSpatialMixin` 实现水体的 3D 坐标映射。
        - **(Capacity)** 自动计算 `water_volume_m3`。

2. **[US-019-02] 水质联动动态投喂 (Water-Linked Feeding)**：✅ 已实现 (2026-02-01)
    - **描述**：作为养殖员，我希望系统根据当前溶氧和水温自动调整投喂系数。
    - **验收条件**：
        - **(Skill)** 类似 `apply_bloom_skill`，当溶氧 < 3mg/L 时，自动生成“停止投喂”的 Agent 指令。
        - **(Logic)** 基于积温算法预测生长速率（SGR）。

3. **[US-019-03] 生物量抽样与存活率校准 (Biomass Sampling)**：✅ 已实现 (2026-02-01)
    - **描述**：作为技术员，我希望记录定期抽样数据，系统自动更新总重量预测并核销预期死亡。
    - **验收条件**：
        - **(DNA)** 继承 `AgriBiologicalInventoryMixin`。
        - **(Math)** 自动计算 `stocking_density = total_biomass / water_volume`。

4. **[US-019-04] 水质灾害实时防御 (Water Quality Defense)**：✅ 已实现 (2026-02-01)
    - **描述**：作为运维专员，我希望当溶氧低于红线时，系统自动启动增氧机并发出高优告警。
    - **验收条件**：
        - **(IoT-Trigger)** 接收 `industrial_iot` 的实时遥测。
        - **(Alert)** 通过 `AgriIncidentAlertMixin` 自动创建紧急任务。

## 2. 业务价值
- **风控核心**: 将缺氧翻塘的事故率降低 90% 以上。
- **降本增效**: 精准投喂可减少 15% 的饲料浪费，并改善水质排放（Scope 3 ESG）。

---
*最后更新：2026-02-01*
