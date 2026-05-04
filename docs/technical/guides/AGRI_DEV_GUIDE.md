# 📖 Odoo 农业生态系统：LLM 自动探索与开发指南

> **LLM 注意事项**：当你第一次接触本项目时，请停止猜测，执行本指南中的“探索指令”。本项目是一个高度定制化的“去工业化”系统，任何违背农业习惯的代码都是不可接受的。

---

## 1. 核心哲学：去工业化 (The "De-industrial" Core)
本项目致力于将 Odoo 的工业基因（MO, BOM, Work Center）转换为农业基因（Intervention, Recipe, Farm Facility）。
- **必须执行的探索**：
  - `grep -r "term.mapping" farm_ux/`：查看术语是如何被拦截和替换的。
  - `cat farm_ux/models/term_mapping.py`：理解术语字典结构。

---

## 2. 模块索引与层级 (Module Hierarchy)
项目遵循 **Core -> Industry -> UX** 的三层架构：
- **`farm_core`**：定义基础模型（地块、生物资产、积温 Mixin）。
  - *探索*：`ls farm_core/models/` 查看农业元数据底座。
- **`farm_processing` / `farm_livestock` 等**：垂直行业逻辑，通常通过 `_inherits` 扩展 Odoo 原生模型。
  - *探索*：`grep -r "_inherits" farm_processing/` 理解 ISL (Industry Specific Layer) 实现。
- **`farm_ux`**：控制用户感官。
  - *探索*：`ls farm_ux/models/` 查看信号灯、大字模式等适配逻辑。

---

## 3. 开发者“肌肉记忆”：自动化指令集 (Auto-Learning Commands)
如果你被分配了一个新任务（例如：修改 VRA 逻辑），请按顺序执行：

1. **定位业务锚点**：
   - `grep -i "VRA" docs/business/EPICS_AND_USER_STORIES.md` -> 获取 Epic 编号。
   - `cat docs/business/epics/EPIC_XX.md` -> 理解验收标准 (AC)。
2. **定位算法底座**：
   - `grep -i "GDD" docs/business/DOMAIN_LOGIC_ALGORITHMS.md` -> 获取数学公式。
3. **定位现有实现**：
   - `grep -r "models.Model" . | grep "vra"` -> 查找相关 Python 类。
   - `find . -name "*view.xml" | xargs grep "vra"` -> 查找相关界面。

---

## 4. 严格编码规范 (Strict Coding Rules)

### A. 命名与术语 (Naming)
- **绝对禁止**：在 XML Label 或 Python String 中出现 "Manufacturing", "Work Order", "Routing"。
- **必须使用**：对应的农业映射词。
- **验证**：每次修改 UI 后，检查是否符合 `farm_ux/data/term_mapping_data.xml` 中的定义。

### B. 空间化逻辑 (GIS)
- 所有 `location` 相关的操作必须检查是否继承了 `farm.location`。
- *指令*：`cat farm_core/models/land_location_management.py`。

### C. 原子编辑与安全性 (Tooling)
- **`replace` 工具使用规范**：
  - `old_string` 必须包含至少 3 行上下文。
  - 修改前必须 `read_file` 确认。
- **大规模重构**：优先使用 `run_shell_command` 结合 `sed` 命令进行行号定位修改。

---

## 5. 验收标准与测试 (DoD: Definition of Done)
1. **代码合规**：符合 Odoo 19 规范且无制造业术语泄露。
2. **测试通过**：模块能正常加载（`-u module_name`）且通过逻辑验证。
3. **文档同步**：必须更新 `progress.md` 并在 `docs/` 下记录新算法。

---
*LLM 引导：现在请先读取 `docs/business/EPICS_AND_USER_STORIES.md`，然后根据你被分配的任务开始“探索阶段”。*

---

## 6. 无损修改律令 (Lossless Mandates V1.2)
- **锚点保护**: 严禁移除 `[ISA-88]`, `[LOSSLESS]` 等物理锚点。
- **500行原则**: 单个 Python 文件行数上限为 500 行。
- **原子提交**: 代码变更与文档更新必须分开提交。

*V1.2 - Synchronized with Global Mandates | 2026-02-01*
