# 天气影响与动态调整算法 (Weather Impact Algorithm)

## 算法目的
分析外部气象数据（温度、光照、风力等）对特定农事活动的影响，动态调整生长预测或对危险作业实施强制拦截。

## 输入参数
- `weather_forecast`: 气象预报数据流 (JSON/Dict)
- `activity_type`: 农事活动类型（如：喷洒、收割、移栽） (String)
- `base_growth_params`: 品种基准生长参数 (Dict)

## 输出结果
- `growth_multiplier`: 生长速率修正系数 (Float)
- `safety_status`: 作业安全状态 (Boolean)
- `recommended_action`: 调整建议 (String)

## 算法流程
1. **气象解析**: 提取未来 24-72 小时的温、湿、风、雨核心指标。
2. **安全阈值过滤**: 
   - 喷洒作业：若风力 > 4 级或即将降雨，`safety_status` = False。
   - 移栽作业：若地温 < 10°C，标记风险。
3. **生长因子调整**:
   - 积温效应：`Adjusted_Daily_GDD` = `(Avg_Temp - Base_Temp) * Light_Coefficient`。
   - 修正系数 = `Adjusted_Daily_GDD` / `Standard_Daily_GDD`。
4. **生成指令**: 自动更新任务计划日期或触发预警 Activity。

## 具体实现 (Implementation)
```python
import numpy as np

def evaluate_weather_safety(activity_type, forecast):
    """
    农事作业安全实时拦截逻辑
    """
    safety = True
    reason = ""
    
    wind_speed = forecast.get('wind_speed', 0)
    rain_prob = forecast.get('rain_probability', 0)
    
    if activity_type == 'spraying':
        if wind_speed > 5.5: # 4级风上限
            safety = False
            reason = "Wind speed too high for spraying."
        elif rain_prob > 60:
            safety = False
            reason = "High probability of rain."
            
    return safety, reason

def calculate_gdd_multiplier(temp_avg, base_temp, standard_gdd):
    """
    计算积温修正系数
    """
    daily_gdd = max(temp_avg - base_temp, 0)
    return daily_gdd / standard_gdd if standard_gdd > 0 else 1.0
```

## 业务规则
- 拦截逻辑优先于调度逻辑：安全拦截必须硬触发 `mail.activity`。
- 多因子加权：光照与温度的乘法效应优于简单的加法。

## 验证方法
- 与历史同期天气及生长记录进行回溯对比。

## 性能指标
- API 解析与计算延迟 < 1 秒。
- 预测修正准确率误差 < 10%。