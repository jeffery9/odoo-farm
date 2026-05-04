# 可持续性指标与碳足迹算法 (Sustainability Metrics Algorithm)

## 算法目的
通过对生产全历程投入品的量化分析，计算农产品的碳排放强度、水资源利用效率及环境足迹，支撑 ESG 报告披露。

## 输入参数
- `intervention_logs`: 全生产季作业记录，含投入品消耗、油耗、用电量 (List[Dict])
- `emission_factors`: 各类物料的排放因子数据库（基于 IPCC 或行业标准） (Dict)
- `total_yield`: 本季总产量 (Float)
- `water_consumption`: 总灌溉及加工用水量 (Float)

## 输出结果
- `carbon_footprint_total`: 总碳排放量 (Float, kg CO2e)
- `carbon_intensity`: 单位产品碳排强度 (Float, kg CO2e / kg)
- `water_efficiency`: 水资源利用效率 (Float, Yield / m³)

## 算法流程
1. **活动水平归集**: 遍历所有 `intervention` 任务，按类别（肥料、农药、柴油、电力）汇总消耗量。
2. **排放折算**: `Σ (Usage[i] * Emission_Factor[i])` 计算各环节碳排。
3. **固碳抵消**: 扣除固碳资产（如林木、免耕）的年度增量值。
4. **指标生成**: 计算水效指标 `WUE = Yield / Water` 及土地利用率指标。
5. **双语披露**: 生成符合 GRI 标准的报表数据。

## 具体实现 (Implementation)
```python
def calculate_carbon_footprint(logs, factors, offset=0.0):
    """
    ESG 核算核心算法
    logs: [{'category': 'fertilizer', 'qty': 100}, ...]
    factors: {'fertilizer': 2.5, 'diesel': 2.68, ...}
    """
    total_emissions = 0.0
    for entry in logs:
        cat = entry.get('category')
        qty = entry.get('qty', 0.0)
        total_emissions += qty * factors.get(cat, 0.0)
    
    net_emissions = max(total_emissions - offset, 0.0)
    return net_emissions

def calculate_resource_efficiency(yield_qty, water_usage):
    """
    水资源利用效率 (Yield per m3)
    """
    return yield_qty / water_usage if water_usage > 0 else 0.0
```

## 业务规则
- 必须支持“隐含碳 (Scope 3)”计算，即包含采购物资的生产碳排。
- 计算结果需锚定在批次（Lot/Batch）上，实现“一物一码一碳排”。

## 验证方法
- 与第三方环境审计报告进行抽样核对。

## 性能指标
- 产季级汇总计算时间 < 5 秒。
- 排放因子覆盖率 > 90%。