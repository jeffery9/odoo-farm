# EPIC 047:IoT 边缘协调与主动控制 (Edge Orchestration & Active Control)
*版本: V1.1 | 状态: ACTIVE | 归口: farm_iot*

## 1. 核心愿景 (Core Vision)
构建农场的“神经肌肉系统”。通过实现 Odoo 控制配方与 MQTT 执行器的双向同步，确保生产指令能够秒级下发至物理设备。

## 2. 三层解耦架构职责 (Three-Tier Architecture Roles)

### 2.1 底层通讯框架 (agri_iot)
- **定位**: 物理世界的驱动程序。
- **职责**: 负责 MQTT Topic 的维护、设备心跳监控及原始数据报文的转发。作为 I/O 通道，不包含任何业务逻辑。

### 2.2 管理中心 (farm_iot)
- **定位**: 全局物联资产配置与审计中心。
- **职责**: 维护数字孪生模型、全局设备映射配置。记录管理类指令的通用审计日志 `farm.command.log`，不直接干预生产逻辑。

### 2.3 配方边缘 (precision_production_iot)
- **定位**: 生产执行层的“战术大脑”。
- **职责**: 专门负责 ISA-88 配方参数的边缘下发。独立于管理中心，直接调用 `agri_iot` 框架，并保存带 MO/Phase 上下文的专用审计日志 `precision.iot.command.log`。

---

## 3. 用户故事集 (User Stories)

### **[US-047-01] 执行器端点定义 (Actuator Endpoints)**
- **描述**: 作为自动化工程师，我希望定义控制配方参数与 MQTT Topic 的映射关系。
- **验收标准 (AC)**:
    - **(Center)** 支持在 `iot.device.mapping` 中定义 `direction` (Inbound/Outbound)。
    - **(Edge)** 支持 JSON Payload Template 定义，如 `{'setpoint': {{value}} }`。
    *   **验收标准 (Acceptance Criteria)**:
        *   **AC1 (界面与交互)**: 用户界面必须清晰展示【执行器端点定义 (Actuator Endpoints)】的核心字段和操作按钮，且响应式兼容移动端访问。
        *   **AC2 (业务流转)**: 核心状态机（State Machine）的流转必须准确无误，确保模块间集成的边界数据一致性。
        *   **AC3 (权限控制)**: 只有具备对应权限组（如 Specialist/Manager）的角色才能执行该业务的写操作或状态确认。


### **[US-047-02] 双向设定点绑定 (Bi-directional Setpoint Binding)**
- **描述**: 作为工艺员，当我修改执行配方 (Recipe) 的 Target Value 时，系统自动下发 MQTT 指令更新设备。
- **验收标准 (AC)**:
    - **(Edge)** 监听 `precision.recipe.parameter` 的变更，调用 `agri_iot` 的下发接口。
    - **(Hardware)** 自动记录生产专用审计日志，实现 Level 2 溯源。
    *   **验收标准 (Acceptance Criteria)**:
        *   **AC1 (界面与交互)**: 用户界面必须清晰展示【双向设定点绑定 (Bi-directional Setpoint Binding)】的核心字段和操作按钮，且响应式兼容移动端访问。
        *   **AC2 (业务流转)**: 核心状态机（State Machine）的流转必须准确无误，确保模块间集成的边界数据一致性。
        *   **AC3 (权限控制)**: 只有具备对应权限组（如 Specialist/Manager）的角色才能执行该业务的写操作或状态确认。


### **[US-047-03] 边缘自律与指令存证 (Edge Autonomy & Audit)**
- **描述**: 作为安全主管，我希望记录每一条控制指令的反馈状态。
- **验收标准 (AC)**:
    - **(Evidence)** 每一条指令记录生命周期：Dispatched -> ACK -> Success/Failed。
    - **(Traceability)** 日志必须关联 MO 和 Phase。

---
*V1.1 - Decoupled Architecture Finalized | 2026-02-02*
    *   **验收标准 (Acceptance Criteria)**:
        *   **AC1 (界面与交互)**: 用户界面必须清晰展示【边缘自律与指令存证 (Edge Autonomy & Audit)】的核心字段和操作按钮，且响应式兼容移动端访问。
        *   **AC2 (业务流转)**: 核心状态机（State Machine）的流转必须准确无误，确保模块间集成的边界数据一致性。
        *   **AC3 (权限控制)**: 只有具备对应权限组（如 Specialist/Manager）的角色才能执行该业务的写操作或状态确认。

