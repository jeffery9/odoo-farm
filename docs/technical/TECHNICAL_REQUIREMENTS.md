# Odoo 19 农场管理系统：技术架构与算法标准登记 (Technical Requirements)

本文档定义了支撑“从田间到餐桌”全链路数字化底座的核心技术规范。

---

## 🏆 [ARCH-ISL]：行业专业化层架构 (Industry Specialized Layer)
**核心决策**：系统采用 **委托继承 (Delegation Inheritance - `_inherits`)** 模式构建多行业底座。

### [US-ISL-01]：底座委托机制
- **逻辑**：针对差异巨大的行业模型（BOM, MO, Lot, Picking），建立“父子表”结构。
- **物理实现**：`livestock.bom` -> `mrp.bom`。行业表只存私有字段，基础表存通用字段。
- **价值**：物理分表，彻底隔离行业数据，同时保留 Odoo 标准的库存与财务兼容性。

### [US-ISL-02]：Mixin 逻辑下沉与通用算法
- **需求**：将跨行业共用的农业逻辑（稀释比、面积计算、质量门控状态机）提取至 `farm.agri.mixin`。

---

## 🟣 [EPIC-TECH-05]：跨行业模型逻辑隔离与数据沙箱
**目标**：确保公共模型在多行业并存时，记录不交叉、逻辑不冲突、界面不冗余。

### [US-TECH-05-01] 动作级记录隔离 (Action-level Isolation) ✅ 已完成
- **描述**：在不同行业 App 的菜单 Action 中注入硬性 Domain（如 `industry_type='livestock'`）。

### [US-TECH-05-02] 搜索域动态适配 (Dynamic Domain Filtering) ✅ 已完成
- **描述**：重载 Many2one 字段的 `domain`，使其根据父记录的行业属性动态过滤可选记录。

### [US-TECH-05-03] 行业感知算法路由 ✅ 已完成
- **描述**：确保特定算法（如 FCR、NPK 换算）仅在符合行业标识的记录上执行。

### [US-TECH-05-04] 行业专属库存序列 (Picking Isolation) ✅ 已完成
- **描述**：根据 MO 行业属性动态选择 Picking Type。地头收获关联 HRV 序列，工业加工关联 PROD 序列。

### [US-TECH-05-05] 智能按钮动态上下文 (Smart Button Contextualization) ✅ 已完成
- **描述**：产品表单的 Smart Buttons（BOM, MO, 健康记录）根据行业开关（is_agri_material 等）动态显隐。

### [US-TECH-05-06] 计量单位行业强制约束 (UoM Enforcement) ✅ 已完成
- **描述**：建立“行业-UoM分类”映射，禁止在养殖行业误用面积单位等跨分类错误。

### [US-TECH-05-07] 跨模块数据沙箱 (Data Sandbox) ✅ 已完成
- **描述**：在 Stock Move 中注入 industry_context 标签，辅助财务实现资产价值的行业分类核算。

### [US-TECH-05-08] 工作中心能力隔离 ✅ 已完成
- **描述**：按行业类型过滤可用工作中心，防止加工设备出现在农机作业选项中。

---

## 🟢 [EPIC-IOT]：农业物联网与自动化采集
**目标**：实现物理设备信号到业务指标的异步自动化转换。

### [US-IOT-01]：通用设备映射协议 (Generic Device Mapper) ✅ 已完成
- **描述**：通过 `iot.device.mapping` 模型定义“MQTT Topic -> 业务字段”的映射。

### [US-TECH-03-02] 遥测数据异步处理引擎 ✅ 已完成
- **描述**：通过 `iot.telemetry.buffer` 承载高频数据，利用 Cron 任务异步回填 MO 能耗记录。

---

## 🔵 [EPIC-GIS]：农业空间智能与位置感知
**目标**：将地块升级为具备空间特征的资产。

### [US-GIS-01]：GeoJSON 边界与面积精算 ✅ 已完成
- **算法**：采用 **Shoelace Formula (鞋带公式)**，根据地块经纬度多边形坐标自动计算实际公顷数。

### [US-GIS-02]：空间批次关联 (Spatial Assignment) ✅ 已完成
- **算法**：基于 **Ray-casting (射线法)**，根据资产 GPS 坐标实时判断并自动更新其所属地块（Location）。

### [GIS-VAL] 生产面积空间校验 ✅ 已完成
- **描述**：在 MO 确认时，强制比对“申报面积”与“地块物理面积”。

---

## 📚 架构历史与决策日志 (Decision Archive)

| 日期 | 决策项 | 选型 | 说明 |
| :--- | :--- | :--- | :--- |
| 2026-01-15 | 模型继承模式 | **委托继承** | 优于“原型继承”或“单一共享表”。 |
| 2026-01-15 | UI 适配策略 | **独立视图** | 彻底摒弃在原生视图中使用臃肿的 invisible 逻辑。 |
| 2026-01-15 | 逻辑复用方式 | **Mixin 模式** | 确保算法代码的一致性与可复用性。 |
