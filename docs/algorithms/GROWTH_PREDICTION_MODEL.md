# 生长预测模型文档 (Growth Prediction Model Documentation)

## 算法目的
基于品种特性、环境条件预测作物生长周期及产量，为生产计划提供科学依据。

## 输入参数
- `crop_variety`: 作物品种信息，包含生长特性参数 (dict)
- `environmental_data`: 环境数据，包含温度、湿度、光照等 (dict)
- `planting_date`: 种植日期 (date)
- `soil_conditions`: 土壤条件，包含肥力、pH值等 (dict)

## 输出结果
- `growth_schedule`: 预测生长阶段时间表 (dict)
- `yield_prediction`: 产量预测结果 (dict)
- `growth_deviation`: 与标准生长的偏差分析 (dict)

## 算法流程
1. **品种特征提取**: 提取作物品种的生长特性参数
2. **环境适应性分析**: 分析环境条件对生长的影响
3. **生长阶段预测**: 预测各生长阶段的持续时间
4. **产量预测计算**: 基于生长条件计算产量预测
5. **风险因素评估**: 评估影响生长的风险因素
6. **动态调整**: 根据实际生长情况调整预测

## 具体实现 (Implementation)
```python
from datetime import timedelta

def predict_growth_stages(planting_date, daily_temp_forecast, base_temp, stage_gdd_targets):
    """
    基于积温 (GDD) 的生长阶段预测
    daily_temp_forecast: [{'date': '2026-02-01', 'avg_temp': 15.5}, ...]
    stage_gdd_targets: {'emergence': 150, 'flowering': 800, 'maturity': 1500}
    """
    cumulative_gdd = 0.0
    predictions = {}
    current_date = planting_date
    
    # 按照阶段目标排序
    sorted_stages = sorted(stage_gdd_targets.items(), key=lambda x: x[1])
    
    for forecast in daily_temp_forecast:
        avg_temp = forecast['avg_temp']
        daily_gdd = max(avg_temp - base_temp, 0)
        cumulative_gdd += daily_gdd
        
        for stage, target in sorted_stages:
            if stage not in predictions and cumulative_gdd >= target:
                predictions[stage] = forecast['date']
                
    return predictions
```

## 业务规则
- 遵循作物生长发育的基本规律
- 考虑当地气候条件的特殊性
- 结合历史生长数据进行校准
- 支持不同品种的生长模型切换

## 验证方法
- 与历史生长数据对比验证
- 田间实测数据校验
- 专家经验数据验证

## 性能指标
- 生长阶段预测准确性 > 85%
- 产量预测偏差 < 15%
- 模型响应时间 < 2秒
