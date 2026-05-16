# 🌐 Odoo 农业生态系统：全景架构与功能规格书

> **版本**: V3.0 (2026-02-02)
> **状态**: 工业级标准 [ISA-88] [L0-L4]
> **核心哲学**: 去工业化、科学驱动、空间闭环

---

## 1. 系统架构图 (System Architecture)
展示了从底层物联网通讯到高层 UI 注入的五层解耦架构，体现了系统的纵向深度与模块化依赖。

```mermaid
flowchart TD
    classDef core fill:#e1f5fe,stroke:#01579b,stroke-width:2px;
    classDef biz fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px;
    classDef sci fill:#fff3e0,stroke:#ef6c00,stroke-width:2px;
    classDef pre fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px;
    classDef ux fill:#eceff1,stroke:#455a64,stroke-width:2px;

    subgraph L4["UX 表现与交互层 (Level 4)"]
        UX["farm_ux (去工业化注入)"]
        Mobile["farm_mobile (移动现场)"]
        Dash["farm_dashboard (经营看板)"]
    end

    subgraph L3["精密物理层 (Level 3 - Precision)"]
        PreProd["farm_operation (ISA-88)"]
        PreIoT["farm_iot (MQTT 闭环)"]
    end

    subgraph L2["科学决策层 (Level 2 - Intelligence)"]
        VRA["farm_agri_science (VRA 引擎)"]
        AI["farm_ai_agent (智能体协调)"]
        Vision["farm_ai_vision (视觉诊断)"]
    end

    subgraph L1["业务执行层 (Level 1 - Operation)"]
        Op["farm_operation (农事干预)"]
        Supply["farm_supply (供应链)"]
        Finance["farm_financial (农业金融)"]
    end

    subgraph L0["核心基础层 (Level 0 - Foundation)"]
        Core["farm_core (GIS/地块/主数据)"]
        ISL["farm_isl (行业标准代理层)"]
        IoT["agri_iot (物联通讯底座)"]
    end

    %% 依赖关系
    IoT --> PreIoT
    Core --> Op
    ISL --> Op
    Op --> VRA
    VRA --> PreProd
    PreProd --> PreIoT
    PreIoT --> Mobile
    VRA --> UX

    class L0 core;
    class L1 biz;
    class L2 sci;
    class L3 pre;
    class L4 ux;
```

---

## 2. 功能结构图 (Functional Structure)
展示了系统面向终端用户的核心业务能力矩阵。

```mermaid
flowchart LR
    classDef category fill:#f9f9f9,stroke:#333,stroke-dasharray: 5 5;
    classDef func fill:#fff,stroke:#333,stroke-width:1px;

    Root["Odoo AgriTech 功能全景"]

    subgraph AgriOps["精准农事管理"]
        F1["农事干预 (Intervention)"]
        F2["生产季与 Cultural Itinerary"]
        F3["收获分级与批次存证"]
    end

    subgraph Precision["VRA 科学变量系统"]
        F4["GDD 生理钟与生长模型"]
        F5["NDVI 空间网格分析"]
        F6["生物量亏缺补偿算法"]
        F7["品种响应曲线 (Mitscherlich)"]
    end

    subgraph IoTAuto["物联与自动化"]
        F8["MQTT 设备实时采集"]
        F9["ISA-88 相位控制 (Recipe)"]
        F10["空间动态设定点 (SD-Loop)"]
    end

    subgraph Business["商业与合规"]
        F11["农业金融与信贷评估"]
        F12["ESG 碳足迹与循环经济"]
        F13["基于品质的动态定价"]
        F14["全链路透明追溯系统"]
    end

    Root --> AgriOps
    Root --> Precision
    Root --> IoTAuto
    Root --> Business

    class AgriOps,Precision,IoTAuto,Business category;
    class F1,F2,F3,F4,F5,F6,F7,F8,F9,F10,F11,F12,F13,F14 func;
```

---

## 3. 架构核心亮点 (Architectural Highlights)

### 3.1 语义隔离与去工业化 (De-industrialization)
系统通过 `farm_ux` 模块实现“动态视图拦截”，将 Odoo 原生的工业术语（MO, BOM, Work Center）实时重映射为农业语境（Intervention, Recipe, Facility）。这保证了系统既拥有强大的制造内核，又具备贴合农民直觉的用户体验。

### 3.2 纵向闭环控制 (Vertical Closed-loop)
系统打通了从 **规划 -> 科学 -> 执行** 的纵向链路：
- **Level 1 (Operation)**: 解决“合规”与“成本”。
- **Level 2 (Science)**: 解决“变量”与“效率”。
- **Level 3 (Precision)**: 解决“执行”与“反馈”。

### 3.3 空间动态设定点驱动 (SD-Loop)
通过 VRA 处方图与 IoT 遥测数据的实时空间匹配（GPS -> Grid Map），系统能够根据设备所处的物理位置自动下发 MQTT 指令修改执行参数（Setpoint），实现了真正的自动化变量作业。

### 3.4 科学底座化 (Science as a Mixin)
所有的生长模型、生理指标和积温计算均封装在核心 Mixin 中，确保了从简易记录到精密自动控制的所有模块都基于同一套科学逻辑，消除了数据烟囱。

---
*文档归档于: docs/architecture/SYSTEM_FULL_LANDSCAPE.md*
