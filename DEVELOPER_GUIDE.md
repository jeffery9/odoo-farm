# 🛠️ Odoo 农业生态系统：技术开发与协作准则 (V1.0)

本指南定义了本项目中所有代码开发、工程重构及 AI 协作的底层规范。所有开发者（包括 AI Agent）必须严格遵守。

---

## 1. 技术栈底座 (The Stack)
- **平台**: Odoo 19 (LGPL)
- **数据库**: PostgreSQL + **PostGIS (强制要求空间功能)**
- **计算库**: NumPy, SciPy (用于农学模型计算)
- **地图**: Leaflet.js (PWA 端)
- **协议**: MQTT / ISO-XML (设备交互)

---

## 2. 核心设计原则 (Core Design Principles)

### 2.1 职责分离 (Separation of Concerns)
- **水平层 (Horizontal)**: `farm_core` 仅定义全行业共有的元数据。严禁在此包含任何特定行业的计算逻辑或财务规则。
- **垂直层 (Vertical)**: 每个行业模块（如 `farm_livestock`, `farm_processing`）应是自治的。行业特有的逻辑应留在各自模块，通过 `_inherits` 代理继承与 Odoo 原生模型交互。
- **表现层 (UX)**: 所有的术语翻译、CSS 注入、菜单重排必须归口 `farm_ux` 或行业模块的 `views/` 目录，禁止业务逻辑与表现层代码混淆。

### 2.2 DRY (Don't Repeat Yourself)
- **Mixin 优先**: 通用的农业属性（如积温计算 GDD、养分记录、空间坐标计算）必须定义为 `AbstractModel` (Mixin)。子模块必须通过继承这些 Mixin 来复用逻辑，严禁在不同模块间复制粘贴相同的计算公式。
- **领域逻辑提取**: 复杂的数学模型应提取为独立的 Python Helper 或专门的 `compute` 方法，确保一个算法在全系统中只有唯一的逻辑源头。

## 3. Odoo 开发范式与继承规范
- **Addon 前缀**: 所有自定义模块必须以 `farm_` 开头。
- **Model 前缀**: 所有自定义模型 (`_name`) **必须以 `farm.` 开头**（例如：`farm.location.grid`）。
- **职责分离原则 (Separation of Concerns)**:
    - **`farm_core` (水平层)**: 仅允许定义全行业通用的“基础元数据”（如地块坐标、品种名称、生物阶段定义、GIS工具）。**严禁**将财务结算、加工工艺、保险算法等垂直业务逻辑写入 Core。
    - **垂直业务模块 (垂直层)**: 财务功能（信用、贷款、保险）必须留在 `farm_finance_*`；加工逻辑留在 `farm_processing`；具体的养殖/种植逻辑留在各自的行业模块中。
    - **跨模块交互**: 垂直模块应通过 `_inherit` 扩展水平层的模型（如在财务模块中扩展 `farm.task` 增加信用分字段），而不是直接修改水平层的代码。
- **UX 表现分离**: 所有的菜单翻译、表单布局微调应通过 `farm_ux` 模块实现，保持业务逻辑模块的纯净。


### 2.2 模型继承规范
- **ISL (Industry Specific Layer)**: 优先使用 `_inherits` (多重继承/代理) 将 Odoo 标准模型（如 `stock.lot`）包装为农业模型（如 `farm.lot.harvest`），以保持 Odoo 原生逻辑的完整性。
- **Mixin 复用**: 继承 `common.agricultural.fields` 等抽象模型以确保基础字段（标识号、生长期、品质等级）的一致性。

---

## 3. 编辑安全性与工具规约 (Critical Safety)

### 3.1 `replace` 工具使用禁令
- **禁止模糊匹配**: `old_string` 必须具有唯一性，严禁省略缩进或删除多行上下文。
- **强制先读后写**: 修改文件前必须执行 `read_file` 确认目标代码段的状态。
- **5 行原则**: 超过 5 行的大规模逻辑修改，禁止使用 `replace`，应改用 `write_file` 或 Shell 命令。

### 3.2 Shell 自动化指令 (Atomic Shell)
- **原子化**: 一个 `run_shell_command` 只执行一个原子任务（如 `mkdir` 或单个 `sed`）。
- **禁止复合**: 严禁在 Call 中使用 `&&`, `||`, `|`, `>` 等操作符，以避免沙箱拦截。
- **大规模搜索**: 优先使用 `search_file_content` 而非原生 `grep`。

---

### 3.3 无损更新原则 (Lossless Update)
- **严禁省略**: 在使用 `write_file` 或 `replace` 时，严禁使用 `...` 或 `(此处省略)` 占位符。这会导致历史文档（如已完成的 User Stories）或代码逻辑被物理删除。
- **全量闭环**: 对于超过 5 行的文档修改，必须执行 `read_file` 获取全文，在本地内存中完成合并后，一次性全量回写。
- **审计留痕**: 所有的更新必须保留原有的序号和标签，仅允许增量追加或对特定错误进行修正。

## 4. 空间数据与性能 (GIS & Performance)
- **空间索引**: 任何新增的 `Geometry` 字段必须在 SQL 层面建立 `GIST` 索引。
- **计算外挂**: 复杂的网格运算（如 VRA 处方计算）必须在 Python 层通过 **NumPy 向量化**处理，严禁在 Odoo 模型循环中进行空间拓扑运算。
- **缓存策略**: 溯源接口等高频读操作必须实现缓存机制。

---

## 5. 协作与交付协议 (The Handshake)

### 5.1 任务开始 (On Task Start)
- 必须读取 `task_plan.md` 和 `progress.md`。
- 必须确认当前处理的 User Story 及其验收标准 (AC)。

### 5.2 进度汇报 (Progress Sync)
- 每完成一个原子步骤（如“创建模型”、“增加视图”），必须向用户简要确认。
- **禁止静默编辑**: 严禁在不解释的情况下连续修改多个文件。

### 5.3 验收定义 (DoD)
- 代码通过 Pylint/Odoo-lint 校验（若适用）。
- `__manifest__.py` 已更新依赖关系。

---
**核心提醒**: 记住，我们是在构建一个科学系统。如果一个算法没有在 `docs/business/DOMAIN_LOGIC_ALGORITHMS.md` 中备案，它就不应该存在。

ref.  `docs/technical/DEVELOPMENT_CONVENTIONS.md`
