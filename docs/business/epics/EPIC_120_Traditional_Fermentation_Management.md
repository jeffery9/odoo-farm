# 史诗 120：传统发酵与酿造工艺管理 (Traditional Fermentation Management)
*目标：建立从制曲发酵到窖藏勾调的全链路管控体系，通过窖池生态存证与动态增值模型，锁定传统酿造的高附加值指纹。*

## 1. 用户故事 (User Stories)

1. **[US-120-01] 窖池/容器数字孪生与生态档案 (Pit DNA)**：💡 待实现
    - **描述**：作为酿造总工，我希望记录每个窖池（或陶坛）的编号、启用年份、维护记录及微生物抽检指标。
    - **验收条件**：
        - **(ISL-Proxy)** `farm.fermentation.vessel` 代理 `mrp.workcenter`。
        - **(DNA-Injection)** 继承 `GeoSpatialMixin` 锁定窖池的空间坐标。
        - **(Evidence)** 关联窖泥理化分析数据（pH、腐殖质）。

2. **[US-120-02] 制曲与发酵动力学监控 (Starter & Fermentation)**：💡 待实现
    - **描述**：作为工艺师，我希望监控发酵过程中的品温、水分及酸度变化趋势。
    - **验收条件**：
        - **(Workflow)** `farm.fermentation.order` 代理 `mrp.production`。
        - **(IoT)** 集成来自 `industrial_iot` 的多点温度监测。
        - **(Skill)** 类似 `on_damaged` 机制，温度超标自动下达“翻曲”或“降温”指令。

3. **[US-120-03] 勾调（调配）与品质指纹聚合 (Blending & Marriage)**：💡 待实现
    - **描述**：作为勾调师，我希望将不同年份、不同等级的原浆进行混合，并自动聚合其 DNA 指纹。
    - **验收条件**：
        - **(Logic)** 继承 `AgriTraceabilityMixin`，实现从原浆到成品酒的哈希链。
        - **(Quality)** 强制关联理化检测报告（总酸、总酯、氨基酸态氮）。

4. **[US-120-04] 年份资产动态增值模型 (Vintage Liquidation)**：💡 待实现
    - **描述**：作为财务经理，我希望原酒价值随陈酿年份自动增长，并反映在资产负债表中。
    - **验收条件**：
        - **(Algorithm)** 继承 `AgriBiologicalValuationMixin`。
        - **(Valuation)** `Fair_Value = Base_Price * (1 + Age_Premium_Rate)^Years`。

## 2. 业务价值
- **文化定价**: 100% 的窖池与年份存证，支撑传统工艺的品牌溢价。
- **品质一致性**: 数字化配方减少 20% 的由于环境波动造成的品质批次差。
- **金融资产化**: 使库存中的长期陈酿资产具备精准的抵押融资评估基础。

---
*最后更新：2026-02-01*
