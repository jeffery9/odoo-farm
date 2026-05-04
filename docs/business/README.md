# 农场管理系统：业务全景索引 (Business Index Central - V8.0)

本目录是 Odoo 19 农场管理系统（Farm Platform）的**业务中枢与治理核心**。它不仅是文档库，更是“业务愿景 -> 规划治理 -> 代码落地”的中央控制台。

## 1. 核心治理架构 (Governance Framework)

系统采用 **“一法一规”** 的双层治理体系，确保产品演进的严肃性与一致性。

| 层级 | 关键文档 | 核心作用 |
| :--- | :--- | :--- |
| **🏛️ 治理宪法** | **[MAINTENANCE_SPEC.md](MAINTENANCE_SPEC.md)** | **最高纲领**。定义生命周期、文档即真理原则、同步机制与审计标准。 |
| **📘 执行规范** | **[CLASSIFICATION_GUIDELINES.md](CLASSIFICATION_GUIDELINES.md)** | **操作指南**。定义 US 六维价值模型、归口精化准则与分类标准。 |

---

## 2. 业务规划全景 (Business Landscape)

| 领域 | 文档入口 | 描述 |
| :--- | :--- | :--- |
| **战略方向** | **[PRODUCT_DIRECTION_SPEC.md](PRODUCT_DIRECTION_SPEC.md)** | 产品愿景、B2G/G2B 双轮驱动战略、L1-L5 演进路线图。 |
| **业务闭环** | **[SOLUTION_OVERVIEW.md](SOLUTION_OVERVIEW.md)** | “种子到餐桌”全链路集成方案，解决痛点与技术架构。 |
| **需求矩阵** | **[EPICS_AND_USER_STORIES.md](EPICS_AND_USER_STORIES.md)** | 史诗全集索引。包含从 001 到 129 的全量 129 个史诗级需求与数百项具有 BDD 验收标准 (AC) 的核心用户故事。 |
| **实施落地** | **[MODULE_PLAN.md](MODULE_PLAN.md)** | **技术映射中心**。定义功能在 Addons 中的物理归属与开发状态。 |
| **领域智慧** | **[DOMAIN_LOGIC_ALGORITHMS.md](DOMAIN_LOGIC_ALGORITHMS.md)** | 核心算法库。NPK 养分平衡、GDD 积温、AI 决策模型等公式定义。 |
| **流程标准** | **[BUSINESS_PROCESS_SPEC.md](BUSINESS_PROCESS_SPEC.md)** | 跨模块集成流程图（Mermaid）、核心硬约束（Hard-Blocks）定义。 |

---

## 3. 核心业务能力域导航 (Capability Domains)

快速跳转至细分领域的详细史诗定义：

### 🟢 核心生产与运营 (Core Production)
- [基础数据](epics/EPIC_001_Agricultural_Master_Data.md) | [种植管理](epics/EPIC_002_Plant_Farming.md) | [畜牧养殖](epics/EPIC_003_Livestock_Aquaculture.md) | [林果园艺](epics/EPIC_064_Perennial_Orchard.md)

### 🚜 资源、设备与作业 (Resources & Operations)
- [现场作业](epics/EPIC_007_Mobile_Field_Ops.md) | [农机管理](epics/EPIC_052_Drone_Operations.md) | [劳动力调度](epics/EPIC_036_HR_Labor_Scheduling.md) | [精准农业(VRA)](epics/EPIC_076_Precision_Production_VRA.md)

### 📦 供应链与加工 (Supply Chain & Processing)
- [集成供应链](epics/EPIC_009_Integrated_Supply_Chain.md) | [产后加工](epics/EPIC_037_Agri_Processing_Management.md) | [BOM配方](epics/EPIC_004_Agri_Supply_Chain_Recipe.md) | [质量控制](epics/EPIC_038_Agri_Quality_Inspection.md)

### 💰 市场、营销与品牌 (Market & Brand)
- [品牌营销](epics/EPIC_008_Marketing_Engagement.md) | [溯源体系](epics/EPIC_079_Holistic_Traceability_Marketing.md) | [CSA订阅](epics/EPIC_066_Urban_Community_Farming.md) | [直播电商](epics/EPIC_051_Live_Streaming_Douyin.md) | [销售与循环利用综合规划](SALES_MARKETING_COMPREHENSIVE_PLAN.md)

### 🛡️ 合规、风险与金融 (Compliance & Finance)
- [认证合规](epics/EPIC_035_Certification_Organic_Farming.md) | [ESG/碳足迹](epics/EPIC_060_Carbon_ESG_Ledger.md) | [农业保险](epics/EPIC_078_Agri_Financial_Credit_Insurance.md) | [合作社协同](epics/EPIC_042_Multi_Entity_Collaboration.md)

### 🧠 智能、数据与 UX (Intelligence & Digital)
- [AI 决策平台](epics/EPIC_088_AI_Decision_Support_Platform.md) | [LLM 集成](epics/EPIC_089_AI_LLM_Integration.md) | [AI 视觉](epics/EPIC_058_AI_Vision.md) | [UX 标准](epics/EPIC_039_Agri_UX_Standard.md)

---

## 4. 黄金开发路径 (The Golden Path)

在开始任何代码开发前，必须遵循以下步骤：

1.  **查阅宪法**：确认 `MAINTENANCE_SPEC.md` 中的状态要求。
2.  **定位需求**：在 `EPICS_AND_USER_STORIES.md` 找到对应的 Epic。
3.  **精化 US**：依据 `CLASSIFICATION_GUIDELINES.md` 完善验收标准（AC）。
4.  **映射模块**：在 `MODULE_PLAN.md` 确认代码归属的 Addon。
5.  **对齐算法**：查阅 `DOMAIN_LOGIC_ALGORITHMS.md` 确保计算逻辑准确。
6.  **执行开发**：代码实现与测试。

---
**Last Updated**: 2026-05-04
**Governance Status**: Active (Constitutional Era)