# Odoo 19 农场管理系统：模块规范与进度看板 (V2.1)

本项目采用高度模块化的架构，将复杂的农业业务拆分为原子化模块，以确保系统的灵活性和 Odoo 19 社区版的兼容性。

## 1. 原子模块组合解决方案 (Atomic Module Composition)

### 核心原则
- **模块原子性**: 单一职责，专注特定领域。
- **ISL 代理继承**: 核心模型透明扩展，逻辑物理隔离。
- **去工业化 UX**: 农业术语拦截映射。

### 模块矩阵与职责定义

| 分类 | 模块目录名 | 核心职责 | 状态 |
| :--- | :--- | :--- | :--- |
| **底座** | `farm_core` | 农场基础主数据、PostGIS 地理信息、土质分析。 | ✅ 完成 |
| | `farm_isl` | ISL 行业标准层：模型重定向、透明代理继承、行业逻辑物理隔离。 | ✅ 完成 |
| | `farm_certification` | 有机/绿色认证状态、转换期管理、证书审计。 | ✅ 完成 |
| **作业** | `farm_operation` | 生产季、农事干预、收获分级。 | ✅ 完成 |
| | `farm_planning` | 技术路线库 (Recipe)、模拟情景、资源预测。 | ✅ 完成 |
| | `farm_livestock` | 畜牧管理：个体动物档案、系谱追踪、健康监测、繁殖周期 [EPIC 64]。 | ✅ 完成 |
| | `farm_breeding` | 育种管理：系谱记录、遗传追踪、繁育计划 [EPIC 10, 42]。 | ✅ 完成 |
| | `farm_processing` | 产后加工：分拣包装、物料平衡、制药/化工行业扩展 [EPIC 14]。 | ✅ 完成 |
| | `farm_aquaculture` | 水产养殖：水质监控、投喂管理、生长跟踪 [ISL 适配]。 | ✅ 完成 |
| **物联** | `farm_iot` | 遥测采集、下控指令、自主规则引擎。 | ✅ 完成 |
| | `industrial_iot` | 底层 MQTT 通信桥接（FastAPI + Odoo）。 | ✅ 完成 |
| | `farm_weather` | 外部天气预报集成、基于天气的作业预警。 | ✅ 完成 |
| **安全** | `farm_safety` | 防疫隔离、休药期拦截、合规校验。 | ✅ 完成 |
| | `farm_quality` | QCP 控制点、HACCP 熔断、溯源审计、召回模拟。 | ✅ 完成 |
| | `farm_data_security` | 数据分类、IoT 设备安全注册、等保合规审计 [EPIC 55]。 | ✅ 完成 |
| **金融** | `farm_financial` | 任务成本分摊、多边净额对冲、信用评分。 | ✅ 完成 |
| | `farm_finance_loan` | 活体资产抵押、农业保险精算。 | ✅ 完成 |
| **智能** | `farm_ai_agent` | AI 协调层、决策闭环、结果聚合引擎。 | ✅ 完成 |
| | `farm_ai_llm_integration` | LLM 农业知识增强、智能报告生成、RAG。 | ✅ 完成 |
| | `farm_ai_vision` | 计算机视觉病害诊断、边缘端离线识别。 | ✅ 完成 |
| **供应** | `farm_supply` | 投入品准入目录、采购合规拦截、FEFO 出库建议。 | ✅ 完成 |
| | `farm_logistics` | 冷链运输、温控标记、多级包装、货架期预测。 | ✅ 完成 |
| **商务** | `farm_agritourism` | 活动预约、资源日历、亲子项目管理。 | ✅ 完成 |
| | `farm_pos` | 采摘即销售，POS 订单关联地块。 | ✅ 完成 |
| | `farm_marketing` | 消费者溯源门户、产品生长故事。 | ✅ 完成 |
| | `farm_label` | 打印标签、批次牌、地块标牌、动物耳标。 | ✅ 完成 |
| | `farm_csa` | CSA 会员订阅引擎、周期性配送单生成。 | ✅ 完成 |
| **UX** | `farm_ux` | 术语映射、三端自适应、信号灯标识。 | ✅ 完成 |
| | `farm_mobile` | 离线 PWA 工作台、语音输入、地理打卡。 | ✅ 完成 |

## 2. 用户故事 (User Story) 分配矩阵 (精简版)

| 史诗 (Epic) | 承载模块 | 状态 |
| :--- | :--- | :--- |
| **Epic 1: 基础数据** | `farm_core` | ✅ |
| **Epic 2: 种植管理** | `farm_operation` | ✅ |
| **Epic 3: 养殖管理** | `farm_livestock`, `farm_iot` | ✅ |
| **Epic 14: 产品加工** | `farm_processing`, `farm_quality` | ✅ |
| **Epic 52: 高级溯源** | `farm_processing`, `farm_quality` | ✅ |
| **Epic 54: ISL 架构** | `farm_isl`, `farm_processing` | ✅ |
| **Epic 55: 网络安全** | `farm_data_security` | ✅ |
| **Epic 58: AI 决策支持** | `farm_ai_agent`, `farm_ai_decision` | ✅ |
| **Epic 59: AI LLM 集成** | `farm_ai_llm_integration` | ✅ |
| **Epic 60: AI 金融分析** | `farm_financial`, `farm_finance_loan` | ✅ |
| **Epic 62: AI 驱动工作流** | `farm_ai_agent`, `farm_workflow` | ✅ |
| **Epic 64: 智能畜禽管理** | `farm_livestock` | ✅ |
| **Epic 27: 农业循环经济** | `farm_waste_mgmt` | 🚧 |
| **Epic 63: 数字孪生农业** | `farm_iot`, `farm_dashboard` | 💡 |

---
**最后更新**: 2026-01-27