# 灌溉调度算法文档 (Irrigation Scheduling Algorithm Documentation)

## 算法目的
基于土壤湿度、气象数据、作物需水量等信息，制定最优灌溉计划，提高水资源利用效率。

## 输入参数
- `soil_moisture_data`: 土壤湿度数据，包含不同深度的湿度值 (dict)
- `weather_data`: 气象数据，包含降雨量、蒸发量、温度等 (dict)
- `crop_water_requirements`: 作物需水量，基于作物类型和生长阶段 (dict)
- `irrigation_system`: 灌溉系统信息，包含流量、压力等参数 (dict)

## 输出结果
- `irrigation_schedule`: 灌溉计划，包含时间、水量等 (dict)
- `water_stress_index`: 作物水分胁迫指数预测 (dict)
- `efficiency_recommendations`: 灌溉效率优化建议 (dict)

## 算法流程
1. **土壤水分平衡计算**: 计算当前土壤水分状况
2. **需水量预测**: 基于作物生长阶段预测需水量
3. **气象影响分析**: 分析降雨和蒸发对土壤水分的影响
4. **灌溉时机判断**: 根据土壤湿度阈值判断灌溉时机
5. **水量计算**: 计算所需灌溉水量
6. **计划优化**: 优化灌溉时间和分布

## 具体实现 (Implementation)
```python
def calculate_irrigation_need(current_moisture, field_capacity, wilting_point, et_crop, rain_forecast):
    """
    计算灌溉需求量 (单位: mm)
    et_crop: 作物蒸腾耗水量
    rain_forecast: 预报降雨量
    """
    # 1. 设定安全阈值 (例如：田间持水量的 60%)
    irrigation_threshold = wilting_point + (field_capacity - wilting_point) * 0.6
    
    # 2. 判断是否需要灌溉
    if current_moisture < irrigation_threshold:
        # 3. 计算亏缺量
        deficit = field_capacity - current_moisture
        
        # 4. 考虑降雨补偿
        net_requirement = max(deficit + et_crop - rain_forecast, 0)
        
        return {
            'status': 'urgent' if current_moisture < wilting_point else 'needed',
            'qty_mm': net_requirement,
            'message': f"Irrigation needed to restore field capacity ({field_capacity}%)."
        }
        
    return {'status': 'adequate', 'qty_mm': 0, 'message': "Soil moisture is sufficient."}
```

## 业务规则
- 严格遵循作物水分生理需求
- 优先考虑天然降水，减少灌溉用水
- 考虑土壤类型和质地对水分保持的影响
- 支持节水灌溉技术和优化

## 验证方法
- 与田间实测土壤湿度数据对比
- 灌溉效果和作物生长状况验证
- 节水效果评估

## 性能指标
- 灌溉时机预测准确性 > 80%
- 水资源利用效率提升 > 15%
- 计算响应时间 < 5秒
