# EPIC-136: WIP Shelf-Life Degradation (在制品动态保质期损耗)

## 1. 业务背景 (Context)
在鲜切沙拉或果汁等高敏生鲜加工中，原料（如剥皮的苹果）一旦脱离冷库进入常温车间，其理化活性就开始急速衰减。目前 Odoo 仅支持最终产成品的保质期推算，无法捕捉半成品在车间（Workcenter）滞留带来的“寿命折损”。

## 2. 核心目标 (Objectives)
* 将车间滞留时间 (Lead Time) 与车间温度 (IoT) 引入保质期衰减公式。
* 动态折算最终产成品的真实保质期 (Dynamic Expiration Date)。
* 在车间发生堵塞时，触发超温/超时报废熔断。

## 3. 用户故事与验收标准 (User Stories & Acceptance Criteria)

### US-136-01: 捕获车间温时积分 (Capture WIP TTI)
**As a** 生产数据架构师 (Data Architect)
**I want to** 记录半成品(WIP)在车间的精确暴露时间与环境温度
**So that** 系统能够拥有计算产品真实折寿的数据基础。

*   **AC1 (时间与温度戳)**:
    *   **Given** 一个处理鲜切蔬菜的工单 (Workorder)
    *   **When** 工人点击 `Start` 然后在 3 小时后点击 `Done`
    *   **Then** 系统不仅记录下 Duration (3小时)，还通过 API 从该工作中心的 IoT 网关抓取这 3 小时内的平均环境温度（如 25°C），并记录在工单日志中。

### US-136-02: 动态扣减最终保质期 (Dynamic Expiration Penalty)
**As a** 质控合规总监 (Quality Assurance Director)
**I want to** 系统根据车间暴露的 TTI 自动扣减产成品的保质期
**So that** 发往超市的生鲜食品绝对安全，不会因为车间堵塞而导致货架期虚高。

*   **AC1 (触发惩罚机制)**:
    *   **Given** 产品的标准保质期为 7 天 (168小时)
    *   **When** Odoo 侦测到其加工工单在 > 20°C 的环境中持续了 4 个小时（超出 1小时容差）
    *   **Then** 在最终生产出成品批次 (`stock.lot`) 时，系统自动将其 `expiration_date` (过期时间) 从计算基准中扣除 48 小时（基于 TTI 衰减公式），并备注“加工滞留折寿”。

### US-136-03: 车间堵塞熔断预警 (WIP Exposure Dashboard Alerts)
**As a** 车间班长 (Floor Supervisor)
**I want to** 在大屏上看清哪些半成品快要“暴露超时”了
**So that** 我能立即干预，把它们送回冷库或优先加工。

*   **AC1 (车间红绿灯)**:
    *   **Given** 正在执行的制造订单看板 (MRP Dashboard)
    *   **When** 某个在制品的停留时间达到衰减阈值的 80%
    *   **Then** 该卡片变为闪烁的橙色，并在达到 100% 时变为红色且触发车间警报音。

## 4. 架构影响 (Architecture Impact)
* **核心模型**: mrp.workorder, stock.lot
* **交互点**: 记录 workorder 的实际执行时长，结合工位的温度设定，在 production 结束生成成品 lot 时，拦截并重写 expiration_date 计算逻辑。
