# 🤖 Odoo 农业生态系统：AI 开发者首席引导手册 (Master Entry)

欢迎。作为本项目的高级 AI 开发者，你必须严格遵循“**规划驱动开发 (Plan-Driven Development)**”流程与架构红线。

## 1. 核心开发工作流 (The Golden Workflow)
在执行任何代码修改前，你必须按顺序经过以下检查点：

1.  **业务对齐 (Checkpoint: Epics/US)**: 
    - 查阅 `docs/business/EPICS_AND_USER_STORIES.md` 定位所属史诗。
    - 深入阅读具体 User Story 的 **验收标准 (AC)**。
2.  **模块规划 (Checkpoint: Module Plan)**:
    - 确认功能归属的 Addon。**严禁**在 `farm_core` 中写垂直业务逻辑。
3.  **算法对标 (Checkpoint: Algorithms)**:
    - 必须与 `docs/algorithms/` 中的 Python 参考逻辑保持 100% 一致。
4.  **技术映射 (Checkpoint: Mapping)**:
    - 确认 Odoo 原生模型的映射关系（如 Intervention -> `mrp.production`）。

## 2. 四大工程律令 (The Four Mandates)
- **律令一：去工业化 (De-industrialize)**
    - UI 中严禁暴露 `MO`, `BOM`, `Work Center`。必须使用映射后的农业术语。
- **律令二：职责分离与 DRY (SoC & DRY)**
    - **逻辑归位**：核心层（元数据）、行业层（业务规则）、表现层（UI）必须严格物理隔离。
    - **逻辑复用**：通用计算（如 GDD、养分计算）必须使用 **Mixin (AbstractModel)**，严禁代码克隆。
- **律令三：ISL 架构 (Industry Standard Layer)**
    - 优先使用 `_inherits` (代理继承) 扩展原生模型，确保标准逻辑与农业逻辑互不干扰。
- **律令四：编辑安全性 (Atomic Safety)**
    - 禁止对超过 5 行的逻辑使用 `replace`。大规模修改必须使用全量回写模式。

## 3. 快速感知指令 (Quick Discovery)
- **业务标准库**：`docs/business/epics/`
- **逻辑公式库**：`docs/algorithms/`
- **术语映射表**：`farm_ux/models/term_mapping.py`
- **底座 Mixin 定义**：`farm_core/models/base_mixins.py`

---
**提示**：在开始新任务时，请先回复：“我已确认该任务归属于 [Module Name]，符合职责分离原则，并已对标相关算法 Mixin。”
