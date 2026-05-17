# EPIC-135: Toll Manufacturing Trust & Quality Mass Balance (委外加工信任与物料平衡)

## 1. 业务背景 (Context)
农村合作社通常缺乏深加工能力，需将初级农产品（如鲜茶叶、生肉）拉至大型加工厂进行“委外代工 (Subcontracting/Toll Manufacturing)”。在此过程中，代工厂“偷换优质原料”或“私自截留印有村集体品牌的包材”是巨大的信任漏洞。

## 2. 核心目标 (Objectives)
* 建立严格的委外物料平衡 (Mass Balance) 校验模型。
* 严密追踪印有高附加值 Logo 的包材流向，防止“飞单”。
* 在 Odoo 原生 Subcontracting 基础上增加农业质检容差卡点。

## 3. 用户故事与验收标准 (User Stories & Acceptance Criteria)

### US-135-01: 委外加工的物料平衡红线 (Toll Manufacturing Mass Balance)
**As a** 合作社理事长 (Coop Manager)
**I want to** 为委外加工单设定“极限得率区间 (Yield Tolerance)”
**So that** 代工厂无法在加工过程中私自截留优质原料或以次充好。

*   **AC1 (触发收货熔断)**: 
    *   **Given** 发给代工厂 1000kg 鲜茶叶（含水率70%），BOM 设置得率下限为 25%
    *   **When** 代工厂交回成品干茶，库管员试图入库 200kg (得率仅 20%)
    *   **Then** Odoo 自动弹窗阻断入库（Validate 按钮失效），并抛出 `Mass Balance Anomaly`（物料平衡异常）警告，强制要求经理介入。
*   **AC2 (动态含水率折算)**: 
    *   **Given** 发出原料前
    *   **When** 合作社录入了鲜叶的当日含水率属性
    *   **Then** 系统能将 25% 的静态得率，动态折算为基于干物质的绝对得率区间。

### US-135-02: 品牌包材的 1:1 损耗追踪 (Branded Packaging Control)
**As a** 品牌防伪官 (Brand Protection Officer)
**I want to** 严格追踪发给代工厂的带有数字防伪码的空纸箱
**So that** 这些印着村集体高溢价 Logo 的包材不会流向黑市。

*   **AC1 (严格发料关联)**:
    *   **Given** 包含“序列号管控 (Serial Tracking)”纸箱的委外单
    *   **When** 代工厂交回 500 盒成品
    *   **Then** 收货界面强制要求库管员扫码验证对应的 500 个空纸箱的 Serial Numbers。
*   **AC2 (严苛的废品核销)**:
    *   **Given** 代工厂声称弄坏了 5 个空纸箱
    *   **When** 合作社进行核销
    *   **Then** 必须走专项的 `Scrap` 流程，上传毁损照片，注销这 5 个防伪码的防伪链验证能力。

### US-135-03: 代工质量一票否决 (Toll Quality Freeze)
**As a** 质检合规员 (QC Inspector)
**I want to** 在代工成品入库后强制插入农残检验卡点
**So that** 不合格的代工产品绝对无法进入合作社自营的社区生鲜店。

*   **AC1 (溯源护照冻结)**:
    *   **Given** 刚从代工厂入库的成品批次 (处于隔离区 Quarantine)
    *   **When** 录入的外部农残化验单 (Lab Test) 结果为 Failed
    *   **Then** 该批次的数字溯源护照直接被冻结为 `Invalid`，且 Odoo POS 终端在扫描该批次条码时直接报错“禁止销售”。

## 4. 架构影响 (Architecture Impact)
* **核心模型**: mrp.production, stock.picking, stock.lot
* **交互点**: 深度拦截 Odoo 的 Subcontracting 流程，在 receipt 环节强制插入质量与物料守恒的钩子计算。
