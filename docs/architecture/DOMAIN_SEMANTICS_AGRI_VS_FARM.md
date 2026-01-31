# 2026 农业系统架构：Agri 与 Farm 语义分层规格 (V3.0)

> **最高核心律令：Agri 优先，Farm 受限**
> 1. **Agri (领域级)**：代表农业科学、物理真理与产业协议的普适性. 是系统的灵魂与骨架。优先使用 `agri.*` 命名空间。
> 2. **Farm (细分级)**：仅代表“土地经营实体”这一特定业务切片。严禁使用 `farm.*` 去承载跨行业普适的农业逻辑。

## 1. 语义象限定义 (Semantic Quadrants)

### 1.1 Agri 层 (域名：agri.*) - 领域标准与客观真理 (核心)
Agri 层承载了农业作为物理系统的全部事实。它应该是**“去中心化”**且**“跨实体”**的。

- **命名规范**: 所有的 AbstractModel (Mixin)、通用 API 协议、跨实体清算逻辑必须使用 `agri.*` 前缀。
- **职责范畴**:
    - **物理事实**: NPK 质量平衡 (`agri.nutrient.mixin`)、碳排放标准 (`agri.sustainability.mixin`)、水分利用率。
    - **协作主权**: A2A 协议、谈判状态机、Evidence Analyzer (审计逻辑)。
    - **价值互联网**: 品质指纹 (Fingerprint)、社区清算账本 (Ledger)、跨农场价值桥 (Value Bridge)。
    - **格栅化底座**: 空间格栅索引算法 (GeoSpatial Grids)。

### 1.2 Farm 层 (域名：farm.*) - 行业应用与具象操作 (受限)
Farm 层仅作为农业领域下的一个**特定应用场景**。通过注入 Agri 层的 Mixins，将行业标准转化为具体的业务价值。

- **命名规范**: 具体的业务实体 (Model)、UI 视图 (View)、本地化调度逻辑使用 `farm.*` 前缀。
- **职责范畴**:
    - **农事工作流**: 具体的农事指令 (Intervention)、播种任务、收获记录。
    - **实体资产**: 地块 (Location)、机器人机队、员工身份、仓库库存。
    - **商业交互**: 消费者营销、认养流程、本地清算分录。
    - **UX 表现**: 专门针对农场主设计的去工业化界面拦截。

## 2. 语义映射与纠偏矩阵 (Semantic Alignment Matrix)

本矩阵定义了从工业化术语到 Agri 领域真理，再到 Farm 具象操作的演进路径。

| 工业化术语 (Industrial) | Agri 领域语义 (Domain) | Farm 行业语义 (Operation) | 修正理由 |
| :--- | :--- | :--- | :--- |
| **Manufacturing Order** | `agri.nutrient.mixin` (养分转化) | `farm.intervention` (农事干预) | 生产本质是物质转化，干预是其实现。 |
| **BOM / Formula** | `agri.impact.standard` (环境标准) | `farm.recipe` (栽培配方) | 配方是操作级的，标准是领域级的。 |
| **Work Center** | `agri.geospatial.grid` (格栅单元) | `farm.field.segment` (地块分区) | 地理坐标属于 Agri，地块划分属于 Farm。 |
| **Inventory Trace** | `agri.evidence.bundle` (物理存证) | `farm.lot.trace` (批次追踪) | 存证是通用的物理事实，批次是库存逻辑。 |
| **Partner Balance** | `agri.clearing.ledger` (社区清算) | `farm.member.balance` (成员账目) | 清算协议是通用的，账目是个体实体的。 |

## 3. 领域细分行业图谱 (Sub-sector Hierarchy)

Agri 是顶层领域，其下通过功能和经营模式进行横向细分。Farm 只是其中之一。

| 领域细分 (Sub-sector) | Agri 核心标准 (Mixin/Protocol) | Farm 具象实体 (Operation Models) |
| :--- | :--- | :--- |
| **种植业 (Planting)** | `agri.nutrient.balance`, `agri.soil.health` | `farm.crop`, `farm.location.field` |
| **畜牧业 (Livestock)** | `agri.animal.welfare`, `agri.feed.conversion` | `farm.animal`, `farm.herd`, `farm.stable` |
| **水产业 (Aquaculture)** | `agri.water.quality`, `agri.bio.density` | `farm.pond`, `farm.aquarium`, `farm.batch` |
| **产后加工 (Processing)** | `agri.mass.balance`, `agri.energy.intensity` | `farm.production.line`, `farm.recipe` |
| **蜂业 (Apiculture)** | `agri.pollination.index`, `agri.migration` | `farm.apiary`, `farm.beehive`, `farm.honey.lot` |
| **林果业 (Orchard)** | `agri.perennial.growth`, `agri.tree.carbon` | `farm.tree`, `farm.block`, `farm.harvest.season` |
| **设施农业 (CEA/GH)** | `agri.climate.control`, `agri.iot.actuation` | `farm.greenhouse`, `farm.rack`, `farm.sensor` |
| **菌物业 (Fungi)** | `agri.substrate.conversion`, `agri.flush.logic` | `farm.growth.room`, `farm.substrate.batch` |
| **农旅/CSA (Commerce)** | `agri.community.contribution`, `agri.esg.score` | `farm.membership`, `farm.event`, `farm.pos` |
| **金融/保险 (Financial)** | `agri.risk.premium`, `agri.asset.valuation` | `farm.loan`, `farm.insurance.policy`, `farm.pledge` |

## 4. 工程执行律令 (Engineering Mandates)

1. **命名一致性**: 
    - 开发者在创建新模型前必须自问：“该逻辑在林场/渔港是否通用？”若能通用，严禁使用 `farm.` 前缀。
    - 严禁在 `agri.*` 命名空间中引用具体的 `farm.*` 业务逻辑。
2. **逻辑下沉**: 如果现有的 `farm.*` 模型中包含具有行业普适性的计算公式，必须将其重构并下沉至 `agri.*` 命名的 Mixin 中。
3. **隔离律令**: 表现层（UI）必须物理隔离。通用计算必须沉淀为 Mixin。
4. **跨行业扩展**: 确保 `agri.*` 协议可以无缝支持多业态并存。一个 Farm 实体可同时继承多个子行业的 Agri Mixins。

## 5. 跨行业扩展性设计 (Cross-sector Extensibility)

1. **共享 Mixins**: 所有子行业共享 `agri.clearing.mixin` 和 `agri.evidence.mixin` 以确保跨实体的对账一致性。
2. **多行业共存**: 一个 Farm 实体可以同时属于种植、畜牧和加工子行业，通过多重继承 Mixins 达到语义聚合。

## 6. 概念体系深度细分 (Detailed Concept Hierarchy)

基于“Agri 为体，Farm 为用”的原则，本章节对系统的细分行业、物理实体与逻辑概念进行全量建模指导。

### 6.1 领域细分行业 (Domain Sub-sectors)
除传统的 `Farming` (大田种植) 外，Agri 领域还包含以下核心细分，它们共享底层的物理与经济协议：
- **Ranching** (牧场经营): 侧重广域放牧、草畜平衡与移动轨迹存证。
- **Viticulture** (葡萄与果酒): 侧重单株资产管理、糖度物候期与工艺配方。
- **Silviculture** (造林与林业): 侧重长周期碳汇、森林健康度与采伐配额。
- **Horticulture** (园艺与花卉): 侧重精细化环境控制、品种专利保护与冷链溯源。
- **Agritech Services** (农业服务): 侧重第三方无人机喷洒、收割博弈与农机共享。

### 6.2 具象物理实体 (Physical Entities)
`Farm` (农场) 是 `Farming` 细分下的物理表现，Agri 领域通过不同的物理载体承载物理事实：
- **Field / Plot** (田块): 种植业的核心物理空间。
- **Greenhouse / CEA Facility** (温室/设施): 受控环境农业的物理边界。
- **Barn / Stable / Coop** (畜舍): 畜牧业个体的物理居所。
- **Pond / Tank / Cage** (鱼塘/网箱): 水产业的物理容器。
- **Processing Unit / Facility** (加工单元): 产后价值转化的物理场站。
- **Distribution Hub** (分拨枢纽): 价值清算与物理流转的交汇点。

### 6.3 普适逻辑概念 (Logical Concepts)
这些概念定义了农业系统的运行逻辑，跨行业通用且必须遵循 `agri.*` 命名：
- **Mass Balance** (物理守恒): NPK 及生物质流转的终极平衡准则。
- **Phenology / Life Cycle** (物候/生命周期): 决定任务触发时机的生物学逻辑。
- **Quality Fingerprint** (品质指纹): 跨实体互信的数字证明。
- **A2A Protocol** (智能体博弈): 解决资源错配与价值发现的经济协议。
- **Sustainability Redline** (可持续红线): 系统级强制执行的环境准则。
- **Evidence Chain** (存证链): 链接传感器数据与清算凭证的逻辑纽带。

---
*最后更新：2026-01-31 (V3.2 全量无损修复版)*