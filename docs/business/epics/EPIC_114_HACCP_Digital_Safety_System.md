# 史诗 114：HACCP 数字化食品安全管控体系 (HACCP Digital Safety)
*目标：建立基于关键控制点 (CCP) 的数字化安全防御体系，实现生产全过程的实时风险监控与违规批次强制隔离。*

> **架构定义**: HACCP 作为 **Safety DNA**，通过 Mixin 注入到所有加工类指令。它不仅仅是记录，而是具备“物理拦截”能力的硬红线。

## 1. 用户故事 (User Stories)

1. **[US-114-01] CCP 关键控制点与限值建模 (CCP & Critical Limits)**：💡 待实现
    - **描述**：作为品控经理，我希望在生产工艺（Recipe）中标记 CCP，并定义其物理报警阈值。
    - **验收条件**：
        - **(ISL-Proxy)** `farm.haccp.point` 代理 `quality.point`。
        - **(Logic)** 增加 `critical_limit_min` 和 `critical_limit_max` 字段。
        - **(Visual)** 在 UI 中以红色醒目标记 CCP。

2. **[US-114-02] 违规实时拦截与批次隔离 (Violation Blocking)**：💡 待实现
    - **描述**：作为车间主管，一旦 CCP 检测数据（如灭菌温度）不达标，系统必须自动拦截该工单的“完成”动作并锁定批次。
    - **验收条件**：
        - **(Gate)** 继承 `AgriQualityGateMixin`。
        - **(Status-Lock)** 违规批次（Lot）自动标记为 `blocked_by_haccp`，禁止执行后续销售或移库。

3. **[US-114-03] 纠偏措施 (Corrective Action) 强制流转**：💡 待实现
    - **描述**：针对发生的 HACCP 违规，我希望系统强制要求相关人员录入纠偏措施，经审核后方可解锁批次。
    - **验收条件**：
        - **(Workflow)** 实现 `action_record_corrective_measure`。
        - **(Audit)** 所有纠偏记录必须锚定到 `AgriTraceabilityMixin` 的指纹中。

4. **[US-114-04] HACCP 验证包一键生成 (Audit Package)**：💡 待实现
    - **描述**：作为合规官，我希望一键导出某批次产品的所有 CCP 监控曲线与质检日志，以应对官方审计。
    - **验收条件**：
        - **(Reporting)** 自动汇总：CCP 记录 + IoT 环境曲线 + 纠偏日志。

## 2. 业务价值
- **零安全事故**: 数字化红线拦截，杜绝人为疏忽导致的食品安全风险。
- **审计合规**: 满足 GlobalGAP、ISO 22000 对 HACCP 数字化记录的最高要求。
- **品牌信任**: 每一瓶精油或每一袋净菜都持有“HACCP 验证指纹”。

---
*最后更新：2026-02-01*
