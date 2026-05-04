# 货架期预测算法 (Shelf-life Prediction Algorithm - Arrhenius)

## 算法目的
根据冷链运输与仓储过程中的实时温度波动（IoT 数据），利用阿伦尼乌斯方程动态计算易腐农产品的品质衰减率，从而预测剩余货架期并触发预警。

## 输入参数
- `reference_temp`: 参考基准温度 (Float, K)
- `q10_factor`: 温度敏感性系数 Q10 (Float)
- `real_time_temp_log`: 实时温度监测序列 (List[Dict])
- `initial_shelf_life`: 标准环境下的初始货架期 (Integer, Days)

## 输出结果
- `remaining_shelf_life`: 剩余货架期 (Float, Days)
- `quality_loss_rate`: 品质损耗率 (Float, 0.0-1.0)
- `expiry_date_update`: 更新后的最迟消费日期 (Datetime)

## 算法流程
1. **数据归集**: 提取生产批次（Lot）自收获以来的全历程温度指纹。
2. **等效时间计算**: 采用 Arrhenius 方程将异常温度下的停留时间折算为基准温度下的等效消耗时间：
   `k = k_ref * exp(-Ea/R * (1/T - 1/T_ref))`。
3. **累积损耗核算**: 累加各个监测点的品质损失。
4. **动态预测**: `Remaining = Total_Life - Σ Equivalent_Time`。
5. **策略触发**: 若剩余期 < 20%，自动生成促销或降级任务。

## 具体实现 (Implementation)
```python
import numpy as np

def predict_shelf_life(temp_series, base_life_days, t_ref=273.15):
    """
    基于 Arrhenius 方程的等效货架期折算
    temp_series: [{'temp_c': 4.5, 'duration_hrs': 2}, ...]
    """
    ea_r = 8000 # 活化能/气体常数 (示例值)
    total_consumed_days = 0.0
    
    for log in temp_series:
        t_kelvin = log['temp_c'] + 273.15
        # 计算相对于基准温度的加速因子
        acceleration_factor = np.exp(-ea_r * (1/t_kelvin - 1/t_ref))
        consumed_days = (log['duration_hrs'] / 24.0) * acceleration_factor
        total_consumed_days += consumed_days
        
    remaining = max(base_life_days - total_consumed_days, 0.0)
    return {
        'remaining_days': round(remaining, 2),
        'is_expired': remaining <= 0,
        'acceleration_avg': total_consumed_days / (sum(l['duration_hrs'] for l in temp_series) / 24.0)
    }
```

## 业务规则
- **补偿机制**: 若 IoT 丢包，系统按该时段最高环温进行保守计算。
- **降级处理**: 货架期缩短至预设阈值时，自动触发 US-09-18 质量降级逻辑。

## 验证方法
- 通过实验室加速破坏性试验（ASLT）验证模型参数。

## 性能指标
- 计算响应时间 < 100ms。
- 货架期预测误差 < 12 小时。
