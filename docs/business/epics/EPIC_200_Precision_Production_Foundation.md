# 史诗 200：精密生产执行基座 (Precision Production Foundation)
*版本: V1.5 (Final Implementation) | 日期: 2026-02-01*

## 1. 核心愿景 (Core Vision)
为具有"过程不可逆、结果概率分布、环境高度敏感"特征的行业，提供一套基于 **ISA-88 (S88)** 国际标准的精密执行引擎。本模块通过从"物料驱动"到"配方/参数驱动"的范式转移，实现了物理现实与数字孪生的深度对齐。

---

## 2. 核心功能规格 (Final Specifications)

### **[US-200-01] 驱动模式与架构解耦 (Drive Mode)**
*   **状态**：DONE
*   **功能**：提供 `material` 与 `parameter` 驱动模式切换。精密模式下，MO 激活"驾驶舱"交互界面。

### **[US-200-02] ISA-88 配方实例化 (Recipe Instantiation)**
*   **状态**：DONE
*   **功能**：实现了 **Master Recipe (主配方)** 与 **Control Recipe (执行配方)** 的分离。
*   **批次缩放 (Batch Scaling)**：支持基于 `Batch Size` 的定额缩放。只有标记为 `is_scalable` 的参数和物料随生产规模自动调整，物理常量（如温度）保持恒定。

### **[US-200-03] 相位自治与并行执行 (Phase Autonomy & Parallelism)**
*   **状态**：DONE
*   **功能**：
    1.  **独立计时**：相位拥有独立的启动/完成生命周期，不强制线性顺序。
    2.  **跨批次聚合**：支持在 `Phase Execution Board` 中跨 MO 批量操作相同相位的样本（如：生物样本并行培养）。
    3.  **原子化交易**：库存核销精确绑定在相位完成时刻。

### **[US-200-04] 过程控制 (SPC) 与执行锁闭 (Process Hold)**
*   **状态**：DONE
*   **功能**：
    1.  **稳定性分级**：根据检测偏差自动分级：`Stable`, `Drifting`, `Out of Control`。
    2.  **安全锁闭**：当临界偏差发生时，自动触发 **Execution Hold**，强制拦截所有后续物理操作。

### **[US-200-05] 自适应主动纠偏 (Active Adaptation)**
*   **状态**：DONE
*   **功能**：系统分析实测数据，自动执行 **三维补偿**：
    1.  **参数补偿**：修改设定点。
    2.  **时长补偿**：动态伸缩执行时间。
    3.  **物料补偿**：按比例缩放试剂投入。

### **[US-200-06] 绩效量化 (Performance Management)**
*   **状态**：DONE
*   **功能**：
    1.  **时效指数 (Efficiency Index)**：计划 vs 实际时长的实时比值。
    2.  **质量指数 (Quality Score)**：基于原生副产品分级结果的财务加权得分。

### **[US-200-07] 财务级产出核销 (Native By-product Grading)**
*   **状态**：DONE
*   **功能**：分级产出通过 Odoo 原生副产品（By-products）功能实现，确保成本分摊与会计准则完美兼容。

### **[US-200-08] 工业物联网 (IIoT) 集成与自动数据采集 (Industrial IoT Integration & Auto Data Capture)**
*   **状态**：DONE
*   **功能**：
    1.  **IIoT 桥接**：与 `agri_iot` 模块集成，支持多种通信协议（MQTT、HTTP、Modbus 等）。
    2.  **自动数据采集**：通过 `precision.iot.device`、`precision.iot.sensor`、`precision.iot.reading` 三个核心模型实现自动测量数据采集。
    3.  **实时控制**：支持向 IoT 设备发送控制命令（设置点、启动/停止相位、校准、紧急停止等）。
    4.  **偏差检测与干预**：自动检测测量值与目标值的偏差，触发干预措施或生产锁定。
    5.  **命令日志**：完整记录所有发送到设备的命令和响应状态。

### **[US-200-09] 农业精准制造桥接 (Agri-Precision Bridge)**
*   **状态**：DONE
*   **功能**：
    1.  **桥接架构**：`agri_precision_core` 模块作为标准 Odoo 应用与农业/半导体精密制造逻辑之间的桥梁。
    2.  **不确定性处理**：通过 `agri.precision.mixin` 处理生产过程中的不确定性，包括动态产量跟踪。
    3.  **分级与品质管理**：实现产品分级功能，支持 Premium/Standard/Substandard 等级。
    4.  **干预机制**：提供干预钩子，支持手动和自动干预（基于传感器读数）。
    5.  **IoT 集成桥接**：将 IoT 传感器数据与农业精密制造逻辑结合，实现环境监测与自动干预。
    6.  **跨模块集成**：在 MRP 生产订单和库存批次中集成精准制造属性，提供统一的用户界面。
    7.  **Agri-IoT 依赖**：依赖 `agri_iot` 模块提供底层物联网通信与设备管理能力。

---

## 3. 设计律令 (The Mandates)
1.  **无损修改 (Lossless Mode)**：任何后续迭代必须保证架构注释与逻辑闭环的完整性。
2.  **ISA-88 术语对齐**：代码与文档必须严格区分 Master 与 Control 实体。
3.  **去工业化 UX**：界面应以"任务"和"状态"为中心，而非原始数据。
4.  **IIoT 集成**：所有相位和传感器数据必须支持实时采集和控制，实现精确制造闭环。

---

*最后更新：2026-02-01 (V2.0 - IoT 增强版)*