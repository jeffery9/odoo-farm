# 史诗 203：IoT 边缘协调与主动控制 (Edge Orchestration & Active Control)
*版本: V1.0 | 状态: DRAFT | 归口: farm_edge_orchestrator*

## 1. 核心愿景 (Core Vision)
构建农场的“神经肌肉系统”。通过实现 Odoo 控制配方与 MQTT 执行器的双向同步，确保生产指令能够秒级下发至物理设备。同时赋予边缘设备一定的自律能力，在离线状态下仍能维持环境参数在科学红线内。

---

## 2. 用户故事集 (User Stories)

### **[US-203-01] 执行器端点定义 (Actuator Endpoints)**
- **描述**: 作为自动化工程师，我希望定义控制配方参数与 MQTT Topic 的映射关系，以便指令能精准送达。
- **验收标准 (AC)**:
    - **(IOT)** 支持定义 `iiot.actuator.endpoint`，包含：控制主题 (Command Topic)、消息模板 (Payload Template) 及响应主题。
    - **(Odoo Mapping)** 端点必须与 `agri.physiology.profile` 中的参数名建立逻辑绑定。

### **[US-203-02] 双向设定点绑定 (Bi-directional Setpoint Binding)**
- **描述**: 作为工艺员，当我修改执行配方 (Recipe) 的 Target Value 时，我希望系统自动下发 MQTT 指令更新设备。
- **验收标准 (AC)**:
    - **(Logic)** 监听 `precision.recipe.parameter` 的 `write` 方法。
    - **(Hardware)** 当 Target 变更且满足安全红线时，自动调用 `agri_iot` 的 `send_command` 方法。

### **[US-203-03] 边缘自律与指令存证 (Edge Autonomy & Audit)**
- **描述**: 作为安全主管，我希望记录每一条控制指令的反馈状态（已接收、执行中、已完成、失败）。
- **验收标准 (AC)**:
    - **(Level 2 Evidence)** 每一条下控指令必须产生一条 `iiot.command.log`，并关联 `precision.intervention.basis`。
    - **(Logic)** 实现“控制闭环”检查：如果执行器在 30s 内未返回 ACK，系统触发“控制失效”警报并记录在生产绩效中。

---

## 3. 核心技术架构 (Architecture)
- **指令协议**: 基于 MQTT JSON Payload。
- **依赖模块**: `agri_iot`, `precision_production`, `farm_operation`。

---
*V1.0 - Active Control Foundation | 2026-02-01*
