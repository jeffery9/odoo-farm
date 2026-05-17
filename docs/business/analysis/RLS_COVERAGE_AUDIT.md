# 三级数据权限控制 (3-Tier RLS) 覆盖率评审报告
# Coverage Audit for Hierarchical Row-Level Security

> **评审目的 (Objective)**：
> 在引入了 "Tier 1 (合作社) -> Tier 2 (农场主) -> Tier 3 (小农户)" 的三级树状隔离架构后，我们需要系统性地盘点 Odoo Farm 100+ 个模块中的敏感数据，确保没有出现“越权可见”或“向下穿透失败”的盲区。

---

## 1. 第一象限：已完成 100% 覆盖的核心资产 (Fully Covered Vectors)

### 1.1 金融与清算体系 (Finance & Settlements)
* **包含模型**：internal.settlement (内部结算), dividend.line (分红), farm.micro.loan (微贷)
* **防护状态**：**Airtight (密不透风)**
* **评审结论**：利用 from_entity_id, to_entity_id, 和 farmer_id 的 parent_id 逻辑，完美实现了 Tier 3 仅见个人，Tier 2 穿透至下属雇工，Tier 1 统揽全局。资金流的安全性达到金融级标准。

### 1.2 空间与物理底座 (Land & Locations)
* **包含模型**：agri.location (带 GIS 的数字地块)
* **防护状态**：**Airtight (密不透风)**
* **评审结论**：利用 original_owner_id 及其 parent_id。即便是被村集体合并为大田 (Mega-Field)，农场主和农户依然能在系统里清晰且唯一地看到属于自己产权的那部分“微地块”。

---

## 2. 第二象限：需要补充覆盖的盲区 (Identified Blind Spots)

经过全库扫视，我们发现以下 **3 个极其敏感的业务域** 尚未接入三级穿透规则，存在数据越权的巨大风险！

### 盲区 1：数字农事作业单与工时 (Operations & Tasks)
* **风险点**：目前 project.task 和 farm.worklog 仅受到 Odoo 原生 Project 模块的扁平化权限控制（分配给我才可见）。
* **后果**：**Tier 2 (农场主) 成了瞎子。** 当他雇佣了 10 个散工去果园打药时，如果任务只分配给了散工，农场主在系统里根本看不到这些作业单的进度，也无法审批他们的工时（Time Bank）。
* **整改方案**：必须注入一条 ir.rule，使得 project.task 的 user_ids.partner_id.parent_id 包含当前用户时，农场主对其拥有 Read/Write 权限。

### 盲区 2：生物资产与物联网数据 (Biological Assets & IoT)
* **风险点**：agri.biological.asset (如某头被标记的种猪)。
* **后果**：如果一头牛被分配给了一个雇工照料，农场主将无法从上帝视角查看这头牛的每日增重（ADG）。如果不隔离，农户 A 甚至能看到农户 B 家牛群的健康状况。
* **整改方案**：将 owner_id.parent_id 穿透逻辑引入 agri.biological.asset。

### 盲区 3：农产品库存与仓储批次 (Inventory & Quality Lots)
* **风险点**：stock.lot (包含农药残留、品质定级的最终产出物)。
* **后果**：合作社会把所有的草莓收上来统一打包（Mega-Lot）。但在被合并前，农户存在自己独立的产出物批次。目前任何登录 Odoo 的人都可以在“库存->批次”里看到全村所有人的收成情况。在中国农村，**“露富”或“知道别人家收成好”是引发基层矛盾的导火索**。
* **整改方案**：为 stock.lot 附加产权归属标签，并强制执行三级隔离。

---

## 3. 下一步行动 (Action Plan)

为了实现真正的“工业级多租户”，我建议立即启动一轮 **RLS 补丁冲刺**，对上述三大盲区（工单、生物资产、库存批次）的 ir.rule 进行精准注入。
只有当这些表也披上装甲后，这个三级权限网才真正称得上是“滴水不漏”。
