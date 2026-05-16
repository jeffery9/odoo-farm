# 农场管理系统：应用架构与用户组设计 (Farm Management System: Application Architecture & User Groups Design)

## 1. 应用层级结构 (Application Hierarchy)

### 1.1 顶层应用菜单 (Top-Level Application Menus)
```
Farm Management (农场管理)
├── Configurations (系统配置)
│   ├── General Settings (通用设置)
│   ├── Industry Modules (行业模块)
│   │   ├── Field Crops Management (大田作物管理) [Enable/Disable]
│   │   ├── Protected Cultivation Management (设施农业管理) [Enable/Disable]
│   │   ├── Orchard Horticulture Management (果树园艺管理) [Enable/Disable]
│   │   ├── Livestock Management (畜牧养殖管理) [Enable/Disable]
│   │   ├── Aquaculture Management (水产养殖管理) [Enable/Disable]
│   │   ├── Medicinal Plants Management (中药材管理) [Enable/Disable]
│   │   ├── Mushroom Management (食用菌管理) [Enable/Disable]
│   │   ├── Apiculture Management (蜂业管理) [Enable/Disable]
│   │   ├── Agricultural Processing Management (农产品加工管理) [Enable/Disable]
│   │   └── Agritourism Management (观光农业管理) [Enable/Disable]
│   └── Composite Industry Settings (复合行业设置)
├── Agricultural Families (农业活动家族)
│   ├── Configurations (配置)
│   ├── Production Campaigns (生产季)
│   └── Operations (作业/干预)
├── Agri-Science & VRA (农学科学与变量处方) [Level 2]
│   ├── Precision VRA (精准变量)
│   │   ├── Prescription Maps (处方图)
│   │   └── VRA Decision Strategies (变量策略)
│   ├── Crop Models (作物模型)
│   │   ├── Physiology Profiles (品种指纹)
│   │   └── Growth Stages (生理阶段)
│   └── Land Grid Mapping (地块网格)
├── Precision Production (精密生产执行) [Level 3]
│   ├── Production Orders (精密订单)
│   ├── Control Recipes (控制配方)
│   ├── Phase Execution (相位执行)
│   └── IoT Real-time Feedback (物联实时反馈)
├── [Industry-Specific Menu] (按启用的行业模块动态显示)
│   ├── Field Crops Management (大田作物管理) *
│   ├── Protected Cultivation Management (设施农业管理) *
│   ├── Orchard Horticulture Management (果树园艺管理) *
│   ├── Livestock Management (畜牧养殖管理) *
│   ├── Aquaculture Management (水产养殖管理) *
│   ├── Medicinal Plants Management (中药材管理) *
│   ├── Mushroom Management (食用菌管理) *
│   ├── Apiculture Management (蜂业管理) *
│   ├── Agricultural Processing Management (农产品加工管理) *
│   └── Agritourism Management (观光农业管理) *
├── Shared Services (共享服务)
│   ├── Quality Control (质量控制)
│   ├── Safety & Crisis (安全与危机)
│   ├── Supply Chain (供应链)
│   ├── Marketing (营销)
│   ├── Labor & HR (人力)
│   ├── Finance & Costs (财务)
│   └── Multi-Entity Collaboration (多实体协同)
```
* - 表示根据行业模块配置动态启用/禁用的菜单项

### 1.2 模块依赖关系 (Module Dependencies)
```
farm_core (基础核心)
├── farm_operation (通用作业/干预引擎 - L1)
│   ├── farm_agri_science (农学科学/VRA 引擎 - L2)
│   │   └── farm_operation (精密生产/ISA-88 - L3)
│   │       └── farm_iot (MQTT 实时闭环)
├── farm_planning (生产规划)
├── farm_iot (通用IoT管理)
├── farm_equipment (设备管理)
├── farm_hr (人力资源)
├── farm_supply (供应链)
├── farm_logistics (物流)
├── farm_marketing (营销)
├── farm_financial (财务)
├── farm_quality (通用质量)
├── farm_safety (通用安全)
├── farm_certification (认证)
├── farm_field_crops (大田作物)
├── farm_protected_cultivation (设施农业)
├── farm_orchard_horticulture (果树园艺)
├── farm_livestock (畜牧养殖)
├── farm_aquaculture (水产养殖)
├── farm_medicinal_plants (中药材)
├── farm_mushroom (食用菌)
├── farm_apiculture (蜂业)
├── farm_agricultural_processing (农产品加工)
├── farm_agritourism (观光农业)
├── farm_multi_farm (多实体协同) *
├── farm_sale_ch (中国销售合规) *
├── farm_cert_ch (中国认证) *
├── farm_subsidy_ch (中国补贴) *
├── farm_waste_mgmt (废物管理) *
├── farm_entity_reg (实体注册) *
├── farm_finance_gov (政府金融) *
├── farm_data_security (数据安全) *
├── farm_ux (去工业化表现层注入)
└── farm_live_streaming (直播电商) *
```
* - 表示史诗19及以后的模块

### 1.3 行业模块配置依赖 (Industry Module Configuration Dependencies)
```
farm_core (基础核心)
├── res.config.settings (配置设置)
    ├── module_farm_field_crops (大田作物管理) [Enable/Disable]
    ├── module_farm_protected_cultivation (设施农业管理) [Enable/Disable]
    ├── module_farm_orchard_horticulture (果树园艺管理) [Enable/Disable]
    ├── module_farm_livestock (畜牧养殖管理) [Enable/Disable]
    ├── module_farm_aquaculture (水产养殖管理) [Enable/Disable]
    ├── module_farm_medicinal_plants (中药材管理) [Enable/Disable]
    ├── module_farm_mushroom (食用菌管理) [Enable/Disable]
    ├── module_farm_apiculture (蜂业管理) [Enable/Disable]
    ├── module_farm_agricultural_processing (农产品加工管理) [Enable/Disable]
    └── module_farm_agritourism (观光农业管理) [Enable/Disable]
```

### 1.4 复合行业支持 (Composite Industry Support)
行业模块可以按需组合启用，支持多种复合业务场景：
- 农旅结合: `field_crops` + `agritourism`
- 设施农旅: `protected_cultivation` + `agritourism`
- 生态养殖: `aquaculture` + `apiculture`
- 加工农旅: `field_crops` + `agricultural_processing` + `agritourism`
- 多元农业: `field_crops` + `livestock` + `mushroom` + `agritourism`

## 2. 技术层级用户组 (Technical User Groups)

### 2.1 基础数据管理组
- **farm.core.user**: 基础主数据管理权限
- **farm.certification.user**: 认证管理权限

### 2.2 生产作业管理组
- **farm.operation.user**: 生产作业管理权限
- **farm.planning.user**: 生产规划权限

### 2.3 物联网与自动化组
- **industrial.iot.user**: IIOT基础权限
- **farm.iot.user**: 农场物联网权限
- **farm.weather.user**: 天气集成权限

### 2.4 质量安全管理组
- **farm.safety.user**: 安全防疫权限
- **farm.quality.user**: 质量控制权限

### 2.5 供应链管理组
- **farm.supply.user**: 投入品管理权限
- **farm.logistics.user**: 物流管理权限

### 2.6 商务营销组
- **farm.agritourism.user**: 观光农业权限
- **farm.pos.user**: POS销售权限
- **farm.marketing.user**: 营销推广权限
- **farm.label.user**: 标签管理权限
- **farm.csa.user**: CSA管理权限

### 2.7 人力资源与财务组
- **farm.hr.user**: 人力资源管理权限
- **farm.financial.user**: 财务管理权限
- **farm.sustainability.user**: 可持续发展权限

### 2.8 高级功能组
- **farm.exchange.user**: 数据交换权限
- **farm.dashboard.user**: 仪表板权限

### 2.9 行业专业用户组 (Industry-Specific User Groups)
行业模块启用后可用的专业权限组：
- **farm.field.crops.user**: 大田作物管理权限
- **farm.protected.cultivation.user**: 设施农业管理权限
- **farm.orchard.horticulture.user**: 果树园艺管理权限
- **farm.livestock.user**: 畜牧养殖管理权限
- **farm.aquaculture.user**: 水产养殖管理权限
- **farm.medicinal.plants.user**: 中药材管理权限
- **farm.mushroom.user**: 食用菌管理权限
- **farm.apiculture.user**: 蜂业管理权限
- **farm.agricultural.processing.user**: 农产品加工管理权限
- **farm.agritourism.user**: 观光农业权限

### 2.10 行业深度合规组
- **farm.subsidy.user**: 补贴管理权限
- **farm.ecology.user**: 生态管理权限
- **farm.sale.ch.user**: 跨境合规权限
- **farm.crisis.user**: 危机管理权限
- **farm.disaster.risk.user**: 灾害风险管理权限
- **farm.finance.loan.user**: 农业金融权限
- **farm.knowledge.user**: 农业知识库权限
- **farm.equipment.user**: 农机管理权限
- **farm.training.user**: 农民培训权限

### 2.11 多实体协同组
- **farm.multi.farm.user**: 多农场协同权限
- **farm.cooperative.user**: 合作社管理权限

### 2.12 中国合规组
- **farm.land.mgmt.user**: 土地管理权限
- **farm.input.reg.user**: 投入品监管权限
- **farm.cert.ch.user**: 中国认证权限
- **farm.subsidy.ch.user**: 中国补贴权限
- **farm.waste.mgmt.user**: 畜禽粪污管理权限
- **farm.green.monitor.user**: 绿色监控权限
- **farm.machinery.ch.user**: 农机补贴权限
- **farm.entity.reg.user**: 实体注册权限
- **farm.finance.gov.user**: 政府金融权限
- **farm.data.security.user**: 数据安全权限

### 2.13 直播电商组
- **farm.live.streaming.user**: 直播管理权限

### 2.14 农学科学管理组 (Agri-Science) - [NEW V3.0]
- **farm.agri.science.user**: 品种指纹、生理模型与 GDD 计算权限
- **farm.vra.strategy.user**: VRA 变量策略设计权限

### 2.15 精密生产执行组 (Precision Production) - [NEW V3.0]
- **farm.operation.user**: ISA-88 订单与配方执行权限
- **farm.operation.iot.user**: 实时设备参数监控与指令下发权限

## 3. 应用层级用户组 (Application User Groups)

### 3.1 农场核心应用组
- **farm.core.app.user**: 农场核心应用权限组合
  - 组合: farm.core.user + farm.certification.user

### 3.2 生产管理应用组
- **farm.production.app.user**: 生产管理应用权限组合
  - 组合: farm.operation.user + farm.planning.user + farm.safety.user + farm.quality.user

### 3.3 物联网应用组
- **farm.iot.app.user**: 物联网应用权限组合
  - 组合: industrial.iot.user + farm.iot.user + farm.weather.user

### 3.4 供应链应用组
- **farm.supply.app.user**: 供应链应用权限组合
  - 组合: farm.supply.user + farm.logistics.user

### 3.5 营销应用组
- **farm.marketing.app.user**: 营销应用权限组合
  - 组合: farm.agritourism.user + farm.pos.user + farm.marketing.user + farm.label.user + farm.csa.user

### 3.6 财务应用组
- **farm.finance.app.user**: 财务应用权限组合
  - 组合: farm.financial.user + farm.subsidy.user + farm.finance.loan.user + farm.finance.gov.user

### 3.7 合规应用组
- **farm.compliance.app.user**: 合规管理应用权限组合
  - 组合: farm.sale.ch.user + farm.ecology.user + farm.crisis.user + farm.disaster.risk.user

### 3.8 中国合规应用组
- **farm.china.compliance.app.user**: 中国合规应用权限组合
  - 组合: farm.land.mgmt.user + farm.input.reg.user + farm.cert.ch.user + farm.subsidy.ch.user + farm.waste.mgmt.user + farm.green.monitor.user + farm.machinery.ch.user + farm.entity.reg.user + farm.data.security.user

### 3.9 多实体协同应用组
- **farm.collaboration.app.user**: 多实体协同应用权限组合
  - 组合: farm.multi.farm.user + farm.equipment.user + farm.hr.user + farm.training.user

### 3.10 直播电商应用组
- **farm.livestream.app.user**: 直播电商应用权限组合
  - 组合: farm.live.streaming.user + farm.marketing.user + farm.pos.user

### 3.11 行业专业应用组 (Industry-Specific Application Groups)
行业模块启用后可用的专业应用权限组合：
- **farm.field.crops.app.user**: 大田作物应用权限组合
  - 组合: farm.field.crops.user + farm.operation.user
- **farm.protected.cultivation.app.user**: 设施农业应用权限组合
  - 组合: farm.protected.cultivation.user + farm.operation.user + farm.iot.user
- **farm.orchard.horticulture.app.user**: 果树园艺应用权限组合
  - 组合: farm.orchard.horticulture.user + farm.operation.user
- **farm.livestock.app.user**: 畜牧养殖应用权限组合
  - 组合: farm.livestock.user + farm.operation.user + farm.hr.user
- **farm.aquaculture.app.user**: 水产养殖应用权限组合
  - 组合: farm.aquaculture.user + farm.operation.user + farm.iot.user
- **farm.medicinal.plants.app.user**: 中药材应用权限组合
  - 组合: farm.medicinal.plants.user + farm.operation.user
- **farm.mushroom.app.user**: 食用菌应用权限组合
  - 组合: farm.mushroom.user + farm.operation.user
- **farm.apiculture.app.user**: 蜂业应用权限组合
  - 组合: farm.apiculture.user + farm.operation.user
- **farm.agricultural.processing.app.user**: 农产品加工应用权限组合
  - 组合: farm.agricultural.processing.user + farm.operation.user + farm.quality.user
- **farm.agritourism.app.user**: 观光农业应用权限组合
  - 组合: farm.agritourism.user + farm.marketing.user + farm.pos.user

### 3.12 农学决策应用组 - [NEW V3.0]
- **farm.science.app.user**: 科学决策应用权限组合
  - 组合: farm.agri.science.user + farm.vra.strategy.user + farm.core.user

### 3.13 精密执行应用组 - [NEW V3.0]
- **farm.precision.app.user**: 精密生产应用权限组合
  - 组合: farm.operation.user + farm.operation.iot.user + farm.iot.user

## 4. 角色层级用户组 (Role User Groups)

### 4.1 农场主 (Farm Owner) - 配置模式
- **权限组成**:
  - base.group_user (内部用户) - 基础权限
  - farm.core.app.user (农场核心应用)
  - farm.production.app.user (生产管理应用)
  - farm.science.app.user (科学决策应用) [NEW]
  - farm.precision.app.user (精密生产应用) [NEW]
  - farm.marketing.app.user (营销应用)
  - farm.finance.app.user (财务应用)
  - farm.compliance.app.user (合规应用)
  - farm.china.compliance.app.user (中国合规应用)
  - farm.collaboration.app.user (协同应用)
  - farm.livestream.app.user (直播电商应用)
  - [Industry-Specific App Groups] (按启用行业模块动态添加) *
  - account.group_account_manager (会计经理) - 财务管理权限
  - purchase.group_purchase_manager (采购经理) - 采购管理权限
  - stock.group_stock_manager (仓库经理) - 仓库管理权限
  - hr.group_hr_manager (人力资源经理) - 人力资源管理权限
  - project.group_project_manager (项目经理) - 项目管理权限
- **职责**: 关注整体经营利润、成本控制、科学闭环及合规性
- **配置权限**: 可在系统配置中启用/禁用行业模块

* - 表示根据启用的行业模块动态添加相应的应用用户组

### 4.2 农业技术员 (Technician) - 配置模式
- **权限组成**:
  - base.group_user (内部用户) - 基础权限
  - farm.core.app.user (农场核心应用)
  - farm.production.app.user (生产管理应用)
  - farm.science.app.user (科学决策应用) [NEW]
  - farm.iot.app.user (物联网应用)
  - farm.supply.app.user (供应链应用)
  - [Industry-Specific App Groups] (按启用行业模块动态添加) *
  - farm.ecology.user (生态管理) - 单独权限
  - farm.knowledge.user (知识库) - 单独权限
  - project.group_project_user (项目用户) - 项目查看权限
  - stock.group_stock_user (仓库用户) - 库存查看权限
* - 表示根据启用的行业模块动态添加相应的应用用户组

- **职责**: 数字化专家，关注作物生长、变量处方、土壤养分及品种指纹管理

### 4.3 农场工人 (Farm Worker / Operator)
- **权限组成**:
  - base.group_user (内部用户) - 基础权限
  - farm.production.app.user (生产管理应用)
  - farm.operation.user (精密生产执行) [NEW]
  - farm.iot.app.user (物联网应用)
  - farm.hr.user (人力资源) - 单独权限
  - project.group_project_user (项目用户) - 任务查看权限
  - stock.group_stock_user (仓库用户) - 库存查看权限
- **职责**: 负责执行具体作业（干预）、操作精密设备并对 IoT 反馈进行现场确认

### 4.4 财务管理员 (Financial Manager)
- **权限组成**:
  - base.group_user (内部用户) - 基础权限
  - farm.finance.app.user (财务应用)
  - farm.supply.app.user (供应链应用)
  - farm.marketing.app.user (营销应用)
  - account.group_account_user (会计) - 财务管理权限
  - purchase.group_purchase_user (采购用户) - 采购管理权限
  - stock.group_stock_user (仓库用户) - 库存管理权限
- **职责**: 负责农业成本核算、采购及销售对账

### 4.5 营销经理 (Marketing Manager)
- **权限组成**:
  - base.group_user (内部用户) - 基础权限
  - farm.marketing.app.user (营销应用)
  - farm.supply.app.user (供应链应用)
  - farm.pos.user (POS) - 管理权限
  - sales.group_sale_manager (销售经理)
- **职责**: 负责品牌推广、CSA 订阅及销售渠道管理

### 4.6 游客 (Visitor/Tourist)
- **权限组成**:
  - base.group_portal (门户用户) - 门户访问权限
  - farm.agritourism.user (观光农业) - 只读权限
  - farm.pos.user (POS销售) - 购买权限
- **职责**: 参与观光农业活动，如采摘、研学等

### 4.7 合作社理事长 (Cooperative Chairman)
- **权限组成**:
  - base.group_user (内部用户) - 基础权限
  - farm.collaboration.app.user (协同应用)
  - farm.finance.app.user (财务应用)
  - farm.compliance.app.user (合规应用)
  - farm.china.compliance.app.user (中国合规应用)
  - hr.group_hr_manager (人力资源经理) - 人力资源管理权限
  - account.group_account_manager (会计经理) - 财务管理权限
  - project.group_project_manager (项目经理) - 项目管理权限
- **职责**: 负责合作社整体运营和战略规划

### 4.8 IT管理员 (IT Administrator)
- **权限组成**:
  - base.group_system (系统管理员) - 系统管理权限
  - farm.data.security.user (数据安全) - 单独权限
  - farm.exchange.user (数据交换) - 单独权限
  - account.group_account_manager (会计经理) - 财务管理权限
  - hr.group_hr_manager (人力资源经理) - 人力资源管理权限
- **职责**: 负责系统运维、数据安全和权限管理

## 5. 权限继承关系图 (Permission Inheritance Diagram - V3.0 Enhanced)

```
┌─────────────────────────────────────────────────────────────────┐
│                        Base Groups                              │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │ base.group_user │  │ base.group_sys  │  │ base.group_port │  │
│  │   (Internal)    │  │    (System)     │  │   (Portal)      │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Application Groups                            │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │ farm.core.app   │  │ farm.prod.app   │  │ farm.iot.app    │  │
│  │    (.user)      │  │     (.user)     │  │     (.user)     │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │ farm.supply.app │  │ farm.market.app │  │ farm.finance.app│  │
│  │     (.user)     │  │     (.user)     │  │     (.user)     │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │ farm.science.app│  │ farm.prec.app   │  │ farm.china.comp.│  │
│  │     (.user)     │  │     (.user)     │  │     app.user    │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Role Groups                                │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │  Farm Owner     │  │   Technician    │  │   Farm Worker   │  │
│  │   (Complete)    │  │   (Specialist)  │  │   (Operator)    │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │ Fin. Manager    │  │ Market Manager  │  │ Visitor/Tourist │  │
│  │   (Finance)     │  │   (Marketing)   │  │   (External)    │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```
注：farm.science.app.user 和 farm.prec.app.user 为 V3.0 引入的科学与精密执行层权限组合。

## 6. 实现要点 (Implementation Highlights)

### 6.1 三层权限架构
- **技术层**: 按功能模块划分的原子权限组
- **应用层**: 按业务应用聚合的复合权限组
- **角色层**: 按业务角色分配的最终用户权限组

### 6.2 权限继承机制
- 采用多层继承机制，角色层继承应用层，应用层继承技术层
- 与Odoo原生用户组集成，确保权限一致性

### 6.3 数据隔离策略
- 通过实体关系实现多农场数据隔离与共享
- 支持按数据类型设置不同的访问级别

### 6.4 合规性保障
- 集成中国农业法规要求的权限控制
- 支持认证、补贴、环保等合规管理权限

### 6.5 科学驱动权限隔离 - [NEW V3.0]
科学层 (L2) 的参数修改权限（如修改 Mitscherlich 品种效率系数）仅授予 `Technician` 角色，严禁 `Operator` 或普通 `Worker` 修改，以确保生产过程的科学严肃性。

### 6.6 空间权限安全 - [NEW V3.0]
VRA 处方图的生成与下发权限与地理围栏 (`agri.geofencing`) 绑定，确保指令仅在合法地理空间内被执行。

## 7. 可配置行业模块权限模型 (Configurable Industry Module Permission Model)

### 7.1 权限动态加载机制
在可配置行业模块架构下，系统根据 `res.config.settings` 中启用的行业模块动态加载相应权限组：

- **动态权限组**: 当启用特定行业模块时，系统自动为相关角色添加对应的行业专业用户组
- **角色适应性**: 基础角色（如农场主、技术员）会根据启用的行业模块自动扩展其权限组合
- **菜单可见性**: 未启用的行业模块对应的菜单项和功能界面将被隐藏

### 7.2 配置模式角色权限
启用行业模块后，角色权限将自动扩展：

**农场主 (Farm Owner)**:
- 原有权限保持不变
- 额外获得所有已启用行业模块的管理权限
- 配置权限：在系统配置中启用/禁用行业模块

**农业技术员 (Technician)**:
- 原有权限保持不变
- 根据启用的行业模块，获得相应的专业操作权限
- 可访问相应行业的数据和功能

**营销经理 (Marketing Manager)**:
- 原有权限保持不变
- 根据启用的行业模块，获得相应的营销和销售权限
- 可管理相应行业的营销活动和销售数据

### 7.3 复合行业权限处理
当启用多个行业模块时：
- 系统自动合并各行业模块的权限组
- 用户可以访问所有启用行业的数据和功能
- 权限冲突通过角色权重和数据隔离策略解决
- 支持跨行业数据关联分析

### 7.4 权限配置最佳实践
- **最小权限原则**: 仅授予用户完成工作所需的最低权限
- **按需启用**: 根据业务需要启用相应行业模块
- **定期审查**: 定期审查启用的行业模块和分配的权限
- **复合管理**: 合理规划复合行业场景下的权限分配