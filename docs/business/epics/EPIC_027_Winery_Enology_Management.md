# EPIC 027:酿造与酒窖工艺管理 (Winery & Enology Management)
*目标：建立从破碎压榨到陈酿调配的全链路酿造管理体系，通过实时发酵监控与橡木桶资产追踪，确保每一瓶酒的卓越品质与指纹级溯源。*

## 1. 用户故事 (User Stories)

1. **[US-027-01] 发酵动力学监控 (Fermentation Tracking)**：💡 待实现
    - **描述**：作为酿酒师，我希望实时记录发酵罐中的糖分下降（Density/Brix）与酒精上升曲线。
    - **验收条件**：
        - **(ISL-Proxy)** `farm.winery.production` 代理 `mrp.production`。
        - **(Logic)** 建立糖醇转换模型：`Alcohol_Potential = (Initial_Brix - Current_Brix) * 0.06`。
        - **(IoT)** 集成来自 `industrial_iot` 的罐温与压力遥测。

2. **[US-027-02] 橡木桶与陈酿资产管理 (Barrel Aging)**：💡 待实现
    - **描述**：作为酒窖主管，我希望追踪每一只橡木桶（Barrel）的材质、使用次数及其内含的原酒批次。
    - **验收条件**：
        - **(ISL-Proxy)** `farm.winery.vessel` 代理 `mrp.workcenter`。
        - **(DNA-Injection)** 继承 `AgriTraceabilityMixin`，记录每一只桶的“历史贡献”。

3. **[US-027-03] 多批次调配与 DNA 聚合 (Blending & Marriage)**：💡 待实现
    - **描述**：作为实验室主任，我希望在调配（Blending）时，系统自动聚合不同年份、不同地块原酒的 DNA 指纹。
    - **验收条件**：
        - **(Logic)** 产成品哈希必须包含所有参与调配的原酒批次（Parent Lots）的摘要。
        - **(Recipe)** `farm.winery.recipe` 支持多级嵌套（Recipe inside Recipe）。

4. **[US-027-04] 理化分析与酿造门控 (Enological Lab Gate)**：💡 待实现
    - **描述**：作为品控专员，我希望在装瓶前强制检查游离二氧化硫（FSO2）、挥发酸及残糖量。
    - **验收条件**：
        - **(Mixin)** 继承 `AgriQualityGateMixin`。
        - **(Gate)** 任何指标超标时，拦截 `action_mark_done`（装瓶指令）。

## 2. 业务价值
- **工艺资产化**: 酿造数据不再是散乱的记录，而是可复用的“工艺资产”。
- **动态清算**: 根据陈酿时长与品质评分，实时更新酒窖资产的市场价值。
- **透明溯源**: 满足消费者对“单园、单桶、传统工艺”的极致透明度追求。

---
*最后更新：2026-02-01*
