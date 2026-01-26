# 积温计算算法文档 (Growing Degree Days Calculation Algorithm)

## 算法目的
基于作物品种的生物学零度计算积温，用于预测作物生长阶段和成熟期。

## 输入参数
- `temp_max`: 日最高温度 (float)
- `temp_min`: 日最低温度 (float)
- `t_base`: 生物学零度（品种定义，如水稻一般为 10°C）(float)
- `crop_variety`: 作物品种信息 (dict)
- `weather_forecast`: 未来天气预报数据 (list of dict)

## 输出结果
- `daily_gdd`: 当日积温值 (float)
- `accumulated_gdd`: 累计积温值 (float)
- `growth_stage_prediction`: 基于积温的生长阶段预测 (str)
- `harvest_date_prediction`: 收获期预测 (date)

## 算法流程
1. **日积温计算**: daily_gdd = max(0, (temp_max + temp_min) / 2 - Tbase)
2. **累计积温计算**: 累计从播种或某个基准日开始的每日积温
3. **生长阶段预测**: 根据累计积温对应品种的生长阶段阈值
4. **动态预测**: 利用未来天气预报预计算累计积温趋势
5. **偏差分析**: 计算实际与预测生长的偏差

## 业务规则
- 生物学零度由作物品种定义
- 当日平均温度低于生物学零度时，当日积温为0
- 支持不同作物品种的差异化积温阈值
- 考虑天气预报数据进行动态预测

## 验证方法
- 与历史生长数据对比验证
- 田间实测生长阶段校验
- 品种标准积温需求对比

## 性能指标
- 计算响应时间 < 1秒
- 生长阶段预测准确性 > 85%
- 收获期预测偏差 < 5天