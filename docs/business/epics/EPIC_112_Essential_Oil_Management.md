# 史诗 112：精油提取工艺与品质全链路管理 (Essential Oil Management)
*目标：建立基于工艺参数精准控制的精油生产体系，通过多级批次 DNA 继承与提取率自动核算，确保高端香料与药用精油的极致溯源。*

## 1. 用户故事 (User Stories)

1. **[US-112-01] 提取工艺 Recipe 建模 (Extraction Protocol)**：✅ 已实现 (2026-02-01)
    - **描述**：作为生产工艺师，我希望在 Recipe (BOM) 中定义不同精油（如薰衣草、檀香）的蒸馏温度、压力和冷却时长。
    - **验收条件**：
        - **(ISL-Proxy)** `farm.essential_oil.recipe` 代理 `mrp.bom`。
        - **(Parameters)** 包含 `distillation_temp`, `target_yield_percent`, `cooling_duration` 字段。

2. **[US-112-02] 提取率 (Extraction Yield) 自动审计**：✅ 已实现 (2026-02-01)
    - **描述**：作为加工经理，我希望系统自动对比“原材料投入重”与“精油产出量”，计算每一批次的提取率偏差。
    - **验收条件**：
        - **(Logic)** `Actual_Yield = (Oil_Output / Material_Input) * 100`。
        - **(Alert)** 若提取率低于标准值 20% 以上，触发 `AgriIncidentAlertMixin`。

3. **[US-112-03] 多对一批次 DNA 链式继承 (Lineage Inheritance)**：✅ 已实现 (2026-02-01)
    - **描述**：作为溯源专员，我希望产成品精油批次能自动聚合所有投入原材料批次的地理和生化 DNA。
    - **验收条件**：
        - **(Traceability)** 继承 `AgriTraceabilityMixin`。
        - **(Logic)** 产成品哈希必须包含所有 `move_raw_ids` 来源批次的 Hash 摘要。

4. **[US-112-04] GC-MS 成分分析与品质门控 (Quality Gate)**：💡 待增强
    - **描述**：作为实验室分析员，我希望记录精油的化学成分组成（气相色谱-质谱法），并据此进行品质分级。
    - **验收条件**：
        - **(Mixin)** 继承 `AgriQualityGateMixin`。
        - **(Gate)** 只有主要成分（如里那醇）达到标准范围，才允许执行 `action_finalize_clearing`。

## 2. 业务价值
- **精准溢价**: 基于 GC-MS 成分的等级划分，使医疗级精油相比普通级获得 2-3 倍的单价溢价。
- **工艺防错**: 自动化的蒸馏参数校验减少 10% 的“过烧”废品率。
- **真实性存证**: 100% 的原料批次继承逻辑，杜绝掺假风险。

---
*最后更新：2026-02-01*
