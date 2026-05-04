# 农业套件 107 模块依赖关系全景审计 (Dependency Panorama)

*版本: V2.0 | 架构演进: 4-Layer Flat Architecture*

## 1. 宏观拓扑概览 (Topological Overview)

本项目包含 107 个物理微服务模块，为解决 Odoo 颗粒度过细导致的“深层依赖链污染”问题，系统架构已正式重构为 **4 个核心业务宏层 (4-Layer Macro Architecture)**。

- **依赖环路状态**: ✅ **Green (无环)**。全局严格禁止反向循环依赖。
- **核心依赖枢纽 (Top 3 Hubs)**:
    1.  `farm_core`: 全局基座（地块、品种、GIS）。
    2.  `farm_operation`: 生产执行引擎。
    3.  `farm_agri_science`: 生物学智能计算底座。

## 2. 四层扁平化架构设计 (4-Layer Flat Architecture)

我们摒弃了物理代码层面可能造成的深达十多层的碎片化网络，在业务边界上强制划分为四大层次：

### Layer 0: 基础设施底座层 (Foundation)
- **定位**: 系统的根基，没有任何对农产品业务的假设，只提供物理和抽象框架。
- **代表模块**: `farm_core` (核心), `agri_iot` (物联协议), `farm_ux` (行业化前端交互)。

### Layer 1: 业务核心框架层 (Core Frameworks)
- **定位**: 将农业的共性特征抽象为中间件引擎，为顶层提供服务，但不涉足具体行业的页面流转。
- **代表模块**: `farm_agri_science` (积温/GDD引擎), `farm_supply_core` (供应链骨架), `precision_production` (ISA-88 精密控制)。

### Layer 2: 垂直行业应用层 (Industry Apps)
- **定位**: 系统中最庞大的一层。它们组装 Layer 1 的引擎，实现不同动植物、加工厂的最终业务闭环。
- **代表模块**: `farm_livestock` (畜牧), `farm_crop` (大田作物), `farm_processing` (深加工), `farm_agritourism` (观光农业)。
- **约束**: **本层级的模块之间严禁互相强依赖**（例如：畜牧不应依赖水产）。必须保持横向解耦，支持客户按需独立卸载。

### Layer 3: 顶层智能与合规网关 (Intelligence & Compliance)
- **定位**: 跨越具体行业的全局收口层。它们从 Layer 2 获取生产数据，进行更高维度的分析、拦截和控制。
- **代表模块**: `farm_ai_agent` (多智能体协调), `farm_esg_compliance` (出口与环境红线拦截), `farm_green_monitor` (双碳核算)。

## 3. 架构律令 (Architecture Mandates)
1. **禁止跨层穿越**: 高层 (Layer 3) 绝对禁止被底层 (Layer 1) 依赖。
2. **同层解耦**: 垂直行业应用层 (Layer 2) 的应用必须相互独立。如需数据交换，必须下沉到 Layer 1 或使用松耦合的消息总线 (Message Bus)。
3. **物理聚合**: 未来在打包发版 (Release) 时，将通过 CI/CD 将同层级的细碎功能融合为一个大一统的 `Odoo App`（如 `farm_suite_core`, `farm_suite_livestock`），以保证最终用户的安装体验扁平清爽。
