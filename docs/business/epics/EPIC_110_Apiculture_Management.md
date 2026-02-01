# 史诗 110：智能养蜂与蜜源追踪管理 (Apiculture Smart Management)
*目标：建立基于蜂群活力监控与蜜源空间分析的数字化养蜂体系，通过转场路径优化实现蜂蜜产量的最大化与全链路溯源。*

## 1. 用户故事 (User Stories)

1. **[US-110-01] 蜂箱数字孪生与蜂王档案 (Hive & Queen Life-log)**：✅ 已实现 (2026-02-01)
    - **描述**：作为养蜂人，我希望记录每个蜂箱的蜂群强度、蜂王年龄及繁育品系。
    - **验收条件**：
        - **(ISL-Proxy)** `farm.lot.hive` 代理 `stock.lot`。
        - **(DNA-Injection)** 继承 `AgriBiologicalInventoryMixin`，将“蜂数”转化为生物量。
        - **(Status)** 维护蜂王状态机（Good, Queenless, New Queen）。

2. **[US-110-02] 蜜源地图与采集半径分析 (Nectar Source GIS)**：💡 待增强
    - **描述**：作为场长，我希望在地图上查看蜂箱位置，并自动计算 3km 采集半径内的蜜源植物覆盖情况。
    - **验收条件**：
        - **(Spatial)** 继承 `GeoSpatialMixin`，实现以蜂箱为圆心的缓冲区分析（Buffer Analysis）。
        - **(Intelligence)** 联动 `farm_weather` 预测流蜜期（Honey Flow）。

3. **[US-110-03] 转场迁徙计划与物流闭环 (Migration & Transhumance)**：💡 待增强
    - **描述**：作为调度员，我希望规划蜂箱从产地 A 到产地 B 的迁徙路径，并记录转场过程中的损耗。
    - **验收条件**：
        - **(Workflow)** 自动生成 `stock.picking` 移库单，并更新 `farm.location` 关联。
        - **(Skill)** 迁移结束自动触发 `action_record_mortality` 评估迁徙压力。

4. **[US-110-04] 蜂蜜采收分级与理化存证 (Honey Grading)**：✅ 已实现 (2026-02-01)
    - **描述**：作为质检员，我希望记录采收时的波美度、色泽及蜜源种类。
    - **验收条件**：
        - **(Mixin)** 继承 `AgriQualityGateMixin` 强制核验水分含量。
        - **(Traceability)** 生成包含蜜源植物指纹的溯源哈希。

## 2. 业务价值
- **产量提升**: 通过蜜源与花期的精准匹配，预计提升蜂蜜单产 20%。
- **风险降低**: 实时监控蜂群强度，减少 50% 的非法分蜂（Swarming）损失。
- **品牌认证**: 100% 蜜源地理指纹存证，支撑高溢价单花蜜销售。

---
*最后更新：2026-02-01*
