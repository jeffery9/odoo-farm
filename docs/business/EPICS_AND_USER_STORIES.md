# Odoo 农业生态系统：全量史诗与用户故事清单 (Digital Agriculture Vision & Full Backlog)

本文件是整个系统向 **L5 完全数字化自主农场** 进化的全量 Backlog 视图。包含了所有 133 个已被定序的 Epic 及其子 User Stories。

## [EPIC 001: 农业基础主数据 (Agricultural Master Data)](../business/epics/EPIC_001_Agricultural_Master_Data.md)
- **US-001-01**: 多业态活动分类
- **US-001-02**: 农业 UOM (计量单位) 弹性转换
- **US-001-03**: 地块 GIS 数字化
- **US-001-04**: 生物资产全生命周期系谱
- **US-001-05**: 繁育代次追踪 (G0-G3)
- **US-001-06**: 生物资产成龄转固核算
- **US-001-07**: 生物资产估值与折旧模型
- **US-001-08**: “一键初始化”行业主数据包
- **US-001-09**: 土地健康与轮作档案

## [EPIC 002: 种植生产管理 (Plant Farming)](../business/epics/EPIC_002_Plant_Farming.md)
- **US-002-01**: 生产季 Campaign 规划
- **US-002-02**: 农事干预记录 (Interventions)
- **US-002-03**: 土壤养分平衡 (N/P/K)
- **US-002-04**: 收获分级入库
- **US-002-05**: GDD 积温生长预测
- **US-002-06**: 喷洒作业气象窗口校验
- **US-002-07**: 专家级“农事历”技术路线库
- **US-002-09**: 技术路线自动调优 (Act - PDCA)
- **US-002-10**: 生产季绩效闭环评估 (Campaign OPE)
- **US-002-11**: 单产损益分析 (CPA - Cost Per Acre)

## [EPIC 003: 畜牧与水产养殖管理 (Livestock & Aquaculture)](../business/epics/EPIC_003_Livestock_Aquaculture.md)
- **US-003-01**: 饲喂计划与配方
- **US-003-02**: 健康与防疫跟踪
- **US-003-03**: 环境与生理闭环监控
- **US-003-04**: 群组变动管理
- **US-003-05**: 死亡成本自动重分配
- **US-003-06**: 视觉化非接触式生物量测定
- **US-003-07**: 垂直业态 KPI (PSY/料肉比) 引擎

## [EPIC 004: 农业特色供应链与 Recipe (Agri-Supply Chain & Recipe)](../business/epics/EPIC_004_Agri_Supply_Chain_Recipe.md)
- **US-004-01**: 农业动态配方 (Tank Mix)
- **US-004-02**: 批次混合追溯 (Blending Traceability)
- **US-004-03**: 农业副产品 (Co-products) 价值分摊
- **US-004-04**: 农资批次有效期滚动预警
- **US-004-05**: 投入品替代逻辑与配方重算 (Substitutable Inputs)
- **US-004-06**: 季节性"版本化"配方管理

## [EPIC 005: 观光农业与体验经济 (Agritourism & Experience)](../business/epics/EPIC_005_Agritourism_Experience.md)
- **US-005-01**: 采摘园/活动预约
- **US-005-02**: 农产品“采摘即销售”
- **US-005-03**: 资源预约管理
- **US-005-04**: 体验项目打包销售
- **US-005-05**: 农场社区全景游线 (Integrated Farm Community Tour)
- **US-005-06**: 生态廊道“生物寻宝”研学 (Eco-Corridor Biodiversity Discovery)
- **US-005-07**: 智能体驱动的“数字农夫”管家 (A2A Digital Farm Guide)
- **US-005-08**: 社区“物料图书馆”沉浸式体验 (Library Immersive Experience)

## [EPIC 006: IIOT 环境感知与自动化 (IIOT & Automation)](../business/epics/EPIC_006_IIOT_Automation.md)
- **US-006-01**: 实时环境监测
- **US-006-02**: 阈值告警与通知
- **US-006-03**: 设备远程控制
- **US-006-04**: 自主规则引擎 (If-This-Then-That)
- **US-006-05**: 传感器校准与漂移审计
- **US-006-06**: 高风险指令"双人确认"机制 (Four-Eyes Control)
- **US-006-07**: 异常指令"一键熔断"与远程锁定

## [EPIC 007: 移动端友好与现场作业 (Mobile-First Field Ops)](../business/epics/EPIC_007_Mobile_Field_Ops.md)
- **US-007-01**: 扫码识别资产
- **US-007-02**: 离线数据采集
- **US-007-03**: 极简作业界面
- **US-007-04**: PWA 安装与桌面快捷方式
- **US-007-05**: 静态资源离线缓存
- **US-007-06**: Service Worker 后台静默同步
- **US-007-07**: 离线作业指南查阅
- **US-007-08**: 投入品安全说明书 (MSDS) 离线同步
- **US-007-09**: "扫码即作业"智能情境上下文 (Contextual Magic Button)
- **US-007-10**: 离线作业优先级同步策略 (Urgent Sync)
- **US-007-11**: 扫码自动定位并打开活跃工单 (Scan-to-Form)
- **US-007-12**: 基于地理位置的"常用物料"智能预填
- **US-007-13**: 键盘替代型"增量芯片"组件 (Stepper & Chips)
- **US-007-14**: 任务"二元状态"巨型开关 (Binary Toggle)
- **US-007-15**: 窄屏"核心信息置top"模式 (Sticky Key Metrics)
- **US-007-16**: 表单字段"单列纵向"自动排版
- **US-007-17**: PDA 高频连续扫码模式 (Rapid Scan Mode)

## [EPIC 008: 精准营销与客户参与 (Marketing & Engagement)](../business/epics/EPIC_008_Marketing_Engagement.md)
- **US-008-01**: 溯源营销 (Farm to Table)
- **US-008-02**: 订阅制农业 (CSA)
- **US-008-03**: 社区与忠诚度管理
- **US-008-04**: 全球化"多时区/多语言"溯源门户
- **US-008-05**: 国际有机认证一键验真

## [EPIC 009: 全链路集成供应链 (Integrated Supply Chain)](../business/epics/EPIC_009_Integrated_Supply_Chain.md)
- **US-009-01**: 需求驱动生产 (MTO)
- **US-009-02**: 智能供给计划 (MRP)
- **US-009-03**: 产地直供物流
- **US-009-04**: 农忙季节性安全库存计划
- **US-009-05**: 采收周转物追踪
- **US-009-06**: 供应商合规资质硬核查
- **US-009-07**: 动态货架期 (Shelf-life) 预测
- **US-009-08**: 产后预冷 (Pre-cooling) 过程追踪
- **US-009-09**: 冷库多温区与湿度精细化管理
- **US-009-10**: 冷库能效与温控稳定性审计
- **US-009-11**: 质量挂钩的采购分级定价 (Quality-Premium Pricing)
- **US-009-12**: 跨境出口单证自动集成 (Export Document Hub)
- **US-009-13**: 高价值包材/托盘循环追踪 (Circular Asset Tracking)
- **US-009-14**: 农资 VMI (供应商管理库存) 自动化
- **US-009-15**: 合作社联合采购与需求聚合 (Joint Procurement)
- **US-009-16**: 供应链供应风险实时预警 (Risk Radar)
- **US-009-17**: 配送“最后一公里”温控与交付存证 (Safe POD)
- **US-009-18**: 冷链异常触发自动库存降级
- **US-009-19**: 基于质量等级的自动收购定价 (Quality-based Pricing)
- **US-009-20**: 保质期驱动的自动出库建议 (FEFO - First Expired First Out)

## [EPIC 010: 农业循环经济与增值销售平台 (Agricultural Circular Economy & Value-Added Sales Platform)](../business/epics/EPIC_010_Sales_Marketing_Zero_Waste.md)
- **US-010-01**: 动态供需匹配与拍卖平台 (Dynamic Supply-Demand Matching & Auction Platform)
- **US-010-02**: 分级销售与多渠道管理系统 (Graded Sales & Multi-Channel Management)
- **US-010-03**: 近效期产品促销与零浪费激励 (Near-Expiry Promotion & Zero-Waste Incentive)
- **US-010-04**: 残次品循环利用市场 (Substandard Product Circular Market)
- **US-010-05**: 副产品增值转化与新产品开发 (By-product Value-Added Conversion & New Product Development)
- **US-010-06**: 滞销产品再加工与价值提升 (Slow-Moving Product Reprocessing & Value Enhancement)
- **US-010-07**: 预测驱动的精准生产与预售系统 (Forecast-Driven Precision Production & Pre-sales)
- **US-010-08**: 智能体驱动的生物资产沉浸式认养 (Agent-Driven Immersive Bio-Asset Adoption)
- **US-010-09**: 数字化未来产量预售与代币化 (Tokenized Future Harvest Pre-sales)

## [EPIC 011: 农业企业可持续发展与价值创造框架 (Agricultural Business Sustainability & Value Creation Framework)](../business/epics/EPIC_011_Business_Sustainability_Framework.md)
- **US-011-01**: 三重目标指标统一管理 (Triple Bottom Line Metrics Management)
- **US-011-02**: 多级可持续商业模式设计 (Multi-scale Sustainable Business Model Design)
- **US-011-03**: 循环经济价值评估体系 (Circular Economy Value Assessment System)
- **US-011-04**: 可持续供应链管理 (Sustainable Supply Chain Management)
- **US-011-05**: 可持续产品全生命周期管理 (Sustainable Product Lifecycle Management)
- **US-011-06**: 自主智能体社交网络与资源撮合 (Autonomous Agent Social Network & Resource Orchestration)

## [EPIC 012: 智能体自主市场与动态定价 (A2A Autonomous Market & Dynamic Pricing)](../business/epics/EPIC_012_A2A_Market_Dynamic_Pricing.md)
- **US-012-01**: 智能体自主议价逻辑 (Agent-to-Agent Price Negotiation)
- **US-012-02**: 去中心化拍卖撮合引擎 (Decentralized Auction Orchestration)
- **US-012-03**: 风险敏感型动态定价 (Risk-Adjusted Dynamic Pricing)
- **US-012-04**: 智能体博弈策略与信誉惩罚 (Game-Theoretic Strategy & Slashing)

## [EPIC 013: 物理协同与共享基础设施 (Physical Synergy & Shared Infrastructure)](../business/epics/EPIC_013_Physical_Synergy_Infrastructure.md)
- **US-013-01**: 连片地块跨界协同治理 (Contiguous Cross-Boundary Land Management)
- **US-013-02**: 共享产后加工中心 (Shared Post-Harvest Processing Facility)
- **US-013-03**: 物理接驳物流协同 (Physical Logistics Handover)
- **US-013-04**: 共享农机“云池”与物理转运 (Shared Machinery Physical Logistics)
- **US-013-05**: 跨农场物理水利与灌溉网络 (Joint Water & Irrigation Infrastructure)
- **US-013-06**: 区域农业微电网与能源共享 (Regional Agri-Microgrid & Energy Sharing)
- **US-013-07**: 跨场生物安全消杀缓冲区 (Shared Biosafety Buffer Zones)
- **US-013-08**: 区域农机维修与保障中心 (Centralized Agri-Machinery Workshop)
- **US-013-09**: 共有设施资产权属与动态成本分摊 (Joint Ownership & Dynamic Cost Allocation)
- **US-013-10**: 资源稀缺状态下的物理优先级调度 (Emergency Resource Rationing & Priority)
- **US-013-11**: 区域级共享无线网路与传感器中继 (Regional Shared Connectivity Hubs)
- **US-013-12**: 跨场废弃物/养分物理转化中心 (Shared Circular Economy Physical Hub)
- **US-013-13**: 农场社区共享生活与农事服务中心 (Shared Farm Community & Service Center)
- **US-013-14**: 区域级生态廊道与生物多样性景观协同 (Collective Ecological Corridors & Biodiversity)
- **US-013-15**: 社区联合应急救援与消防安防体系 (Joint Emergency Rescue & Safety Community)
- **US-013-16**: 农场社区物理工具与种质“图书馆” (Community Tool & Germplasm Library)

## [EPIC 014: 跨社区价值结算与清算 (Inter-Community Value Clearing & Settlement)](../business/epics/EPIC_014_Inter_Community_Value_Clearing_Settlement.md)
- **US-014-01**: 多维价值评估引擎 (Multi-dimensional Valuation Engine)
- **US-014-02**: A2A 结算协议谈判与智能合约 (A2A Settlement Negotiation)
- **US-014-03**: 物理价值证明审计 (Physical Value-Proof Audit)
- **US-014-04**: 自动化内部分帐与债务抵销 (Internal Netting & Debt Offsetting)
- **US-014-05**: 社区影响红利自动分配 (Community Impact Dividend)
- **US-014-06**: 治理审计与争议仲裁溯源 (Governance & Conflict Resolution)
- **US-014-07**: 碳资产货币化与现金清算 (Carbon Asset Monetization & Cash-out)

## [EPIC 015: 花卉与观赏园艺管理 (Floriculture & Ornamental Horticulture)](../business/epics/EPIC_015_Floriculture_Management.md)
- **US-015-01**: DIF 驱动的开花诱导配方 (DIF-Driven Bloom Recipe)
- **US-015-02**: 动态积温 (GDD) 生理阶段预测
- **US-015-03**: 基于采收状态的瓶插寿命 (Vase-life) 智能预测
- **US-015-04**: IoT 触发的冷链红线拦截与预警
- **US-015-05**: 观赏资产 GIS 单株精准定位 (Single Plant GIS Tracking)

## [EPIC 016: 中药材与药用植物管理 (Medicinal Plants Management)](../business/epics/EPIC_016_Medicinal_Plants_Management.md)
- **US-016-01**: 道地性地理指纹 (Daodi Origin Fingerprint)
- **US-016-02**: 有效成分动态积累追踪 (Active Compound Tracking)
- **US-016-03**: 最佳药效采收窗口预测 (Optimal Harvest Window)
- **US-016-04**: GMP 炮制工艺与质量门控 (GMP Processing & Quality Gate)

## [EPIC 017: 茶叶生产与精制管理 (Tea Industry Management)](../business/epics/EPIC_017_Tea_Industry_Management.md)
- **US-017-01**: 茶季与采摘轮次管理 (Seasonal Flush Tracking)
- **US-017-02**: 茶叶精制工艺 Recipe 建模 (Processing Recipe)
- **US-017-03**: 鲜叶到成品的多级溯源 (Multi-stage Traceability)
- **US-017-04**: 茶叶等级与感官评审存证 (Sensory Evaluation)

## [EPIC 018: 畜牧养殖智能管理 (Livestock Smart Management)](../business/epics/EPIC_018_Livestock_Smart_Management.md)
- **US-018-01**: 个体电子档案与繁殖状态机 (Individual Life-log)
- **US-018-02**: 饲料转化率 (FCR) 与日增重 (ADG) 实时监控
- **US-018-03**: 动态免疫排期与休药期红线 (Vaccination & PHI)
- **US-018-04**: 活体抵押资产动态估值 (Livestock Mortgage Valuation)

## [EPIC 019: 水产养殖智能管理 (Aquaculture Smart Management)](../business/epics/EPIC_019_Aquaculture_Smart_Management.md)
- **US-019-01**: 池塘/网箱数字孪生 (Pond Digital Twin)
- **US-019-02**: 水质联动动态投喂 (Water-Linked Feeding)
- **US-019-03**: 生物量抽样与存活率校准 (Biomass Sampling)
- **US-019-04**: 水质灾害实时防御 (Water Quality Defense)

## [EPIC 020: 育苗与育种管理 (Nursery & Breeding)](../business/epics/EPIC_020_Nursery_Breeding.md)
- **US-020-01**: 育苗工厂管理
- **US-020-02**: 育种性状跟踪
- **US-020-03**: 芽率/活力实验室测试
- **US-020-04**: 嫁接/组培过程损耗追踪
- **US-020-05**: 系谱追踪 (Pedigree Tracking)
- **US-020-06**: 性状分析与报告 (Trait Analysis and Reporting)
- **US-020-07**: 自动化苗圃移植 (Automated Nursery Transplantation)
- **US-020-08**: 性状比较向导 (Trait Comparison Wizard)
- **US-020-09**: 育种项目管理 (Breeding Program Management)

## [EPIC 021: 智能养蜂与蜜源追踪管理 (Apiculture Smart Management)](../business/epics/EPIC_021_Apiculture_Management.md)
- **US-021-01**: 蜂箱数字孪生与蜂王档案 (Hive & Queen Life-log)
- **US-021-02**: 蜜源地图与采集半径分析 (Nectar Source GIS)
- **US-021-03**: 转场迁徙计划与物流闭环 (Migration & Transhumance)
- **US-021-04**: 蜂蜜采收分级与理化存证 (Honey Grading)

## [EPIC 022: 食用菌生产与环境精准控制管理 (Mushroom Smart Management)](../business/epics/EPIC_022_Mushroom_Management.md)
- **US-022-01**: 菌包批次数字孪生 (Mushroom Batch Life-log)
- **US-022-02**: 基质配方与灭菌参数建模 (Substrate Recipe)
- **US-022-03**: 出菇期多潮次产量核销 (Flush Yield Tracking)
- **US-022-04**: 环境因子（CO2/湿/温）主动防御

## [EPIC 023: 精油提取工艺与品质全链路管理 (Essential Oil Management)](../business/epics/EPIC_023_Essential_Oil_Management.md)
- **US-023-01**: 提取工艺 Recipe 建模 (Extraction Protocol)
- **US-023-02**: 提取率 (Extraction Yield) 自动审计
- **US-023-03**: 多对一批次 DNA 链式继承 (Lineage Inheritance)
- **US-023-04**: GC-MS 成分分析与品质门控 (Quality Gate)

## [EPIC 024: 净菜加工与包装全链路管理 (Net Vegetables Management)](../business/epics/EPIC_024_Net_Vegetables_Management.md)
- **US-024-01**: 净菜加工损耗与得率核销 (Yield & Loss Tracking)
- **US-024-02**: 多级嵌套包装与标签打印 (Packaging Hierarchy)
- **US-024-03**: 微生物安全门控与 QCP (Microbial Safety)
- **US-024-04**: 鲜切产品极速货架期预测 (Shelf-life Alert)

## [EPIC 025: HACCP 数字化食品安全管控体系 (HACCP Digital Safety)](../business/epics/EPIC_025_HACCP_Digital_Safety_System.md)
- **US-025-01**: CCP 关键控制点与限值建模 (CCP & Critical Limits)
- **US-025-02**: 违规实时拦截与批次隔离 (Violation Blocking)
- **US-025-03**: 纠偏措施 (Corrective Action) 强制流转
- **US-025-04**: HACCP 验证包一键生成 (Audit Package)

## [EPIC 026: 葡萄园精密管理与风土数字化 (Viticulture Smart Management)](../business/epics/EPIC_026_Viticulture_Management.md)
- **US-026-01**: 风土指纹与地块档案 (Terroir & Plot DNA)
- **US-026-02**: 年度架式修剪与挂果控制 (Pruning & Training)
- **US-026-03**: 糖酸比动态监测与采收窗口预测 (Brix & Ripeness)
- **US-026-04**: 压榨转化率与出汁率核销 (Pressing Efficiency)

## [EPIC 027: 酿造与酒窖工艺管理 (Winery & Enology Management)](../business/epics/EPIC_027_Winery_Enology_Management.md)
- **US-027-01**: 发酵动力学监控 (Fermentation Tracking)
- **US-027-02**: 橡木桶与陈酿资产管理 (Barrel Aging)
- **US-027-03**: 多批次调配与 DNA 聚合 (Blending & Marriage)
- **US-027-04**: 理化分析与酿造门控 (Enological Lab Gate)

## [EPIC 028: 火腿加工与窖藏工艺管理 (Dry-Cured Ham Management)](../business/epics/EPIC_028_Ham_Processing_Management.md)
- **US-028-01**: 鲜腿入库与原料 DNA 继承 (Fresh Leg Intake)
- **US-028-02**: 脱水率与重量动态核销 (Dehydration Tracking)
- **US-028-03**: 窖藏环境门控与温湿度存证 (Cellar Environment)
- **US-028-04**: 年份资产动态估值 (Vintage Asset Valuation)

## [EPIC 029: 水产加工与冷冻链条管理 (Aquatic Product Processing)](../business/epics/EPIC_029_Aquatic_Processing_Management.md)
- **US-029-01**: 捕捞入库与生鲜 DNA 继承 (Fresh Catch Intake)
- **US-029-02**: 加工得率与包冰率核销 (Glazing & Yield Tracking)
- **US-029-03**: 极速冻结中心温度监控 (Flash Freezing Control)
- **US-029-04**: 微生物指标与出口核验 (Microbial Gate)

## [EPIC 030: 商业种子研发与分销合规管理 (Seed Industry Management)](../business/epics/EPIC_030_Seed_Industry_Management.md)
- **US-030-01**: 遗传谱系与亲本指纹 (Parental Lineage)
- **US-030-02**: 种子“四检”品质门控 (Seed Testing Gate)
- **US-030-03**: 种子处理与包衣工艺 (Coating Recipe)
- **US-030-04**: 品种权 (PVP) 分销合规核验

## [EPIC 031: 防疫、植保与生物安全 (Epidemic Prevention & Biosafety)](../business/epics/EPIC_031_Epidemic_Prevention_Biosafety.md)
- **US-031-01**: 防疫/植保排期
- **US-031-02**: 隔离与疫情处理
- **US-031-03**: 农残与药效跟踪
- **US-031-04**: 疫点空间缓冲隔离带自动生成
- **US-031-05**: 生物安全门禁轨迹交叉审计
- **US-031-06**: 多点位生物安全屏障审计 (Biosafety Audit)
- **US-031-07**: 农药/兽药负面清单动态拦截 (Smart Restriction)
- **US-031-08**: 风险区域动态等级调整 (Act - PDCA)
- **US-031-09**: 跨农场众包疫情预警与证据分析 (Cross-Farm Crowdsourced Alerting)
- **US-031-10**: 区域生物安全屏障物理共享 (Regional Biosafety Barriers)
- **US-031-11**: 农药/兽药负面清单的社区级共识 (Collective Negative List)

## [EPIC 032: 传统发酵与酿造工艺管理 (Traditional Fermentation Management)](../business/epics/EPIC_032_Traditional_Fermentation_Management.md)
- **US-032-01**: 窖池/容器数字孪生与生态档案 (Pit DNA)
- **US-032-02**: 制曲与发酵动力学监控 (Starter & Fermentation)
- **US-032-03**: 勾调（调配）与品质指纹聚合 (Blending & Marriage)
- **US-032-04**: 年份资产动态增值模型 (Vintage Liquidation)

## [EPIC 033: 稻渔/稻虾共生生态管理 (Rice-Fish/Shrimp Symbiosis)](../business/epics/EPIC_033_Rice_Fish_Symbiosis_Management.md)
- **US-033-01**: 共生空间档案与水位建模 (Symbiotic Plot DNA)
- **US-033-02**: 稻渔复合配方与养分转换 (Symbiotic Nutrient)
- **US-033-03**: 植保施药的安全红线拦截 (Pesticide Safety Gate)
- **US-033-04**: 一地双收的复合产量核销 (Co-harvest Tracking)

## [EPIC 034: 工厂化循环水养殖（RAS）精密管控 (RAS Factory Fisheries)](../business/epics/EPIC_034_RAS_Factory_Fisheries.md)
- **US-034-01**: 维生系统 (LSS) 数字孪生与组件生命周期
- **US-034-02**: 代谢物负荷（氨氮/硝酸盐）精准门控
- **US-034-03**: 极致能效比 (PUE) 与电耗核销
- **US-034-04**: 水循环故障自动闭环防御

## [EPIC 035: 认证、绿色食品与有机农业 (Certification & Organic Farming)](../business/epics/EPIC_035_Certification_Organic_Farming.md)
- **US-035-01**: 投入品黑白名单
- **US-035-02**: 转换期管理
- **US-035-03**: 认证证书与合规审计
- **US-035-04**: 环保与可持续指标
- **US-035-05**: GlobalG.A.P. 合规自评与差距分析
- **US-035-06**: 跨国有机标准并行校验
- **US-035-07**: 土壤有机质与肥力修复动态台账
- **US-035-08**: 有机种源合规与非转基因校验
- **US-035-09**: 平行生产（Parallel Production）物理隔离审计

## [EPIC 036: 劳动力管理与调度 (HR & Labor Scheduling)](../business/epics/EPIC_036_HR_Labor_Scheduling.md)
- **US-036-01**: 农业技能与角色管理
- **US-036-02**: 动态派工与计划
- **US-036-03**: 现场工时记录 (Timesheet)
- **US-036-04**: 劳动力成本自动分摊
- **US-036-05**: 采收计件与绩效联动

## [EPIC 037: 农产品加工管理 (Agri-Processing Management)](../business/epics/EPIC_037_Agri_Processing_Management.md)
- **US-037-01**: 初加工一入多出模型
- **US-037-02**: 深加工多级配方 Recipe
- **US-037-03**: 全链路批次溯源 (Positive & Reverse)
- **US-037-04**: 加工成本与能耗核算
- **US-037-05**: 加工损耗容差管理
- **US-037-08**: 智能化“净菜/预制菜”分拣过程追踪
- **US-037-09**: 关键工艺配方的版本与保密控制
- **US-037-10**: 自动化包装流水线与条码序列化
- **US-037-11**: 基于原料属性的“配方自动修正”
- **US-037-12**: 连续化生产线效率与工序审计
- **US-037-13**: 原子级“物料平衡”守恒校验
- **US-037-14**: 多组分“拆解与联产”逻辑
- **US-037-15**: 属性传递与“增量标签”系统
- **US-037-17**: 有效成分标准化与“效价”自动折算
- **US-037-18**: 过敏原隔离与设备“清场”审计
- **US-037-19**: GMP 环境监控与生产批记录绑定
- **US-037-20**: 食品加工行业 ISL 模型
- **US-037-21**: 生产许可证 (SC) 范围核查与预警
- **US-037-23**: 配方损耗动态修正 (Act - PDCA)
- **US-037-24**: 制药行业模型实现
- **US-037-25**: 化工行业 ISL 模型
- **US-037-26**: 法律强制"双向追溯"测试与召回模拟

## [EPIC 038: 农业质量控制与检测 (Agri-Quality & Inspection)](../business/epics/EPIC_038_Agri_Quality_Inspection.md)
- **US-038-01**: 质量检查点定义 (Inspection Points)
- **US-038-02**: 农事记录与检测关联
- **US-038-03**: 样品管理与留样记录
- **US-038-04**: 质量预警与不合格处理
- **US-038-05**: 批次入库默认锁定与释放机制
- **US-038-06**: 跨社区双盲检测与匿名化 (Cross-Community Blind Audit)
- **US-038-07**: 现场快速检测 (Quick-Test) 结果直录
- **US-038-08**: 数字化感官评价 (Sensory Profile)
- **US-038-09**: 数字化品质指纹与区块链存证 (Digital Quality Fingerprint)
- **US-038-10**: 加工环节关键控制点 (CCP) 硬拦截
- **US-038-11**: 实验室 LIMS 集成 (Lab Management)
- **US-038-12**: 质检结果的置信度审计 (Inspection Confidence Audit)

## [EPIC 039: 用户体验与术语去工业化 (Agri-UX & De-industrialization)](../business/epics/EPIC_039_Agri_UX_Standard.md)
- **US-039-01**: 术语农业化深度映射 (Deep Term Mapping)
- **US-039-02**: 行业化表单布局
- **US-039-03**: 视觉化状态标识
- **US-039-04**: 个性化工作空间定制
- **US-039-05**: 智能上下文帮助
- **US-039-07**: 多感官交互体验
- **US-039-09**: 无障碍设计与包容性
- **US-039-11**: 农业 Chatter 增强分组
- **US-039-12**: 行业上下文快捷切换
- **US-039-13**: 农业企业级首页 (Dashboard)
- **US-039-14**: 农业专用图标系统
- **US-039-15**: 农事任务“一键批量完工” (Batch Closure)
- **US-039-16**: 极简“状态滑块”交互 (Gesture Switch)
- **US-039-17**: “红绿灯”式巨型极简确认控件 (Traffic-Light Controls)
- **US-039-18**: 户外“强光模式”一键切换 (High-Visibility Mode)
- **US-039-19**: 字段控件“点选化”适配 (Selection-First UI)
- **US-039-20**: 快捷备注“标签组合” (Tag-based Notes)
- **US-039-21**: 拇指驱动的“底部动作条” (Thumb-Friendly Bar)
- **US-039-22**: 窄屏“卡片式”信息降维 (Mobile Card Simplification)
- **US-039-24**: PDA 工业级硬件交互集成 (PDA Hardware Mapping)
- **US-039-25**: 去工业化表单动态拦截器 (View Interceptor)

## [EPIC 040: 行业深度与合规 (Advanced Industry & Compliance)](../business/epics/EPIC_040_Advanced_Industry_Compliance.md)
- **US-040-01**: 农机与设备资产管理
- **US-040-02**: 政策与补贴管理
- **US-040-03**: 应急预案与危机管理
- **US-040-04**: 农业金融与信贷
- **US-040-05**: 生物多样性与生态指标
- **US-040-06**: 跨境合规与出口
- **US-040-07**: 农业知识库
- **US-040-08**: 农民培训与技能认证
- **US-040-09**: 多农场/合作社协同
- **US-040-10**: 气象灾害预警集成
- **US-040-11**: 生物资产公允价值实时核算
- **US-040-12**: 农药/化肥国家登记证数据库集成 (Registry Lookup)
- **US-040-13**: 行业病虫害图谱与药剂匹配库 (Pest & Disease Encyclopedia)

## [EPIC 041: 中国合规与政策适配 (China Compliance & Policy Adaptation)](../business/epics/EPIC_041_China_Compliance_Policy_Adaptation.md)
- **US-041-01**: 土地承包与用途管制 (Land Contract & Usage Control)
- **US-041-02**: 农药兽药监管对接 (Pesticide/Veterinary Drug Regulatory Integration)
- **US-041-03**: 食用农产品合格证管理 (Edible Agricultural Product Certificate Management)
- **US-041-04**: 农业补贴申报与管理 (Agricultural Subsidy Application & Management)
- **US-041-05**: 畜禽粪污资源化管理 (Livestock Waste Resource Management)
- **US-041-06**: 化肥农药减量管理 (Fertilizer & Pesticide Reduction Management)

## [EPIC 042: 多实体协同与合作社管理 (Multi-Entity Collaboration & Cooperative)](../business/epics/EPIC_042_Multi_Entity_Collaboration.md)
- **US-042-01**: 多农场实体关系建模
- **US-042-02**: 租户级数据隔离与共享
- **US-042-03**: 跨农场资源调度与协同
- **US-042-04**: 合作社级财务汇总与分摊
- **US-042-05**: 加盟农场标准化管理
- **US-042-22**: 内部交易“零余额”对冲结算 (Netting Settlement)
- **US-042-23**: 成员农场 OPE 对标排行榜 (Member Benchmarking)
- **US-042-06**: 成员股份与惠农分红管理 (Shares & Dividends)
- **US-042-07**: 内部“农资信用额度”管理 (Internal Credit)
- **US-042-08**: 共享农机池与动态结算 (Shared Machinery Pool)
- **US-042-09**: 合作社统一质检与品牌准入 (Collective QC)
- **US-042-24**: “公司+农户”合同种植管理
- **US-042-25**: 合作社双重目的管理 (Commercial & Government Purposes)
- **US-042-26**: 成员多社身份灵活性 (Individual Multi-Membership)
- **US-042-27**: 产品/批次单社归属唯一性 (Product-Cooperative Exclusivity)

## [EPIC 043: 农业精准制造桥接核心 (Agri-Precision Bridge Core)](../business/epics/EPIC_043_Agri_Precision_Core_Architecture.md)
- **US-AGRI-01**: 不确定性处理 (Uncertainty Handling)
- **US-AGRI-02**: 产品分级 (Product Grading)
- **US-AGRI-03**: 干预机制 (Intervention Mechanism)
- **US-AGRI-04**: IoT 集成桥接 (IoT Integration Bridge)
- **US-AGRI-05**: 跨模块集成 (Cross-Module Integration)

## [EPIC 044: 精密生产执行基座 (Precision Production Foundation)](../business/epics/EPIC_044_Precision_Production_Foundation.md)
- **US-044-01**: 驱动模式与架构解耦 (Drive Mode)
- **US-044-02**: ISA-88 配方实例化 (Recipe Instantiation)
- **US-044-03**: 相位自治与并行执行 (Phase Autonomy & Parallelism)
- **US-044-04**: 过程控制 (SPC) 与执行锁闭 (Process Hold)
- **US-044-05**: 自适应主动纠偏 (Active Adaptation)
- **US-044-06**: 绩效量化 (Performance Management)
- **US-044-07**: 财务级产出核销 (Native By-product Grading)
- **US-044-08**: 工业物联网 (IIoT) 集成与自动数据采集 (Industrial IoT Integration & Auto Data Capture)
- **US-044-09**: 农业精准制造桥接 (Agri-Precision Bridge)

## [EPIC 045: 农学科学底座 (Agri-Science Foundation)](../business/epics/EPIC_045_Agri_Science_Base.md)
- **US-045-01**: 品种生理指纹与基准 (Physiology Fingerprint)
- **US-045-02**: 生理阶段与积温驱动 (Physiological Stages & GDD)
- **US-045-03**: 环境阈值矩阵与 SPC 联动 (Environmental Matrix)
- **US-045-04**: 养分吸收动态模型 (Nutrient Uptake Curves)
- **US-045-05**: 科学向导
- **US-045-06**: 视觉物候标定与反馈 (Vision-Phenology Sync)
- **US-045-07**: 生物压力累积评估 (Biological Stress Analysis)
- **US-045-08**: 生物资源转化效率 (Biological Conversion Efficiency)
- **US-045-09**: 科学性能看板 (Scientific Performance Dashboard)

## [EPIC 046: AI 智能决策支持 (AI Decision Support)](../business/epics/EPIC_046_AI_Decision_Support.md)
- **US-046-01**: 压力驱动的主动补救决策 (Stress-Driven Recovery)
- **US-046-02**: 采收期动态预测与预售联动 (Dynamic Harvest Window)
- **US-046-03**: 决策存证与“人机博弈”闭环 (Decision Audit)

## [EPIC 047: IoT 边缘协调与主动控制 (Edge Orchestration & Active Control)](../business/epics/EPIC_047_Edge_Orchestration_Active_Control.md)
- **US-047-01**: 执行器端点定义 (Actuator Endpoints)
- **US-047-02**: 双向设定点绑定 (Bi-directional Setpoint Binding)
- **US-047-03**: 边缘自律与指令存证 (Edge Autonomy & Audit)

## [EPIC 048: 农业主动干预 UX (Agri-UX for Active Intervention)](../business/epics/EPIC_048_Agri_UX_Active_Intervention.md)
- **US-048-01**: AI 决策动态浮窗 (AI Decision Pop-over)
- **US-048-02**: “一键执行”原子交互 (One-Tap Execution)
- **US-048-03**: 决策反馈与博弈 (Decision Feedback Loop)

## [EPIC 049: Blockchain-based Biological Asset Evidence](../business/epics/EPIC_049_Blockchain_Biological_Asset_Evidence.md)
- **US-049-01**: 生物量价值建模 (Biological Value Modeling)
- **US-049-02**: 关键行为哈希存证 (Evidence Hashing)
- **US-049-03**: 异步存证分发 (Blockchain Notarization)
- **US-049-04**: 生物资产电子证书 (Growth Certificate)

## [EPIC 050: 智能灌溉管理 (Intelligent Irrigation Management)](../business/epics/EPIC_050_Intelligent_Irrigation_Management.md)
- **US-050-01**: 土壤湿度监测与分析 (Soil Moisture Monitoring & Analysis)
- **US-050-02**: 智能灌溉决策 (AI-driven Irrigation Decision)
- **US-050-03**: 灌溉设备智能控制 (Irrigation Equipment Smart Control)
- **US-050-04**: 水资源优化与节水分析 (Water Resource Optimization & Conservation Analysis)

## [EPIC 051: 直播与抖音对接 (Live Streaming & Douyin Integration)](../business/epics/EPIC_051_Live_Streaming_Douyin.md)
- **US-051-01**: 抖音账号授权与绑定
- **US-051-02**: 商品库同步与管理
- **US-051-03**: 直播间商品关联
- **US-051-04**: 订单自动回传与处理
- **US-051-05**: 直播数据统计与分析
- **US-051-06**: 直播预告与推广
- **US-051-07**: 直播内容存档与复用
- **US-051-08**: 网络达人签约与 MCN 合同管理
- **US-051-09**: 达人带货业绩自动归集 (Attribution)
- **US-051-10**: 达人佣金自动结算与对账
- **US-051-11**: 营销样品 (Seed/Sample) 管理

## [EPIC 052: 农用无人机作业集成 (Agricultural Drone Operations)](../business/epics/EPIC_052_Drone_Operations.md)
- **US-052-01**: 无人机机队管理
- **US-052-02**: 飞手资质自动校验
- **US-052-03**: 航线规划集成 (GCS Link)
- **US-052-04**: 自动喷洒作业核销
- **US-052-05**: 飞防成本动态核算
- **US-052-06**: 实时作业遥测监控
- **US-052-07**: 飞防质量历史回溯

## [EPIC 053: 地理围栏与资产边界安全 (Geofencing & Boundary Security)](../business/epics/EPIC_053_Geofencing_Security.md)
- **US-053-01**: 虚拟围栏规划 (Virtual Fence Design)
- **US-053-02**: 畜禽越界实时告警
- **US-053-03**: 无人机飞行围栏同步
- **US-053-04**: 农机作业范围审计
- **US-053-05**: 自动防疫隔离带拦截
- **US-053-06**: 地理围栏告警策略
- **US-053-07**: 围栏效力历史报告

## [EPIC 054: 移动端现场打卡与工时校验 (Mobile Site Check-in)](../business/epics/EPIC_054_Mobile_Site_Checkin.md)
- **US-054-01**: 现场地理打卡 (Site Check-in)
- **US-054-02**: 自动地块匹配校验
- **US-054-03**: 自动工时记录同步
- **US-054-04**: 现场拍照存证
- **US-054-05**: 离线打卡支持
- **US-054-06**: 强制人脸/活体核身 (Core-Closure)
- **US-054-07**: 蓝牙/NFC 自动近场打卡

## [EPIC 055: 通用现场证据存证系统 (Generic Field Evidence)](../business/epics/EPIC_055_Generic_Field_Evidence.md)
- **US-055-01**: 万物皆可取证
- **US-055-02**: 自动化地理水印
- **US-055-03**: 空间证据合规审计
- **US-055-04**: 证据看板展示
- **US-055-05**: 证据链哈希校验 (Core-Closure)

## [EPIC 056: 现场作业服务 (Field Operations Services)](../business/epics/EPIC_056_Field_Operations_Services.md)
- **US-056-01**: 农业语音输入服务 (Agricultural Voice Input Service)
- **US-056-02**: 离线卫星地图服务 (Offline Satellite Map Service)
- **US-056-03**: 远程专家连线服务 (Remote Expert Connection Service)
- **US-056-04**: GIS地图化任务派发 (GIS-based Task Dispatch)
- **US-056-05**: 远程专家实时连线 (Remote Expert Real-time Connection)
- **US-056-06**: 增强现实 (AR) 虚拟地头桩 (AR Virtual Field Stake)
- **US-056-07**: “抢单式”任务即时响应模式 (Agri-Task Grab)
- **US-056-08**: 语音宏指令 (Voice Agri-Macros)

## [EPIC 057: 农业循环经济与废弃物资源化 (Circular Economy)](../business/epics/EPIC_057_Circular_Economy.md)
- **US-057-01**: 粪污/秸秆资源化登记 (Waste Resource Registration)
- **US-057-02**: 内部转化投入品换算 (Internal Conversion Valuation)
- **US-057-03**: 危险废弃物（药瓶/地膜）合规处置
- **US-057-04**: 沼气/生物质能转化量化
- **US-057-05**: 合作社/产业园资源跨场协同 (Cooperative/Industrial Park Cycle)
- **US-057-06**: 基于地理空间的空间循环网络 (GIS-driven Geospatial Cycle)
- **US-057-07**: 行政区域级循环治理 (Regional/Administrative Cycle)

## [EPIC 058: AI 预测性洞察与智能视觉 (AI & Vision)](../business/epics/EPIC_058_AI_Vision.md)
- **US-058-01**: 计算机视觉病害诊断
- **US-058-02**: 动态产量预测模型
- **US-058-03**: 边缘端 (Edge AI) 离线病害识别
- **US-058-04**: 产量对标与生产偏差分析 (Benchmark)

## [EPIC 059: 农业金融风险与保险联动 (Agri-Risk & Insurance)](../business/epics/EPIC_059_Agri_Risk_Insurance.md)
- **US-059-01**: 期货价格监控预警
- **US-059-02**: 气象指数保险定损自动存证

## [EPIC 060: 碳足迹追踪与可持续性账座 (Carbon & ESG Ledger)](../business/epics/EPIC_060_Carbon_ESG_Ledger.md)
- **US-060-01**: 作业过程碳排自动核算
- **US-060-02**: 固碳增汇资产管理
- **US-060-03**: 投入品隐含碳 (Scope 3) 自动抓取
- **US-060-04**: ESG 合规报告一键披露
- **US-060-05**: 反刍动物甲烷排放量化追踪
- **US-060-06**: 生物多样性信贷 (Biodiversity Credits)
- **US-060-07**: 欧盟碳边境调节机制 (CBAM) 导出适配
- **US-060-08**: 碳信用签发前“数字 MRV”透明化证明
- **US-060-10**: 环境影响评估
- **US-060-11**: 生物多样性保护跟踪
- **US-060-14**: 行业特定 ESG 数据模型 ISL 扩展

## [EPIC 061: 逆向供应链与精准召回 (Reverse Supply Chain)](../business/epics/EPIC_061_Reverse_Recall.md)
- **US-061-01**: 质量危机一键阻断 (Kill Switch)
- **US-061-02**: 消费者逆向追溯审计
- **US-061-03**: 下游受影响客户自动化预警推送

## [EPIC 062: 品牌价值、地理标志与有机诚信体系 (Brand, GI & Organic)](../business/epics/EPIC_062_Brand_Organic_Integrity.md)
- **US-062-01**: 产地风土数字化 (Terroir Profiling)
- **US-062-02**: 地理标志 (GI) 防伪集成
- **US-062-03**: 品牌渠道保护白名单
- **US-062-04**: 有机诚信实时评分 (Integrity Scoring)
- **US-062-05**: 品牌+风土动态展示页
- **US-062-06**: 外部审计员“远程透明化”查验门户
- **US-062-07**: 生态缓冲区多样性监控与展示

## [EPIC 063: 设施农业、温室与植物工厂 (CEA & Vertical Farming)](../business/epics/EPIC_063_CEA_Vertical_Farming.md)
- **US-063-01**: 水肥一体化/光照自动控制
- **US-063-02**: "位点级"空间库存管理

## [EPIC 064: 多年生作物、林果与茶园管理 (Perennial & Orchard)](../business/epics/EPIC_064_Perennial_Orchard.md)
- **US-064-01**: 果树/植株个体生命周期档案
- **US-064-02**: 采收指标动态监控 (含糖/酸度)
- **US-064-03**: 植株更新与补植计划
- **US-064-04**: 多年生作物负载量管理 (Thinning)

## [EPIC 065: 特种养殖与高密度工业化养殖 (Intensive Livestock)](../business/epics/EPIC_065_Intensive_Livestock.md)
- **US-065-01**: 生物安全电子通行证
- **US-065-02**: 饲养密度预警与环控联动
- **US-065-03**: FCR 实时动态转化透视
- **US-065-04**: 动物福利合规监控

## [EPIC 066: 城市农业、共享认养与微农场 (Urban & Community Farming)](../business/epics/EPIC_066_Urban_Community_Farming.md)
- **US-066-01**: “一平米菜地”认养全流程
- **US-066-02**: 共享农机/工具租借管理
- **US-066-03**: 城市微型传感器接入

## [EPIC 067: 农业综合生产效能 (OPE) 与决策智能 (Agri-OPE Intelligence)](../business/epics/EPIC_067_Agri_OPE_Intelligence.md)
- **US-067-01**: OPE (Overall Production Effectiveness) 计算引擎
- **US-067-02**: 面积加权滚动聚合算法 (Weighted Rollup)
- **US-067-04**: 品种/技术路径对标分析 (Benchmark)
- **US-067-05**: 水肥利用效率深度透视 (WUE/NUE)
- **US-067-03**: 实时 OPE 审计仪表盘

## [EPIC 068: 牲畜健康监测与智能管理 (Livestock Health Monitoring & Smart Management)](../business/epics/EPIC_068_Livestock_Health_Monitoring.md)
- **US-068-01**: 牲畜健康指标监测 (Livestock Health Indicator Monitoring)
- **US-068-02**: 智能喂养管理 (Smart Feeding Management)
- **US-068-03**: 疾病预防与治疗管理 (Disease Prevention & Treatment Management)
- **US-068-04**: 繁殖育种智能管理 (Breeding & Reproduction Smart Management)

## [EPIC 069: 农业气象站与环境监测 (Agricultural Weather Station & Environmental Monitoring)](../business/epics/EPIC_069_Agricultural_Weather_Station.md)
- **US-069-01**: 多参数环境数据采集 (Multi-parameter Environmental Data Collection)
- **US-069-02**: 本地化天气预报 (Localized Weather Forecasting)
- **US-069-03**: 环境异常预警 (Environmental Anomaly Alert)
- **US-069-04**: 历史数据分析与趋势预测 (Historical Data Analysis & Trend Prediction)
- **US-069-05**: 跨农场气象数据共享与共识校验 (Cross-Farm Weather Consensus)
- **US-069-06**: 区域级灾害天气物理联动响应 (Joint Disaster Response)
- **US-069-07**: 微气候资产所有权与维护分摊 (Weather Asset Ownership)

## [EPIC 070: 精准施肥系统 (Precision Fertilization System)](../business/epics/EPIC_070_Precision_Fertilization_System.md)
- **US-070-01**: 土壤养分检测与分析 (Soil Nutrient Detection & Analysis)
- **US-070-02**: 作物营养需求建模 (Crop Nutritional Demand Modeling)
- **US-070-03**: 变量施肥处方生成 (Variable Rate Fertilization Prescription)
- **US-070-04**: 施肥效果评估与优化 (Fertilization Effect Assessment & Optimization)

## [EPIC 071: 无人机作物监测与管理 (Drone-based Crop Monitoring & Management)](../business/epics/EPIC_071_Drone_Based_Crop_Monitoring.md)
- **US-071-01**: 作物生长状况监测 (Crop Growth Status Monitoring)
- **US-071-02**: 病虫害智能识别 (AI-driven Pest & Disease Recognition)
- **US-071-03**: 无人机农事作业 (Drone-based Agricultural Operations)
- **US-071-04**: 无人机数据整合与分析 (Drone Data Integration & Analysis)

## [EPIC 072: 智能温室控制 (Smart Greenhouse Control)](../business/epics/EPIC_072_Smart_Greenhouse_Control.md)
- **US-072-01**: 温室环境参数监测 (Greenhouse Environmental Parameter Monitoring)
- **US-072-02**: 智能环境控制算法 (AI-driven Environmental Control Algorithm)
- **US-072-03**: 作物生长阶段自适应控制 (Crop Growth Stage Adaptive Control)
- **US-072-04**: 远程监控与移动管理 (Remote Monitoring & Mobile Management)

## [EPIC 073: 杂草识别与智能控制 (Weed Identification & Smart Control)](../business/epics/EPIC_073_Weed_Identification_Control.md)
- **US-073-01**: 杂草种类智能识别 (AI-driven Weed Species Recognition)
- **US-073-02**: 精准除草作业 (Precision Weeding Operations)
- **US-073-03**: 除草剂使用优化 (Herbicide Usage Optimization)
- **US-073-04**: 杂草抗性监测与管理 (Herbicide Resistance Monitoring & Management)

## [EPIC 074: 产后品质管理与保鲜 (Post-harvest Quality Management & Preservation)](../business/epics/EPIC_074_Post_Harvest_Quality_Management.md)
- **US-074-01**: 产后品质实时监测 (Post-harvest Quality Real-time Monitoring)
- **US-074-02**: 智能保鲜环境控制 (Smart Preservation Environment Control)
- **US-074-03**: 保质期预测与库存优化 (Shelf-life Prediction & Inventory Optimization)
- **US-074-04**: 成品分级与包装优化 (Product Grading & Packaging Optimization)

## [EPIC 075: 农业知识管理与智能决策支持 (Agricultural Knowledge Management & Intelligent Decision Support)](../business/epics/EPIC_075_Agricultural_Knowledge_Management.md)
- **US-075-01**: 农业知识库构建 (Agricultural Knowledge Base Construction)
- **US-075-02**: 智能农事建议系统 (AI-driven Farming Recommendation System)
- **US-075-03**: 农业问答系统 (Agricultural Q&A System)
- **US-075-04**: 决策支持与风险评估 (Decision Support & Risk Assessment)

## [EPIC 076: 精准生产与变量作业 (Precision Production & VRA)](../business/epics/EPIC_076_Precision_Production_VRA.md)
- **US-076-01**: PostGIS 空间网格化引擎 (Spatial Grid Engine)
- **US-076-02**: 卫星 NDVI 栅格自动映射 (Remote Sensing Mapping)
- **US-076-03**: 变量处方图算法引擎 (VRA Prescription Engine)
- **US-076-04**: 农机指令导出 (ISO-XML & Shapefile Export)
- **US-076-05**: 实喷图回传与库存对账闭环 (As-Applied Closure)

## [EPIC 077: 生物生长智能与动态决策 (Biological Growth Intelligence)](../business/epics/EPIC_077_Biological_Growth_Intelligence.md)
- **US-077-01**: 数字化品种模型 (Digital Varietal Twin)
- **US-077-02**: 动态物候期预测与预警 (Phenology Intelligence)
- **US-077-03**: 智能水肥精准建议引擎 (Agro-Science Recommendation)
- **US-077-04**: 产量风险建模与动态概率预测 (Yield Risk Modeling)

## [EPIC 078: 农业金融信用与指数保险 (Agri-Financial Credit & Insurance)](../business/epics/EPIC_078_Agri_Financial_Credit_Insurance.md)
- **US-078-01**: 作业真实性校验算法 (Task Evidence Scoring)
- **US-078-02**: 农场生产信用评分卡 (Farm Credit Score)
- **US-078-03**: 气象指数保险自动化理赔 (Index-based Insurance)
- **US-078-04**: 协作下的金融结算中心 (Co-op Financial Hub)

## [EPIC 079: 全息溯源与交互式品牌营销 (Holistic Traceability & Marketing)](../business/epics/EPIC_079_Holistic_Traceability_Marketing.md)
- **US-079-01**: 全息交互式溯源 PWA (Interactive Traceability UI)
- **US-079-02**: 品牌风土 (Terroir) 时空档案集成
- **US-079-03**: 关键作业节点的"真实影像"挂载
- **US-079-04**: 科学种植减碳证书 (Low-carbon Certificate)

## [EPIC 080: 层级视图容器与多维管理视角 (Hierarchy View Containers)](../business/epics/EPIC_080_Hierarchy_View_Containers.md)
- **US-080-01**: 逻辑管理容器 (Logical View Containers)
- **US-080-02**: 树状层级嵌套 (Recursive Nesting)
- **US-080-03**: 跨模型 OPE 聚合引擎 (Cross-model Aggregation)
- **US-080-04**: 容器级权限控制 (Container-based Permissions)
- **US-080-05**: 跨视角性能对标分析 (Perspective Benchmarking)
- **US-080-06**: 跨公司管理视角 (Cross-company Perspectives)

## [EPIC 081: 计算机视觉分析 (Computer Vision Analysis)](../business/epics/EPIC_081_Computer_Vision_Analysis.md)
- **US-081-01**: 病虫害图像识别与诊断
- **US-081-02**: 视觉智能分拣与品质评估
- **US-081-03**: 作物生长监测与产量预测

## [EPIC 082: 高级溯源系统 (Advanced Traceability System)](../business/epics/EPIC_082_Advanced_Traceability_System.md)
- **US-082-01**: 批次溯源与链式追踪
- **US-082-02**: 全球追溯标准合规
- **US-082-03**: 批次混合与比例追溯

## [EPIC 083: 数字化农业平台 (Digital Agriculture Platform)](../business/epics/EPIC_083_Digital_Agriculture_Platform.md)
- **US-083-01**: AI 决策引擎核心
- **US-083-02**: 农业知识库与模型管理
- **US-083-03**: 智能推荐与预测分析

## [EPIC 084: ISL 行业标准层架构 (Industry Standard Layer - ISL)](../business/epics/EPIC_084_ISL_Architecture.md)
- **US-084-01**: MRP 生产订单 ISL 模型实现
- **US-084-02**: MRP Recipe ISL 模型实现
- **US-084-03**: MRP 工作中心 ISL 模型实现
- **US-084-04**: 库存批次 ISL 模型实现
- **US-084-05**: 销售订单 ISL 模型实现
- **US-084-06**: 采购订单 ISL 模型实现
- **US-084-07**: 产品模板 ISL 模型实现
- **US-084-08**: 库存调拨 ISL 模型实现
- **US-084-09**: MRP 工单 ISL 模型实现
- **US-084-10**: 质量控制点 ISL 模型实现
- **US-084-11**: ISL 模型重定向机制
- **US-084-12**: 行业特定扩展机制
- **US-084-13**: 性能优化与缓存
- **US-084-14**: 数据迁移与兼容性

## [EPIC 085: 农业网络安全与数据保护 (Agricultural Cybersecurity & Data Protection)](../business/epics/EPIC_085_Agricultural_Cybersecurity.md)
- **US-085-01**: 农场网络安全架构
- **US-085-02**: 农业数据隐私与合规保护
- **US-085-03**: IoT 设备安全管理
- **US-085-04**: 智能施肥决策
- **US-085-09**: 设备故障预测与维护

## [EPIC 086: ESG 合规与可持续发展管理 (ESG Compliance & Sustainability)](../business/epics/EPIC_086_ESG_COMPLIANCE_MANAGEMENT.md)
- **US-086-01**: 农业补贴追踪管理
- **US-086-02**: 生物多样性指标监测
- **US-086-03**: 出口合规检查
- **US-086-04**: 可持续农业实践认证
- **US-086-05**: ESG 数据治理与质量控制
- **US-086-06**: 利益相关者 ESG 报告定制化
- **US-086-07**: 可持续发展目标追踪与管理
- **US-086-08**: 供应链可持续性评估
- **US-086-09**: 可持续发展情景分析与预测
- **US-086-11**: ESG 合规报告一键生成
- **US-086-12**: 碳足迹综合报告
- **US-086-13**: 生物多样性保护综合报告
- **US-086-14**: 行业特定 ESG 报告模板
- **US-086-21**: ESG 风险评级与披露报告
- **US-086-22**: ESG 合规数据综合披露

## [EPIC 087: 综合农业物联网平台 (Integrated Agricultural IoT Platform)](../business/epics/EPIC_087_Integrated_Agricultural_IoT_Platform.md)
- **US-087-01**: 多源传感器网络管理 (Multi-source Sensor Network Management)
- **US-087-02**: 智能设备控制与调度 (Smart Device Control & Scheduling)
- **US-087-03**: 实时数据分析与预警 (Real-time Data Analysis & Alert)
- **US-087-04**: 农业物联网安全防护 (Agricultural IoT Security Protection)

## [EPIC 088: AI 智能决策支持平台 (AI Decision Support Platform)](../business/epics/EPIC_088_AI_Decision_Support_Platform.md)
- **US-088-01**: AI 代理类型与执行方式
- **US-088-02**: AI 协调层与跨模块集成
- **US-088-03**: AI 决策引擎与智能工作流
- **US-088-04**: 智能作物推荐系统
- **US-088-05**: 病虫害治理策略决策
- **US-088-06**: 养分自动校准决策 (Autonomous Nutrient Correction Decision)
- **US-088-07**: 智能灌溉调度建议
- **US-088-08**: 知识库向量索引同步 (Knowledge Embedding Sync)
- **US-088-09**: 智能采收时机与品质预测 (Smart Harvest Timing & Quality Prediction)
- **US-088-10**: 气象灾害风险评估
- **US-088-11**: 市场行情趋势预测
- **US-088-12**: 劳动力需求智能分析
- **US-088-13**: 土壤退化与健康评估
- **US-088-14**: 农机能耗优化路径规划
- **US-088-15**: 活体资产抵押贷款管理
- **US-088-16**: 作业产量保险精算与赔付
- **US-088-17**: 农碳信用交易与金融化
- **US-088-18**: 农业期货与套期保值管理

## [EPIC 089: AI 大语言模型集成与 RAG 增强 (AI LLM Integration & RAG)](../business/epics/EPIC_089_AI_LLM_Integration.md)
- **US-089-01**: LLM 服务配置与管理
- **US-089-02**: 农业知识问答系统
- **US-089-03**: 智能服务调用与结果处理
- **US-089-07**: ISL 架构依赖说明
- **US-089-08**: 自动化向量化任务 engines (Automated Embedding Job)
- **US-089-09**: 语义上下文检索与注入 (Semantic Context Retrieval)
- **US-089-10**: 业务数据语义网格化 (Business Data Semantic Grid)

## [EPIC 090: AI 金融分析与风险评估 (AI Financial Analytics & Risk Management)](../business/epics/EPIC_090_AI_Financial_Analytics.md)
- **US-090-01**: 农业保险 AI 服务集成
- **US-090-02**: 金融风险 AI 分析
- **US-090-03**: AI 金融决策协调
- **US-090-04**: 动态收益管理与套期保值建议 (Revenue Management)
- **US-090-05**: 投入品采购时机 AI 预测

## [EPIC 091: 农用机器人与自动化 (Agricultural Robotics & Automation)](../business/epics/EPIC_091_Agricultural_Robotics_Automation.md)
- **US-091-01**: 自动化设备集成管理
- **US-091-02**: 机器人作业任务调度
- **US-091-03**: 自动化作业监控与质量控制
- **US-091-04**: 机器人 A2A 协议集成 (Robotic A2A Integration)
- **US-091-05**: 物理轨迹自动存证 (Automated Robotic Evidence)
- **US-091-06**: 机器人电量自律博弈 (Energy-Aware Bargaining)

## [EPIC 092: AI 驱动的协调与工作流 (AI-Driven Coordination & Workflow)](../business/epics/EPIC_092_AI_Driven_Coordination_Workflow.md)
- **US-092-01**: AI 协调层设计
- **US-092-02**: 工作流编排与执行
- **US-092-03**: 结果聚合与综合分析
- **US-092-04**: Odoo MCP Server 架构实现 (Odoo MCP Server Implementation)
- **US-092-05**: 智能体工具调用授权与安全 (MCP Tool Auth & Safety)
- **US-092-06**: 自主智能体通信协议 (OpenClaw A2A Protocol)

## [EPIC 093: 数字孪生农业 (Digital Twin Agriculture)](../business/epics/EPIC_093_Digital_Twin_Agriculture.md)
- **US-093-01**: 农场数字孪生建模
- **US-093-02**: 实时数据同步与仿真
- **US-093-03**: 数字孪生决策支持

## [EPIC 094: 智能畜禽管理 (Smart Livestock Management)](../business/epics/EPIC_094_Smart_Livestock_Management.md)
- **US-094-01**: 个体动物档案管理
- **US-094-02**: 智能健康监测与预警
- **US-094-03**: 精准饲喂管理
- **US-094-04**: 生殖与繁殖管理
- **US-094-05**: 环境控制与优化
- **US-094-06**: 产量与性能分析
- **US-094-07**: 食品安全与追溯
- **US-094-08**: 智能环控与设施管理
- **US-094-09**: 饲料库存与成本管理
- **US-094-10**: 疫病防控与用药管理

## [EPIC 095: 极致匠心农业与包容性作业管理 (Artisan Excellence & Inclusive Operations)](../business/epics/EPIC_095_Japan_Exquisite_Agriculture.md)
- **US-095-01**: 包容性辅助 UI 模式 (Inclusive UX Mode)
- **US-095-02**: 精准熟化与脱水工艺监控 (Precision Curing/Drying)
- **US-095-03**: 农业标准成本簿记 (Agricultural Standard Costing)
- **US-095-04**: 补贴申请存证自动化 (Subsidy Evidence Automation)

## [EPIC 096: 全球出口合规审计中枢 (Global Export Compliance Engine)](../business/epics/EPIC_096_Global_Export_Compliance_Engine.md)
- **US-096-01**: 自动化国际准入审计 (Automated GlobalGAP/FSMA Audit)
- **US-096-02**: 化学品安全间隔期 (PHI/Withdrawal) 红线监控
- **US-096-03**: 合规审计日志与缺口报告 (Compliance Logs & Gap Analysis)
- **US-096-04**: 生产合规技术档案一键生成 (Technical Dossier Export - 以色列模式)
- **US-096-05**: 供应链 ESG 红线监测与预警 (ESG Compliance Fortress - 巴西模式)

## [EPIC 097: 产销撮合协同平台 (Market-Direct Connection Platform)](../business/epics/EPIC_097_Market_Direct_Connection_Platform.md)
- **US-097-01**: 全球市场需求实时匹配 (Global Demand Matching)
- **US-097-02**: 订单生产全过程透明化 (Order Transparency)
- **US-097-03**: 高端品牌权益与合规标签联动 (Premium Brand Integration)
- **US-097-04**: 消费者交互与反向需求反馈 (C2M Feedback Loop - 日本模式)
- **US-097-05**: 动态品质-物流匹配决策 (Dynamic Logistics Routing - 智利模式)

## [EPIC 098: 供应链模块职责分离 (Supply Chain Module Separation)](../business/epics/EPIC_098_Supply_Chain_Module_Separation.md)
- **US-098-01**: 供应链基础框架重构
- **US-098-02**: 采购与投入品管理模块化
- **US-098-03**: 质量与定价管理模块化
- **US-098-04**: 物流与冷链管理模块化
- **US-098-05**: 供应链分析与风险监控模块化
- **US-098-06**: 供应链模块间集成接口定义
- **US-098-07**: 供应链数据迁移与兼容性保障
- **US-098-08**: 供应链性能优化与监控
- **US-098-09**: 供应链合规性与审计支持
- **US-098-10**: 供应链用户体验优化

## [EPIC 099: AI 驱动的智能供应链 (AI Driven Smart Supply Chain)](../business/epics/EPIC_099_AI_Driven_Smart_Supply_Chain.md)
- **US-099-01**: AI 采购决策支持
- **US-099-02**: AI 库存优化算法
- **US-099-03**: AI 需求预测模型
- **US-099-04**: AI 供应链风险预警
- **US-099-05**: AI 视觉质量检测
- **US-099-06**: AI 智能物流调度
- **US-099-07**: AI 供应链协调引擎
- **US-099-08**: AI 供应商智能评估
- **US-099-09**: AI 价格预测与优化
- **US-099-10**: AI 供应链可视化控制塔
- **US-099-11**: AI 供应链异常检测
- **US-099-12**: AI 供应链自动化工作流

## [EPIC 100: 多农场供应链协同 (Multi-Farm Supply Chain Collaboration)](../business/epics/EPIC_100_Multi_Farm_Supply_Chain_Collaboration.md)
- **US-100-01**: 合作社联合采购与需求聚合 (Joint Procurement Aggregation)
- **US-100-02**: 跨农场库存共享与虚拟可见 (Cross-Farm Inventory Synergy)
- **US-100-03**: 协同物流接驳与路径优化 (Collaborative Logistics Handover)
- **US-100-04**: 跨农场统一质量标准与检测协同 (Collective Quality Standardization)
- **US-100-05**: 跨农场供应链综合绩效分析 (Cross-Farm Performance Analytics)
- **US-100-06**: 多农场供应链风险共担机制 (Multi-Farm Risk Sharing)
- **US-100-07**: 联合供应商库与智能准入 (Shared Supplier Portal)
- **US-100-08**: 合作社收益分配与全链路追溯 (Fair Dividend & Traceability)
- **US-100-09**: 农场间设备与人工去中心化互助 (F2F Decentralized Resource Sharing)
- **US-100-10**: 区域级灾害与疫情联合防御 (Joint Crisis & Pest Defense)

## [EPIC 101: 供应链全链路集成 (Supply Chain End-to-End Integration)](../business/epics/EPIC_101_Supply_Chain_End_to_End_Integration.md)
- **US-101-01**: 供应链与生产计划集成
- **US-101-02**: IoT 驱动的供应链监控
- **US-101-03**: 供应链与营销系统集成
- **US-101-04**: 供应链财务核算集成
- **US-101-05**: 全链路追溯系统
- **US-101-06**: 供应链异常处理机制
- **US-101-07**: 供应链移动端支持
- **US-101-08**: 供应链实时数据同步
- **US-101-09**: 供应链合规性监控
- **US-101-10**: 供应链智能报告生成

## [EPIC 102: 品牌保护与知识产权 (Brand Protection and Intellectual Property)](../business/epics/EPIC_102_Brand_Protection_Intellectual_Property.md)
- **US-102-01**: 品牌商标保护管理
- **US-102-02**: 产品外观设计保护
- **US-102-03**: 产地证明与品牌关联
- **US-102-04**: 品牌侵权监控
- **US-102-05**: 知识产权合规管理
- **US-102-06**: 品牌授权与许可管理

## [EPIC 103: 品牌与供应链协同 (Brand and Supply Chain Synergy)](../business/epics/EPIC_103_Brand_Supply_Chain_Synergy.md)
- **US-103-01**: 品牌质量标准与供应链集成
- **US-103-02**: 品牌声誉与供应链绩效关联
- **US-103-03**: 品牌供应链透明度管理
- **US-103-04**: 品牌价值与供应链成本优化
- **US-103-05**: 品牌认证与供应链合规协同
- **US-103-06**: 品牌故事与供应链溯源整合
- **US-103-07**: 品牌风险与供应链风险管理

## [EPIC 104: 供应链需求侧管理 (Supply Demand-Side Management)](../business/epics/EPIC_104_Supply_Demand_Side_Management.md)
- **US-104-01**: 多维度需求预测模型
- **US-104-02**: 消费者行为分析引擎
- **US-104-03**: 需感情感分析系统
- **US-104-04**: 市场数据集成平台
- **US-104-05**: 竞争对手监控分析
- **US-104-06**: 价格敏感性分析
- **US-104-07**: 促销效果评估
- **US-104-08**: 动态库存优化
- **US-104-09**: 柔性生产计划
- **US-104-10**: 供应链弹性管理
- **US-104-11**: 客户需求共创平台
- **US-104-12**: 个性化推荐系统

## [EPIC 105: 供应链风险管控 (Supply Chain Risk Management)](../business/epics/EPIC_105_Supply_Chain_Risk_Management.md)
- **US-105-01**: 供应链风险识别引擎 (Supply Chain Risk Identification Engine)
- **US-105-02**: 供应链韧性评估 (Supply Chain Resilience Assessment)
- **US-105-03**: 供应链应急预案管理 (Supply Chain Contingency Planning)
- **US-105-04**: 多源风险数据集成 (Multi-source Risk Data Integration)

## [EPIC 106: 供应链碳足迹追踪 (Supply Chain Carbon Footprint Tracking)](../business/epics/EPIC_106_Supply_Chain_Carbon_Footprint_Tracking.md)
- **US-106-01**: 碳足迹数据采集引擎 (Carbon Footprint Data Collection Engine)
- **US-106-02**: 智能碳减排策略 (AI-driven Carbon Reduction Strategy)
- **US-106-03**: 供应商碳合规管理 (Supplier Carbon Compliance Management)
- **US-106-04**: 碳中和认证与报告 (Carbon Neutrality Certification & Reporting)

## [EPIC 107: 全球供应链治理 (Global Supply Chain Governance)](../business/epics/EPIC_107_Global_Supply_Chain_Governance.md)
- **US-107-01**: 多国法规合规引擎 (Multi-country Regulatory Compliance Engine)
- **US-107-02**: 跨文化供应链协同 (Cross-cultural Supply Chain Collaboration)
- **US-107-03**: 全球供应链透明度管理 (Global Supply Chain Transparency Management)
- **US-107-04**: 国际贸易风险监控 (International Trade Risk Monitoring)

## [EPIC 108: 高级VRA算法与生理决策融合 (Advanced VRA Algorithms & Physiological Fusion)](../business/epics/EPIC_108_Advanced_VRA_Algorithms_Multi_source_Data_Fusion.md)
- **US-108-01**: 土壤传感器数据实时集成 (Soil Sensor Data Integration)
- **US-108-02**: 气象数据动态调整 (Dynamic Weather Adjustment)
- **US-108-03**: 无人机多光谱数据融合 (UAV Multispectral Data Fusion)
- **US-108-04**: 机器学习参数辅助 (Optional ML Assistance)
- **US-108-05**: 生理阶段敏感性权重 (Growth-Stage Aware Logic)
- **US-108-06**: 公式化生物量亏缺补偿 (Deterministic Biomass Deficit)
- **US-108-07**: 逆境安全裁剪逻辑 (Stress-based Safety Clipping)
- **US-108-08**: 养分-生物量质能平衡 (Nutrient-Biomass Mass Balance)
- **US-108-09**: 动态风险对冲策略 (Dynamic Risk Hedging)
- **US-108-10**: 空间 RUE 差异化补偿 (Spatial RUE Compensation)
- **US-108-11**: 养分转化动力学实时修正 (Nutrient Transformation Kinetics)
- **US-108-12**: 叶面积指数 (LAI) 驱动的光合潜力校准 (LAI-Driven Potential Calibration)
- **US-108-13**: 品种响应曲线自适应 (Cultivar-Specific Response - G×E×M)

## [EPIC 109: VRA经济性分析与优化 (VRA Economic Analysis & Optimization)](../business/epics/EPIC_109_VRA_Economic_Analysis_Optimization.md)
- **US-109-01**: VRA成本效益分析引擎 (VRA Cost-Benefit Analysis Engine)
- **US-109-02**: 动态经济阈值优化 (Dynamic Economic Threshold Optimization)
- **US-109-03**: VRA投资回报预测 (VRA ROI Prediction)

## [EPIC 110: VRA环境影响评估 (VRA Environmental Impact Assessment)](../business/epics/EPIC_110_VRA_Environmental_Impact_Assessment.md)
- **US-110-01**: VRA碳足迹核算 (VRA Carbon Footprint Calculation)
- **US-110-02**: 水体保护VRA策略 (Water Body Protection VRA Strategy)
- **US-110-03**: 土壤健康VRA模型 (Soil Health VRA Model)

## [EPIC 111: VRA设备智能调度与协调 (Smart VRA Equipment Coordination)](../business/epics/EPIC_111_VRA_Equipment_Smart_Coordination.md)
- **US-111-01**: 多机协同作业调度 (Multi-Machine Coordinated Scheduling)
- **US-111-02**: 农机作业冲突预防 (Machine Operation Conflict Prevention)
- **US-111-03**: 智能加油补给调度 (Smart Refueling Schedule)

## [EPIC 112: AI驱动的全链路预测性维护 (AI-driven Predictive Maintenance Across Value Chain)](../business/epics/EPIC_112_AI_Driven_Predictive_Maintenance.md)
- **US-112-01**: 农机设备健康监测 (Farm Equipment Health Monitoring)
- **US-112-02**: 供应链节点预测性维护 (Predictive Maintenance for Supply Chain Nodes)
- **US-112-03**: 维护成本优化 (Maintenance Cost Optimization)
- **US-112-04**: 智能维护工单系统 (Smart Maintenance Work Order System)

## [EPIC 113: 碳中和与可持续发展管理 (Carbon Neutral & Sustainability Management)](../business/epics/EPIC_113_Carbon_Neutral_Sustainability_Management.md)
- **US-113-01**: 碳足迹全链路追踪 (Full-Chain Carbon Footprint Tracking)
- **US-113-02**: 碳中和目标规划与监控 (Carbon Neutrality Goal Planning & Monitoring)
- **US-113-03**: 碳信用与碳交易管理 (Carbon Credit & Trading Management)
- **US-113-04**: 可持续农业实践认证 (Sustainable Agriculture Practice Certification)

## [EPIC 114: 农业风险与保险管理 (Agricultural Risk Management & Insurance)](../business/epics/EPIC_114_Agricultural_Risk_Management_Insurance.md)
- **US-114-01**: 农业风险识别与评估 (Agricultural Risk Identification & Assessment)
- **US-114-02**: 智能风险预警系统 (AI-driven Risk Early Warning System)
- **US-114-03**: 农业保险产品管理 (Agricultural Insurance Product Management)
- **US-114-04**: 风险对冲与金融衍生品 (Risk Hedging & Financial Derivatives)

## [EPIC 115: 农业数字孪生与仿真建模 (Agricultural Digital Twin & Simulation Modeling)](../business/epics/EPIC_115_Digital_Twin_Simulation_Modeling.md)
- **US-115-01**: 农场数字孪生构建 (Farm Digital Twin Construction)
- **US-115-02**: 作物生长仿真模型 (Crop Growth Simulation Model)
- **US-115-03**: 农场运营优化仿真 (Farm Operations Optimization Simulation)
- **US-115-04**: 风险与应急仿真 (Risk & Emergency Simulation)

## [EPIC 116: 区块链溯源与食品安全保障 (Blockchain Traceability & Food Safety Assurance)](../business/epics/EPIC_116_Blockchain_Traceability_Food_Safety.md)
- **US-116-01**: 区块链溯源数据记录 (Blockchain Traceability Data Recording)
- **US-116-02**: 消费者溯源查询系统 (Consumer Traceability Query System)
- **US-116-03**: 食品安全监控与预警 (Food Safety Monitoring & Alert)
- **US-116-04**: 溯源数据验证与审计 (Traceability Data Verification & Audit)

## [EPIC 117: 数据交换与标准化 (Data Exchange & Standardization)](../business/epics/EPIC_117_Data_Exchange_Standardization.md)
- **US-117-01**: 农业数据资源目录管理
- **US-117-02**: 数据交换接口标准化
- **US-117-03**: 数据质量监控与治理
- **US-117-04**: 数据安全与隐私保护

## [EPIC 118: 订单农业与农户结算管理 (Contract Farming & Farmer Settlement)](../business/epics/EPIC_118_Contract_Farming_Settlement.md)
- **US-118-01**: "公司+农户"联营合同管理
- **US-118-02**: 自动化抵减回购结算
- **US-118-03**: 农户生产绩效雷达与评级
- **US-118-04**: 农资赊销与交售自动冲抵结算

## [EPIC 119: 智慧温室环境控制 (Smart Greenhouse Control)](../business/epics/EPIC_119_Advanced_Greenhouse_Environment_Control.md)
- **US-119-01**: 温室环境多参数协同控制
- **US-119-02**: 智能灌溉与营养液管理
- **US-119-03**: 温室能耗优化与碳减排
- **US-119-04**: 政府监管平台对接
- **US-119-05**: 电商平台 API 集成

## [EPIC 120: CSA社区支持农业与订单管理 (CSA Subscription & Order Management)](../business/epics/EPIC_120_CSA_Subscription_Management.md)
- **US-120-01**: CSA订阅引擎实现 (CSA Subscription Engine Implementation)
- **US-120-02**: 每周蔬菜包配置 (Weekly Vegetable Bag Configuration)
- **US-120-03**: 自动配送日程生成 (Automated Delivery Schedule Generation)
- **US-120-04**: 会员门户与自助服务 (Member Portal & Self-Service)
- **US-120-05**: 支付与账单集成 (Payment & Billing Integration)
- **US-120-06**: 收获规划集成 (Harvest Planning Integration)

## [EPIC 121: 农用机器人与自动化 (Agricultural Robotics & Automation)](../business/epics/EPIC_121_Agricultural_Robotics_Automation.md)
- **US-121-01**: 自动化设备集成管理 (Automated Device Integration Management)
- **US-121-02**: 机器人作业任务调度 (Robot Task Scheduling)
- **US-121-03**: 自动化作业监控与质量控制 (Automated Operation Monitoring & Quality Control)

## [EPIC 122: 商户管理与农旅商业平台 (Merchant Management & Agri-tourism Platform)](../business/epics/EPIC_122_Merchant_Management_Platform.md)
- **US-122-01**: 展位 GIS 空间规划 (Booth GIS Space Planning)
- **US-122-02**: 商家资质 Activity 审查流 (Merchant Qualification Activity Review Flow)
- **US-122-03**: 联营流水抽成结算 (Joint Operation Revenue Sharing Settlement)
- **US-122-04**: 第三方商户 PWA 移动门户 (Third-party Merchant PWA Mobile Portal)

## [EPIC 123: 蜂业与迁徙养殖管理 (Apiculture & Migration Management)](../business/epics/EPIC_123_Apiculture_Migration_Management.md)
- **US-123-01**: 蜂群全生命周期追踪 (Bee Colony Full Lifecycle Tracking)
- **US-123-02**: 迁徙路径与花期图联动 (Migration Path & Bloom Period Linkage)
- **US-123-03**: 蜂箱内部 IoT 环境监控 (Hive Internal IoT Environment Monitoring)

## [EPIC 124: 中药材与炮制管理 (Medicinal Herbs & TCM Processing)](../business/epics/EPIC_124_Medicinal_Herbs_Processing.md)
- **US-124-01**: "道地性"环境因子验证 (Authenticity Environmental Factor Verification)
- **US-124-02**: 规范化炮制工艺控制 (Standardized Processing Control)

## [EPIC 125: 食用菌与潮次管理 (Fungi & Multi-flush Harvest Management)](../business/epics/EPIC_125_Fungi_Multi_Flush_Management.md)
- **US-125-01**: 菌棒批次与接种追踪 (Mushroom Spawn Batch & Inoculation Tracking)
- **US-125-02**: "潮次"循环采收记录 (Flush Cycle Harvest Recording)

## [EPIC 126: 种质资源与生物样本库 (Germplasm & Genetic Bank)](../business/epics/EPIC_126_Germplasm_Genetic_Bank.md)
- **US-126-01**: 超低温样本库位管理 (Ultra-low Temperature Sample Storage Management)
- **US-126-02**: 遗传物质确权与授权管理 (Genetic Material Rights & Authorization Management)

## [EPIC 127: 生物质能源与外部ESG市场 (Bio-energy & External ESG Marketplace)](../business/epics/EPIC_127_BioEnergy_ESG_Marketplace.md)
- **US-127-01**: 废弃物衍生品对外贸易 (Waste-derived Products External Trade)
- **US-127-02**: 外部ESG交易所数据对接 (External ESG Exchange Data Integration)

## [EPIC 128: 中央厨房运营管理 (Central Kitchen Operations)](../business/epics/EPIC_128_Central_Kitchen_Operations.md)
- **US-128-01**: 多终端需求自动汇总与生产触发 (Multi-terminal Demand Auto-aggregation & Production Trigger)
- **US-128-02**: 标准化"大灶配方"与规模化换算 (Standardized "Large-scale Recipe" & Scale Conversion)
- **US-128-03**: 净菜与半成品序列化库存管理 (Fresh-cut & Semi-finished Product Serialized Inventory Management)
- **US-128-04**: 多点"冷链统配"与配送存证 (Multi-point "Cold Chain Unified Distribution" & Delivery Documentation)
- **US-128-05**: 数字化 HACCP 食安关键点管理 (Digital HACCP Food Safety Critical Point Management)

## [EPIC 129: 智慧供应链协同 (Smart Supply Chain Collaboration)](../business/epics/EPIC_129_Smart_Supply_Chain_Collaboration.md)
- **US-129-01**: 供应链可视化与协同 (Supply Chain Visualization & Collaboration)
- **US-129-02**: 需求预测与库存优化 (Demand Forecasting & Inventory Optimization)
- **US-129-03**: 供应链风险管理与韧性 (Supply Chain Risk Management & Resilience)
## [EPIC 130: 再生农业与土壤微生态 (Regenerative Agriculture & Soil Microbiome)](../business/epics/EPIC_130_Regenerative_Agriculture_Microbiome.md)
- **US-130-01**: 土壤微生物群落图谱 (Soil Microbiome Profiling)
- **US-130-02**: 免耕与绿肥覆盖干预管理 (No-Till & Cover Crop Interventions)
- **US-130-03**: 生物多样性净值审计 (Biodiversity Net Gain - BNG)
- **US-130-04**: 再生农业认证溢价追踪 (Regenerative Certification Premium)

## [EPIC 131: 新型蛋白与生物转化农业 (Alternative Proteins & Bio-conversion)](../business/epics/EPIC_131_Alternative_Proteins_Biomanufacturing.md)
- **US-131-01**: 黑水虻 (BSF) 生物转化全生命周期管理
- **US-131-02**: 动态有机废弃物混合配方 (Dynamic Waste Formulation)
- **US-131-03**: 光生物反应器微藻培养控制 (Microalgae Photobioreactor Control)
- **US-131-04**: 新型蛋白深加工与成分萃取追踪 (Extraction Processing)

## [EPIC 132: 农光互补与能源微电网 (Agrivoltaics & Energy Microgrids)](../business/epics/EPIC_132_Agrivoltaics_Energy_Microgrids.md)
- **US-132-01**: 农光一体化 GIS 资产映射 (Agrivoltaics GIS Mapping)
- **US-132-02**: 实时发电与农业能耗聚合 (Energy Flow Monitoring)
- **US-132-03**: 需求响应与智慧负荷调度 (Demand-Response Scheduling)
- **US-132-04**: 新能源农机 V2G 充放电管理 (V2G Agri-Machinery Integration)

## [EPIC 133: 机器人与无人机“蜂群”协同编队 (Swarm Robotics Coordination)](../business/epics/EPIC_133_Swarm_Robotics_Coordination.md)
- **US-133-01**: 蜂群任务拆分与动态分配 (Swarm Mission Partitioning)
- **US-133-02**: 空间同步与防碰撞路由规划 (Spatial Coordination & Collision Avoidance)
- **US-133-03**: 蜂群状态全景看板 (Swarm Status Dashboard)
- **US-133-04**: 动态领航者-跟随者切换协议 (Leader-Follower Handover)

