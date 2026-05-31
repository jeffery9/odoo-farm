# Odoo 19 农场管理系统 (FMS) 架构蓝图

本项目采用“工业级全栈功能矩阵 (Industrial Full-Stack Matrix)”。架构设计通过高密度的功能模块堆叠，实现了从物理底层到认知表现层的全链路科学覆盖。

## 1. 系统组件堆叠图 (Component Stack)
展示系统模块间的物理容器与继承关系。

```mermaid
flowchart TD
    classDef layerBox fill:#fdfefe,stroke:#333,stroke-width:2px;
    classDef coreSpine fill:#fff9c4,stroke:#fbc02d,stroke-width:2px;

    subgraph L4 [<b>L4: 用户交互层</b>]
        direction LR
        UX["farm_ux"] --- Dash["farm_dashboard"] --- Mob["farm_mobile"]
    end

    subgraph L3 [<b>L3: 精密执行层</b>]
        direction LR
        Pre["farm_operation"] --- PIoT["farm_iot"]
    end

    subgraph L2 [<b>L2: 科学决策层</b>]
        direction LR
        VRA["farm_agri_science"] --- AI["farm_ai_agent"]
    end

    subgraph L1 [<b>L1: 业务引擎层</b>]
        direction LR
        Op["farm_operation"] --- Sup["farm_supply"] --- Fin["farm_financial"]
    end

    subgraph L0 [<b>L0: 内核底座层</b>]
        direction LR
        Core["farm_core"] --- ISL["farm_isl"]
    end

    Core ==> Op ==> VRA ==> Pre ==> UX
    class Pre,PIoT,VRA,Op coreSpine;
```

## 2. 系统逻辑分层矩阵 (Layered Functional Matrix)

该图通过功能簇的密集堆叠展示系统的技术广度与深度，最大限度减少连线干扰。

```mermaid
flowchart TD
    %% 样式定义
    classDef pLayer fill:#e1f5fe,stroke:#01579b,stroke-width:2px;
    classDef aLayer fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px;
    classDef sLayer fill:#fff3e0,stroke:#ef6c00,stroke-width:2px;
    classDef bLayer fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px;
    classDef iLayer fill:#f5f5f5,stroke:#333,stroke-width:2px;
    classDef component fill:#fff,stroke:#999,stroke-width:1px,font-size:12px;

    %% I. 表现与交互层
    subgraph Presentation ["<b>V. 表现与认知交互层 (Presentation & Cognitive Interface)</b>"]
        direction LR
        subgraph P_UI ["UI 注入引擎"]
            P1["去工业化动态映射"]:::component
            P2["多端自适应布局"]:::component
        end
        subgraph P_Field ["现场交互"]
            P3["PWA 离线地理存证"]:::component
            P4["AR 辅助巡检界面"]:::component
        end
        subgraph P_AI ["决策交互"]
            P5["RAG 农艺知识问答"]:::component
            P6["智能预警横幅"]:::component
        end
    end

    %% II. 应用服务与调度层
    subgraph Application ["<b>IV. 应用服务与协同调度层 (Application & Orchestration)</b>"]
        direction LR
        subgraph A_Agent ["AI 智能体集群"]
            A1["任务编排智能体"]:::component
            A2["多源决策聚合器"]:::component
        end
        subgraph A_IoT ["物联数据中枢"]
            A3["实时遥测分发器"]:::component
            A4["设备影子同步 (Twin)"]:::component
        end
        subgraph A_Rule ["规则自动化"]
            A5["地理围栏判定引擎"]:::component
            A6["异常触发工作流"]:::component
        end
    end

    %% III. 农学科学与决策层
    subgraph Science ["<b>III. 农学科学内核层 (Agri-Science Kernel)</b>"]
        direction LR
        subgraph S_Model ["生物生长模型"]
            S1["GDD 生理钟计算"]:::component
            S2["Logistic 曲线模拟"]:::component
            S3["品种响应指纹 (GEM)"]:::component
        end
        subgraph S_VRA ["空间决策引擎"]
            S4["VRA 变量处方算法"]:::component
            S5["生物量亏缺补偿"]:::component
            S6["LAI 光合潜力校准"]:::component
        end
        subgraph S_Env ["环境动力学"]
            S7["养分转化动力学修正"]:::component
            S8["气象风险对冲模型"]:::component
        end
    end

    %% IV. 精密物理执行层
    subgraph Precision ["<b>II. 精密物理执行层 (Precision & Physical Loop)</b>"]
        direction LR
        subgraph E_Batch ["ISA-88 批量控制"]
            E1["Procedure 过程管理"]:::component
            E2["Unit 控制配方"]:::component
            E3["Phase 原子相位执行"]:::component
        end
        subgraph E_Loop ["实时控制环 (SD-Loop)"]
            E4["GPS 空间位置匹配"]:::component
            E5["Setpoint 动态注入"]:::component
            E6["PID 流量/压力反馈"]:::component
        end
    end

    %% V. 基础设施与领域底座
    subgraph Infrastructure ["<b>I. 基础设施与领域底座 (Infrastructure & Domain Foundation)</b>"]
        direction LR
        subgraph I_Data ["数据与空间内核"]
            I1["PostGIS 矢量数据库"]:::component
            I2["Asset DNA 继承模型"]:::component
            I3["Odoo 19 Registry"]:::component
        end
        subgraph I_Bus ["通讯与安全总线"]
            I4["MQTT / ISO-XML 协议"]:::component
            I5["RBAC 空间权限矩阵"]:::component
            I6["分布式审计日志"]:::component
        end
    end

    %% 核心纵向连接 (仅保留脊柱)
    Infrastructure ==> Science ==> Precision ==> Presentation

    %% 样式应用
    Presentation:::pLayer
    Application:::aLayer
    Science:::sLayer
    Precision:::bLayer
    Infrastructure:::iLayer
```

## 3. 核心设计哲学 (Design Philosophy)

### 3.1 Agri (领域事实) vs. Farm (业务实体) 的解耦
系统严格遵循 **“Agri 优先，Farm 受限”** 的语义原则：
*   **Agri 层**：定义跨农场的“物理真理”与“科学标准”（如：品种养分需求、传感器原始报文提取规则）。
*   **Farm 层**：定义特定实体的“业务切片”与“经营活动”（如：地块分配、特定干预记录、财务核销）。
*   **收益**：实现了“科学逻辑”与“业务流程”的物理隔离，支持同一套科学内核服务于多种不同的农场经营模式。

### 3.2 ISL (Industry Standard Layer) 代理机制
首创多态代理架构，通过 `_inherits` 机制在底层供应链（MRP/Stock）保持稳定的同时，为不同垂直行业（种植、养殖、果木）提供高度特化的 UI 交互与业务逻辑映射。

## 4. 三大核心闭环 (The Three Core Loops)

### 4.1 科学执行闭环 (The SD-Loop)
**感知 (IoT Telemetry)** → **建模 (Science Kernel)** → **决策 (VRA Engine)** → **分解 (ISA-88 Phase)** → **执行 (MQTT Setpoint)** → **验证 (Physical Feedback)**。
实现了从传感器数据到物理动作的自动化、科学化闭环。

### 4.2 数据 DNA 价值流 (The Value Stream)
**投入品溯源 (Seed/Fertilizer)** → **作业存证 (Spatial Map)** → **生物转化 (Growth Model)** → **ESG 核算 (Carbon Ledger)** → **溢价销售 (Traceability Passport)**。
确保每一批次产品都携带完整的“生命履历”，支撑高端品牌溢价。

### 4.3 金融级组织隔离 (RLS Firewall)
**村集体 (L1)** → **承包户 (L2)** → **临时散工 (L3)**。
首创三级动态 RLS 防火墙，支持垂直穿透式监控与水平绝密隔离，解决了合作社模式下的隐私与审计痛点。

## 5. 配置管理模式 (Configuration)

---
*V4.0 - 2026-05-31 | 工业级分布式架构 | 2026 深度重构同步版*
