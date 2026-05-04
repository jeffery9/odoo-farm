# 逻辑斯蒂生长曲线算法文档 (Logistic Growth Curve Algorithm)

## 算法目的
利用逻辑斯蒂生长曲线模型预测作物生物量和产量，进行生长偏差分析和预警。

## 输入参数
- `t`: 时间变量 (float or list of float)
- `l_max`: 最大期望生物量/产量 (float)
- `k`: 生长速率常数 (float)
- `t0`: 生长最快的时间点（拐点）(float)
- `w_actual`: 实际观测生物量 (float, optional for deviation analysis)

## 输出结果
- `w_predicted`: 预测生物量 W(t) = L / (1 + exp(-k(t - t0))) (float)
- `growth_rate`: 当前生长速率 (float)
- `deviation_analysis`: 实际与预测偏差分析 (dict)
- `warning_status`: 偞长偏差预警状态 (str)

## 算法流程
1. **参数初始化**: 基于作物品种和历史数据确定 L, k, t0 参数
2. **预测计算**: 使用逻辑斯蒂公式 W(t) = L / (1 + exp(-k(t - t0))) 计算预测值
3. **偏差分析**: 计算 (W_actual - W_predicted) / W_predicted 比值
4. **预警判断**: 若偏差 > 20%，触发生长异常预警
5. **趋势预测**: 基于当前生长状态预测后续生长趋势

## 具体实现 (Implementation)
```python
import numpy as np

def logistic_growth_function(t, L, k, t0):
    """
    逻辑斯蒂生长公式核心实现
    W(t) = L / (1 + exp(-k(t - t0)))
    """
    return L / (1 + np.exp(-k * (t - t0)))

def analyze_growth_deviation(t_current, w_actual, variety_params):
    """
    分析生长偏差
    variety_params: {'L': 100, 'k': 0.1, 't0': 50}
    """
    L, k, t0 = variety_params['L'], variety_params['k'], variety_params['t0']
    w_expected = logistic_growth_function(t_current, L, k, t0)
    
    deviation = (w_actual - w_expected) / w_expected
    
    status = 'normal'
    if deviation < -0.2:
        status = 'critical_retardation'
    elif deviation < -0.1:
        status = 'warning_slow'
    elif deviation > 0.2:
        status = 'vigorous'
        
    return {
        'expected': round(w_expected, 2),
        'actual': w_actual,
        'deviation_pct': round(deviation * 100, 2),
        'status': status
    }
```

## 业务规则
- 支持不同作物的差异化生长曲线参数
- 当偏差 > 20% 时触发农技预警通知
- 结合积温算法进行更精确的生长预测
- 支持蒙特卡洛模拟生成概率分布预测

## 验证方法
- 与历史生长数据对比验证
- 田间实测生物量校验
- 产量预测准确性评估

## 性能指标
- 生长阶段预测准确性 > 80%
- 异常预警触发准确率 > 75%
- 计算响应时间 < 500毫秒
