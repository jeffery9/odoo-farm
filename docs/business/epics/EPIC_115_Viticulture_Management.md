# 史诗 115：葡萄园精密管理与风土数字化 (Viticulture Smart Management)
*目标：建立基于风土指纹与糖酸比动态预测的葡萄园管理体系，实现从架式修剪到精准采收的全生命周期闭环。*

## 1. 用户故事 (User Stories)

1. **[US-115-01] 风土指纹与地块档案 (Terroir & Plot DNA)**：💡 待实现
    - **描述**：作为酿酒师，我希望记录每个葡萄地块的坡度、日照方向及底土层成分。
    - **验收条件**：
        - **(ISL-Proxy)** `farm.viticulture.plot` 代理 `farm.location`。
        - **(DNA-Injection)** 继承 `GeoSpatialMixin` 记录 `slope` 和 `aspect`。
        - **(Terroir)** 集成 `AgriSoilAnalysisMixin` 锁定 pH 与有机质数据。

2. **[US-115-02] 年度架式修剪与挂果控制 (Pruning & Training)**：💡 待实现
    - **描述**：作为农事主管，我希望记录每一行的修剪方式（如单臂居由）及预留芽数。
    - **验收条件**：
        - **(Workflow)** `farm.viticulture.cycle` 代理 `mrp.production`。
        - **(Skill)** 关联年度任务与预期的“目标产量”。

3. **[US-115-03] 糖酸比动态监测与采收窗口预测 (Brix & Ripeness)**：💡 待实现
    - **描述**：作为实验室经理，我希望在临近采收期时每天录入糖度与酸度，系统自动预测最佳采收日。
    - **验收条件**：
        - **(Algorithm)** 继承 `AgriGrowthCycleMixin` (GDD)，关联积温与糖分累积曲线。
        - **(Alert)** 当糖酸比（Brix/Acid Ratio）达到平衡点时，触发采收预警。

4. **[US-115-04] 压榨转化率与出汁率核销 (Pressing Efficiency)**：💡 待实现
    - **描述**：作为压榨车间主任，我希望系统自动核算从鲜葡萄批次到原汁批次的转化率。
    - **验收条件**：
        - **(Logic)** 继承 `AgriTraceabilityMixin`，实现“固体批次”向“流体批次”的指纹继承。
        - **(Math)** 自动计算 `extraction_yield_v_w` (升/公斤)。

## 2. 业务价值
- **品质溢价**: 通过精准采收窗口控制，确保原酒品质稳定性提升 20%。
- **成本透明**: 实现从“单瓶酒”到“单行葡萄”的完全成本穿透。
- **GI 认证**: 100% 的风土数字化证据，支持高端地理标志（GI）认证。

---
*最后更新：2026-02-01*
