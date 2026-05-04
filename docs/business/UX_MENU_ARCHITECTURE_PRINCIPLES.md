# 农场生态系统：UX/UI 菜单与应用架构原则 (UX/UI Architecture Principles)

*版本: V1.0 | 状态: 强制执行 (Mandatory)*

本系统摒弃了传统 ERP 庞大、冗长且相互嵌套的“巨石型菜单 (Monolithic Menus)”，转而拥抱现代 SaaS 的“工具化 (Tool-based)”设计思想。

## 1. 核心设计哲学 (Core Philosophy): Tools, Not Trees

在现代农业场景中，用户（从拖拉机手到农场主）是在**特定场景下执行特定任务**。他们需要的是一件“称手的工具”，而不是一本“百科全书”。

*   **反模式 (Anti-Pattern)**: 
    *   ❌ 创建一个巨大的“农场管理 (Farm Management)”根菜单，然后把种植、养殖、设备、合同、报表全塞进无限层级的下拉菜单中。
*   **最佳实践 (Best Practice)**: 
    *   ✅ 将每一个核心业务域独立为一个顶层 App（在 Odoo 应用抽屉中拥有独立图标）。
    *   ✅ 例如：打开【温室控制】App，里面只有温室相关的仪表盘和阈值设定；打开【农业测序】App，里面只有基因和土壤样本数据。

## 2. 顶层 App 拆分原则 (App Splitting Guidelines)

当开发一个新的 `farm_xxx` 模块时，如何决定是新建一个 App（顶层菜单）还是依附于现有的 App？

1.  **角色与场景隔离 (Role & Scenario Isolation)**: 如果该模块的使用者与现有 App 的使用者角色（Role）不同，或者工作场景完全分离，**必须新建顶层 App**。
    *   *案例*: 【拖拉机维保】和【农产品电商销售】属于完全不同的部门，必须是两个独立的 App。
2.  **菜单层级极限 (Depth Limit)**: 任何 App 内部的菜单层级**绝对禁止超过 3 层**（根菜单 -> 一级分类 -> 动作）。如果某项功能需要建立第 5 层菜单，说明该 App 已经过度臃肿，必须将其剥离为新的 App。
3.  **微应用即服务 (Micro-App as a Service)**: 像使用手机 App 一样使用 Odoo。【病虫害诊断】、【VRA处方图生成】、【碳足迹测算】都应该是召之即来、挥之即去的独立工具应用。

## 3. Odoo 菜单实现规范 (Implementation Rules)

在编写 `views/menu.xml` 时，强制遵循以下代码规范：

### 3.1 根菜单 (Root Menu) 必须明确且独立
```xml
<!-- ✅ Correct: Creating a focused, independent tool App -->
<menuitem id="menu_farm_robotics_root" 
          name="Swarm Robotics" 
          web_icon="farm_robotics,static/description/icon.png"
          sequence="30"/>
```

### 3.2 避免滥用 `parent` 进行深层嵌套
```xml
<!-- ❌ Incorrect: Stuffing a complex tool under a generic "Settings" or "Operations" tree -->
<menuitem id="menu_robotics_config" name="Robots" parent="farm_core.menu_general_operations_hardware_settings" sequence="10"/>

<!-- ✅ Correct: Keeping it flat within its own App domain -->
<menuitem id="menu_robotics_config" name="Fleet Config" parent="menu_farm_robotics_root" sequence="10"/>
```

### 3.3 ISL (行业标准层) 的菜单隐形继承
对于重用 `mrp.production` (制造单) 等底层逻辑的模块，**绝对禁止**将菜单项挂载到原生 Odoo 的 `Manufacturing` 菜单下。必须在自己的 App 根菜单下，通过 Action 定义调用底层模型。

```xml
<!-- 在农业 App 中调用底层 MRP 模型，实现“干预任务”的管理，而不是让农民去打开“制造”应用 -->
<menuitem id="menu_agri_interventions" 
          name="Field Interventions" 
          parent="menu_farm_operation_root" 
          action="mrp.mrp_production_action" 
          sequence="10"/>
```

## 4. 结论 (Conclusion)
我们的 UI/UX 目标是：**降低农业从业者的认知负荷**。每一个点击开启的应用，都必须是一个高度收敛、上下文清晰、所见即所得的专业工具。


## 5. 主数据分散化与业务归口原则 (Distributed Master Data Principle)

在传统 ERP 中，往往会设置一个庞大且臃肿的“基础数据 (Master Data)”模块，这就导致了跨部门的认知灾难。在本农业套件中，我们强制执行**“主数据必须完全分散到各专业 App 中”**的准则。

### 5.1 核心主张：主数据属于它被最高频消费的场景
*   **反模式 (Anti-Pattern)**: 
    *   ❌ 设立一个全局的“主数据”顶级应用，把农机设备、种子品种、传感器型号、地理围栏全塞进一个菜单。这会导致拖拉机手必须在一堆“育苗记录”里去寻找“添加新农机”的入口。
*   **最佳实践 (Best Practice)**: 
    *   ✅ **属于该 App 的主数据，在该 App 内就能看到和管理。** 主数据的维护入口应当作为底层支撑，无缝融入到日常业务执行的上下文中。

### 5.2 落地规范 (Implementation Guidelines)
1.  **按域挂载 (Domain-Specific Mount)**:
    *   **🌿 种植管理 App**: 其配置菜单只挂载“作物品种”、“生长基点模型”、“地块档案”。
    *   **🐄 畜牧管理 App**: 其配置菜单只挂载“动物血统”、“健康检查标准”、“饲料配方表”。
    *   **📡 IoT 应用 App**: 其配置菜单只挂载“网关路由”、“传感器预警阈值”。
2.  **多维投影 (Multi-Projection via Actions)**: 
    对于跨 App 使用的全局通用数据（如：员工档案、农产品字典、农场大区），绝对不允许让用户切换到“员工 App”或者“库存 App”去寻找。
    *   **实现方式**: 在各个需要使用到这些数据的 App 的 `Configuration`（配置）菜单下，直接复用 `ir.actions.act_window` 投影对应的视图。确保用户停留在当前的 App 环境中完成闭环操作。


## 6. 与 5 层架构的 UI 映射关系 (UI Mapping to 5-Layer Architecture)

我们的 UI 设计完全倒影了后端的 **5-Layer Macro Architecture**：
*   **L0/L1 层 (底座与引擎)**: 通常在前端**不可见**，或者只作为“开发者模式”下的隐藏配置菜单存在。它们为上层提供驱动力，但不占用顶层 App 图标资源。
*   **L2 层 (垂直行业)**: 构成了用户桌面上 90% 的 **独立 App 图标**（如：【畜牧】,【深加工】,【大田种植】）。这就是为什么我们强调 Tools Not Trees。
*   **L3 层 (智能与合规)**: 表现为全局看板（Dashboard）或悬浮在 L2 单据之上的警告横幅（Alerts/Wizards），提供无缝的“降维打击式” UX 体验。
