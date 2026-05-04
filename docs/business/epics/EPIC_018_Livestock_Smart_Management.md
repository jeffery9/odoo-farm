# EPIC 018:畜牧养殖智能管理 (Livestock Smart Management)
*目标：建立个体级的全生命周期管理体系，通过 FCR 动态优化与实时健康监控，实现畜牧资产的高效率转化与金融级估值。*

## 1. 用户故事 (User Stories)

1. **[US-018-01] 个体电子档案与繁殖状态机 (Individual Life-log)**：✅ 已实现 (2026-02-01)
    - **描述**：作为养殖技术员，我希望记录每一头畜禽的耳标、性别、谱系及繁殖状态（如：哺乳、怀孕、空怀）。
    - **验收条件**：
        - **(ISL-Proxy)** `farm.lot.livestock` 代理 `stock.lot`。
        - **(DNA-Injection)** 继承 `AgriBiologicalInventoryMixin` 进行数量动态管理。
        - **(Status-Migration)** 实现从 `immature` 到 `lactating` 的状态自动流转。

2. **[US-018-02] 饲料转化率 (FCR) 与日增重 (ADG) 实时监控**：✅ 已实现 (2026-02-01)
    - **描述**：作为生产主管，我希望根据饲喂记录与称重数据，自动计算每批次的转化效率。
    - **验收条件**：
        - **(Logic)** `FCR = Total_Feed / Total_Weight_Gain`。
        - **(Alert)** 若 ADG 低于品种标准曲线 15%，系统自动触发 `AgriIncidentAlertMixin`。

3. **[US-018-03] 动态免疫排期与休药期红线 (Vaccination & PHI)**：💡 待增强
    - **描述**：作为兽医，我希望系统根据生长阶段自动排布免疫任务，并强制拦截处于休药期内的出栏操作。
    - **验收条件**：
        - **(Mixin)** 继承 `AgriCertificationStatusMixin` 记录免疫效期。
        - **(Gate)** `AgriQualityGateMixin` 拦截休药期未结束的 `stock.picking`。

4. **[US-018-04] 活体抵押资产动态估值 (Livestock Mortgage Valuation)**：✅ 已实现 (2026-02-01)
    - **描述**：作为财务总监，我希望基于实时重量和市场行情，为金融机构提供可信的资产估值。
    - **验收条件**：
        - **(Algorithm)** 继承 `AgriBiologicalValuationMixin`。
        - **(Evidence)** 估值报告必须包含质量指纹（Quality Fingerprint），锚定最近一次称重证据。

## 2. 业务价值
- **精益转化**: 提升 FCR 效率 5%-10%，直接降低饲料成本。
- **资产变现**: 通过透明的活体估值，使畜牧资产具备 100% 的抵押融资能力。
- **安全保障**: 确保 100% 无抗/无残出栏，满足出口级合规要求。

---
*最后更新：2026-02-01*
