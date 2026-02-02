# 史诗 201：农学科学底座 (Agri-Science Foundation)
*版本: V1.2 (Deep Simulation Expansion) | 状态: ACTIVE | 归口: farm_agri_science*

## 1. 核心愿景 (Core Vision)
构建一个支持科学决策的“生物学参考底座”。通过定义品种的生理指纹、动态生长模型和环境阈值矩阵，将农学逻辑（Science）与生产执行（Execution）无缝打通。本模块是系统实现“自适应生产”的核心认知源头。

---

## 2. 精细化用户故事 (Detailed User Stories)

### **[US-201-01] 品种生理指纹与基准 (Physiology Fingerprint)**
- **描述**: 作为农技专家，我希望为每个品种定义关键生理参数，以便系统能够识别该品种的发育极限。
- **验收标准 (AC)**:
    - **(Logic)** 支持定义“三基点温度”：T-base (发育起点), T-opt (最适温度), T-max (停止发育温度)。
    - **(Logic)** 支持定义 NPK 敏感性权重，作为配方自适应调整的修正系数。
    - **(Odoo Mapping)** 相关数据注入 `product.product` (Variety 层级)。

### **[US-201-02] 生理阶段与积温驱动 (Physiological Stages & GDD)**
- **描述**: 作为工艺员，我希望定义不以“日历天”为单位，而以“有效积温 (GDD)”为触发条件的生长阶段。
- **验收标准 (AC)**:
    - **(Logic)** 实现阶段跳转的 GDD 累积逻辑：Stage Transition = Current GDD >= Stage.GDD_Threshold。
    - **(Science-Driven)** 阶段名称必须符合农学标准（如：V1, V2, R1 等 BBCH 标度）。
    - **(UX)** 在执行界面提供“生理进度条”，展示当前 GDD 在总发育期中的百分比。

### **[US-201-03] 环境阈值矩阵与 SPC 联动 (Environmental Matrix)**
- **描述**: 作为质量主管，我希望定义每个生理阶段特有的“安全运行域”，以便自动触发 SPC 锁闭。
- **验收标准 (AC)**:
    - **(ISA-88)** 不同的阶段可以有不同的温湿度、光照、浓度容差矩阵。
    - **(Logic)** 当实测值偏离生理安全域（而非仅仅配方目标）时，自动将 `process_status` 标记为 OOC 并锁闭执行。

### **[US-201-04] 养分吸收动态模型 (Nutrient Uptake Curves)**
- **描述**: 作为工艺架构师，我希望系统能根据当前的生理阶段，自动计算理想的营养配比。
- **验收标准 (AC)**:
    - **(Logic)** 支持“阶段化配方系数”：例如在 Flowering 阶段，自动将 K 肥权重系数上调 20%。
    - **(Science-Driven)** 提供基于干物质积累量预测的养分需求函数。

### **[US-201-05] 科学向导：配方自校验 (Scientific Recipe Validator)**
- **描述**: 作为系统管理员，我希望在定义 Master Recipe 时，系统能自动检查设定点是否越过了品种的生理红线。
- **验收标准 (AC)**:
    - **(De-industrialized)** 如果 Master Recipe 设定的温度 > T-max，系统必须抛出“生物学不合规”警告而非工业逻辑错误。

---


### **[US-201-06] 视觉物候标定与反馈 (Vision-Phenology Sync)**
- **描述**: 作为 AI 工程师，我希望利用视觉识别结果动态修正 GDD 预测进度，以消除环境微气候导致的偏差。
- **验收标准 (AC)**:
    - **(IOT)** 支持接收来自 `farm_ai_vision` 的物候阶段识别信号。
    - **(Logic)** 实现“真值校准”逻辑：识别到的生理阶段优先级高于数学预测值。

### **[US-201-07] 生物压力累积评估 (Biological Stress Analysis)**
- **描述**: 作为农技专家，我希望量化环境偏差（过冷/过热）对生物体的累积压力，并预测对最终产量的损害。
- **验收标准 (AC)**:
    - **(Logic)** 引入“压力积分”模型：Stress = Integral(Current - Optimal) dt。
    - **(Science-Driven)** 实现基于压力的采收日期动态调整预测。

### **[US-201-08] 生物资源转化效率 (Biological Conversion Efficiency)**
- **描述**: 作为 ESG 审计员，我希望评估生物资产对水、肥、光的转化效率（RUE/WUE）。
- **验收标准 (AC)**:
    - **(ESG)** 记录并核算每一单位投入（水/肥/电）生成的干物质估算量。
    - **(Logic)** 提供“资源转化 KPI”，作为科学底座的绩效输出。


### **[US-201-09] 科学性能看板 (Scientific Performance Dashboard)**
- **描述**: 作为农场经营者，我希望通过图形化看板对比不同品种、不同批次的资源利用效率（RUE/WUE），以优化资源投入。
- **验收标准 (AC)**:
    - **(UX)** 提供透视表视图 (Pivot)，支持按品种、生理阶段分组分析 WUE 和 RUE。
    - **(UX)** 提供趋势图 (Graph)，展示积温 (GDD) 与干物质积累、水耗之间的相关性。
    - **(Science-Driven)** 看板需直接提取自 `farm.agri.science.mixin` 的计算结果。

## 3. 核心算法引用 (Algorithm Reference)
- **GDD 发育核算**: 对标 `docs/algorithms/GDD_CALCULATION_ALGORITHM.md`。
- **BBCH 标度映射**: 参考国际标准物候期分类法。
- **NPK 动态平衡**: 对标 `docs/algorithms/NUTRIENT_BALANCE_ALGORITHM.md`。

---
## 4. 物理资产与锚点 (Architectural Anchors)
- **核心 Mixin**: `farm.agri.science.mixin`
- **模型实体**: `agri.growth.stage`, `agri.physiology.profile`

---
*V1.1 - Deep Refinement: From Logic to Biology | 2026-02-01*
