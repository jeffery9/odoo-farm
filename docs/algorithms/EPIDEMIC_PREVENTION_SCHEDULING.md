# 动态防疫与植保排期算法 (Epidemic Prevention & Crop Protection Scheduling)

## 算法目的
基于品种的标准防疫/植保模板，结合实际出生或种植日期，自动生成全周期的任务排期，并动态校验休药期以确保食品安全。

## 输入参数
- `start_date`: 任务起始日期（如出生日期或播种日期） (Date)
- `prevention_template_id`: 关联的防疫模板 ID (Integer)
- `expected_harvest_date`: 计划收获日期 (Date)

## 输出结果
- `scheduled_tasks`: 自动生成的任务排期列表 (List[Dict])
- `earliest_safe_harvest_date`: 最早安全收获日期 (Date)
- `withdrawal_conflicts`: 休药期冲突详情 (List[Dict])

## 算法流程
1. **模板匹配**: 加载 `farm.prevention.template` 中定义的 `T + N` 天作业序列。
2. **时间轴展开**: 为每一项作业计算 `planned_date = start_date + N`。
3. **休药期核算**: 
   - 提取所有排期任务中投入品的 `withdrawal_period`（休药期）。
   - 计算 `Individual_Safe_Date = Task_Date + Withdrawal_Period`。
4. **安全窗口锁定**: `earliest_safe_harvest_date = max(Individual_Safe_Dates)`。
5. **冲突拦截**: 若 `expected_harvest_date < earliest_safe_harvest_date`，触发调度异常。

## 具体实现 (Implementation)
```python
from datetime import timedelta

def generate_prevention_schedule(start_date, template_lines):
    """
    基于 SOP 模板生成防疫/植保任务排期
    template_lines: [{'offset_days': 10, 'product_id': 1, 'withdrawal_days': 21}, ...]
    """
    schedule = []
    max_safe_date = start_date
    
    for line in template_lines:
        planned_date = start_date + timedelta(days=line['offset_days'])
        safe_date = planned_date + timedelta(days=line['withdrawal_days'])
        
        schedule.append({
            'date': planned_date,
            'product_id': line['product_id'],
            'safe_date': safe_date
        })
        
        if safe_date > max_safe_date:
            max_safe_date = safe_date
            
    return schedule, max_safe_date

def validate_harvest_safety(harvest_date, max_safe_date):
    if harvest_date < max_safe_date:
        return False, f"Harvest too early. Safe date is {max_safe_date}."
    return True, "Safe to harvest."
```

## 业务规则
- **优先级原则**: 防疫任务不可跳过，若排期落在节假日，需根据前置/后延规则自动调整。
- **动态修正**: 若实际作业日期偏离计划日期，系统需实时重算最早安全收获日。

## 验证方法
- 模拟高频防疫排期场景，验证收获日期的硬性逻辑拦截。

## 性能指标
- 100 项排期计算时间 < 1 秒。
- 调度成功率 100%。