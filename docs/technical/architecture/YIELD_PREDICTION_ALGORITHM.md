# 产量预测与生产偏差分析算法 (Yield Prediction & Deviation Analysis)

## 算法目的
集成历史产量数据、实时环境参数（积温、水分）与农事干预强度，动态预测本产季的预期收成，并定位导致产量损失的关键致偏因素。

## 输入参数
- `historical_yield_data`: 过去 3-5 年该地块及品种的产量记录 (List[Float])
- `current_gdd`: 当前累计积温 (Float)
- `input_intensity_index`: 投入品（水肥）强度指数 (Float)
- `weather_deviation_score`: 气象灾害偏离度评分 (Float)

## 输出结果
- `predicted_yield`: 预测产量 (Float, kg/单位面积)
- `confidence_interval`: 置信区间 (Tuple[Float, Float])
- `loss_attribution`: 产量损失归因分析 (Dict)

## 算法流程
1. **基准提取**: 计算该品种在地块上的历史加权平均产量。
2. **环境修正**: 应用 GDD 生长系数，预测当前进度下的生物量潜力。
3. **投入品补偿**: 根据施肥/灌溉量对比 SOP 标准，计算产量增益或赤字。
4. **回归预测**: 使用线性回归或随机森林模型合成最终预测值。
5. **偏差定位**: 对比预测值与目标值，按权重输出气象、植保、营养等维度的贡献度。

## 具体实现 (Implementation)
```python
import numpy as np

def estimate_yield(avg_hist_yield, gdd_progress, input_score, disaster_score):
    """
    产量预测模型 (简化的加权修正法)
    gdd_progress: 0.0 - 1.0 (积温进度)
    input_score: 0.0 - 1.2 (1.0 为 SOP 标准)
    disaster_score: 0.0 - 1.0 (0 为无灾害)
    """
    # 1. 基础生物量增长因子 (基于积温)
    # 假设生长速率随积温呈逻辑回归或正态分布，此处用线性修正
    base_potential = avg_hist_yield * (1.0 + (gdd_progress - 0.5) * 0.2)
    
    # 2. 投入品增益修正
    # 过量投入不一定线性增产，此处使用对数函数模拟报酬递减
    input_modifier = np.log1p(input_score) / np.log1p(1.0)
    
    # 3. 灾害扣减
    disaster_penalty = 1.0 - (disaster_score * 0.8)
    
    prediction = base_potential * input_modifier * disaster_penalty
    
    return {
        'predicted_yield': max(prediction, 0.0),
        'upper_bound': prediction * 1.15,
        'lower_bound': prediction * 0.85,
        'risk_level': 'high' if disaster_score > 0.3 else 'low'
    }
```

## 业务规则
- 若积温进度落后 > 20%，系统必须强制触发“收获窗口延后”预警向场长推送 Activity。
- 预测结果需支持按季度动态更新，并写入 `farm.production.forecast` 记录。

## 验证方法
- 产季结束后对比实收产量与模型预测值的 RMSE（均方根误差）。

## 性能指标
- 模型推理时间 < 2 秒。
- 采收前 30 天预测精度 > 85%。