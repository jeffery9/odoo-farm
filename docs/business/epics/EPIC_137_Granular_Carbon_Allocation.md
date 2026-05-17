# EPIC-137: Granular Energy & Carbon Allocation (精细化能源与碳足迹分摊)

## 1. 业务背景 (Context)
深加工（如烘焙、冻干、冷链）是农业产业链中的高耗能节点。传统财务通常将每月几万块的电费作为“制造费用 (Overhead)”一刀切地按工时分摊给所有产品。但这掩盖了不同批次（如烘得特别干的茶 vs 普通茶）真实的能耗与碳足迹差异，无法支撑高端有机农产品的“碳中和精确标签”。

## 2. 核心目标 (Objectives)
* 与车间级 IoT 智能电表打通，记录每张工单的真实千瓦时 (kWh)。
* 将电耗精确折算为财务成本与 Scope 2 碳排放量。
* 将这些碳/财务成本精确追加到该特定批次的最终单位成本 (Unit Cost) 中。

## 3. 用户故事与验收标准 (User Stories & Acceptance Criteria)

### US-137-01: 工单直连智能电表 (Workorder IoT Meter Integration)
**As a** 车间设备管理员 (Equipment Manager)
**I want to** 将高耗能设备（如茶叶杀青机、烘干机）的 IoT 电表与 Odoo 的工作中心绑定
**So that** 我们能精确知道每一张工单耗了多少度电。

*   **AC1 (精准捕获能耗)**:
    *   **Given** 杀青机绑定了 IoT 电表 MAC 地址
    *   **When** 工人在平板上点击工单的 `Done`
    *   **Then** 系统自动调用 IoT 网关查询 `Start` 到 `Done` 期间的电表增量，并将例如 `15.5 kWh` 的读数写入该工单的能耗字段中。

### US-137-02: 精确的财务制造成本分摊 (Granular Landed Cost)
**As a** 财务管控总监 (Financial Controller)
**I want to** 每一度电都转化为精确的财务成本叠加到该批次产品上
**So that** 高端和低端产品的真实利润率(Gross Margin)不再被平均值掩盖。

*   **AC1 (动态存货估值)**:
    *   **Given** 系统配置的工业电价为 $0.15/kWh
    *   **When** 一张耗电 100 kWh 的工单完工
    *   **Then** 系统自动生成一条关联到该产成品批次的 `stock.valuation.layer` (存货估值层)，价值为 $15.00，科目类别为“直接制造成本-电力”。

### US-137-03: 批次级 Scope 2 碳足迹烙印 (Lot-Level Scope 2 Carbon Footprint)
**As a** ESG 与品牌营销总监 (ESG & Brand Director)
**I want to** 电耗直接转化为碳排放量并烙印在区块链溯源护照上
**So that** 应对欧盟 CBAM 法规，并向中产消费者讲述硬核的环保故事。

*   **AC1 (碳账本自动核算)**:
    *   **Given** 当地电网的碳排放因子为 0.5 kg CO2e / kWh
    *   **When** 上述 100 kWh 的工单完工
    *   **Then** 系统的 `agri.carbon.ledger` 自动记入一条 50kg CO2e 的 Scope 2 排放记录，并与该产成品的批次 ID 终身绑定。
*   **AC2 (C 端展示)**:
    *   **Given** 消费者扫码
    *   **When** 查看产品数字护照
    *   **Then** 界面清晰显示：“本批次茶叶在加工烘焙环节，共产生 50kg 碳足迹，已通过农场果园的 Scope 3 碳汇完成中和。”

## 4. 架构影响 (Architecture Impact)
* **核心模型**: mrp.workorder, agri.carbon.ledger (假设模型), stock.valuation.layer
* **交互点**: 在 mrp.workorder 完工时捕获 IoT 数据，触发额外的财务分摊条目和 ESG 账本条目。
