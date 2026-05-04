# 2026 农业社区 AI 协同系统技术规格说明书 (Technical Specification)

## 1. 核心愿景与设计哲学
本系统旨在通过去工业化术语、地理空间优先、Mixin 驱动的通用计算以及 A2A 协作，将传统的单场 ERP 进化为“分布式农业社区智能体网络”。

### 核心原则
- **UI 物理隔离 (De-industrialized UI)**: 严禁在用户界面出现工业化术语（MO/BOM/Workcenter）。必须通过底层视图拦截器强制替换为农业术语。
- **逻辑沉淀 Mixin**: 跨模块的通用计算逻辑必须沉淀为抽象 Mixin，严禁在业务模型中硬编码。
- **地理空间优先**: 所有物理实体（地块、设备、接驳点）必须具备 PostGIS 地理属性。
- **可持续性为先 (Sustainability-First)**: **碳足迹与生态贡献是系统的最高价值标准。** 任何业务决策必须通过可持续性红线校验。
- **公平收益结算**: 通过多维价值评估与内部分账，确保所有社区参与者（无论规模大小）都能从中受益。

---

## 2. 去工业化视图拦截引擎 (View Interceptor Spec)
为实现 UI 物理隔离，系统引入 `AgriViewMixin`：
- **机制**: 重写 Odoo 底层的 `fields_view_get` 方法。
- **逻辑**: 
    1. 扫描 XML 视图中的 Label 和 String 属性。
    2. 匹配 `term.mapping` 数据库中的行业映射关系。
    3. 动态替换“工厂类”术语（如 `Workcenter` -> `Field`, `Manufacturing Order` -> `Intervention`）。
    4. 自动隐藏与农业场景无关的工业化原生字段（如 `Efficiency_Factor`, `Scrap_Rate`）。

---

## 3. Mixin 架构设计 (The Mixin Library)

### 3.1 `SustainabilityMixin` (Epic 101/30)
- **职责**: **系统的“价值度量衡”与准则。** 自动化三重底线（TBL）计算与 ESG 价值重估。
- **强制约束**: 所有 `Intervention` 必须在确认前调用此 Mixin 评估预估碳强度。
- **核心接口**: `compute_carbon_footprint()`, `get_social_impact_score()`, `validate_sustainability_redline()`.

### 3.2 `NutrientMixin` (Epic 27)
- **职责**: 跨阶段 NPK 养分平衡与循环。
- **核心接口**: `calculate_mass_balance()`, `get_nutrient_fingerprint()`, `forecast_compost_value()`.

### 3.3 `CollaborativeMixin` (Epic 70)
- **职责**: 跨农场实体（Multi-company）协作与需求聚合。
- **核心接口**: `get_shared_inventory()`, `request_joint_procurement()`, `apply_internal_netting()`.

### 3.4 `GrowthMixin` (Epic 47)
- **职责**: 物候期与积温生理追踪。对标 `GDD_Evaluator` 算法。
- **核心接口**: `get_physiological_age()`, `predict_next_phenology_eta()`.

### 3.5 `SharedQualityMixin` (Epic 15/70)
- **职责**: 社区统一品质标准与交叉审计。
- **物理载体**: 引入 **“品质指纹 (Quality Fingerprint)”** 机制，包含理化指标、检测时空坐标及检测员信誉分。

### 3.6 `ClearingEngineMixin` (Epic 104)
- **职责**: 跨实体的价值清算、内部分帐与利益分配。
- **价值基准**: 结算不以单一货币为准，而以 **“物理贡献 + 可持续性分值”** 作为核心对价单位。
- **货币化 (Monetization)**: 将 Impact Credits 最终转化为 `account.move` 的财务凭证，支持债务抵扣与外部现金分红。
- **接口**: `calculate_net_balance()`, `generate_settlement_proof()`, `monetize_impact_credits()`.

---

## 4. A2A 协同与神经系统 (Autonomous Coordination)

### 4.1 通信协议 (`PlanAPI`)
- **载荷结构**:
  ```json
  {
    "agent_id": "UUID",
    "intent": "RESOURCE_EXCHANGE | THREAT_ALERT | WEATHER_CONSENSUS",
    "steps": ["Step_1", "Step_2"],
    "dependencies": {"Step_2": ["Step_1"]},
    "constraints": {"allowed_tools": ["intervention_service"]},
    "context_memory": "Base64_Snapshot"
  }
  ```

### 4.2 评价逻辑 (`EvidenceAnalyzer`)
- **双重置信度评价**:
  - `Positive_Confidence`: 确认事件真实性的概率。
  - `Negative_Confidence`: 确认事件为误报/伪造的概率。
  - `Uncertainty`: 证据不足导致的模糊区间。
- **算法**: `analyze_evidence_dual_confidence` + `Voter_Quorum` (法定人数共识)。

### 4.3 社交信誉 (`Credit_Score`)
- **模型**: `Moltbook` 风格信誉账本。
- **惩罚机制**: `Apply_Slashing` (信誉扣减) 与全网隔离。

### 4.4 跨社区价值结算模型 (Community Clearing Model)
为了确保参与者收益，系统强制执行以下结算模式：
- **内部分帐 (Internal Netting)**：成员支出可由其向社区提供的物理资源价值自动抵销。
- **碳信用抵销 (Carbon Credit Netting)**：正向碳贡献直接转化为社区内部的“通用支付能力”。
- **易货估值 (Barter Valuation)**：服务换资源，基于 `SkillBase` 与 `GDD` 自动核算等价物理工时。
- **结算证据 (Value-Proof)**：所有结算动作必须绑定 PostGIS 物理轨迹或 IoT 计量数据。

---

## 5. 地理空间计算规格 (Spatial Specs)
- **空间聚合**: 使用 `ST_Union` 和 `ST_Contains` 实现“地块 -> 社区 -> 区域”的价值自动汇总。
- **物流优化**: 基于 `ST_Distance` 自动计算物流溢价分摊，确保地理弱势农场获益公平。
- **变量作业 (VRA)**: 5m-10m 矢量网格，NumPy 向量化处理。

---

## 6. ISL 架构下的数据隔离与共享
遵循“Your machine, Your rules”原则：
- **代理继承 (`_inherits`)**: 行业标准层 (ISL) 保持 Native Odoo 模型与农业增强模型的数据库解耦。
- **受控共享**: 只有通过 A2A 协议授权、并满足 `Credit_Score` > 800 的外部实体方可接入。

---

## 7. 脚手架自举顺序 (Implementation Sequence)
为避免循环依赖，开发应遵循以下顺序：
1. **Level 0**: `AgriViewMixin` (UI 隔离) 与 `SustainabilityMixin` (价值基准)。
2. **Level 1**: `GeoSpatialMixin` (空间网格) 与 `NutrientMixin` (养分循环)。
3. **Level 3**: `A2A_Protocol_Base` (通信) 与 `EvidenceAnalyzer` (审计)。
4. **Level 4**: `ClearingEngineMixin` (经济结算)。

---

## 8. 工程标准
- **文件限制**: Python 源码严禁超过 500 行。
- **环境红线审计**: 任何导致碳强度异常波动的代码变更必须在测试用例中明确体现其对 ESG 指标的影响。
- **原子提交**: 逻辑代码与文档（Epic/Spec）同步更新。

---
*最后更新：2026-01-31*
