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

## 具体实现 (Implementation)
```python
def calculate_daily_gdd(t_max, t_min, t_base, t_cap=None):
    """
    计算日有效积温
    t_cap: 假设为上限温度(如玉米 30°C)，超过此温度生长不再加速
    """
    if t_cap:
        t_max = min(t_max, t_cap)
        t_min = min(t_min, t_cap)
        
    avg_temp = (t_max + t_min) / 2.0
    gdd = max(avg_temp - t_base, 0.0)
    return gdd

def predict_harvest_date(start_date, current_gdd, target_gdd, forecast_data, t_base):
    """
    预测收获日期
    forecast_data: [{'date': '2026-05-01', 't_max': 25, 't_min': 15}, ...]
    """
    remaining_gdd = target_gdd - current_gdd
    if remaining_gdd <= 0:
        return start_date # 已经成熟
        
    accumulated_forecast = 0.0
    for day in forecast_data:
        daily = calculate_daily_gdd(day['t_max'], day['t_min'], t_base)
        accumulated_forecast += daily
        if accumulated_forecast >= remaining_gdd:
            return day['date']
            
    # 如果预报数据不足，按历史均值估算 (此处简化返回 None)
    return None
```

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
