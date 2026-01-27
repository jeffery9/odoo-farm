# 成本核算算法文档 (Cost Calculation Algorithm Documentation)

## 算法目的
自动分摊投入品、人工、设备等成本到具体地块和批次，提供精准的成本分析和盈利能力评估。

## 输入参数
- `production_activities`: 生产活动记录，包含施肥、灌溉、收获等 (list)
- `input_consumption`: 投入品消耗记录，包含种子、肥料、农药等 (list)
- `labor_hours`: 人工工时记录，包含人员、时间、任务 (list)
- `equipment_usage`: 设备使用记录，包含设备、时间、油耗等 (list)
- `batch_info`: 批次信息，包含地块、作物、时间等 (dict)

## 输出结果
- `total_cost`: 总成本计算结果 (dict)
- `cost_breakdown`: 成本分解明细 (dict)
- `unit_cost`: 单位成本计算 (dict)
- `profitability_analysis`: 盈利能力分析 (dict)

## 算法流程
1. **成本归集**: 收集各类生产活动的成本数据
2. **直接成本计算**: 计算直接相关的成本（种子、肥料等）
3. **间接成本分摊**: 按合理标准分摊间接成本（人工、设备等）
4. **批次成本分配**: 将成本分配到具体批次
5. **成本分析**: 生成成本分析报告
6. **动态更新**: 根据新增活动更新成本数据

## 具体实现 (Implementation)
```python
def calculate_batch_cost(batch_id, activities, input_costs, labor_costs, equipment_costs):
    """
    计算特定批次的生产成本
    activities: 属于该批次的所有作业列表
    input_costs: {'product_id': cost_per_unit, ...}
    labor_costs: {'employee_id': rate_per_hour, ...}
    """
    total_input = 0.0
    total_labor = 0.0
    total_equipment = 0.0
    
    for act in activities:
        # 1. 投入品成本 (种子、化肥等)
        for line in act.input_lines:
            total_input += line.qty * input_costs.get(line.product_id, 0.0)
            
        # 2. 人工成本
        for labor in act.labor_lines:
            total_labor += labor.hours * labor_costs.get(labor.employee_id, 0.0)
            
        # 3. 设备成本 (折旧+油耗)
        for equip in act.equipment_lines:
            total_equipment += equip.hours * equipment_costs.get(equip.equipment_id, 0.0)
            
    total_cost = total_input + total_labor + total_equipment
    
    return {
        'batch_id': batch_id,
        'total_cost': total_cost,
        'breakdown': {
            'inputs': total_input,
            'labor': total_labor,
            'equipment': total_equipment
        },
        'margin_analysis': (act.harvest_value - total_cost) / act.harvest_value if act.harvest_value > 0 else 0
    }
```

## 业务规则
- 遵循农业会计准则
- 支持多种成本分摊方法
- 区分直接成本和间接成本
- 考虑损耗和废品的影响

## 验证方法
- 与财务手工核算结果对比
- 分批成本平衡性验证
- 多维度成本分析验证

## 性能指标
- 计算准确性 > 99%
- 大批量数据处理时间 < 5秒
- 成本分摊逻辑验证通过率 100%
