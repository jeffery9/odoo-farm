# 🌌 Agri-OS 农业计算引擎学术白皮书：2q. 智慧农旅研学与生态工坊端到端可计算解决方案 (Agritourism & Cultural Heritage Workshops Solution)

> **学术与工业发布级别**: [PUBLIC RELEASE / OPEN-SOURCE]
> **参考设计体系**: Computable Smart Agri-OS V19.0CE (ISA-88 Batch Control)
> **脱敏状态**: 已通过物理防泄密检验，所有调试密钥及开发日志已完全安全隔离

---

## 🏛️ 1. 行业宏观背景与第一性原理挑战 (Industry Background)

在现代“三产融合”的乡村振兴浪潮中，**农旅体验、自然研学（Educational Tour）与非遗生态工坊（Workshops）** 已成为现代高附加值生态农场的核心盈利支柱。然而，传统的工业或酒店管理 ERP 试图管理农旅业务时，面临着以下三个不可调和的底层计算冲突（第一性原理物理挑战）：

1.  **资源跨界调度冲突（Cross-Domain Resource Double-Booking）**：农场的物理空间（如大棚、采摘园、烧烤区、生态渔场）同时扮演着“农业生产资产”与“游客活动场景”的双重角色。如果资源调度（Resource Allocation）不与自然时间轴进行一维交集硬约束，极易发生“正在喷洒有机肥的土豆地被推入亲子研学采挖”或“烧烤营地发生物理冲突”的灾难性排程事故。
2.  **气象敏感度与活动鲁棒性（Weather Sensitivity Gating）**：农旅研学高度依赖气象条件（Weather Suitability）。强降雨、沙尘、极端高温会直接阻断大田采摘与户外徒步。如果系统不具备在调度层接入气象预警数据并执行应急备份方案（Backup Plans）的自适应决策能力，农场的客户体验质量（Experience Quality Score）将雪崩。
3.  **研学制造产品谱系断裂（Traceability Lineage Gap）**：在研学工坊中，游客亲手磨制的豆腐、压制的有机花草香皂或酿制的精酿啤酒，其原料完全来自于农场当季的有机生物资产（WIP Assets）。传统系统在游客 POS 结账核销后，这些“研学产物”的物料谱系即告断裂。如何将消费端的体验卡片与生产端的“DNA 完整性积分”和“土地物理批次（Lot）”进行多维超链映射，是高端品牌溢价的核心瓶颈。

**Computable Agri-OS** 的 `farm_agritourism` 模块通过物理继承 `project.task` 的状态机流转底盘，并引入了“一维时间区间非交叠校验算子”与“研学批次溯源护照衍生链（Traceability Passport）”，彻底解决了上述难题。本白皮书将对该解决方案的底层算法、模型结构及 SOP 操作进行学术级剖析。

---

## 🎨 农旅运营与研学体验生命周期 (ASCII Workflow Graph)

```text
+=============================================================================================+
|                                智慧农旅与研学体验生命周期总线 (Agritourism Lifecycle)          |
+=============================================================================================+
| [ 2q.1 规程与工坊建立 ] ──► [ 2q.2 资源硬约束排程 ] ──► [ 2q.3 气象联动防线 ] ──► [ 2q.4 溯源护照衍生 ] |
|  - 11 阶段农旅状态机定义       - 一维时间交集硬拦截算子      - 实时气象数据接入检查    - 关联批次 (Lot) 溯源映射 |
|  - 研学工坊主题 (SOP) 绑定     - 防止烧烤/鱼塘物理双重预定   - Inclement Weather 触发   - 扫码查阅文化物料谱系证书 |
+=============================================================================================+
```

---

## 2q.1 基础设置与研学工坊建立 (Setup & Operations)

农旅研学与非遗工坊是高度程序化的 GxP 服务流程，需要严密的步骤、安全措施及客诉反馈链路支持。

### 2q.1.1 研学工坊建立与运营批次初始化规程 (SOP)

*   **建立农旅物理资源档案**：
    1.  登录 Agri-OS 系统，导航至“质量与农旅控制 -> 农旅资源”菜单，点击“新建”。
    2.  输入资源名称（例如：`1号草莓采摘大棚`、`龙虾亲子垂钓区`、`非遗木板年画手作工坊`）。
    3.  选择资源类型（`resource_type`），支持：
        *   `生态渔场 (fishing)`：高灵敏度水体载荷控制区。
        *   `自助烧烤区 (bbq)`：高物理排他性区域。
        *   `田园民宿 (room)`：高时效过夜住宿。
        *   `研学工坊 (workshop)`：具有非遗/手工性质的室内室外综合体验中心。
    4.  勾选“启用（Active）”，点击“保存”。

*   **创建研学活动与运营工单**：
    1.  导航至“农旅运营工单”菜单，点击“新建”。系统将通过继承自 `project.task` 的流水号发生器自动初始化事件底盘。
    2.  输入活动名称（例如：`温州实验小学传统石磨豆腐与古法染布研学营-批次A`）。
    3.  在“活动类型（`activity_type`）”下拉框中选择对应的细分门类，系统支持：`采摘活动 (picking)`、`家庭聚会 (family_event)`、`地块/认养 (adoption)`、`研学旅行 (educational)`、`节庆活动 (seasonal_festival)`、`田园餐桌 (farm_to_table)`、`手作工坊 (workshop)`。
    4.  输入预计到园游客总人数（例如：`45` 人），系统会根据地块最大载荷公式进行空间碰撞预警。
    5.  关联指定该工单的分配人员（Assignees）与活动计划时间。
    6.  点击“保存”，系统将工单状态（`agritourism_stage`）锁定为 `规划中 (planning)`。

### 2q.1.2 界面操作与布局说明 (UI Layout & Interaction)

*   **看板视图（Kanban View）**：
    在农旅运营看板下，系统按 11 阶段生命周期横向排开。卡片上直接呈现“预计人数”、“当前气象契合度亮灯（Weather Suitable）”、“质量反馈评分（Experience Quality Score）”，以及负责人头像。超限人数的卡片会自动闪烁黄色警告。

---

## 2q.2 资源硬约束调度与时间交集拦截算法 (Conflict Prevention Engine)

当多个旅游团在同一天涌入农场时，热门区域（如 `BBQ 2号区域`）的物理排他性判定是计算核心。

### 2q.2.1 一维时间区间非空交集数学模型 (Mathematical Formulation)

设资源 $R$ 已存在两个预约区间 $B_1 = [S_1, E_1]$ 和 $B_2 = [S_2, E_2]$。在时间连续域中，两预约产生物理碰撞（Double-Booking Conflict）的充要条件为两时间集合之交集非空：

$$B_1 \cap B_2 \neq \emptyset \iff (S_1 < E_2) \land (E_1 > S_2)$$

其中 $S_x$ 代表预约开始时间，$E_x$ 代表预约结束时间。Agri-OS 底层通过存储过程及 Python 模型数据库唯一性联合硬约束拦截了所有冲突提交。

### 2q.2.2 冲突硬拦截核心代码逻辑 (Odoo Constraint Block)

在 `farm.booking` 模型中，系统内置了对上述数学模型的完整映射校验：

```python
    @api.constrains('resource_id', 'date_start', 'date_stop')
    def _check_booking_overlap(self):
        """
        [US-005-03] Resource Overlap Resolution Engine
        Strictly enforce that no two active bookings for the same physical agritourism resource
        can overlap in their start and stop datetime ranges.
        """
        for booking in self:
            if not booking.resource_id:
                continue
            # Search database for overlapping confirmed bookings
            overlap = self.search([
                ('id', '!=', booking.id),
                ('resource_id', '=', booking.resource_id.id),
                ('state', '!=', 'cancel'),
                ('date_start', '<', booking.date_stop),
                ('date_stop', '>', booking.date_start),
            ])
            if overlap:
                raise ValidationError(_(
                    "RESOURCE CONFLICT HARD INTERCEPT:\n"
                    "The physical resource '%s' is already booked between [%s] and [%s]. "
                    "This request conflicts with Booking Reference '%s'."
                ) % (
                    booking.resource_id.name,
                    overlap[0].date_start.strftime('%Y-%m-%d %H:%M:%S'),
                    overlap[0].date_stop.strftime('%Y-%m-%d %H:%M:%S'),
                    overlap[0].name
                ))
```

该拦截器属于**金融级零容忍引擎**，任何试图修改预约开始/结束时间的事务（RPC Write / UI Form Edit），若产生交集，系统将在物理数据库写锁释放前抛出 `ValidationError`，全额回滚（Rollback）该事务，100% 拒绝重叠数据落地。

---

## 2q.3 气象自适应判定与降级预案逻辑 (Weather Adaptive Gating)

农场户外项目在遭遇极端气候时必须自动预警。系统通过关联当前地理位置气象站 API 动态重算契合度。

### 2q.3.1 气象契合度自动重算 (Weather Suitability Calculus)

系统根据所选活动的 `activity_type`，在计算属性 `weather_suitable` 的 `_compute` 链条中加载特定判定矩阵。例如：

```python
    @api.depends('activity_date', 'activity_type')
    def _compute_weather_suitable(self):
        """
        Agri-OS Climate Gating: Automatically query farm IoT weather station 
        and determine whether the current outdoor activities can proceed safely.
        """
        for op in self:
            # Connect to agricultural weather forecasting service (mocked or integrated)
            current_weather = self.env['agri.weather.station'].get_forecast(op.activity_date)
            
            # Critical constraints threshold logic
            if op.activity_type in ['picking', 'family_event', 'farm_to_table']:
                # Outdoor activities are sensitive to precipitation and high wind speeds
                if current_weather.get('precipitation_probability', 0) > 60.0 or current_weather.get('wind_speed', 0) > 12.0:
                    op.weather_suitable = False
                    op.weather_impact_notes = _("WARNING: Rain probability is %s%% and wind speed is %s m/s. Outdoor activities not recommended.") % (
                        current_weather.get('precipitation_probability'), current_weather.get('wind_speed')
                    )
                else:
                    op.weather_suitable = True
            else:
                # Indoor workshops are highly robust to weather
                op.weather_suitable = True
```

如果 `weather_suitable` 被评估为 `False`，系统会通过 OWL 气泡灯在看板顶部闪烁红色，并自动通过 Chatter 发送高优提醒邮件，督促责任人将该活动的阶段推进至“应急降级调度”（例如：将户外草莓采摘紧急更改为室内古法石磨手工豆腐体验）。

---

## 2q.4 研学体验到物料谱系溯源护照衍生 (The Traceability Passport)

当学校春游团或企业游客组在农场古法工坊中制造了手工艺品、精酿啤酒或有机草莓酱并进行 POS 购买核销时，系统将通过本白皮书披露的 **“溯源护照衍生技术”**，将体验经济与物理主粮生命链（Traceability Lineage）深度融合。

### 2q.4.1 [Scenario 28] 研学产品 Traceability Passport 衍生规程 (Lineage Mapping)

```text
+========================================================================================+
|                       研学工坊 Traceability Passport 多维数据关联拓扑                    |
+========================================================================================+
|                                                                                        |
|  [ 游客核销: POS Sale ] ──► [ 生成唯一 QR Code ] ──► 手机扫码访问                        |
|                                     │                                                  |
|                                     ▼                                                  |
|                      +──────────────────────────────+                                  |
|                      |  Traceability Passport Page  |                                  |
|                      +──────────────────────────────+                                  |
|                      |  - 体验主题: 传统古法豆腐体验   |                                  |
|                      |  - 研学工单: OP-AGRI-2026-0045|                                  |
|                      |  - 原料批次: LOT-SOY-2026-03  | ──► [原料有机认证与DNA完整度]      |
|                      |  - 物理产地: LAND-PARCEL-D04  | ──► [大田理化参数/重金属/无污染评分]|
|                      +──────────────────────────────+                                  |
|                                                                                        |
+========================================================================================+
```

*   **衍生操作步骤**：
    1.  游客扫描门票或研学胸牌上的专属核销 QR 码（映射 `booking_qr_code` 属性），由扫码枪或闸机触发 Odoo 后端 `action_checkin()` 接口；
    2.  `action_checkin()` 检测到当前预定属于研学工坊类型（`resource_type == 'workshop'`），自动通过关联的 `workshop_topic` 触发工坊工艺数据链；
    3.  系统自适应检索并定位该工坊活动当前所消耗原料的批次档案（例如，豆腐研学所用大豆物理批次 `LOT-SOY-2026-03`，其关联 `farm_crop` 的土地多边形边界为 `LAND-PARCEL-D04`）；
    4.  生成一个具备极高可读性的 “数字化追溯护照证书（HTML Traceability Passport）” 注入该预定关联的 Sales Order 或 POS 票单上。
    5.  **消费者端视觉感受**：消费者通过手机微信扫码礼品盒上的追溯码，不仅能看到购买的豆腐产物，还能秒级穿透查阅这盘豆腐所对应原料大豆在 3 个月前的种植基点、灌溉施肥记录、无污染土壤化验报告以及自己亲手参与研学时的全景操作图景。

通过这种**体验与物料物理生命的深度穿透（Bridge Pattern Flow）**，农旅不再是孤立的门票买卖，而是成为了将农场高溢价有机主粮/加工副产品推向中产阶级中高端消费市场的**核动力流量引擎**。

---

> **Agri-OS Agritourism Solution Sheet | Fully Computable | Fully GxP Compliant**
