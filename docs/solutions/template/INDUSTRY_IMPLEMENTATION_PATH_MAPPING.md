# 🗺️ 垂直行业细分与已实现模块匹配映射表 (V1.0)

本文件定义了如何利用现有的核心与专用模块，通过特定的技术路径（ISL + DNA）快速构建目标行业的解决方案。

---

## 1. 核心工具箱 (Implemented Capability Pool)

在匹配前，首先明确我们已具备的核心能力模块：
*   **`farm_core`**：提供空间 DNA (PostGIS)、养分 DNA、清算引擎。
*   **`farm_isl`**：提供标准模型（MO/BOM/Lot）的透明代理机制。
*   **`farm_operation`**：提供干预任务框架、气象拦截、智能指令。
*   **`farm_breeding`**：提供苗圃管理、成活率追踪、品种性状建模。
*   **`farm_processing`**：提供多级包装、HACCP 门控、批次 DNA 继承。
*   **`farm_esg_compliance`**：提供可持续性 Mixin、三重底线评估、插件化开关。
*   **`farm_ai_core`**：提供双重置信度审计、RAG 向量化接口。

---

## 2. 行业匹配与实施路径 (Sector Matching & Path)

### **A. 商业种子产业 (Seed Industry)**
*   **匹配模块**：`farm_breeding` (育苗) + `farm_processing` (包衣加工) + `farm_esg_compliance` (合规)
*   **实施路径**：
    1.  建立 `farm_seed_industry` 模块。
    2.  **ISL 代理**：`farm.seed.batch` 代理 `stock.lot`。
    3.  **DNA 注入**：注入 `AgriTraceabilityMixin` (亲本溯源) 和 `AgriQualityGateMixin` (发芽率检测)。
    4.  **复用逻辑**：复用 `farm_breeding` 的移栽逻辑进行制种田管理。

### **B. 商业林业与木材 (Forestry & Timber)**
*   **匹配模块**：`farm_core` (空间定位) + `farm_esg_carbon` (碳汇计算) + `farm_operation` (长周期任务)
*   **实施路径**：
    1.  建立 `farm_forestry` 模块。
    2.  **ISL 代理**：`farm.forest.plot` 代理 `farm.location`。
    3.  **DNA 注入**：注入 `GeoSpatialMixin` (单株定位) 和 `AgriGrowthCycleMixin` (轮伐期积温预测)。
    4.  **复用逻辑**：利用 `farm_esg_carbon` 模块的算法核算单株生物量固碳。

### **C. 蚕桑丝绸 (Sericulture)**
*   **匹配模块**：`farm_livestock` (养蚕) + `farm_field_crops` (桑园) + `farm_processing` (缫丝加工)
*   **实施路径**：
    1.  建立 `farm_sericulture` 模块。
    2.  **ISL 代理**：`farm.silkworm.batch` 代理 `stock.lot`。
    3.  **DNA 注入**：注入 `AgriGrowthCycleMixin` (5 龄状态机)。
    4.  **复用逻辑**：复用 `farm_livestock` 的 FCR 逻辑计算“叶丝转化率”。

### **D. 精油与茶叶 (Essential Oils & Tea)**
*   **匹配模块**：`farm_agricultural_processing` (精制) + `farm_operation` (采摘) + `farm_iot` (工艺监控)
*   **实施路径**：
    1.  **细分路径**：在 `farm_agricultural_processing` 下通过 `seasonal_bom` 实现。
    2.  **ISL 代理**：`farm.extraction.order` 代理 `mrp.production`。
    3.  **DNA 注入**：注入 `AgriQualityGateMixin` (萃取率、含水量)。
    4.  **复用逻辑**：复用 `farm_operation` 的积温预测确定最佳采摘期 (Flush)。

### **E. 城市农业 (Urban Agriculture)**
*   **匹配模块**：`farm_csa` (认养) + `farm_iot` (微控制) + `farm_mobile` (远程观测)
*   **实施路径**：
    1.  建立 `farm_urban_farming` 模块。
    2.  **ISL 代理**：`farm.micro.unit` 代理 `stock.lot` (单盆/单架)。
    3.  **DNA 注入**：注入 `AgriAgentInstructionMixin` (自动灌溉补光)。
    4.  **复用逻辑**：利用 `farm_csa` 的 `adopted_lot_id` 实现用户与微地块的绑定。

---

## 3. 技术实施律令 (Golden Rules)

1.  **组合优于重构**：优先通过 `_inherit` 多个已实现模块来组装新行业，严禁重复造轮子。
2.  **Mixin 基因对齐**：新行业的特征必须优先检查是否能由 L0-L4 层的 Mixin 承载。
3.  **去工业化强制执行**：所有新行业必须在 `farm_ux` 中注册其专属的术语映射。

---
*最后更新：2026-02-01*
