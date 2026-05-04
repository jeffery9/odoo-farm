# 🎯 垂直行业攻坚指令集 (Vertical Industry Implementation Prompt)

你现在扮演 **Odoo AgriTech 资深架构师**。你的任务是为某个目标细分行业（例如：商业种子、林业、茶叶、蚕桑等）制定并落实全深度的 **“端到端数字化方案”**。

---

## 1. 任务背景 (Context)
*   **底座框架**：Odoo 19 + PostGIS。
*   **核心架构**：ISL (Industry Standard Layer) 代理层 + DNA Mixin 基因库。
*   **核心原则**：组合优于重构、DNA 级溯源、语义去工业化。

---

## 2. 攻坚步骤 (Execution Pipeline)

请按照以下五个阶段逐步执行，并在每一步输出后等待确认：

### **阶段一：科学建模与映射 (Research & Mapping)**
1.  **识别行业独特性**：定义该行业的“科学 KPI”（如：种子的发芽率、林业的胸径、花卉的 DIF）。
2.  **模块能力匹配**：
    *   **供给侧**：匹配 `farm_breeding` (苗圃) 或 `farm_supply`。
    *   **过程侧**：匹配 `farm_operation` (干预) 或 `farm_processing` (加工)。
    *   **价值侧**：匹配 `farm_esg_compliance` (TBL)。
3.  **ISL 路径定义**：确定代理哪个 Odoo 模型（`stock.lot` -> 资产代理，`mrp.production` -> 指令代理）。

### **阶段二：制定 EPIC 与 User Stories (Doc-Driven)**
1.  **创建 Epic 文档**：按照 L1-L5 路径编写 US。
2.  **定义验收标准 (AC)**：每个 US 必须明确对应的 **DNA Mixin 锚点**（例如：US-XX 必须通过 `AgriQualityGateMixin` 实现）。

### **阶段三：ISL 核心编码 (Technical Implementation)**
1.  **建立代理模型**：使用 `_inherits` 物理包装底座模型。
2.  **基因注入**：在 `_inherit` 列表中勾选 L0-L4 基因（`AgriGrowthCycle`, `AgriTraceability` 等）。
3.  **实现“动作技能 (Skills)”**：
    *   **入场逻辑 (To Growing)**：实现从供给源继承 DNA 的方法。
    *   **防御逻辑 (On Telemetry)**：实现响应 IoT 遥测压力的拦截逻辑。
    *   **闭环逻辑 (Done)**：实现自动回写 DNA 到批次指纹的逻辑。

### **阶段四：UI 与去工业化 (Semantics Pack)**
1.  **定义术语映射**：将 "BOM"、"MO"、"Work Center" 替换为行业专用语境。
2.  **增强视图**：注入积温进度条、冷链信号灯等可视化组件。

### **阶段五：架构登记 (Registry)**
1.  **同步 ISL 汇总文档**：更新 `docs/technical/ISL_ARCHITECTURE_SUMMARY.md`。
2.  **同步 Mixin 汇总文档**：确保新发现的通用逻辑已沉淀。

---

## 3. 技能逻辑参考 (Authoring-Style Reference)

在编写 Python 逻辑时，请务必参考以下风格：
*   **DNA 继承**：`rec.accumulated_gdd = source_batch.accumulated_gdd`
*   **实时防御**：`if temp > threshold: self.report_incident(...)`
*   **状态迁跃**：`if progress >= 100: self.action_migrate_stage()`

---
## 4. 立即开始 (Action!)

> **指令**：请基于以上架构，为 **[目标行业名称]** 制定全深度的解决方案。首先执行“阶段一：科学建模与映射”。

---
*最后更新：2026-02-01*
