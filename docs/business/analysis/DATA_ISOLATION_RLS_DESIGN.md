# Odoo Farm 数据隔离与 RLS (Row-Level Security) 策略设计

> **背景 (Context)**：
> 在 Odoo Farm 的终极“合作社与小农经济”模式下，一个数据库实例中会同时存在 1个合作社管理员 (Coop Manager) 和 50-1000 名小农户 (Smallholders/Workers)。
> 如果不加限制，农户 A 可以看到农户 B 的土地、生物资产、结算单甚至小额贷款审批情况。这在多实体协同中是绝对不允许的。
> 本设计方案利用 Odoo 的 ir.rule (记录规则) 实现硬编码级别的数据隔离。

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
