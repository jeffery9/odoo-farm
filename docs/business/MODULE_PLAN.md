# Odoo 19 农场管理系统：模块规范与进度看板 (V3.0)

> **产品规划律令 (2026)**: 
> 1. 本文档是产品规划活动的核心载体，任何核心架构的变更、新 Level 的突破必须在代码入库前/后 24 小时内在此文档中完成语义对齐。
> 2. 只有在此文档中完成“职责定义”的功能才具备物理实现的合法性。

本项目采用高度模块化的架构，将复杂的农业业务拆分为原子化模块，以确保系统的灵活性和 Odoo 19 社区版的兼容性。

## 原子模块组合解决方案 (Atomic Module Composition Solution)

### 核心原则 (Core Principles)
- **模块原子性 (Modular Atomicity)**: 每个模块实现单一职责，专注于特定业务领域
- **组合灵活性 (Compositional Flexibility)**: 通过配置实现模块的灵活组合，支持不同业务场景
- **业务隔离 (Business Isolation)**: 模块间业务逻辑相互独立，避免耦合干扰
- **可插拔性 (Pluggability)**: 模块可独立安装、启用、停用和卸载

### 组合模式 (Composition Patterns)
- **垂直行业组合**: 同一产业链上下游模块组合（如：`farm_field_crops` + `farm_agricultural_processing`）
- **功能增强组合**: 基础业务模块与功能增强模块组合（如：`farm_operation` + `farm_iot`）
- **服务集成组合**: 业务模块与服务模块组合（如：`farm_livestock` + `farm_mobile`）
- **复合业务组合**: 多个行业模块组合支持复合型农业经营（如：`farm_apiculture` + `farm_agritourism` + `farm_marketing`）

### 配置管理 (Configuration Management)
- **res.config.settings**: 通过配置界面实现模块的启用/禁用
- **依赖解析**: 自动处理模块间的依赖关系
- **权限聚合**: 模块启用时自动聚合相应权限
- **界面调整**: 根据启用模块动态调整用户界面

### 实施约束 (Implementation Constraints)
- **接口标准化**: 模块间通过标准化接口进行交互
- **数据模型扩展**: 通过继承机制扩展现有数据模型
- **事件驱动通信**: 模块间通过事件系统进行松耦合通信
- **权限控制独立**: 每个模块维护自己的权限体系

## 2. 产品治理与规范文档

### 2.1 核心规范文档
- **产品方向规范**: `docs/business/PRODUCT_DIRECTION_SPEC.md` - 定义产品发展方向、治理机制和战略规划
- **史诗-插件实施规范**: `docs/business/EPIC_ADDON_MAPPING_SPEC.md` - 定义史诗和用户故事在 Odoo 插件中的 实施标准
- **规划维护管理规范**: `docs/governance/MAINTENANCE_SPEC.md` - 定义史诗、用户故事、模 块规划的维护管理流程
- **模块规范与进度看板**: 本文档 - 定义模块矩阵、职责和开发计划

### 模块矩阵与全量追踪看板 (Total Epic Tracking Matrix)

| 史诗 (Epic) | 包含的 US ID | 承载模块 (预估/实际) | 状态 |
|---|---|---|---|
| **Epic 001: 农业基础主数据 (Agricultural Master Data)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 002: 种植生产管理 (Plant Farming)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 003: 畜牧与水产养殖管理 (Livestock & Aquaculture)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 004: 农业特色供应链与 Recipe (Agri-Supply Chain & Recipe)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 005: 观光农业与体验经济 (Agritourism & Experience)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 006: IIOT 环境感知与自动化 (IIOT & Automation)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 007: 移动端友好与现场作业 (Mobile-First Field Ops)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 008: 精准营销与客户参与 (Marketing & Engagement)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 009: 全链路集成供应链 (Integrated Supply Chain)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 010: 农业循环经济与增值销售平台 (Agricultural Circular Economy & Value-Added Sales Platform)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 011: 农业企业可持续发展与价值创造框架 (Agricultural Business Sustainability & Value Creation Framework)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 012: 智能体自主市场与动态定价 (A2A Autonomous Market & Dynamic Pricing)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 013: 物理协同与共享基础设施 (Physical Synergy & Shared Infrastructure)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 014: 跨社区价值结算与清算 (Inter-Community Value Clearing & Settlement)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 015: 花卉与观赏园艺管理 (Floriculture & Ornamental Horticulture)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 016: 中药材与药用植物管理 (Medicinal Plants Management)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 017: 茶叶生产与精制管理 (Tea Industry Management)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 018: 畜牧养殖智能管理 (Livestock Smart Management)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 019: 水产养殖智能管理 (Aquaculture Smart Management)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 020: 育苗与育种管理 (Nursery & Breeding)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 021: 智能养蜂与蜜源追踪管理 (Apiculture Smart Management)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 022: 食用菌生产与环境精准控制管理 (Mushroom Smart Management)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 023: 精油提取工艺与品质全链路管理 (Essential Oil Management)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 024: 净菜加工与包装全链路管理 (Net Vegetables Management)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 025: HACCP 数字化食品安全管控体系 (HACCP Digital Safety)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 026: 葡萄园精密管理与风土数字化 (Viticulture Smart Management)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 027: 酿造与酒窖工艺管理 (Winery & Enology Management)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 028: 火腿加工与窖藏工艺管理 (Dry-Cured Ham Management)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 029: 水产加工与冷冻链条管理 (Aquatic Product Processing)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 030: 商业种子研发与分销合规管理 (Seed Industry Management)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 031: 防疫、植保与生物安全 (Epidemic Prevention & Biosafety)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 032: 传统发酵与酿造工艺管理 (Traditional Fermentation Management)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 033: 稻渔/稻虾共生生态管理 (Rice-Fish/Shrimp Symbiosis)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 034: 工厂化循环水养殖（RAS）精密管控 (RAS Factory Fisheries)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 035: 认证、绿色食品与有机农业 (Certification & Organic Farming)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 036: 劳动力管理与调度 (HR & Labor Scheduling)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 037: 农产品加工管理 (Agri-Processing Management)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 038: 农业质量控制与检测 (Agri-Quality & Inspection)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 039: 用户体验与术语去工业化 (Agri-UX & De-industrialization)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 040: 行业深度与合规 (Advanced Industry & Compliance)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 041: 中国合规与政策适配 (China Compliance & Policy Adaptation)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 042: 多实体协同与合作社管理 (Multi-Entity Collaboration & Cooperative)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 043: 农业精准制造桥接核心 (Agri-Precision Bridge Core)** | US-AGRI-01 等 5 个 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 044: 精密生产执行基座 (Precision Production Foundation)** | US-044-01 等 9 个 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 045: 农学科学底座 (Agri-Science Foundation)** | US-045-01 等 9 个 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 046: AI 智能决策支持 (AI Decision Support)** | US-046-01 等 3 个 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 047: IoT 边缘协调与主动控制 (Edge Orchestration & Active Control)** | US-047-01 等 3 个 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 048: 农业主动干预 UX (Agri-UX for Active Intervention)** | US-048-01 等 3 个 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 049: Blockchain-based Biological Asset Evidence** | US-049-01 等 4 个 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 050: 智能灌溉管理 (Intelligent Irrigation Management)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 051: 直播与抖音对接 (Live Streaming & Douyin Integration)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 052: 农用无人机作业集成 (Agricultural Drone Operations)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 053: 地理围栏与资产边界安全 (Geofencing & Boundary Security)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 054: 移动端现场打卡与工时校验 (Mobile Site Check-in)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 055: 通用现场证据存证系统 (Generic Field Evidence)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 056: 现场作业服务 (Field Operations Services)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 057: 农业循环经济与废弃物资源化 (Circular Economy)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 058: AI 预测性洞察与智能视觉 (AI & Vision)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 059: 农业金融风险与保险联动 (Agri-Risk & Insurance)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 060: 碳足迹追踪与可持续性账座 (Carbon & ESG Ledger)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 061: 逆向供应链与精准召回 (Reverse Supply Chain)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 062: 品牌价值、地理标志与有机诚信体系 (Brand, GI & Organic)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 063: 设施农业、温室与植物工厂 (CEA & Vertical Farming)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 064: 多年生作物、林果与茶园管理 (Perennial & Orchard)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 065: 特种养殖与高密度工业化养殖 (Intensive Livestock)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 066: 城市农业、共享认养与微农场 (Urban & Community Farming)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 067: 农业综合生产效能 (OPE) 与决策智能 (Agri-OPE Intelligence)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 068: 牲畜健康监测与智能管理 (Livestock Health Monitoring & Smart Management)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 069: 农业气象站与环境监测 (Agricultural Weather Station & Environmental Monitoring)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 070: 精准施肥系统 (Precision Fertilization System)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 071: 无人机作物监测与管理 (Drone-based Crop Monitoring & Management)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 072: 智能温室控制 (Smart Greenhouse Control)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 073: 杂草识别与智能控制 (Weed Identification & Smart Control)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 074: 产后品质管理与保鲜 (Post-harvest Quality Management & Preservation)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 075: 农业知识管理与智能决策支持 (Agricultural Knowledge Management & Intelligent Decision Support)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 076: 精准生产与变量作业 (Precision Production & VRA)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 077: 生物生长智能与动态决策 (Biological Growth Intelligence)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 078: 农业金融信用与指数保险 (Agri-Financial Credit & Insurance)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 079: 全息溯源与交互式品牌营销 (Holistic Traceability & Marketing)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 080: 层级视图容器与多维管理视角 (Hierarchy View Containers)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 081: 计算机视觉分析 (Computer Vision Analysis)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 082: 高级溯源系统 (Advanced Traceability System)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 083: 数字化农业平台 (Digital Agriculture Platform)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 084: ISL 行业标准层架构 (Industry Standard Layer - ISL)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 085: 农业网络安全与数据保护 (Agricultural Cybersecurity & Data Protection)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 086: ESG 合规与可持续发展管理 (ESG Compliance & Sustainability)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 087: 综合农业物联网平台 (Integrated Agricultural IoT Platform)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 088: AI 智能决策支持平台 (AI Decision Support Platform)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 089: AI 大语言模型集成与 RAG 增强 (AI LLM Integration & RAG)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 090: AI 金融分析与风险评估 (AI Financial Analytics & Risk Management)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 091: 农用机器人与自动化 (Agricultural Robotics & Automation)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 092: AI 驱动的协调与工作流 (AI-Driven Coordination & Workflow)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 093: 数字孪生农业 (Digital Twin Agriculture)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 094: 智能畜禽管理 (Smart Livestock Management)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 095: 极致匠心农业与包容性作业管理 (Artisan Excellence & Inclusive Operations)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 096: 全球出口合规审计中枢 (Global Export Compliance Engine)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 097: 产销撮合协同平台 (Market-Direct Connection Platform)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 098: 供应链模块职责分离 (Supply Chain Module Separation)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 099: AI 驱动的智能供应链 (AI Driven Smart Supply Chain)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 100: 多农场供应链协同 (Multi-Farm Supply Chain Collaboration)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 101: 供应链全链路集成 (Supply Chain End-to-End Integration)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 102: 品牌保护与知识产权 (Brand Protection and Intellectual Property)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 103: 品牌与供应链协同 (Brand and Supply Chain Synergy)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 104: 供应链需求侧管理 (Supply Demand-Side Management)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 105: 供应链风险管控 (Supply Chain Risk Management)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 106: 供应链碳足迹追踪 (Supply Chain Carbon Footprint Tracking)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 107: 全球供应链治理 (Global Supply Chain Governance)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 108: 高级VRA算法与生理决策融合 (Advanced VRA Algorithms & Physiological Fusion)** | US-108-01 等 13 个 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 109: VRA经济性分析与优化 (VRA Economic Analysis & Optimization)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 110: VRA环境影响评估 (VRA Environmental Impact Assessment)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 111: VRA设备智能调度与协调 (Smart VRA Equipment Coordination)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 112: AI驱动的全链路预测性维护 (AI-driven Predictive Maintenance Across Value Chain)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 113: 碳中和与可持续发展管理 (Carbon Neutral & Sustainability Management)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 114: 农业风险与保险管理 (Agricultural Risk Management & Insurance)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 115: 农业数字孪生与仿真建模 (Agricultural Digital Twin & Simulation Modeling)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 116: 区块链溯源与食品安全保障 (Blockchain Traceability & Food Safety Assurance)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 117: 数据交换与标准化 (Data Exchange & Standardization)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 118: 订单农业与农户结算管理 (Contract Farming & Farmer Settlement)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 119: 智慧温室环境控制 (Smart Greenhouse Control)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 120: CSA社区支持农业与订单管理 (CSA Subscription & Order Management)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 121: 农用机器人与自动化 (Agricultural Robotics & Automation)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 122: 商户管理与农旅商业平台 (Merchant Management & Agri-tourism Platform)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 123: 蜂业与迁徙养殖管理 (Apiculture & Migration Management)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 124: 中药材与炮制管理 (Medicinal Herbs & TCM Processing)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 125: 食用菌与潮次管理 (Fungi & Multi-flush Harvest Management)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 126: 种质资源与生物样本库 (Germplasm & Genetic Bank)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 127: 生物质能源与外部ESG市场 (Bio-energy & External ESG Marketplace)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 128: 中央厨房运营管理 (Central Kitchen Operations)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |
| **Epic 129: 智慧供应链协同 (Smart Supply Chain Collaboration)** | 待定义 | `farm_...` | 🔄 敏捷推进中 |

| **Epic 130: 再生农业与土壤微生态 (Regenerative Agriculture & Soil Microbiome)** | US-130-01 等 4 个 | `farm_ecology`, `farm_agri_science` | 🔄 敏捷推进中 |
| **Epic 131: 新型蛋白与生物转化农业 (Alternative Proteins & Bio-conversion)** | US-131-01 等 4 个 | `farm_processing`, `farm_iot` | 🔄 敏捷推进中 |

| **Epic 132: 农光互补与能源微电网 (Agrivoltaics & Energy Microgrids)** | US-132-01 等 4 个 | `farm_iot`, `farm_equipment` | 🔄 敏捷推进中 |
| **Epic 133: 机器人与无人机“蜂群”协同编队 (Swarm Robotics Coordination)** | US-133-01 等 4 个 | `farm_robotics`, `farm_ai_agent` | 🔄 敏捷推进中 |

### 模块职责边界说明
- **Base Modules**: 核心数据和基础服务
- **Operation Modules**: 核心业务操作
- **Technology Modules**: 技术支撑模块
- **Business Modules**: 商业功能模块
- **Compliance Modules**: 合规和质量模块
