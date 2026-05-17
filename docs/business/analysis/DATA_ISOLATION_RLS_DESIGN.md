# Odoo Farm 数据隔离与 RLS (Row-Level Security) 策略设计

> **背景 (Context)**：
> 在 Odoo Farm 的终极“合作社与小农经济”模式下，一个数据库实例中会同时存在 1个合作社管理员 (Coop Manager) 和 50-1000 名小农户 (Smallholders/Workers)。
> 如果不加限制，农户 A 可以看到农户 B 的土地、生物资产、结算单甚至小额贷款审批情况。这在多实体协同中是绝对不允许的。
> 本设计方案利用 Odoo 的 ir.rule (记录规则) 实现硬编码级别的数据隔离。


---

## 4. 升级版：三级树状组织架构的权限隔离 (Hierarchical Multi-Tier RLS)

> **进阶需求**：现代农业合作社并非扁平结构，而是呈现出 **合作社 (Cooperative) -> 独立农场主 (Farm Owner) -> 雇佣农工/小散户 (Worker)** 的三级树状嵌套结构。我们需要通过更加动态的 Domain 规则实现“向下穿透可见，向上平行隔离”。

### 4.1 角色与底层数据结构映射 (The 3-Tier Odoo Mapping)
> **核心定律**：合作社 (Tier 1) 对应 Odoo 的 res.company；其下的农场与农户 (Tier 2/3) 属于公司内部的团队/部门 (Team) 层级。

* **Tier 1: 合作社管理员 (Coop Manager)** 
  * -> 映射到 group_farm_manager。
  * -> **架构地位**：利用 Odoo 原生的多公司机制 (Multi-Company)。在单公司下，Manager 的 Domain 为 [(1, '=', 1)]。他自动被 Odoo 的原生 company_id 防火墙隔离，绝对看不到其他合作社（其他 Company）的数据。
* **Tier 2: 独立农场主 / 承包大户 (Farm Owner / Team Leader)** 
  * -> 映射到 group_farm_specialist。
  * -> **架构地位**：属于公司内的一个 Team 或 Department。他在 res.partner 或 hr.employee 中作为 Parent 节点。
* **Tier 3: 基层雇工 / 小散户 (Worker)** 
  * -> 映射到 group_farm_worker。
  * -> **架构地位**：作为叶子节点，其 parent_id 或 department_id 指向 Tier 2 的大户。

### 4.2 动态隔离域设计 (Dynamic Domain Design)

为了实现层级穿透，我们在 Odoo 的 ir.rule 中不只判断 user.id，而是深入解析用户的组织关系网：

* **Tier 3 (Worker) 规则**：
  * **逻辑**：极度私密，仅看自己。
  * **代码 (Domain)**：[('user_id', '=', user.id)] 或 [('partner_id', '=', user.partner_id.id)]。
* **Tier 2 (Farm Owner) 规则**：
  * **逻辑**：不仅能看自己的数据，还能向下穿透，看到**挂靠在自己农场名下**的所有雇工或土地数据。但绝对看不到同村其他农场主的数据（平行隔离）。
  * **代码 (Domain)**：['|', ('owner_id', '=', user.partner_id.id), ('parent_id', '=', user.partner_id.id)]。如果是结算单，则判断付款/收款方是否属于自己的子农场组织架构。
* **Tier 1 (Coop Manager) 规则**：
  * **逻辑**：管理整个村集体。能看到所有加入了该合作社的农场和散户的数据。但看不到隔壁村合作社的数据（通过 Multi-Company 防火墙）。
  * **代码 (Domain)**：[(1, '=', 1)] (在多公司模式下，Odoo 的公司级防火墙会自动限制在当前合作社公司内)。

---

## 一、 角色体系重塑 (Role Hierarchy)

我们复用并扩展 farm_core 的原生组：
1. **group_farm_worker (基层农户/操作员)**：只能看**自己的**数据。
2. **group_farm_specialist (技术专家/队长)**：可以看本业务线或本服务队的数据。
3. **group_farm_manager (合作社管理员)**：拥有上帝视角，可以看整个合作社的所有数据（受限于公司/company_id 级别隔离）。

---

## 二、 核心四大维度的隔离规则 (The 4 Pillars of Isolation)

### 1. 资产与土地的隔离 (Asset & Land)
* **涉及模型**：agri.biological.asset (生物资产), agri.location (带测绘的地块)
* **隔离逻辑**：
  * **农户 (Worker)**：只能看 user_id = user.id 或 owner_id = user.id 的地块和牛羊资产。
  * **管理员 (Manager)**：[(1, '=', 1)] (所有资产可见)。

### 2. 财务与资金流的隔离 (Financial Settlements & Credit)
* **涉及模型**：internal.settlement (内部结算), farm.micro.loan (微贷), dividend.line (分红明细)
* **隔离逻辑**：
  * **农户 (Worker)**：这属于绝对隐私。只能看 to_entity_id = user.partner_id.id 或 farmer_id = user.id 的资金流水和贷款记录。
  * **管理员 (Manager)**：可以统揽全社的流水。

### 3. 农事作业与工时的隔离 (Operations & Worklogs)
* **涉及模型**：project.task (农事工单), farm.worklog (工时打卡与时间银行)
* **隔离逻辑**：
  * **农户 (Worker)**：只能看分配给自己的工单 [('user_ids', 'in', [user.id])]，以及自己填写的工时日志 [('employee_id.user_id', '=', user.id)]。

### 4. 数据交易与大市场隔离 (Marketplace & Exchange)
* **涉及模型**：internal.marketplace (拼单直采平台)
* **隔离逻辑**：
  * **上架大厅**：所有激活的商品大家都能看。
  * **订单详情**：农户只能看自己发起的“求购单 (Demand)”或“供应单 (Supply)”。

---

## 三、 代码落地指南 (Implementation Plan)

我们将在特定的关键模块中，注入 security/ir_rule.xml：
* 在 farm_core 强化底层地块和生物资产的规则。
* 在 farm_multi_farm_financial 建立财务结算防火墙。
* 在 farm_financial_credit 建立小额信贷防火墙。
* 在 farm_operation / farm_hr 锁定工单与工时可见性。

*(These rules ensure that the system is fully compliant with data privacy regulations while enabling massive rural cooperative ecosystems.)*
