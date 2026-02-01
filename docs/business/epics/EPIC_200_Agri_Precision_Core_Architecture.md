# EPIC 200: 农业精准制造桥接核心 (Agri-Precision Bridge Core)
*版本: V1.0 | 日期: 2026-02-01*

## 1. 核心愿景 (Core Vision)
`agri_precision_core` 模块是精密制造与标准 ERP 之间的关键桥梁。通过提供抽象层，该模块使标准的 Odoo MRP/Stock 模块能够处理农业与半导体行业特有的"不确定性、分级、干预"三大挑战。

---

## 2. 模块架构 (Module Architecture)

### **[AGRI-001] Mixin 抽象层 (Mixin Abstraction Layer)**
*   **组件**: `agri.precision.mixin`
*   **职责**:
    1.  **不确定性处理**: 动态产量跟踪 (`expected_yield_accuracy`, `last_metrology_date`)
    2.  **分级管理**: 产品分级 (`quality_grade` - Premium/Standard/Substandard)
    3.  **干预机制**: 技能钩子 (`intervention_count`, `is_critical_status`)
    4.  **IoT 集成**: 传感器设备关联 (`iot_device_ids`, `iot_status`)

### **[AGRI-002] 标准应用桥接 (Standard App Bridge)**
*   **组件**: `odoo_app_bridge.py`
*   **职责**:
    1.  **MRP 继承**: 扩展 `mrp.production` 添加精准制造属性
    2.  **Stock 继承**: 扩展 `stock.lot` 添加分级功能
    3.  **Phase 继承**: 扩展 `precision.recipe.phase` 添加相位级干预逻辑
    4.  **集成接口**: 提供与 `precision_production` 模块的无缝集成

### **[AGRI-003] 用户界面桥接 (UI Bridge)**
*   **组件**: `precision_bridge_views.xml`
*   **职责**:
    1.  **表单继承**: 在标准表单中注入精准制造字段
    2.  **状态指示**: IoT 状态和干预计数显示
    3.  **操作按钮**: 快速干预和校准功能
    4.  **监控页面**: IoT 监控专用标签页

---

## 3. 核心功能规格 (Core Features)

### **[US-AGRI-01] 不确定性处理 (Uncertainty Handling)**
*   **目标**: 农业/半导体生产过程本质上具有不确定性，需要动态跟踪产量预期
*   **实现**:
    - `expected_yield_accuracy` (产量信心百分比)
    - `last_metrology_date` (最后校准/采样时间)
    - 动态校准功能: `action_update_yield_estimate()`

### **[US-AGRI-02] 产品分级 (Product Grading)**
*   **目标**: 生产结果需要按质量分级，支持财务核算
*   **实现**:
    - `quality_grade` 三元分级系统 (Premium/Standard/Substandard)
    - 与 `stock.lot` 集成，每个批次携带分级结果
    - UI 丝带显示 (Premium 绿色，Substandard 红色)

### **[US-AGRI-03] 干预机制 (Intervention Mechanism)**
*   **目标**: 提供人工和自动干预能力，应对生产过程中的变化
*   **实现**:
    - `intervention_count` (干预循环计数)
    - `is_critical_status` (关键状态标记)
    - `action_apply_corrective_skill()` (纠正技能应用)
    - 与 `precision.intervention` 模块集成

### **[US-AGRI-04] IoT 集成桥接 (IoT Integration Bridge)**
*   **目标**: 将工业物联网传感器数据与精准制造逻辑结合
*   **实现**:
    - `iot_device_ids` (IoT 设备关联)
    - `iot_status` (IoT 状态监控)
    - `action_trigger_iot_based_intervention()` (基于传感器的自动干预)
    - 与 `precision.iot.*` 模块深度集成

### **[US-AGRI-05] 跨模块集成 (Cross-Module Integration)**
*   **目标**: 在不修改标准模块的前提下扩展功能
*   **实现**:
    - 使用 `_inherit` 机制扩展标准模型
    - 保持标准业务逻辑完整性
    - 提供农业/半导体专用术语映射

---

## 4. 设计模式 (Design Patterns)

### **[PATTERN-AGRI-01] Mixin 驱动架构 (Mixin-Driven Architecture)**
- 通过 `agri.precision.mixin` 实现代码复用
- 遵活地将精准制造功能注入不同模型
- 遵活性和可测试性

### **[PATTERN-AGRI-02] 桥接模式 (Bridge Pattern)**
- 解耦标准 ERP 功能与行业特定逻辑
- 保持标准模块的纯净性
- 提供无缝集成体验

### **[PATTERN-AGRI-03] 事件驱动干预 (Event-Driven Intervention)**
- 基于传感器数据的自动干预
- 手动干预能力保留
- 与现有干预系统兼容

---

## 5. 集成接口 (Integration Interfaces)

### **[INTERFACE-AGRI-01] 与 precision_production 集成**
- `mrp.production` 继承 `precision.recipe.phase` 继承
- `precision.intervention` 创建与管理
- 产量信心与效率指数同步

### **[INTERFACE-AGRI-02] 与 precision_production_iot 集成**
- `precision.iot.device`、`precision.iot.sensor`、`precision.iot.reading` 关联
- 传感器数据驱动的干预逻辑
- 实时状态监控

### **[INTERFACE-AGRI-03] 与 agri_iot 集成**
- 依赖 `agri_iot` 模块提供底层物联网通信能力
- 通过 `agri.iot.device` 模型访问工业物联网设备
- 支持 MQTT、HTTP 等多种通信协议
- 提供设备管理、遥测数据处理、指令下发功能

### **[INTERFACE-AGRI-04] 标准 Odoo 模块兼容**
- 与 `mrp`、`stock` 模块原生兼容
- 继承机制保持标准功能
- 用户界面无缝融合

---

## 6. 技术架构 (Technical Architecture)

```
┌─────────────────┐    ┌─────────────────────┐    ┌─────────────────────┐
│   Standard      │    │  Agri-Precision     │    │  Industry Specific  │
│   Odoo Apps     │◄──►│     Core (Mixin)    │◄──►│   Precision Logic   │
│  (MRP, Stock)   │    │(_inherit mechanism) │    │(Agriculture/Semi)   │
└─────────────────┘    └─────────────────────┘    └─────────────────────┘
                              │
                              ▼
                    ┌─────────────────────┐
                    │   UI Integration    │
                    │ (Forms, Buttons,    │
                    │  Dashboards, etc.)  │
                    └─────────────────────┘
```

---

*最后更新：2026-02-01 (V1.0 - Bridge Core 定型版)*