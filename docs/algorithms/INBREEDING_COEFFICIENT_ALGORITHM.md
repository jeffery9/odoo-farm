# 系谱与近交系数计算算法 (Inbreeding Coefficient Algorithm)

## 算法目的
通过递归分析生物资产（种畜/种苗）的系谱，计算近交系数并检测近亲繁殖风险，确保群体遗传多样性。

## 输入参数
- `subject_male_id`: 拟配种雄性 ID (Integer)
- `subject_female_id`: 拟配种雌性 ID (Integer)
- `max_generation`: 溯源最大代数（默认 5 代） (Integer)

## 输出结果
- `inbreeding_coefficient`: 近交系数 (Float, 0.0-1.0)
- `common_ancestors`: 共同祖先列表及对应代次 (List[Dict])
- `risk_level`: 风险等级 (Selection: low, medium, high)

## 算法流程
1. **生成家族树**: 递归获取双方各 `max_generation` 代的所有祖先路径。
2. **寻找共同祖先**: 提取双方祖先集合的交集。
3. **路径路径累加**: 对于每一对共同祖先，计算其通过该祖先连接的路径代数 `n1` 和 `n2`。
4. **公式计算**: `F = Σ (1/2)^(n1+n2+1) * (1 + Fa)`，其中 `Fa` 是祖先本身的近交系数（若无则设为 0）。
5. **判定等级**: 若 `F > 0.0625`（相当于堂兄弟近交），标记为高风险。

## 具体实现 (Implementation)
```python
def get_ancestors(env, lot_id, max_gen, current_gen=1):
    """递归获取祖先字典 {ancestor_id: generation_distance}"""
    if current_gen > max_gen or not lot_id:
        return {}
    lot = env['stock.lot'].browse(lot_id)
    ancestors = {}
    for parent in [lot.father_id, lot.mother_id]:
        if parent:
            ancestors[parent.id] = current_gen
            ancestors.update(get_ancestors(env, parent.id, max_gen, current_gen + 1))
    return ancestors

def calculate_inbreeding(env, male_id, female_id):
    """计算 Wright's 系数"""
    male_tree = get_ancestors(env, male_id, 5)
    female_tree = get_ancestors(env, female_id, 5)
    
    common = set(male_tree.keys()) & set(female_tree.keys())
    f_coeff = 0.0
    for ancestor in common:
        n1 = male_tree[ancestor]
        n2 = female_tree[ancestor]
        f_coeff += (0.5) ** (n1 + n2 + 1)
        
    return f_coeff
```

## 业务规则
- 系谱缺失处理：若关键节点信息缺失，系统需标记为“数据不足”并执行保守评估。
- 自动拦截：在“配种任务（Breeding Intervention）”保存时自动触发。

## 验证方法
- 使用标准系谱案例（如已知全同胞、半同胞配对）进行数学结果对标。

## 性能指标
- 5 代溯源计算时间 < 2 秒。
- 内存消耗平稳（通过路径剪枝优化）。