# 农场管理系统：业务全景索引 (Business Index Central - V6.0)

本目录是 Odoo 19 农场管理系统（Farm Platform）的知识底座。它不仅是文档的集合，更是一个**业务与技术的映射中心**，通过结构化的索引，打通了“从业务愿景到代码实现”的完整链路。

## 1. 业务架构全景地图 (Documentation Map)

| 层级 | 文档名称 | 解决的核心问题 |
| :--- | :--- | :--- |
| **战略层** | **[PRODUCT_DIRECTION_SPEC.md](PRODUCT_DIRECTION_SPEC.md)** | 我们要往哪里走？系统的愿景与核心价值。 |
| | **[SOLUTION_OVERVIEW.md](SOLUTION_OVERVIEW.md)** | 系统是如何闭环的？一二三产融合的整体方案。 |
| **规划层** | **[EPICS_AND_USER_STORIES.md](EPICS_AND_USER_STORIES.md)** | 我们需要做哪些功能？45 个史诗与 200+ 用户故事索引。 |
| | **[MODULE_PLAN.md](MODULE_PLAN.md)** | 功能实现在哪个 Addon？User Story 到代码模块的物理映射。 |
| **执行层** | **[US_REFINEMENT_STRATEGY.md](US_REFINEMENT_STRATEGY.md)** | 用户故事如何写才及格？原子级 AC（验收条件）精化准则。 |
| | **[DOMAIN_LOGIC_ALGORITHMS.md](DOMAIN_LOGIC_ALGORITHMS.md)** | 核心农业计算公式是什么？NPK、GDD、FCR 等算法底座。 |
| **标准层** | **[EPIC_US_MODULE_PLAN_MAINTENANCE_SPEC.md](EPIC_US_MODULE_PLAN_MAINTENANCE_SPEC.md)** | 如何维护这些文档？增量更新与痕迹保留规范。 |
| | **[BUSINESS_PROCESS_SPEC.md](BUSINESS_PROCESS_SPEC.md)** | 流程图怎么画？Mermaid 建模标准。 |

## 2. 核心业务能力域导航 (Capability Domains)

通过下方链接，可直接跳转至细分领域的详细史诗（Epics）定义：

### 🟢 核心经营与生产 (Core ERP)
- [基础数据](epics/EPIC_01_Agricultural_Master_Data.md) | [种植管理](epics/EPIC_02_Plant_Farming_Management.md) | [养殖管理](epics/EPIC_03_Livestock_Aquaculture.md) | [BOM配方](epics/EPIC_04_Agri_Supply_Chain_BOM.md)

### 供应、物流与冷链 (Supply Chain)
- [集成供应链](epics/EPIC_09_Integrated_Supply_Chain.md) | [冷藏仓储](epics/EPIC_09_Integrated_Supply_Chain.md) | [物流配送](epics/EPIC_09_Integrated_Supply_Chain.md)

### 🔴 质量、安全与加工 (Safety & Processing)
- [农产品加工](epics/EPIC_14_Agri_Processing_Management.md) | [质量控制](epics/EPIC_15_Agri_Quality_Inspection.md) | [中央厨房](epics/EPIC_45_Central_Kitchen_Operations.md) | [安全防疫](epics/EPIC_11_Epidemic_Prevention_Biosafety.md)

### 🟡 合规、社会化与金融 (Compliance & Social)
- [中国合规](epics/EPIC_18_China_Compliance.md) | [合作社协同](epics/EPIC_19_Multi_Entity_Collaboration.md) | [国际标准](epics/EPIC_20_Data_Standardization.md) | [碳足迹/ESG](epics/EPIC_30_Carbon_ESG_Ledger.md)

### 🔵 数字化、UX 与移动端 (Digital & UX)
- [三端适配 UX](epics/EPIC_16_Agri_UX_Standard.md) | [现场作业](epics/EPIC_07_Mobile_Field_Ops.md) | [物联感知](epics/EPIC_06_IIOT_Automation.md) | [AI 洞察](epics/EPIC_28_AI_Vision.md)

## 3. 核心维护准则 (Strict Maintenance Guidelines)

为确保项目知识资产的可追溯性，所有编辑操作必须遵循：
1. **留痕式更新**: **严禁物理删除**现有业务逻辑。过时内容必须使用 `~~Markdown删除线~~`。
2. **三端视角**: UX 需求必须显式区分 PC、PDA 和手机的交互差异。
3. **技术归口**: 新增 US 必须同步在 **[MODULE_PLAN.md](MODULE_PLAN.md)** 中明确其 Addon 归口。
4. **双语政策**: 报表、标签、溯源页等面向客户的产出物必须标注双语要求。

---
**Last Updated**: 2026-01-14  
**Index Status**: Synchronized with V6.0 Baseline
