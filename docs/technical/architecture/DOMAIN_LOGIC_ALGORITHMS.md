# 农场管理系统：领域逻辑与算法规格 (Domain Logic & Algorithms)

## 1. 种植业：养分平衡算法 (Nutrient Balance)

系统需根据施肥干预自动更新地块养分状态。

- **算法公式**:
  `Balance(Element) = Σ(Input_Qty * Input_Concentration) / Area`
- **应用逻辑**:
    1. 每次施肥干预（Intervention）完成后，提取投入品（如：复合肥）的 N-P-K 比例字段。
    2. 计算本次施入的总养分量（kg）。
    3. 除以 `project.task` 定义的 `size_value` (面积)。
    4. 将结果记录在 `farm.production.nutrient_log` 中。
- **输入**: 投入品数量、浓度、地块面积
- **输出**: 养分平衡状态
- **复杂度**: O(1)
- **异常处理**: 当输入参数为负数或面积为零时，抛出验证异常

## 2. 水产/畜牧：动态饲喂量预测 (Feed Estimation)

根据生长阶段和当前生物量自动建议投喂量。

- **算法模型**:
  `Daily_Feed = Estimated_Biomass * Feeding_Rate(Stage)`
- **计算逻辑**:
    1. `Estimated_Biomass` = `Initial_Count` * `Estimated_Survival_Rate` * `Standard_Weight_at_Age`.
    2. `Standard_Weight_at_Age` 从品种（Variety）的"生长曲线表"中获取。
    3. 系统每日通过定时任务（Cron）生成建议的干预任务（Intervention Proposal）。
- **输入**: 初始数量、存活率、年龄、品种生长曲线
- **输出**: 每日推荐投喂量
- **复杂度**: O(1)
- **异常处理**: 当存活率超过100%或体重为负时，触发健康预警

## 3. 观光农业：资源可用性检查 (Resource Availability)

防止研学活动或设施预约的时间冲突。

- **检查规则**:
    1. 当创建 `agritourism` 类型的任务（预约）时，触发校验。
    2. 检索相同 `land_parcel_id` (如：1号烧烤位) 在 `date_start` 到 `date_end` 期间是否存在已确认的任务。
    3. 若存在重叠（Overlap），则抛出警告并阻止确认。
- **算法复杂度**: O(n), 其中 n 为相关时间区间的任务数
- **优化策略**: 使用区间树数据结构可优化至 O(log n + k), k 为重叠任务数
- **异常处理**: 检测到时间冲突时返回冲突详情和建议解决方案

## 4. 物联网与传感器数据处理 (IoT & Sensor Data Processing)

处理来自传感器、无人机和其他IoT设备的数据，实现实时监控和预警。

- **算法模型**:
    - **实时监控**: `Alert = Sensor_Value > Threshold OR Sensor_Value < Threshold`
    - **数据融合**: `Fused_Value = Weighted_Average(Values_from_Multiple_Sensors)`
    - **异常检测**: `Anomaly = |Sensor_Value - Moving_Average| > K * Standard_Deviation`
- **处理逻辑**:
    1. 实时收集来自各类传感器（温度、湿度、pH值、光照强度等）的数据流。
    2. 使用滑动窗口算法计算移动平均值和标准差。
    3. 当传感器值偏离正常范围超过设定阈值时，触发警报。
    4. 对多个传感器数据进行加权平均融合，提高数据可靠性。
- **输入**: 传感器数据流、阈值参数、权重系数
- **输出**: 融合后的数据、异常警报、趋势分析
- **复杂度**: O(1) per data point
- **异常处理**: 当传感器数据连续异常或数据包丢失时，使用历史数据插值并记录设备故障日志

## 5. 防疫与植保：动态排期算法 (Epidemic Prevention Scheduling)

- **逻辑描述**: 根据品种（Variety）定义的"标准防疫模版"自动生成任务。
- **计算逻辑**:
    1. 获取生产任务（Task）的"开始日期（或出生日期）"。
    2. 匹配该品种对应的 `farm.prevention.template`。
    3. 模板定义：`T + N天` 执行 `某种疫苗/农药`。
    4. 系统自动生成 `project.task` (子任务) 或 `mrp.production`，预填计划日期。
    5. **休药期锁定**: `Harvest_Date` 必须大于 `Last_Prevention_Date + Withdrawal_Period`。若冲突，系统自动延后收获建议日。
- **算法复杂度**: O(m), m 为防疫模板中的条目数
- **异常处理**: 当休药期与收获时间冲突时，自动计算新的安全收获日期并通知用户

## 6. 育种：系谱与近亲系数计算 (Breeding & Pedigree)

- **逻辑描述**: 记录生物资产的祖辈信息，防止近亲繁殖。
- **计算逻辑**:
    1. 每个生物资产（Lot/Asset）关联 `father_id` 和 `mother_id`。
    2. **路径搜索**: 递归向上搜索 5 代祖先。
    3. **近亲检查**: 在进行"配种干预（Breeding Intervention）"时，系统自动对比公母双方的祖先树。
    4. 若发现共同祖先在 3 代以内，系统弹出"近交风险"警告。
- **算法模型**:
    `Inbreeding_Coefficient = Σ(1/2)^(n1+n2+1)` 对于每对共同祖先
    其中 n1, n2 是从两个配对个体到共同祖先的代数
- **输入**: 配对个体ID、系谱数据库
- **输出**: 近交系数、共同祖先列表
- **复杂度**: O(d^g), d为平均后代数, g为搜索代数(默认5代)
- **异常处理**: 当系谱信息不完整时，标记为"信息不足"并建议进一步验证

## 7. 育苗：移栽量与损耗计算 (Nursery Transition)

- **逻辑描述**: 从育苗中心向大田移栽时的数量折算。
- **计算逻辑**:
    1. `Total_Plants_Needed = Target_Area * Target_Density / (1 - Estimated_Nursery_Loss)`.
    2. **转场逻辑**: 育苗任务结束时，系统生成 `stock.picking`（内部调拨），将"种苗"从"育苗区"移动到"生产区"。
    3. 自动计算"苗龄"，并作为生产任务的初始参数。
- **输入**: 目标面积、目标密度、预估损耗率
- **输出**: 所需种苗总数、移栽建议
- **复杂度**: O(1)
- **异常处理**: 当预估损耗率 >= 100% 时，提示参数错误

## 8. 有机合规：转换期与黑名单实时校验

- **逻辑描述**: 确保生产过程绝对符合认证标准。
- **校验逻辑**:
    1. 在 `mrp.production`（农事作业）添加投入品时触发。
    2. 检查当前 `project.project` 的 `certification_type`。
    3. 若为"有机"，则查询所选 `product.product` 的 `aquaculture_composition` 是否包含在该认证标准的 `forbidden_substances` 名单中。
    4. 若命中，禁止保存并记录审计异常。
- **算法复杂度**: O(k), k 为禁用物质列表长度
- **异常处理**: 校验失败时记录审计日志并返回具体的违规物质信息

## 9. 天气影响算法 (Weather Impact Algorithms)

处理天气数据对农业生产的影响，包括生长速率调整、灌溉需求计算等。

- **算法模型**:
    - **温度影响**: `Growth_Rate_Multiplier = f(Temperature, Base_Temp, Optimal_Temp, Ceiling_Temp)`
    - **光照影响**: `Photosynthesis_Rate = Light_Intensity * Efficiency_Factor`
    - **综合影响**: `Adjusted_Daily_Growth = Base_Growth * Temp_Factor * Light_Factor * Water_Factor`
- **计算逻辑**:
    1. 从天气API获取实时和预测数据（温度、湿度、光照、降水、风速）。
    2. 计算各环境因子对特定作物生长的影响系数。
    3. 综合多个因子调整作物的预期生长速率。
    4. 根据天气预报生成农业生产建议。
- **输入**: 天气数据、作物类型、基准生长参数
- **输出**: 生长速率调整系数、生产建议、预警信息
- **复杂度**: O(1) per calculation
- **异常处理**: 当天气数据缺失时，使用历史平均值进行估算并标记数据质量

## 10. 灌溉管理算法 (Irrigation Management)

基于土壤湿度、作物需求和天气条件的智能灌溉调度。

- **算法模型**:
    - **土壤水分平衡**: `Soil_Moisture(t+1) = Soil_Moisture(t) + Irrigation - Evapotranspiration - Drainage`
    - **灌溉需求**: `Irrigation_Required = Target_Moisture - Current_Moisture`
    - **蒸发蒸腾量**: `ET = ETo * Crop_Coefficient`, 其中 `ETo` 为参照蒸发蒸腾量
- **计算逻辑**:
    1. 实时监测土壤湿度传感器数据。
    2. 计算作物特定的蒸发蒸腾量（ETc）。
    3. 根据土壤类型、作物生长阶段和天气条件确定灌溉阈值。
    4. 生成灌溉计划并在达到阈值时自动执行或提醒。
- **输入**: 土壤湿度、作物类型、生长阶段、天气数据、土壤参数
- **输出**: 灌溉建议、灌溉计划、用水量预测
- **复杂度**: O(1)
- **异常处理**: 当传感器故障时，基于历史数据和天气预报估算灌溉需求

## 11. 产量预测算法 (Yield Prediction)

基于历史数据、环境因素和作物生长模型预测收获产量。

- **算法模型**:
    - **机器学习模型**: 集成多个算法（线性回归、随机森林、神经网络）进行预测
    - **生长模型**: `Yield = Σ(Base_Yield * Environmental_Factors * Management_Factors)`
    - **置信区间**: `Prediction_Interval = Mean ± Z * Standard_Error`
- **计算逻辑**:
    1. 收集历史产量数据、环境参数、管理操作记录。
    2. 使用时间序列分析方法识别产量模式。
    3. 结合当前生长阶段和环境条件调整预测。
    4. 提供预测分布和置信区间。
- **输入**: 历史产量、环境数据、作物品种、生长阶段
- **输出**: 预测产量、置信区间、风险评估
- **复杂度**: O(n) for training, O(1) for prediction
- **异常处理**: 当数据不足时，提供基于品种平均值的基准预测

## 12. 定价与收益优化算法 (Pricing & Revenue Optimization)

基于市场条件、供需关系和成本结构的动态定价策略。

- **算法模型**:
    - **供需定价**: `Price = Base_Price * (1 + (Demand - Supply) / Market_Base)`
    - **季节性调整**: `Seasonal_Factor = f(Month, Harvest_Time, Market_Trends)`
    - **收益优化**: `Optimal_Price = argmax[(Price - Cost) * Expected_Quantity_Sold]`
- **计算逻辑**:
    1. 分析市场价格趋势和竞争情况。
    2. 根据收获时间、库存水平和季节性需求调整价格。
    3. 考虑价格弹性计算最优定价策略。
    4. 支持批量折扣和会员定价策略。
- **输入**: 市场价格、需求预测、成本结构、季节性参数
- **输出**: 推荐价格、定价策略、收益预测
- **复杂度**: O(1)
- **异常处理**: 当市场数据不可用时，使用成本加成法计算基准价格

## 13. 资源优化算法 (Resource Optimization)

优化设备、劳动力和场地的分配以提高运营效率。

- **算法模型**:
    - **任务调度**: 使用启发式算法（如遗传算法、模拟退火）优化任务排序
    - **设备分配**: `Minimize Σ(Task_Duration + Setup_Time + Travel_Time)`
    - **人员调度**: 基于技能匹配和可用性的多目标优化
- **计算逻辑**:
    1. 收集所有待执行任务的详细信息（类型、持续时间、技能要求、设备需求）。
    2. 分析设备和人员的可用性时间表。
    3. 使用优化算法生成任务调度方案，考虑优先级、截止时间和资源约束。
    4. 持续监控执行情况并根据需要重新调度。
- **输入**: 任务列表、资源可用性、约束条件、优先级
- **输出**: 优化调度方案、资源分配计划、完成时间预测
- **复杂度**: O(n^2) for basic scheduling, higher for advanced optimization
- **异常处理**: 当资源冲突无法解决时，提供替代方案和冲突详情

## 14. 质量评估算法 (Quality Assessment)

基于视觉识别和物理参数的自动化产品质量分级。

- **算法模型**:
    - **图像分析**: 使用计算机视觉检测颜色、形状、缺陷
    - **分级模型**: `Grade = f(Size, Weight, Color, Defect_Score)`
    - **货架期预测**: `Shelf_Life = Base_Life * Storage_Factors`
- **计算逻辑**:
    1. 通过摄像头或传感器收集产品质量参数。
    2. 使用预训练模型识别和量化缺陷。
    3. 根据行业标准和客户要求进行分级。
    4. 预测产品货架期并优化库存管理。
- **输入**: 图像数据、物理测量值、分级标准
- **输出**: 质量等级、缺陷报告、货架期预测
- **复杂度**: O(n) for image processing, where n is pixel count
- **异常处理**: 当图像质量不足时，标记为"需人工检查"

## 15. 可持续性指标算法 (Sustainability Metrics)

计算环境影响和可持续发展指标。

- **算法模型**:
    - **碳足迹**: `Carbon_Footprint = Σ(Activity_Emission_Factor * Activity_Level)`
    - **水效**: `Water_Efficiency = Yield / Water_Consumed`
    - **生态影响**: 综合多项环境指标的标准化指数
- **计算逻辑**:
    1. 收集农业生产活动的数据（能耗、投入品使用、产量、土地利用）。
    2. 应用IPCC等权威机构的排放因子计算碳排放。
    3. 计算水效、土地利用效率等资源利用指标。
    4. 生成可持续性报告和改进建议。
- **输入**: 农业活动数据、排放因子、基准值
- **输出**: 碳足迹、资源效率指标、可持续性评分
- **复杂度**: O(n), where n is number of activities
- **异常处理**: 当数据不完整时，使用缺省值或估算值进行计算并标记不确定性