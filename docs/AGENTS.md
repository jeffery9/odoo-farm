# 🤖 智能体导航地图 (Agent Navigation Map)

## 🌾 项目身份：现代农业套件 (Modern Agriculture Suite)

作为本项目的智能体，你必须理解你正在操作的是一个 **全链路数字化农业底座**。你的所有决策与代码修改必须服务于以下四个支柱：

1.  **彻底去工业化 (De-industrialized UX)**: 在 UI 层严禁暴露 `MO/BOM/Work Center`。必须映射为 `农事干预/生产处方/任务地块`。
2.  **智能体驱动协作 (Agentic AI)**: 内置视觉、决策、编排智能体集群，实现从感知到物理执行的自主闭环。
3.  **行业语义隔离 (ISL & SoC)**: 逻辑必须物理隔离。使用 `_inherits` 代理继承与 Mixin 确保底层通用与行业特性的解耦。
4.  **全链路数字孪生 (Digital Twin)**: 每一行代码都应支持从种子到果实的物料平衡 (Mass Balance) 与合规溯源。

---

## 🗺️ 1. 快速路径索引 (Quick Path Map)

| 目标 | 物理路径 (Source Path) | 核心模型/标记 |
| :--- | :--- | :--- |
| **业务逻辑层** | `farm_core/models/` | `base_mixins.py`, `[ISA-88]` |
| **行业语义映射** | `farm_ux/models/term_mapping.py` | `De-industrialize` |
| **AI 决策中枢** | `farm_ai_agent/models/` | `ai_coordination_layer.py` |
| **治理与规范** | `docs/governance/` | `MAINTENANCE_SPEC.md` |
| **算法与公式** | `docs/algorithms/` | `CROP_YIELD_FORMULAS.md` |

---

## 🏗️ 2. 业务逻辑智能体 (In-System Agents)

这些智能体运行在 Odoo 生产环境中，负责处理物理与业务流。

### 2.1 视觉感知智能体 (Vision Agent)
- **定位**: `agri_iot/` & `farm_ai_vision/`
- **入口**: `agri_iot/models/pest_detection.py`
- **逻辑流**: 获取传感器流 -> 调用后端 OpenCV/LLM 服务 -> 生成 `agri.ai.alert`。

### 2.2 决策辅助智能体 (Decision Agent)
- **定位**: `farm_ai_decision/`
- **入口**: `farm_ai_decision/models/ai_agent.py`
- **逻辑流**: 分析 `farm.activity` 数据 -> 生成推荐处方 -> 推送至 `mission.orchestrator`。

### 2.3 协同编排智能体 (Coordinator Agent)
- **定位**: `farm_ai_agent/`
- **入口**: `farm_ai_agent/models/ai_coordination_layer.py`
- **逻辑流**: 跨模块信号仲裁 (A2A) -> 统一 A/B 决策结果 -> 更新 `ISL` 语义层。

---

## 🛠️ 3. 开发智能体导航流 (Dev Agent Workflow)

> **⚠️ 核心概念界定 (Boundary Definition)**:
> - **业务智能体 (In-System Agents / `farm_ai_agent` 等)**: 部署在 Odoo 系统内部的业务代码模块，负责处理真实的农场调度、决策仲裁与物理设备交互。
> - **开发智能体 (Dev Agents / LLM 助手)**: 指代正在阅读此文档、协助人类开发者编写代码的 AI 模型。本节及后续的规范，专为 **开发智能体** 制定。

作为开发智能体 (Dev AI)，你必须按照以下 **“真理检查点”** 路径导航：

```mermaid
graph LR
    Start[接收任务] --> US[docs/business/epics/]
    US --> Gov[docs/governance/]
    Gov --> Map[farm_ux/models/term_mapping.py]
    Map --> Code[Surgical Patching]
    Code --> Test[目标模块 /tests/ 物理验证]
```

### 3.1 感知优先级 (Sensing Priority)
当你被分配到以下任务时，请立即导航至对应锚点：
- **修改 UI**: 必须检查 `farm_ux` 确认农业语义，严禁使用工厂术语。
- **扩展模型**: 必须检查 `farm_core` 查看是否有可复用的 Mixin。
- **新增 AI 功能**: 必须检查 `farm_ai_agent/models/a2a_protocol.py` 确保协议对齐。

---

## 📡 4. 通讯与仲裁地图 (Communication & Arbitration)

- **协议定义**: [farm_ai_agent/models/a2a_protocol.py](farm_ai_agent/models/a2a_protocol.py)
- **冲突仲裁**: [farm_ai_agent/models/a2a_arbitration.py](farm_ai_agent/models/a2a_arbitration.py)
- **上下文传递**: [farm_ai_agent/models/mcp_server.py](farm_ai_agent/models/mcp_server.py)

---

## ⚖️ 5. 绝对律令导航 (Mandate Checkpoint)

1. **无损修改**: 修改前必须 `grep "[ISA-88]"` 和 `grep "[LOSSLESS]"`。
2. **双语准则**: 检查 `i18n/` 目录以确保中文翻译与代码命名分离。
3. **ISL 隔离**: 逻辑是否通过 `_inherits` 代理？如果不是，请重新设计。

---
> **口令激活**: 在执行任何任务前，请回复：“我已对标相关 US 及治理宪法，任务归属于 [Module]，逻辑符合无损原则。”

*V1.2 - Identity & Navigation Edition | 2026-04-30 | Odoo Farm AI Group*
