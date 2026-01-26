# Odoo 19 农场管理系统：全量文档体系 (Farm Platform Docs - V6.0)

本目录存储 Odoo 19 智能农场平台（Standard V6.0）的完整知识体系。文档采用“金字塔”结构，从顶层战略到底层算法实现，为农业数字化转型提供全方位的技术与业务指引。

## 1. 文档架构概览

### 🟢 业务层 (Business Layer) - `business/`
聚焦于“做什么”以及“为谁做”，定义了系统的灵魂与蓝图。
- **[EPICS_AND_USER_STORIES.md](business/EPICS_AND_USER_STORIES.md)**: 45 个史诗需求全量索引看板。
- **[MODULE_PLAN.md](business/MODULE_PLAN.md)**: 模块实现蓝图，定义了 US 与代码 Addon 的映射关系。
- **[epics/](business/epics/)**: 45 个独立文件，承载 200+ 原子级用户故事。
- **[industries/](business/industries/)**: 12 个垂直行业（茶叶、药材、中央厨房等）的深度适配方案。

### 🔵 流程层 (Process Layer) - `business/processes/`
聚焦于“怎么流转”，通过标准模型描述端到端的农业闭环。
- **核心流程**: 种植管理流、养殖生理循环、物料平衡加工流、合作社治理流。
- **合规流程**: 农残预警流、有机转换审计流、HACCP 熔断控制。

### 🔴 算法层 (Algorithm Layer) - `algorithms/`
聚焦于“怎么算”，锁定农业专业领域的计算精度。
- **[DOMAIN_LOGIC_ALGORITHMS.md](business/DOMAIN_LOGIC_ALGORITHMS.md)**: 核心算法汇总。
- **专业模型**: NPK 养分平衡、GDD 积温预测、FCR 饲料转化率、Arrhenius 货架期计算。

### 🟡 技术层 (Technical Layer) - `technical/`
聚焦于“怎么实现”，定义了代码层级的工程标准。
- **[DEVELOPMENT_CONVENTIONS.md](technical/DEVELOPMENT_CONVENTIONS.md)**: Odoo 19 核心开发规范（Atomic Module, TDD, Mobile-First）。
- **[ODOO_MAPPING_SPEC.md](technical/ODOO_MAPPING_SPEC.md)**: 农业语义到 Odoo 原生模型（MRP/Project/Stock）的映射指南。
- **[ux_design_system.md](ux_design_system.md)**: 适配 PC、PDA 与手机的三端交互标准。

### 🟣 模型层 (Model Layer) - `model_summary.md`
系统模型的全面概览与详细技术规格。
- **[model_summary.md](model_summary.md)**: 📊 综合模型摘要，从核心基础设施到专业运营的全量模块映射，按逻辑顺序组织（Core → Land Management → Planning → Operations → Specialized → Support）。

## 2. 核心原则 (Core Principles)

1. **增量更新 (Incremental Updates)**: 保持历史痕迹，使用状态符号（✅, 🚧, 💡）追踪进度。
2. **三端视角 (Cross-Device View)**: 每一个 UX 文档必须覆盖不同终端的交互差异。
3. **真实性背书 (Traceability)**: 所有合规文档必须关联具体的 IoT 存证或法律台账要求。
4. **双语化 (Bilingual Policy)**: 内部编程英文，业务备注中文，外部交互双语。

## 3. 垂直行业支持 (Multi-Industry Verticals)

系统内置了针对以下细分行业的全套数据包与流程预置：
- **种植业**: 大田作物、设施温室、果树园艺、茶园、中药材、食用菌。
- **养殖业**: 畜牧个体/群体、水产养殖、蜜蜂迁徙养殖。
- **加工业**: 初加工分级、深加工配方、中央厨房、保健品 GMP 生产。

## 4. 维护与贡献

- 所有的变更建议必须先在相应的 Epic 或 Process 文档中细化。
- 更新 `MODULE_PLAN.md` 以确保新功能有明确的 Addon 归口。
- 文档更新后应同步刷新 `EPICS_AND_USER_STORIES.md` 索引状态。

---
**版本**: Standard V6.0.3 (Enhanced Model Documentation)
**更新日期**: 2026-01-17
