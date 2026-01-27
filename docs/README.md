# 🌾 Odoo 农业生态系统：全量知识库 (Farm Docs Portal)

欢迎。本项目是基于 **Odoo 19** 的一二三产融合智慧农场平台。本知识库记录了从业务愿景到代码实现的完整生命周期。

---

## 🗺️ 快速导航 (Quick Navigation)

### 🚀 业务蓝图 (Business & Planning)
了解我们要解决什么问题，以及如何分步实现。
- **[史诗与用户故事全集](business/EPICS_AND_USER_STORIES.md)**: 📂 索引 64 个史诗，涵盖精准农学、金融与 AI。
- **[模块开发进度看板](business/MODULE_PLAN.md)**: 🗺️ 明确 User Story 与代码 Addon 的映射关系及开发状态。
- **[史诗详情库](business/epics/)**: 📄 200+ 原子级用户故事的详细 **验收标准 (AC)**。
- **[垂直行业方案](business/industries/)**: 🍵 针对茶业、药材、中央厨房等 12 个行业的深度适配。

### 🧠 领域智能 (Agri-Intelligence)
农业生产中的“科学大脑”。
- **[核心算法规格库](algorithms/)**: 🧮 涵盖 NPK 平衡、GDD 积温预测、系谱分析等 43 个核心算法及其 **Python 参考实现**。
- **[算法总纲](business/DOMAIN_LOGIC_ALGORITHMS.md)**: 📖 农业逻辑的数学模型汇总。

### 🛠️ 技术工程 (Technical Specifications)
面向人类开发者的编码准则与架构定义。
- **[开发者总纲](../DEVELOPER_GUIDE.md)**: ⚖️ **职责分离、DRY** 与编辑安全性红线。
- **[Odoo 映射规格书](technical/ODOO_MAPPING_SPEC.md)**: 🔗 农业概念（如 Intervention）到 Odoo 原生模型（如 `mrp.production`）的映射。
- **[ISL 架构定义](technical/ISL_Architecture/)**: 🏗️ 行业标准层（Industry Standard Layer）代理继承模式。
- **[三端交互设计规范](ux_design_system.md)**: 📱 适配 PC、PDA 与移动端的去工业化交互标准。

### 🤖 AI 协作 (AI/LLM Onboarding)
- **[AI 开发者引导手册](LLM_START_HERE.md)**: 🤖 LLM 接入项目后的“第一阅读文件”，定义了规划驱动开发的黄金路径。

---

## 🏗️ 架构四大律令 (The Four Mandates)

1.  **去工业化 (De-industrialize)**: 消除制造业术语，UI 必须使用符合农业直觉的表达。
2.  **职责分离 (SoC)**: `farm_core` 负责底座，垂直模块负责逻辑，`farm_ux` 负责感官。
3.  **DRY (Don't Repeat Yourself)**: 通用计算必须沉淀为 **Mixin**，严禁代码克隆。
4.  **空间优先 (Spatial First)**: 所有的位置与地块操作必须基于 **PostGIS** 与向量化运算。

---

## 📅 版本信息
- **文档版本**: V6.1.0 (Refined Global Index)
- **最后更新**: 2026-01-27
- **状态**: 64 个史诗已定案，43 个核心算法已补全。