# 🤖 Odoo 农业生态系统：AI 开发者首席引导手册 (Master Entry)

欢迎。作为本项目的高级 AI 开发者，你必须严格遵循 **“文档驱动开发 (Doc-Driven)”** 流程与 **“无损修改律令”**。严禁在没有物理文档支持的情况下直接进入代码实现。

---


> **Agent Execution Policy**: Please read [../AGENTS.md](../AGENTS.md) for strict Git branching, commit separation, and specific Odoo 19 implementation rules.

## 1. 核心开发模式：文档驱动 (The Doc-Driven范式)
在执行任何代码修改前，你必须严格按物理顺序经过以下“真理检查点”：

1.  **规划与史诗 (Planning & Epics)**: 
    - 查阅 `docs/product_management/EPICS_AND_USER_STORIES.md` 定位业务目标。
    - **强制动作**：在实现前，必须先在 `docs/business/epics/` 下完善 US 及其验收标准 (AC)。
2.  **治理对齐 (Governance Sync)**:
    - 阅读 [docs/governance/MAINTENANCE_SPEC.md](docs/governance/MAINTENANCE_SPEC.md) 确认无损更新的操作要求。
    - 查阅 [docs/governance/DEVELOPMENT_CONVENTIONS.md](docs/governance/DEVELOPMENT_CONVENTIONS.md) 获取 TDD 与 500 行上限规范。
3.  **看板同步 (Module Plan)**:
    - 更新 `docs/product_management/MODULE_PLAN.md` 标记你的任务归口与进度。
4.  **算法与实现 (Algorithms & Implementation)**:
    - 算法必须与 `docs/technical/architecture/` 下的规格 100% 对标。
    - 代码中必须引用 US 编号，格式为 `# [US-XX-XX]`。

---


## 🚨 核心架构律令：4-Layer Macro Architecture
本农业套件包含 100+ 微服务模块，为了防止依赖雪崩，代码生成与设计**必须且只能**遵循以下 4 层扁平架构：
1. **L0 (Foundation)**: 底层底座 (`farm_core`, `farm_isl`, `farm_ux`)
2. **L1 (Core Engines)**: 算法引擎 (`farm_agri_science`, `farm_operation`)
3. **L2 (Industry Apps)**: 生产应用 (`farm_crop`, `farm_livestock`)。**绝对红线：L2 内部严禁横向依赖！**
4. **L3 (Value & Intelligence)**: 商业交易与顶层智能 (`farm_financial_insurance`, `farm_ai`, `farm_esg_compliance`)

## 2. 三大绝对律令 (The Absolute Mandates)

### 2.1 无损更新 (Lossless Update) - 最高红线
- **禁止精简**：严禁自主简化代码、文档或注释。
- **锚点保护**：代码中的 `[ISA-88]`, `[LOSSLESS]`, `[US-XXX]` 标记是物理资产，**严禁移除**。
- **读-改-核**：修改前必须 `read_file` 全文，修改后必须执行 `git diff` 进行锚点计数校验。

### 2.2 去工业化 UX (De-industrialize)
- **语义隔离**：UI 严禁暴露 `MO`, `BOM`, `Work Center`。
- **映射驱动**：所有表现层修改必须对标 `farm_ux/models/term_mapping.py` 的农业语义。


### 2.4 编程语言准则 (Bilingual Policy)
- **Code in English**: 所有的代码物理命名必须使用 **英文**。
- **Doc in Chinese**: 所有的代码注释、Docstring 必须使用 **中文**（保留 [ISA-88] 等架构标记）。

### 2.3 职责分离与 ISL 架构 (SoC & ISL)
- **ISL 模式**：优先使用 `_inherits` (代理继承) 扩展原生模型。
- **逻辑隔离**：水平层 (Core)、行业层 (Business)、表现层 (UI) 必须物理隔离。通用逻辑强制沉淀为 Mixin。

---

## 3. 快速感知路径 (Quick Path)
- **项目宪法中心**：`docs/governance/`
- **业务标准库**：`docs/business/epics/`
- **逻辑公式库**：`docs/technical/architecture/`
- **底座 Mixin 定义**：`farm_core/models/base_mixins.py`

---
**提示**：在开始新任务时，你必须回复：“我已对标相关 US 及治理宪法，任务归属于 [Module]，逻辑符合无损原则。”

*V2.0 - Doc-Driven & Governance Edition | 2026-02-01*
- **ISL 架构指南**: 查阅 `docs/technical/architecture/ISL_ARCHITECTURE.md` 以了解多态代理拦截机制的设计准则。
- **依赖关系审计**: 查阅 `docs/technical/architecture/DEPENDENCY_ANALYSIS.md` 以了解 110+ 个模块的拓扑层级与依赖枢纽。