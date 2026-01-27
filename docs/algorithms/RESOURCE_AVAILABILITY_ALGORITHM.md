# 资源可用性检查算法 (Resource Availability Algorithm)

## 算法目的
在观光农业、农机共享等场景中，确保特定设施、场地或设备在预定时间内不发生冲突，保障业务闭环。

## 输入参数
- `resource_id`: 目标资源 ID（如地块、烧烤位、农机） (Integer)
- `date_start`: 计划开始时间 (Datetime)
- `date_end`: 计划结束时间 (Datetime)
- `exclude_task_id`: 排除的当前任务 ID（用于更新校验） (Integer)

## 输出结果
- `is_available`: 是否可用 (Boolean)
- `conflict_tasks`: 冲突的任务列表 (List[Dict])

## 算法流程
1. **构建查询**: 在 `project.task` 或 `farm.booking` 中检索与 `resource_id` 关联的记录。
2. **重叠判断**: 筛选满足以下条件的记录：
   - `status` 为 'confirmed' 或 'in_progress'。
   - `id` 不等于 `exclude_task_id`。
   - `date_start` < `target_date_end` 且 `date_end` > `target_date_start`。
3. **返回结果**: 若结果集为空，则 `is_available` 为 True。

## 具体实现 (Implementation)
```python
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class FarmResourceMixin(models.AbstractModel):
    _name = 'farm.resource.mixin'

    def check_availability(self, resource_id, start, end, exclude_id=None):
        """
        Odoo ORM 实现资源冲突检测
        """
        domain = [
            ('land_parcel_id', '=', resource_id),
            ('state', 'in', ['confirmed', 'in_progress']),
            ('date_start', '<', end),
            ('date_end', '>', start),
        ]
        if exclude_id:
            domain.append(('id', '!=', exclude_id))
            
        conflicts = self.env['project.task'].search(domain)
        
        if conflicts:
            return {
                'available': False,
                'conflicts': conflicts.read(['name', 'date_start', 'date_end', 'user_id'])
            }
        return {'available': True, 'conflicts': []}
```

## 业务规则
- 缓冲区检查：对于农旅资源，可预设清场时间（如 30 分钟），自动累加到 `date_end`。
- 优先级规则：VIP 会员预约可触发低优先级草稿任务的自动调整。

## 验证方法
- 使用并发压力测试模拟多用户同时预约同一资源的边界情况。

## 性能指标
- 响应时间 < 100ms（基于数据库 B-tree 索引）。
- 并发支持 > 50 TPS。