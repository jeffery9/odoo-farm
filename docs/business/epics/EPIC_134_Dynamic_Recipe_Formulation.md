# EPIC-134: Dynamic Recipe Formulation (动态配方补偿引擎)

## 1. 业务背景 (Context)
与工业制造的恒定原料不同，农产品的理化指标（如含糖量 Brix、含水率、酸度）受气候和批次影响极大。如果使用静态 BOM，加工产成品的口感和质量将出现剧烈波动。食品加工企业急需能够根据原料即时质检数据，自动逆向调整辅料（水、糖、添加剂）投料比的动态配方能力。

## 2. 核心目标 (Objectives)
* 实现 BOM 比例与 lot_properties（如含水率、糖度）的动态联动。
* 确保批次间产出品的理化指标绝对一致 (Batch-to-Batch Consistency)。
* 减少过度添加（如防腐剂或糖分）造成的辅料浪费。

## 3. 用户故事与验收标准 (User Stories & Acceptance Criteria)

### US-134-01: 定义配方补偿公式 (Define Formulation Formula)
**As a** 配方研发经理 (Formula R&D Manager)
**I want to** 在 BOM (物料清单) 的辅料行上定义基于主料理化指标的计算公式
**So that** 系统知道如何在生产时动态调整辅料的投料量。

*   **AC1 (公式语法验证)**: 
    *   **Given** 我在配置草莓酱的 BOM
    *   **When** 我为“白砂糖”组件勾选“动态补偿”并输入公式 `base_qty + (12 - raw_material.lot_properties.brix) * 0.5`
    *   **Then** 系统应通过 AST 语法树校验该公式的合法性，并允许保存。
*   **AC2 (边界保护)**: 
    *   **Given** 一个配置了动态配方的 BOM
    *   **When** 我设置了计算公式
    *   **Then** 我必须同时设置该辅料的 `Min_Qty` 和 `Max_Qty`，以防止计算异常导致投料量离谱。

### US-134-02: 领料时的动态调平 (Dynamic Adjust on Material Consumption)
**As a** 车间主任 (Production Supervisor)
**I want to** 在制造订单 (MO) 选中具体原料批次时，系统自动重算辅料需求
**So that** 工人严格按照修正后的完美比例进行投料，保证口感一致性。

*   **AC1 (自动触发重算)**:
    *   **Given** 一张处于草稿 (Draft) 状态的 MO，标准需白糖 5kg
    *   **When** 库管为“草莓”组件指定了批次号 `LOT-001` (其属性 Brix=9%)
    *   **Then** MO 上的白糖需求量 (To Consume) 瞬间自动更新为 `8kg`，并标注红色“已动态补偿”图标。
*   **AC2 (禁止随意修改)**:
    *   **Given** 系统已执行了动态补偿
    *   **When** 产线工人尝试手动修改辅料需求量
    *   **Then** 界面应阻断修改，或强制要求输入主管的覆核密码。

### US-134-03: 追溯护照中的配方快照 (Traceability Log)
**As a** 质检员 / 消费者 (QC / Consumer)
**I want to** 在产成品的批次履历中看到“实际配比快照”
**So that** 能够追溯某一批次产品口感偏差的确切原因。

*   **AC1 (履历生成)**:
    *   **Given** 一张已完工 (Done) 的 MO
    *   **When** 我查看生成的成品批次记录 (`stock.lot`) 的溯源树
    *   **Then** 我能看到一个名为“配方微调日志”的页签，明确记录：“标准糖 5kg -> 实际投料 8kg (原因：原料批次 LOT-001 Brix 偏差)”。

## 4. 架构影响 (Architecture Impact)
* **核心模型**: mrp.bom, mrp.production
* **交互点**: 需要在 mrp.production.action_confirm 阶段，注入钩子，读取 stock.lot 的 properties，并执行 AST 数学公式重新计算 stock.move (原料需求) 的数量。
