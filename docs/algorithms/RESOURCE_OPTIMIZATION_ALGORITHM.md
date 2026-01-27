# 资源调度优化算法 (Resource Optimization Algorithm)

## 算法目的
优化农机、劳动力及场地资源的分配，最小化作业转换时间与空闲成本，确保农忙高峰期的任务准时完成。

## 输入参数
- `task_queue`: 待执行任务列表，含优先级与截止时间 (List[Dict])
- `available_resources`: 当前可用资源库，含技能等级与位置 (List[Dict])
- `travel_matrix`: 资源在不同地块间的移动成本矩阵 (Matrix[Float])
- `constraints`: 硬性约束（如：防雨作业限制、机器油耗极限） (Dict)

## 输出结果
- `optimized_schedule`: 优化后的任务指派计划 (List[Dict])
- `resource_utilization`: 预计资源利用率 (Float)
- `bottleneck_alerts`: 潜在瓶颈预警 (List[String])

## 算法流程
1. **任务分级**: 按 `Priority / (Due_Date - Current_Time)` 进行任务紧急度排序。
2. **贪心初始分配**: 为最高优先级任务分配最近的合格资源。
3. **启发式搜索**: 采用启发式算法（如模拟退火）迭代优化，减少 `Σ Travel_Time + Σ Setup_Time`。
4. **冲突消解**: 检查场地占用冲突，动态平移低优先级任务。
5. **计划发布**: 生成甘特图数据并推送至 `farm_planning` 模块。

## 具体实现 (Implementation)
```python
def greedy_schedule(tasks, resources, travel_costs):
    """
    基础贪心调度实现
    tasks: [{'id': 1, 'priority': 5, 'location': 'A'}, ...]
    resources: [{'id': 'tractor_1', 'location': 'B', 'status': 'idle'}, ...]
    """
    # 1. 优先处理高优先级且紧急的任务
    sorted_tasks = sorted(tasks, key=lambda x: x['priority'], reverse=True)
    assignments = []
    
    for task in sorted_tasks:
        best_resource = None
        min_cost = float('inf')
        
        # 2. 寻找最近的可用资源
        for res in resources:
            if res['status'] == 'idle':
                cost = travel_costs[res['location']][task['location']]
                if cost < min_cost:
                    min_cost = cost
                    best_resource = res
        
        if best_resource:
            assignments.append({
                'task_id': task['id'],
                'resource_id': best_resource['id'],
                'travel_cost': min_cost
            })
            best_resource['status'] = 'busy' # 标记为占用
            
    return assignments
```

## 业务规则
- **技能匹配**: 严禁将高精度植保任务分配给无相应资质的工人。
- **连续作业限制**: 考虑工人疲劳度，强制在连续作业 4 小时后插入休息间隔。

## 验证方法
- 对比实际任务完工时间与模型预测完成时间的 MAE（平均绝对误差）。

## 性能指标
- 100 任务/20 资源规模下调度计算时间 < 5 秒。
- 空转时间减少率 > 20%。