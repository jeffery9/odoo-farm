# EPIC 029:水产加工与冷冻链条管理 (Aquatic Product Processing)
*目标：建立从捕捞入库到冷冻包装的全过程管控体系，通过包冰率精确核销与微生物安全门控，确保水产品的食品安全与贸易诚信。*

## 1. 用户故事 (User Stories)

1. **[US-029-01] 捕捞入库与生鲜 DNA 继承 (Fresh Catch Intake)**：💡 待实现
    - **描述**：作为加工经理，我希望记录捕捞批次，并自动继承水体环境（如溶氧历史、水温）指纹。
    - **验收条件**：
        - **(Logic)** 继承 `AgriTraceabilityMixin`。
        - **(Linkage)** 强制关联 `farm.lot.aquaculture` 原始批次。

2. **[US-029-02] 加工得率与包冰率核销 (Glazing & Yield Tracking)**：💡 待实现
    - **描述**：作为生产主管，我希望记录包冰前后的重量，自动核算包冰率并确保净重符合标签声明。
    - **验收条件**：
        - **(Math)** `Glazing_Rate = (Frozen_Weight - Net_Weight) / Frozen_Weight`。
        - **(Audit)** 自动生成“包冰合规证明”，作为质量指纹的一部分。

3. **[US-029-03] 极速冻结中心温度监控 (Flash Freezing Control)**：💡 待实现
    - **描述**：作为车间品控，我希望监控速冻机的运行曲线，确保产品中心温度在规定时间内降至 -18℃。
    - **验收条件**：
        - **(IoT)** 接收速冻机温度探头数据。
        - **(Gate)** 继承 `AgriQualityGateMixin`，若速冻曲线不合格，拦截批次入库。

4. **[US-029-04] 微生物指标与出口核验 (Microbial Gate)**：💡 待实现
    - **描述**：作为合规官，我希望在出口前自动核验组胺、重金属等检测记录是否符合目标市场（如 EU/US）标准。
    - **验收条件**：
        - **(Logic)** 继承 `AgriCertificationStatusMixin`。
        - **(Validation)** 自动匹配 `farm.export.compliance` 数据库。

## 2. 业务价值
- **贸易诚信**: 精确的包冰率核销防止超量包冰，提升品牌信誉。
- **安全拦截**: 实时监控速冻红线，杜绝由于失温导致的细菌超标风险。
- **高效溯源**: 实现从“鱼罐头/冷冻鱼片”到“育苗池”的全链路成本与 DNA 穿透。

---
*最后更新：2026-02-01*
