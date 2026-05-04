# 定价与收益优化算法 (Pricing & Revenue Optimization Algorithm)

## 算法目的
基于市场供需、收获时机、库存保质期及生产成本，动态计算最优销售价格，以最大化农场的整体经营收益。

## 输入参数
- `base_cost`: 单位生产成本 (Float)
- `market_price_stream`: 实时市场价格数据流 (List[Float])
- `inventory_age_days`: 当前库存库龄/鲜度 (Integer)
- `shelf_life_total`: 产品总货架期 (Integer)
- `demand_forecast`: 未来周期需求预测系数 (Float)

## 输出结果
- `recommended_price`: 建议销售单价 (Float)
- `discount_trigger`: 促销触发建议 (Boolean)
- `expected_revenue_gain`: 预计收益增量 (Float)

## 算法流程
1. **成本底线计算**: 设定最低售价 `Min_Price = base_cost * (1 + Min_Margin)`。
2. **市场灵敏度调整**: 计算市场偏离度，`Market_Factor = (Current_Market - Avg_Market) / Market_SD`。
3. **鲜度衰减修正**: 若 `inventory_age / shelf_life > 0.7`，执行线性价格衰减，以加速去库存。
4. **供需杠杆应用**: 根据 `demand_forecast` 动态调增价格杠杆。
5. **最优解合成**: `Final_Price = max(Min_Price, base_price * Multipliers)`。

## 具体实现 (Implementation)
```python
def calculate_dynamic_price(cost, market_avg, stock_age, total_life, demand_index):
    """
    动态定价策略
    demand_index: 1.0 为基准, > 1.0 表示高需求
    """
    min_margin = 0.2
    floor_price = cost * (1 + min_margin)
    
    # 1. 鲜度衰减因子
    freshness_ratio = stock_age / total_life
    decay_factor = 1.0
    if freshness_ratio > 0.8:
        decay_factor = 0.6 # 临期 6 折
    elif freshness_ratio > 0.6:
        decay_factor = 0.85
        
    # 2. 供需修正
    # 需求每增加 10%，价格调增 5%
    demand_modifier = 1.0 + (demand_index - 1.0) * 0.5
    
    suggested_price = market_avg * demand_modifier * decay_factor
    
    return {
        'price': max(suggested_price, floor_price),
        'is_promotion': decay_factor < 1.0,
        'margin': (max(suggested_price, floor_price) - cost) / cost
    }
```

## 业务规则
- **会员保护**: 最终价格计算需为 VIP 协议保留预设的固定折扣空间。
- **防止恶意低价**: 除非主管审批，否则严禁售价低于 `base_cost`。

## 验证方法
- 通过 A/B 测试对比不同定价策略下的动销率与总利润额。

## 性能指标
- 计算时间 < 200ms。
- 收益优化提升度 > 8%（基于历史模拟）。