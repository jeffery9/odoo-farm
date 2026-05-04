# 育苗移栽量与损耗计算算法 (Nursery Transition Algorithm)

## 算法目的
计算从育苗中心向大田移栽时所需的种苗总数，并核算各阶段损耗，确保大田定植密度达标。

## 输入参数
- `target_area`: 目标种植面积 (Float, 亩/公顷)
- `target_density`: 目标定植密度 (Float, 株/单位面积)
- `nursery_loss_rate`: 育苗期预估损耗率 (Float, 0.0-1.0)
- `transportation_loss_rate`: 移栽运输预估损耗率 (Float, 0.0-1.0)

## 输出结果
- `total_seeds_needed`: 总需种量/播种量 (Integer)
- `available_seedlings`: 预计可用壮苗数 (Integer)
- `transition_efficiency`: 移栽效率评分 (Float)

## 算法流程
1. **净需量计算**: `Net_Plants = target_area * target_density`。
2. **总需求倒推**: `total_seeds_needed = Net_Plants / [(1 - nursery_loss_rate) * (1 - transportation_loss_rate)]`。
3. **苗龄追踪**: 根据播种任务日期自动计算当前苗龄，判定是否达到移栽标准。
4. **内部调拨**: 完工后自动触发 `stock.picking` 将资产从育苗库位移动至生产地块。

## 具体实现 (Implementation)
```python
import math

def calculate_nursery_requirements(area, density, nursery_loss, trans_loss):
    """
    计算育苗播种量
    """
    if nursery_loss >= 1.0 or trans_loss >= 1.0:
        return {'error': 'Loss rate cannot be 100% or more.'}
        
    net_plants = area * density
    
    # 分阶段计算以提高透明度
    available_after_nursery = net_plants / (1 - trans_loss)
    gross_seeds = available_after_nursery / (1 - nursery_loss)
    
    return {
        'net_plants': net_plants,
        'seeds_to_sow': math.ceil(gross_seeds),
        'reserve_qty': math.ceil(gross_seeds - net_plants)
    }
```

## 业务规则
- 损耗率严禁设置为 100% 或以上。
- 支持“补苗”逻辑：若大田定植后存活率不佳，可二次触发计算。

## 验证方法
- 对比实际领苗数量与大田最终成活株数。

## 性能指标
- 计算复杂度 O(1)。
- 数据精度保留至个位数。