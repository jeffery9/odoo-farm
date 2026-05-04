# 动态饲喂量预测算法 (Feed Estimation Algorithm)

## 算法目的
根据生物资产的生长阶段、存活率和当前总生物量，自动计算并建议每日最优投喂量，实现精准饲喂并降低饵料系数。

## 输入参数
- `initial_count`: 初始放养数量 (Integer)
- `estimated_survival_rate`: 预估存活率 (Float, 0.0-1.0)
- `age_days`: 日龄/生长期 (Integer)
- `growth_curve`: 品种标准生长曲线数据 (Dict/PyTree)
- `feeding_rate_table`: 不同阶段的投喂率表 (Dict)

## 输出结果
- `daily_feed_qty`: 建议每日总投喂量 (Float, kg)
- `estimated_biomass`: 当前预估总生物量 (Float, kg)
- `standard_weight`: 当前日龄标准个体体重 (Float, g)

## 算法流程
1. **获取个体权重**: 从 `growth_curve` 中检索当前 `age_days` 对应的标准体重。
2. **计算存活生物量**: `Estimated_Biomass` = `initial_count` * `estimated_survival_rate` * `standard_weight` / 1000。
3. **匹配投喂率**: 根据 `age_days` 所属的生长阶段，从 `feeding_rate_table` 获取对应的投喂百分比。
4. **计算总投喂量**: `daily_feed_qty` = `Estimated_Biomass` * `Feeding_Rate`。
5. **异常校验**: 检查计算结果是否超出该品种的安全投喂区间。

## 具体实现 (Implementation)
```python
def calculate_daily_feed(initial_count, survival_rate, age_days, growth_curve, feeding_rates):
    """
    Odoo 19 农事干预建议核心逻辑
    """
    # 1. 从生长曲线获取标准体重 (g)
    # growth_curve 格式示例: {0: 1.5, 10: 5.2, 30: 25.0 ...}
    sorted_ages = sorted(growth_curve.keys())
    standard_weight = 0.0
    for i in range(len(sorted_ages)-1):
        if sorted_ages[i] <= age_days < sorted_ages[i+1]:
            # 线性插值
            x0, x1 = sorted_ages[i], sorted_ages[i+1]
            y0, y1 = growth_curve[x0], growth_curve[x1]
            standard_weight = y0 + (y1 - y0) * (age_days - x0) / (x1 - x0)
            break
    
    # 2. 计算预估生物量 (kg)
    biomass = (initial_count * survival_rate * standard_weight) / 1000.0
    
    # 3. 匹配当前阶段投喂率
    # feeding_rates 格式示例: {'fry': 0.05, 'juvenile': 0.03, 'adult': 0.015}
    current_rate = 0.0
    if age_days < 30:
        current_rate = feeding_rates.get('fry', 0.0)
    elif age_days < 90:
        current_rate = feeding_rates.get('juvenile', 0.0)
    else:
        current_rate = feeding_rates.get('adult', 0.0)
        
    return {
        'daily_feed_qty': biomass * current_rate,
        'estimated_biomass': biomass,
        'standard_weight': standard_weight
    }
```

## 业务规则
- 存活率严禁超过 100%。
- 若环境温度（IoT 联动）偏离舒适区，需根据修正系数自动调减投喂量。
- 每日投喂量建议应作为 Intervention Proposal 自动推送至移动端。

## 验证方法
- 对比实际收获总生物量与模型预估值的偏差。
- 定期抽样实测个体体重，反向修正生长曲线。

## 性能指标
- 计算时间 < 0.5 秒。
- 生物量预估误差 < 15%。