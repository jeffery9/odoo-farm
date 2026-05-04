# EPIC 033:稻渔/稻虾共生生态管理 (Rice-Fish/Shrimp Symbiosis)
*目标：建立基于生态协同的稻渔复合管理体系，通过共生养分核销与严苛的施药风险拦截，实现绿色溢价与生态效益的双重锁定。*

## 1. 用户故事 (User Stories)

1. **[US-033-01] 共生空间档案与水位建模 (Symbiotic Plot DNA)**：💡 待实现
    - **描述**：作为场长，我希望记录地块的插秧密度、环沟比例及水深要求。
    - **验收条件**：
        - **(ISL-Proxy)** `farm.symbiotic.plot` 代理 `farm.location`。
        - **(DNA-Injection)** 继承 `GeoSpatialMixin` 实现田块与环沟的空间布局映射。

2. **[US-033-02] 稻渔复合配方与养分转换 (Symbiotic Nutrient)**：💡 待实现
    - **描述**：作为农艺师，我希望在配方中锁定鱼虾排泄物对水稻氮源的替代比例。
    - **验收条件**：
        - **(ISL-Proxy)** `farm.symbiotic.recipe` 代理 `mrp.bom`。
        - **(Logic)** 继承 `NutrientMixin` 核算“内部循环养分”。

3. **[US-033-03] 植保施药的安全红线拦截 (Pesticide Safety Gate)**：💡 待实现
    - **描述**：作为植保员，在对水稻喷药前，系统必须自动核验药剂对鱼虾的毒性，严防翻塘。
    - **验收条件**：
        - **(Gate)** 继承 `AgriQualityGateMixin`。
        - **(Validation)** 若药剂含有对水产高毒成分（如阿维菌素），强制拦截 `action_confirm`（干预指令）。

4. **[US-033-04] 一地双收的复合产量核销 (Co-harvest Tracking)**：💡 待实现
    - **描述**：作为财务经理，我希望在同一个生产周期内分别核收水稻与鱼/虾批次，并分摊共同成本。
    - **验收条件**：
        - **(Workflow)** `farm.symbiotic.order` 支持多产成品（Multi-output）逻辑。
        - **(Traceability)** 稻米批次自动继承鱼虾活跃度的“生态指纹”。

## 2. 业务价值
- **绿色溢价**: 通过“无农药残留、生态共生”存证，提升产品单价 30% 以上。
- **化肥减量**: 科学核算共生肥力，预计减少化肥施用量 20%-40%。
- **风险防控**: 数字化红线拦截，将复合种养中的“药害损失”降至零。

---
*最后更新：2026-02-01*
