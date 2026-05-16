# Odoo 19 农场管理系统：技术映射规格书 (Total Traceability Edition)

基于 Odoo 19 的原生功能，我们将农业业务概念进行如下映射。本文档采用**全量留痕方式**记录从 V1.0 (初始设计) 到 V2.0 (ISL 委托继承架构) 的演进过程。

---

## 1. 基础架构映射 (Infrastructure)

| 农业概念 | Odoo 19 原生模型 | 扩展逻辑与演进 |
| :--- | :--- | :--- |
| **Activity (活动)** | `project.project` | 增加 `activity_family` (种植/畜牧/水产/观光) 字段。 |
| **ActivityProduction (生产实施)** | `project.task` | 关联 `campaign_id`。作为干预措施的父节点。 |
| **Support (支撑对象)** | ~~`product.product`~~ -> **`stock.location`** | ~~地块、池塘、动物群组均映射为带有“农业属性”的产品 [V1.0 弃用]~~ -> **现重构为货位以支撑 GIS 空间算法 [V2.0 准则]。** |
| **Variety (品种)** | `product.template` | 使用产品模板管理生物品种。 |

---

## 2. 核心底座架构演进 (The ISL Layer Evolution)

| 农业操作 | Odoo 19 基础层 (Base) | ~~旧方案：直接扩展 (_inherit) [V1.0]~~ | **新方案：委托继承 (_inherits) [V2.0]** |
| :--- | :--- | :--- | :--- |
| **Intervention (干预)** | `mrp.production` | ~~直接在 mrp.production 增加行业字段~~ | **ISL 子模型：`livestock.production`, `processing.production`** |
| **Input (投入品)** | `mrp.bom.line` | 肥料、种子、饲料作为 BOM 组件。 | 保持不变，注入行业 Domain 过滤。 |
| **Output (产出品)** | `product.product` | 收获物作为制造产出。 | 保持不变。 |
| **Recipe (配方)** | `mrp.bom` | ~~直接在 mrp.bom 增加行业字段~~ | **ISL 子模型：`livestock.bom`, `processing.bom`** |
| **Asset (批次资产)** | `stock.lot` | ~~简单 Lot 跟踪~~ | **ISL 增强：谱系、体重、生命阶段动态追踪 [V2.0]。通过 farm_mrp 钩子实现解耦 [V3.0]。** |

---

## 2.5 核心底座架构演进 V3.0 (The Refined ISL Infrastructure)

在 V3.0 中，我们引入了 **`farm_mrp`** 作为所有农业 ISL 模块的共同底座，实现了以下关键改进：

1. **自动生命周期管理**：当创建标准 `mrp.bom` 或 `mrp.production` 时，系统根据 `industry_type` 自动创建对应的 ISL 子表记录。
2. **解耦的批次摘要**：通过 `_get_isl_summary_parts` 钩子，各行业模块独立注入批次显示信息，底座不再硬编码行业逻辑。
3. **透明视图路由**：完善了 `get_formview_action`，确保用户始终处于其行业专有的 Form 视图中，并保持上下文一致性。


---

## 3. 生产与干预映射细化 (Production & Intervention)

- **种植行业 (Crop Farming)**：
    - **模型**：直接使用 `mrp.production` 增强。
    - **逻辑**：将农事作业视为“制造订单”。
- **畜牧/水产 (Livestock & Aquaculture)**：
    - **模型**：~~直接扩展 [V1.0]~~ -> **委托模型 `livestock.production` [V2.0]**。
    - **逻辑**：记录入栏、生长、出栏全过程。
- **农产品加工 (Processing)**：
    - **模型**：~~直接扩展 [V1.0]~~ -> **委托模型 `processing.production` [V2.0]**。

---

## 4. 库存与地理信息 (Stock & GIS)

| 农业资源 | Odoo 19 原生模型 | 实现细节 |
| :--- | :--- | :--- |
| **Land Parcel (地块)** | `stock.location` | ~~简单货位 [V1.0]~~ -> **增加 GeoJSON 边界与 Shoelace 面积精算算法 [V2.0]。** |
| **Biological Asset** | `stock.lot` | ~~简单批次号 [V1.0]~~ -> **ISL 增强：谱系、体重、生命阶段动态追踪 [V2.0]。** |

---

## 5. 营销与客户连接 (Marketing & Demand)

| 业务需求 | Odoo 19 社区版实现方案 | 规格说明 |
| :--- | :--- | :--- |
| **溯源二维码** | `portal` + `qweb` | 在产品包装上打印包含任务 ID 的 URL。匿名访问者通过 Portal 页面查看该任务关联的干预记录及遥测数据聚合。 |
| **订阅农业 (CSA)** | `contract` (OCA) / 定期发票 | 利用 Odoo 销售订单的“定期重复”功能管理长期供应。 |
| **需求驱动生产 (MTO)** | `stock.route` | 当销售订单（需求）确认时，自动触发相关的农事生产任务。 |

---

## 6. IIOT 与 移动端架构 (MQTT 集成细化)

| 场景 | 技术路径 | 规格细节 |
| :--- | :--- | :--- |
| **MQTT Broker** | Mosquitto / EMQX | 建议使用外部 Broker 处理高频并发连接。 |
| **Odoo 接入层** | `paho-mqtt` 客户端 | Odoo 启动监听线程，或通过 Webhook 接收消息。 |
| **数据同步** | ~~直接回填业务记录 [V1.0]~~ | **利用 `iot.telemetry.buffer` 异步处理，防止数据库死锁 [V2.0]。** |
| **Topic 映射** | ~~硬编码处理 [V1.0]~~ | **通过 `iot.device.mapping` 实现灵活映射协议 [V2.0]。** |

---

## 7. 育苗、育种与防疫映射 (Breeding & Biosafety Mapping)

| 业务需求 | Odoo 19 社区版实现方案 | 规格说明 |
| :--- | :--- | :--- |
| **育苗转场管理** | `stock.picking` + `project.task` | 育苗期在“育苗温室”货位。移栽时生成内部调拨单并更新任务关联地块。 |
| **防疫/植保计划** | `mrp.routing.workcenter` | 为不同阶段预设“防疫路线”，自动生成包含特定疫苗/农药的 MO。 |
| **系谱/性状跟踪** | ~~`product.template` 属性 [V1.0]~~ | **现使用 `livestock.lot` 的 `parent_lot_ids` 递归关联实现 [V2.0]。** |
| **安全采摘期校验** | `computed fields` + `ir.cron` | 在地块/资产模型计算休药期，若处于安全期则锁定收获。 |

---

## 8. 有机/绿色认证控制 (Organic Certification Control)

| 业务需求 | Odoo 19 社区版实现方案 | 规格说明 |
| :--- | :--- | :--- |
| **投入品准入控制** | `mrp.production` (Constraint) | 扩展 `action_confirm` 方法，检查投入品是否在黑名单中。 |
| **认证状态跟踪** | `documents` (OCA) + `stock.location` | 在地块模型增加认证等级（常规/转换/有机）及证书附件关联。 |
| **生产审计日志** | `mail.tracking.value` | 利用 Odoo 审计轨迹记录所有关键投入品，确保不可篡改。 |

---

## 9. 农场人力与劳动力调度 (HR & Labor Scheduling)

| 业务需求 | Odoo 19 社区版实现方案 | 规格说明 |
| :--- | :--- | :--- |
| **农业技能管理** | `hr.skill` | 使用原生技能管理框架，定义农业技能类型。 |
| **现场工时采集** | `hr.timesheet` | 扩展工时表模型，增加 `production_id` 关联。 |
| **劳动力成本分摊** | `analytic.account` | 工资根据工时比例自动分摊到具体项目和任务。 |

---

## 10. 农产品加工管理映射 (Agri-Processing)

| 业务需求 | Odoo 19 社区版实现方案 | 实现细节与算法 [V2.0 增强] |
| :--- | :--- | :--- |
| **初加工分级** | `mrp.production` | 支持一入多出，强制执行物料守恒算法。 |
| **能耗核算** | `mrp.production` | **实现 `energy_reading_start/end` 及成本分摊算法。** |
| **层级包装** | `stock.package` | **实现“单品 -> 中箱 -> 托盘”的多级层级嵌套逻辑。** |
| **递归溯源** | `stock.lot` | **实现 Recursive Traceability 算法，一键穿透至地块。** |

---

## 11. 农业质量控制与检测 (Agri-Quality & Inspection)

| 业务需求 | Odoo 19 社区版实现方案 | 规格说明 |
| :--- | :--- | :--- |
| **检查点与标准** | 自定义 `farm.quality.point` | 定义作业类型与检查项的关联。 |
| **质量硬拦截 (Gate)**| `quality_gate_status` | **MO 完成前强制审批，未通过严禁 Mark Done [V2.0]。** |

---

## 12. 模块体系结构 (Addon Responsibilities)

- **farm_core**: 核心元数据、GIS 面积算法、地块管理。
- **farm_operation**: 农事作业任务流。
- **farm_livestock**: 养殖 ISL 子模型、FCR 算法、健康排程。
- **farm_processing**: 加工 ISL 子模型、物料平衡、递归溯源、层级包装。
- **farm_iot**: 动态映射协议、异步 Buffer 处理。

---

## 13. App 与 Addon 架构映射 (App Architecture)

### 13.1 App 定义原则
App 负责行业隔离。每个 App 通过其专属 Action 注入行业 Domain 过滤。

| App 名称 | 行业标识 (Context) | 映射子模型 (ISL) |
| :--- | :--- | :--- |
| **Smart Processing**| `field_crop` | `processing.production` |
| **Smart Livestock** | `livestock` | `livestock.production` |
| **Smart Crop** | `crop` | `mrp.production` (Base) |

### 13.2 菜单层级映射 [V1.0 逻辑保留]
```
顶级 App 菜单 (在 farm_multi_farm/views/menu.xml 中定义)
├── Cooperative Management (合作社管理)
│   ├── Cooperatives (合作社) -> cooperative.entity
│   └── Farm Entities (农场实体) -> farm.entity
├── Resource Sharing (资源共享)
│   └── Resource Sharing -> resource.sharing
├── Internal Settlements (内部结算)
│   └── Internal Settlements -> internal.settlement
```

---
**存档时间**：2026-01-15  
**架构师**：Gemini CLI & User  
**状态**：ISL 架构已定案，文档全量留痕存档完毕。