# EPIC-134: Dynamic Recipe Formulation (动态配方补偿引擎)

## 1. 业务背景 (Context)
与工业制造的恒定原料不同，农产品的理化指标（如含糖量 Brix、含水率、酸度）受气候和批次影响极大。如果使用静态 BOM，加工产成品的口感和质量将出现剧烈波动。食品加工企业急需能够根据原料即时质检数据，自动逆向调整辅料（水、糖、添加剂）投料比的动态配方能力。

## 2. 核心目标 (Objectives)
* 实现 BOM 比例与 lot_properties（如含水率、糖度）的动态联动。
* 确保批次间产出品的理化指标绝对一致 (Batch-to-Batch Consistency)。
* 减少过度添加（如防腐剂或糖分）造成的辅料浪费。

## 3. 用户故事 (User Stories)
* **[US-134-01]** 作为配方研发员，我可以在 BOM 中定义“目标理化指标”和“辅料补偿公式”，以便系统能根据主料动态计算。
* **[US-134-02]** 作为车间主任，当领料时，如果本批次草莓糖度仅为 9%（标准为12%），系统能自动将 BOM 中糖的投料指令从 5kg 修改为 8kg。
* **[US-134-03]** 作为质检员，我需要系统记录下每次动态调平前后的实际配比，用于后续的口味追溯。

## 4. 架构影响 (Architecture Impact)
* **核心模型**: mrp.bom, mrp.production
* **交互点**: 需要在 mrp.production.action_confirm 阶段，注入钩子，读取 stock.lot 的 properties，并执行 AST 数学公式重新计算 stock.move (原料需求) 的数量。
