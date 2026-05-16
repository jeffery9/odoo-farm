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

## 3. 配置管理模式 (Configuration)

系统通过 `res.config.settings` 原子化控制以下行业能力的注入：
- **种植**: 大田 (`field_crops`)、设施 (`protected_cultivation`)、果树 (`orchard`)
- **养殖**: 畜牧 (`livestock`)、水产 (`aquaculture`)、蜂业 (`apiculture`)
- **加工**: 农产品加工 (`agricultural_processing`)、观光农业 (`agritourism`)

## 4. 核心业务闭环 (The Core Loops)

### 4.1 科学执行闭环 (The SD-Loop)
**感知** (IoT Telemetry) → **建模** (Science Kernel) → **决策** (VRA Engine) → **分解** (ISA-88 Phase) → **执行** (MQTT Setpoint) → **验证** (Physical Feedback)。

### 4.2 数据 DNA 价值流
**投入品溯源** (Seed/Fertilizer) → **作业存证** (Precision Map) → **生物转化** (Growth Model) → **ESG 核算** (Carbon Ledger) → **溢价销售** (Consumer Portal)。

---
*V3.7 - 2026-02-02 | 高密度功能矩阵架构 | 100% 无损维护*
