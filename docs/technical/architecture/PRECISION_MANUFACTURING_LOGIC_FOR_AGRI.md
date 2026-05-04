# 🏭 精密制造逻辑下的农业建模规格 (Precision Manufacturing Logic for Agri)

**版本**: V1.0  
**日期**: 2026-02-01  
**核心思维**: 将农业视为“露天的精密晶圆厂”，利用半导体工业逻辑应对农业生产的动态性与不确定性。

---

## 1. 核心范式：从“固定得率”到“动态分选”

在传统工业中，合格品是二元的（Pass/Fail）。但在半导体与农业中，产出是**多维度的等级分布**。

### **A. Binning (性能分箱) vs. Grading (品质分级)**
*   **半导体逻辑**：同一批晶圆由于物理波动，会被分选为 i9, i7, i5 等不同等级。
*   **农业逻辑**：同一批次采收，由于微环境差异，产出特级、一级、二级或次品。
*   **系统实现**：
    *   **ISL 代理**：通过 `stock.lot` 的行业代理（如 `farm.lot.grape`）持有品质指纹。
    *   **多产出指令**：`mrp.production` 代理模型支持在单次 Done 动作中产生多个不同 Grade 的批次。
    *   **价值挂钩**：`AgriBiologicalValuationMixin` 根据分级结果自动触发公允价值溢价或减值。

### **B. Yield Ramp (良率爬坡) vs. Biological Efficiency (生物转化率)**
*   **半导体逻辑**：通过不断调整工艺参数，使良率从 30% 提升至 90%。
*   **农业逻辑**：通过精准干预，提高 FCR (料肉比) 或 BE (生物转化率)。
*   **系统实现**：
    *   **动态采样**：利用 `AgriBiologicalInventoryMixin` 的 `action_record_sampling` 方法，在中途动态修正预期产量。
    *   **偏差分析**：系统对比“理论配方 (Recipe)”与“实际产出 (Yield)”，识别环境干扰因子。

---

## 2. 工艺控制：从“线性步序”到“动态干预”

农业生产的“步骤”较少，但每个步骤的“控制深度”极高，且时间窗口随生物反馈动态移动。

### **A. APC (先进工艺控制) vs. Dynamic Intervention (动态干预)**
*   **半导体逻辑**：实时监控光刻参数，发现漂移立即闭环补偿。
*   **农业逻辑**：实时监控溶氧、光照或品温，发现异常立即触发“补偿技能”。
*   **系统实现**：
    *   **防御机制**：实现 `handle_telemetry` 方法（类似 `on_damaged` 风格），将 IoT 压力直接转化为业务动作。
    *   **Skill 注入**：`AgriAgentInstructionMixin` (Level 4 DNA) 将专家的补偿策略转化为 JSON 指令下达给执行器。

### **B. Metrology (在线测量) vs. Physiological Monitoring (生理监测)**
*   **半导体逻辑**：每一道刻蚀后都进行测量，以决定下一道工序的参数。
*   **农业逻辑**：基于积温 (GDD) 监测生理阶段，以决定施肥或采收的时机。
*   **系统实现**：
    *   **积温驱动**：`AgriGrowthCycleMixin` 充当了“生物计时器”，它不是基于日历排程，而是基于“生物生理进度”排程。

---

## 3. 跨行业映射汇总 (Cross-Industry Mapping)

| 概念 | 半导体制造 (Semiconductor) | 我们的农业实现 (Agri-Dev) | 驱动 Mixin / 机制 |
| :--- | :--- | :--- | :--- |
| **批次载体** | Wafer ID (晶圆 ID) | **Biological Lot (生物批次)** | `stock.lot` 代理 |
| **分选逻辑** | Speed Binning | **Quality Grading** | `AgriQualityGateMixin` |
| **不确定性** | Yield Fluctuation | **Biological Uncertainty** | `AgriBiologicalInventory` |
| **实时闭环** | Run-to-Run Control | **On Telemetry Feedback** | `AgriAgentInstruction` |
| **溯源指纹** | Wafer Map | **Quality Fingerprint** | `AgriTraceabilityMixin` |

---

## 4. 开发者实施律令

1.  **禁止硬编码产量**：所有产量预测必须基于 `AgriBiologicalInventoryMixin` 的动态校准接口。
2.  **强制品质分级**：所有采收/加工产出模型必须实现 `Quality Gate`，且产出 Lot 必须持有等级指纹。
3.  **反馈优先**：逻辑实现应优先考虑“感知后的动作触发（On Telemetry）”，而非静态的状态字段。

---
*最后更新：2026-02-01*
