# EPIC 108:高级VRA算法与生理决策融合 (Advanced VRA Algorithms & Physiological Fusion)
*目标：整合土壤、气象、无人机多源数据，并注入 [EPIC 045] 的生理钟与生长模型，实现基于第一性原理的精准变量决策。*

## 1. 基础架构层 (Infrastructure Layer)

### **[US-108-01] 土壤传感器数据实时集成 (Soil Sensor Data Integration)**：✅ 完成 (2026-02-02)
- **描述**: 作为农技员，我希望系统能实时集成土壤湿度、温度、养分传感器数据，用于VRA处方优化。
- **验收条件**:
    - **(IoT Integration)** 系统需支持主流土壤传感器协议（LoRaWAN, NB-IoT, WiFi）的数据采集。
    - **(Spatial Mapping)** 传感器数据必须与VRA网格单元自动匹配，实现空间定位。
    - **(Real-time Processing)** 实现传感器数据的实时处理和更新，确保处方图的时效性。
    *   **验收标准 (Acceptance Criteria)**:
        *   **AC1 (界面与交互)**: 用户界面必须清晰展示【土壤传感器数据实时集成 (Soil Sensor Data Integration)：✅ 完成 (2026-02-02)】的核心字段和操作按钮，且响应式兼容移动端访问。
        *   **AC2 (业务流转)**: 核心状态机（State Machine）的流转必须准确无误，确保模块间集成的边界数据一致性。
        *   **AC3 (权限控制)**: 只有具备对应权限组（如 Specialist/Manager）的角色才能执行该业务的写操作或状态确认。


### **[US-108-02] 气象数据动态调整 (Dynamic Weather Adjustment)**：✅ 完成 (2026-02-02)
- **描述**: 作为农场主，我希望VRA处方能根据短期天气预报动态调整，避免在降雨前施用。
- **验收条件**:
    - **(API Integration)** 集成权威气象预报API，获取3-7天的高精度预报数据。
    - **(Conditional Logic)** 根据降雨概率、风速、温度等条件自动调整处方执行策略。
    - **(Notification)** 提供天气风险预警，建议最佳施用时间窗口。
    *   **验收标准 (Acceptance Criteria)**:
        *   **AC1 (界面与交互)**: 用户界面必须清晰展示【气象数据动态调整 (Dynamic Weather Adjustment)：✅ 完成 (2026-02-02)】的核心字段和操作按钮，且响应式兼容移动端访问。
        *   **AC2 (业务流转)**: 核心状态机（State Machine）的流转必须准确无误，确保模块间集成的边界数据一致性。
        *   **AC3 (权限控制)**: 只有具备对应权限组（如 Specialist/Manager）的角色才能执行该业务的写操作或状态确认。


### **[US-108-03] 无人机多光谱数据融合 (UAV Multispectral Data Fusion)**：✅ 完成 (2026-02-02)
- **描述**: 作为技术员，我希望将无人机获取的高分辨率多光谱数据与卫星NDVI结合，提升局部区域精度。
- **验收条件**:
    - **(Image Processing)** 支持无人机多光谱图像的自动处理 and NDVI计算。
    - **(Data Fusion)** 实现高分辨率无人机数据与低分辨率卫星数据的智能融合算法。
    - **(Anomaly Detection)** 自动识别田间异常区域并生成重点关注处方。
    *   **验收标准 (Acceptance Criteria)**:
        *   **AC1 (界面与交互)**: 用户界面必须清晰展示【无人机多光谱数据融合 (UAV Multispectral Data Fusion)：✅ 完成 (2026-02-02)】的核心字段和操作按钮，且响应式兼容移动端访问。
        *   **AC2 (业务流转)**: 核心状态机（State Machine）的流转必须准确无误，确保模块间集成的边界数据一致性。
        *   **AC3 (权限控制)**: 只有具备对应权限组（如 Specialist/Manager）的角色才能执行该业务的写操作或状态确认。


### **[US-108-04] 机器学习参数辅助 (Optional ML Assistance)**：💡 待执行 (2026)
- **描述**: 作为数据分析师，我希望系统能基于历史作业效果辅助优化算法参数。
- **验收条件**:
    - **(Historical Analysis)** 系统需收集并分析历史VRA作业的产量、成本、环境影响数据。
    - **(ML Algorithm)** 集成强化学习算法，持续优化VRA策略参数。
    - **(Performance Tracking)** 提供模型性能评估和改进效果可视化报告。
    *   **验收标准 (Acceptance Criteria)**:
        *   **AC1 (界面与交互)**: 用户界面必须清晰展示【机器学习参数辅助 (Optional ML Assistance)：💡 待执行 (2026)】的核心字段和操作按钮，且响应式兼容移动端访问。
        *   **AC2 (业务流转)**: 核心状态机（State Machine）的流转必须准确无误，确保模块间集成的边界数据一致性。
        *   **AC3 (权限控制)**: 只有具备对应权限组（如 Specialist/Manager）的角色才能执行该业务的写操作或状态确认。


## 2. 科学提升层 (Scientific Vertical Enhancement)

### **[US-108-05] 生理阶段敏感性权重 (Growth-Stage Aware Logic)**：✅ 完成 (2026-02-02)
- **描述**: 作为农艺师，我希望根据作物当前的生理阶段（GDD 进度）动态调整处方剂量。
- **验收标准 (AC)**:
    - **(Formula)** 最终剂量 = 基准剂量 * 空间系数 (NDVI) * 生理权重 (Stage Multiplier)。
    - **(Config)** 支持定义 `agri.vra.stage.rule`，为 V1-Vn 及 R1-Rn 阶段设置不同的养分补偿系数。
    *   **验收标准 (Acceptance Criteria)**:
        *   **AC1 (界面与交互)**: 用户界面必须清晰展示【生理阶段敏感性权重 (Growth-Stage Aware Logic)：✅ 完成 (2026-02-02)】的核心字段和操作按钮，且响应式兼容移动端访问。
        *   **AC2 (业务流转)**: 核心状态机（State Machine）的流转必须准确无误，确保模块间集成的边界数据一致性。
        *   **AC3 (权限控制)**: 只有具备对应权限组（如 Specialist/Manager）的角色才能执行该业务的写操作或状态确认。


### **[US-108-06] 公式化生物量亏缺补偿 (Deterministic Biomass Deficit)**：✅ 完成 (2026-02-02)
- **描述**: 作为精准农业专家，我希望基于 Logistic 曲线计算“应有生物量”与“实测生物量”的亏缺，并以此作为处方依据。
- **验收标准 (AC)**:
    - **(Calculation)** 亏缺量 $\Delta W = W_{logistic}(GDD) - W_{actual}$。
    - **(Integration)** 处方生成算法自动调用 `agri.science.mixin` 进行亏缺量到养分需求的转换。
    *   **验收标准 (Acceptance Criteria)**:
        *   **AC1 (界面与交互)**: 用户界面必须清晰展示【公式化生物量亏缺补偿 (Deterministic Biomass Deficit)：✅ 完成 (2026-02-02)】的核心字段和操作按钮，且响应式兼容移动端访问。
        *   **AC2 (业务流转)**: 核心状态机（State Machine）的流转必须准确无误，确保模块间集成的边界数据一致性。
        *   **AC3 (权限控制)**: 只有具备对应权限组（如 Specialist/Manager）的角色才能执行该业务的写操作或状态确认。


### **[US-108-07] 逆境安全裁剪逻辑 (Stress-based Safety Clipping)**：✅ 完成 (2026-02-02)
- **描述**: 作为安全主管，我希望在极端逆境（高温、干旱）下自动限制高浓度施肥，避免二次伤害。
- **验收标准 (AC)**:
    - **(Logic)** 当 `biological_stress_index > 35` 时，强制执行处方上限裁剪 (Clipping)。
    - **(Audit)** 记录因生物压力触发的“强制减量”审计记录。
    *   **验收标准 (Acceptance Criteria)**:
        *   **AC1 (界面与交互)**: 用户界面必须清晰展示【逆境安全裁剪逻辑 (Stress-based Safety Clipping)：✅ 完成 (2026-02-02)】的核心字段和操作按钮，且响应式兼容移动端访问。
        *   **AC2 (业务流转)**: 核心状态机（State Machine）的流转必须准确无误，确保模块间集成的边界数据一致性。
        *   **AC3 (权限控制)**: 只有具备对应权限组（如 Specialist/Manager）的角色才能执行该业务的写操作或状态确认。


## 3. 高维优化层 (High-Dimension Scientific Optimization)

### **[US-108-08] 养分-生物量质能平衡 (Nutrient-Biomass Mass Balance)**：✅ 完成 (2026-02-02)
- **描述**: 作为数据科学家，我希望弃用模糊的 Base Rate，改用基于产出的质能平衡模型。
- **逻辑**: `Prescription = (Target_Yield - Current_Biomass) * Nutrient_Content_Ratio / Use_Efficiency`。
- **验收标准 (AC)**:
    - 实现 `agri.nutrient.balance.model`，将产量目标与实时生物量对齐。
    - 处方生成算法支持基于干物质积累速率的动态配比。
    *   **验收标准 (Acceptance Criteria)**:
        *   **AC1 (界面与交互)**: 用户界面必须清晰展示【养分-生物量质能平衡 (Nutrient-Biomass Mass Balance)：✅ 完成 (2026-02-02)】的核心字段和操作按钮，且响应式兼容移动端访问。
        *   **AC2 (业务流转)**: 核心状态机（State Machine）的流转必须准确无误，确保模块间集成的边界数据一致性。
        *   **AC3 (权限控制)**: 只有具备对应权限组（如 Specialist/Manager）的角色才能执行该业务的写操作或状态确认。


### **[US-108-09] 动态风险对冲策略 (Dynamic Risk Hedging)**：✅ 完成 (2026-02-02)
- **描述**: 作为风险官，我希望处方能根据“投入产出比”进行概率削减。
- **逻辑**: 如果未来 10 天降雨概率 < 20% 且灌溉能力受限，自动减少 15% 的追肥，防止投资损失。
- **验收标准 (AC)**:
    - 建立“气象-经济”联合惩罚函数。
    - 处方生成时支持“保守/标准/激进”三种确定性模式切换。
    *   **验收标准 (Acceptance Criteria)**:
        *   **AC1 (界面与交互)**: 用户界面必须清晰展示【动态风险对冲策略 (Dynamic Risk Hedging)：✅ 完成 (2026-02-02)】的核心字段和操作按钮，且响应式兼容移动端访问。
        *   **AC2 (业务流转)**: 核心状态机（State Machine）的流转必须准确无误，确保模块间集成的边界数据一致性。
        *   **AC3 (权限控制)**: 只有具备对应权限组（如 Specialist/Manager）的角色才能执行该业务的写操作或状态确认。


### **[US-108-10] 空间 RUE 差异化补偿 (Spatial RUE Compensation)**：✅ 完成 (2026-02-02)
- **描述**: 基于历史表现，识别地块中不同网格的光能利用率 (RUE) 差异，进行“按能分配”。
- **逻辑**: 对于 RUE 较高的网格，增加上限阈值；对于由于土壤物理限制导致 RUE 较低的区域，执行减量。
- **验收标准 (AC)**:
    - 建立网格级的 RUE 历史档案。
    - 实现基于光合生产潜力的空间边际收益优化。
    *   **验收标准 (Acceptance Criteria)**:
        *   **AC1 (界面与交互)**: 用户界面必须清晰展示【空间 RUE 差异化补偿 (Spatial RUE Compensation)：✅ 完成 (2026-02-02)】的核心字段和操作按钮，且响应式兼容移动端访问。
        *   **AC2 (业务流转)**: 核心状态机（State Machine）的流转必须准确无误，确保模块间集成的边界数据一致性。
        *   **AC3 (权限控制)**: 只有具备对应权限组（如 Specialist/Manager）的角色才能执行该业务的写操作或状态确认。


## 4. 深度交互层 (Bio-Physical Interaction Layer)

### **[US-108-11] 养分转化动力学实时修正 (Nutrient Transformation Kinetics)**：✅ 完成 (2026-02-02)
- **描述**: 作为土壤物理学家，我希望根据实时土壤温湿度，计算施入氮素的转化速率（矿化/挥发），动态修正有效剂量。
- **逻辑**: `Actual_Effective_Rate = Applied_Rate * f(Soil_Temp, Soil_Moisture, pH)`。
- **验收标准 (AC)**:
    - 实现土壤养分动力学解析器，动态修正 VRA 处方的实际有效载荷。
    *   **验收标准 (Acceptance Criteria)**:
        *   **AC1 (界面与交互)**: 用户界面必须清晰展示【养分转化动力学实时修正 (Nutrient Transformation Kinetics)：✅ 完成 (2026-02-02)】的核心字段和操作按钮，且响应式兼容移动端访问。
        *   **AC2 (业务流转)**: 核心状态机（State Machine）的流转必须准确无误，确保模块间集成的边界数据一致性。
        *   **AC3 (权限控制)**: 只有具备对应权限组（如 Specialist/Manager）的角色才能执行该业务的写操作或状态确认。


### **[US-108-12] 叶面积指数 (LAI) 驱动的光合潜力校准 (LAI-Driven Potential Calibration)**：✅ 完成 (2026-02-02)
- **描述**: 基于 AI 视觉或多光谱反演的叶面积指数 (LAI)，计算每个网格的 CO2 固定潜力，而非单纯的 NDVI 绿度。
- **逻辑**: 利用 Beer-Lambert 定律计算冠层光截获，修正处方中的生产潜力上限。
- **验收标准 (AC)**:
    - 建立 LAI 与养分需求上限的非线性映射函数。
    *   **验收标准 (Acceptance Criteria)**:
        *   **AC1 (界面与交互)**: 用户界面必须清晰展示【叶面积指数 (LAI) 驱动的光合潜力校准 (LAI-Driven Potential Calibration)：✅ 完成 (2026-02-02)】的核心字段和操作按钮，且响应式兼容移动端访问。
        *   **AC2 (业务流转)**: 核心状态机（State Machine）的流转必须准确无误，确保模块间集成的边界数据一致性。
        *   **AC3 (权限控制)**: 只有具备对应权限组（如 Specialist/Manager）的角色才能执行该业务的写操作或状态确认。


### **[US-108-13] 品种响应曲线自适应 (Cultivar-Specific Response - G×E×M)**：✅ 完成 (2026-02-02)
- **描述**: 不同品种对养分的响应曲线（Law of Dimishing Returns）不同。我希望系统能根据品种指纹（Genotype）自动调整处方的边际收益拐点。
- **逻辑**: 根据 `farm_agri_science` 中的生理指纹，动态加载 Mitscherlich 方程参数。
- **验收标准 (AC)**:
    - 处方单支持根据“品种特异性响应系数”进行个性化计算。
    *   **验收标准 (Acceptance Criteria)**:
        *   **AC1 (界面与交互)**: 用户界面必须清晰展示【品种响应曲线自适应 (Cultivar-Specific Response - G×E×M)：✅ 完成 (2026-02-02)】的核心字段和操作按钮，且响应式兼容移动端访问。
        *   **AC2 (业务流转)**: 核心状态机（State Machine）的流转必须准确无误，确保模块间集成的边界数据一致性。
        *   **AC3 (权限控制)**: 只有具备对应权限组（如 Specialist/Manager）的角色才能执行该业务的写操作或状态确认。


## 业务价值
- **核心价值**: 整合土壤传感器、气象站、无人机遥感等多源数据，提升VRA处方精度，实现更科学的变量作业决策
- **目标用户**: 农技员、农场主、技术员、数据分析师
- **量化收益**: 通过多源数据融合提高VRA处方的科学性和准确性，基于天气预报动态调整减少不利天气条件下的作业风险，利用高分辨率无人机数据实现局部异常区域的精准处理，基于历史数据的机器学习模型实现算法的自我优化

## 技术挑战
- **复杂性**: 需要处理土壤传感器集成、气象数据调整、无人机数据融合、机器学习模型优化等复杂VRA技术
- **性能要求**: 实时数据处理和多源数据融合需高效准确
- **安全合规**: 需要符合农业数据安全、IoT设备管理和数据隐私相关法规要求
- **集成难点**: 与土壤传感器、气象API、无人机设备、卫星数据等多源系统的集成

---
*V4.0 - Bio-Physical Interaction & Cultivar Response | 2026-02-02*
