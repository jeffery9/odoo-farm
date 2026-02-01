# 史诗 106：中药材与药用植物管理 (Medicinal Plants Management)
*目标：通过有效成分动态监测与道地性全过程存证，建立符合 GMP 标准的中药材全生命周期管理体系。*

## 1. 用户故事 (User Stories)

1. **[US-106-01] 道地性地理指纹 (Daodi Origin Fingerprint)**：💡 待实现
    - **描述**：作为药材基地主管，我希望系统自动核验地块的土质、海拔是否符合该品种的“道地性”要求。
    - **验收条件**：
        - **(Spatial-Audit)** 继承 `GeoSpatialMixin`，自动关联地块海拔与土质数据。
        - **(Standard-Check)** 自动对比品种 DNA 中的“道地标准”，不符时触发警告。

2. **[US-106-02] 有效成分动态积累追踪 (Active Compound Tracking)**：💡 待实现
    - **描述**：作为药学技术员，我希望基于积温与实时检测数据，绘制有效成分的积累曲线。
    - **验收条件**：
        - **(Algorithm)** 继承 `AgriGrowthCycleMixin`，将 `accumulated_gdd` 与有效成分浓度关联。
        - **(Feedback)** 实验室检测数据（Analysis）自动回写至批次 DNA。

3. **[US-106-03] 最佳药效采收窗口预测 (Optimal Harvest Window)**：💡 待实现
    - **描述**：作为生产主管，我希望系统在有效成分达到峰值时自动通知采收。
    - **验收条件**：
        - **(Skill)** 类似 `apply_bloom_skill`，当积温达到药效阈值，自动迁移至 `ready_to_harvest` 阶段。

4. **[US-106-04] GMP 炮制工艺与质量门控 (GMP Processing & Quality Gate)**：💡 待实现
    - **描述**：作为加工经理，我希望在炮制（加工）过程中严格执行温湿度控制和 HACCP 校验。
    - **验收条件**：
        - **(ISL-Gate)** 继承 `AgriQualityGateMixin`，强制核验每一道工序（如洗、切、蒸、烘）的 QCP。

## 2. 业务价值
- **溢价核心**: 具备实验室数据支撑的道地药材可获得 50% 以上的贸易溢价。
- **合规降险**: 自动化的 GMP 审计包生成，减少 80% 的人工整理工作量。

---
*最后更新：2026-02-01*
