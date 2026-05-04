# 行业标准层 (Industry Standard Layer - ISL) 架构白皮书

*版本: V2.0 | 状态: Core Enforced*

## 1. 架构愿景 (Architecture Vision)

在构建农业全产业链系统时，最致命的架构陷阱就是**“巨石型模型污染”** (Monolithic Model Pollution)。
由于农业的垂直细分极其严重（例如：大田种植的“播种”、水产养殖的“投喂”、食品加工的“发酵”在底层都是消耗库存的生产行为，但它们所需的业务字段、合规校验和界面呈现完全不同），如果直接在 Odoo 原生的 `mrp.production` 上追加所有行业的专属字段，会导致该模型膨胀至数千个字段，视图中充满复杂的 `invisible` 判定，最终导致系统崩溃且无法维护。

**ISL (Industry Standard Layer)** 架构应运而生。它是我们在 Odoo 社区版上首创的**“多态透明代理网关”**，实现了底层交易与上层业务的彻底解耦。

## 2. 核心设计机制 (Core Mechanisms)

### 2.1 委派继承 (Delegation Inheritance) - `_inherits`
ISL 放弃了传统的 `_inherit` (经典扩展)，转而使用 `_inherits` (代理继承/多态)。

以加工制造为例：
*   底层坚如磐石：Odoo 原生的 `mrp.production` 保持原封不动，继续处理其最擅长的库存预留、路由流转和会计成本分摊。
*   上层千面代理：我们创建了多个行业专属的 ISL 模型（例如 `farm.ras.production` 用于工厂化水产，`agri.mrp.production` 用于食品加工），它们通过 `mrp_production_id` 外键与底层模型建立 1:1 的硬链接。

### 2.2 透明视图重定向拦截 (Transparent View Interception)
这是 ISL 的魔法所在。
我们在底层的 `mrp.production` 模型中重写了 `get_formview_action()` 方法。当用户在任何地方（比如采购单的智能按钮，或者某个仪表盘）点击一条底层制造单记录时：
1.  重定向引擎 (`agri.isl.model.redirector`) 被唤醒。
2.  引擎通过读取该记录的 `industry_type` 字段（例如 `food_processing`）。
3.  引擎**拦截原生的跳转响应**，将视图动作 (Action) 的 `res_model` 动态替换为 `agri.mrp.production`，并加载其专属的视图。
4.  **用户体验**: 对于用户来说，点击不同的订单，看到的是完全不同的、量身定制的专业界面（完全没有多余字段的干扰）。

### 2.3 行业隔离的强合规检查 (Domain-Isolated Compliance)
借助于 ISL，不同行业的合规校验互不干扰：
*   食品加工 ISL (`_check_industry_compliance`): 可以在点击“标记为完成”时，强制校验是否上传了 `HACCP 计划`。
*   化工投入品 ISL: 可以强制校验是否符合危险品 `GMP Compliance`。

## 3. 落地规范 (Implementation Guidelines)

任何新的垂直农业模块（如：`farm_viticulture` 葡萄栽培）如果要实现其特有的生产或库存逻辑，**必须**遵循以下规范：

1.  **禁止污染基座**: 绝对禁止直接在 `mrp.production` 或 `stock.move` 的 Python 文件里添加该行业特有的字段（如 `sugar_content_brix`）。
2.  **建立专属 ISL 模型**: 必须新建 `farm.viticulture.production`，使用 `_inherits = {'mrp.production': 'mrp_production_id'}`。
3.  **注册重定向路由**: 在 `agri.isl.model.redirector` 的 `special_mappings` 字典中注册您的模型路由。
4.  **设计专属 UI**: 为您的 ISL 模型编写无干扰的纯净视图（Form/Tree），并挂载到您专属的顶级 App 菜单下（参考 *UX_MENU_ARCHITECTURE_PRINCIPLES.md*）。

---
**附注**: 目前，系统已经在底层准备好了分布分发的重定向沙盒 (`get_formview_action`)，随着各子行业 UI 视图的物理落地，该网关将全面接管系统的全局导航。
