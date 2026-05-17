# EPIC-135: Toll Manufacturing Trust & Quality Mass Balance (委外加工信任与物料平衡)

## 1. 业务背景 (Context)
农村合作社通常缺乏深加工能力，需将初级农产品（如鲜茶叶、生肉）拉至大型加工厂进行“委外代工 (Subcontracting/Toll Manufacturing)”。在此过程中，代工厂“偷换优质原料”或“私自截留印有村集体品牌的包材”是巨大的信任漏洞。

## 2. 核心目标 (Objectives)
* 建立严格的委外物料平衡 (Mass Balance) 校验模型。
* 严密追踪印有高附加值 Logo 的包材流向，防止“飞单”。
* 在 Odoo 原生 Subcontracting 基础上增加农业质检容差卡点。

## 3. 用户故事 (User Stories)
* **[US-135-01]** 作为合作社理事长，当我发出 1000kg 鲜叶（含水率70%）去代工时，系统能自动锁定代工厂必须交回 280kg-320kg 的干茶，否则拒绝收货结算。
* **[US-135-02]** 作为库管员，我发出的每一只带有溯源二维码的空纸箱，代工厂必须1:1绑定成品还回，系统严禁包材库存在代工厂产生无法解释的“损耗”。
* **[US-135-03]** 作为质检员，当代工厂交回的成品在农残或多边缩水率校验失败时，系统能自动冻结该批次的数字护照。

## 4. 架构影响 (Architecture Impact)
* **核心模型**: mrp.production, stock.picking, stock.lot
* **交互点**: 深度拦截 Odoo 的 Subcontracting 流程，在 receipt 环节强制插入质量与物料守恒的钩子计算。
