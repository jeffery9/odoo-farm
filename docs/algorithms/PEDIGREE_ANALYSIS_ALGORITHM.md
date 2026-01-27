# 系谱分析算法文档 (Pedigree Analysis Algorithm)

## 算法目的
分析作物或畜禽的系谱关系，计算近交系数、亲缘关系和遗传多样性。

## 输入参数
- `pedigree_data`: 系谱数据 (个体ID, 父本ID, 母本ID)
- `individual_list`: 个体列表
- `generation_info`: 世代信息
- `population_structure`: 群体结构信息
- `breed_info`: 品种信息

## 输出结果
- `inbreeding_coefficients`: 近交系数
- `relationship_matrix`: 亲缘关系矩阵
- `coancestry_matrix`: 共祖关系矩阵
- `kinship_coefficients`: 亲缘系数
- `genetic_donor_contribution`: 遗传贡献分析
- `pedigree_completeness`: 系谱完整性评估

## 算法流程
1. **系谱整理**: 构建系谱关系网络，验证系谱完整性
2. **关系矩阵计算**: 使用Wright算法计算亲缘关系矩阵
3. **近交系数计算**: 计算各个体的近交系数
4. **遗传贡献分析**: 计算祖先对后代的遗传贡献
5. **多样性评估**: 计算群体遗传多样性指标
6. **系谱验证**: 检查系谱逻辑一致性和异常
7. **结果可视化**: 生成系谱树和关系网络图

## 具体实现 (Implementation)
```python
def calculate_kinship_matrix(pedigree):
    """
    计算加性亲缘关系矩阵 (Numerator Relationship Matrix, A)
    pedigree: list of (id, sire, dam), 已排序确保父母在子女前
    """
    n = len(pedigree)
    A = np.zeros((n, n))
    
    # 映射 ID 到索引
    id_map = {item[0]: i for i, item in enumerate(pedigree)}
    
    for i in range(n):
        idx, s_id, d_id = pedigree[i]
        s_idx = id_map.get(s_id)
        d_idx = id_map.get(d_id)
        
        # 1. 计算对角线元素 (1 + F_i)
        if s_idx is not None and d_idx is not None:
            A[i, i] = 1 + 0.5 * A[s_idx, d_idx]
        else:
            A[i, i] = 1.0
            
        # 2. 计算非对角线元素
        for j in range(i):
            if s_idx is not None and d_idx is not None:
                A[i, j] = A[j, i] = 0.5 * (A[j, s_idx] + A[j, d_idx])
            elif s_idx is not None:
                A[i, j] = A[j, i] = 0.5 * A[j, s_idx]
            elif d_idx is not None:
                A[i, j] = A[j, i] = 0.5 * A[j, d_idx]
            else:
                A[i, j] = A[j, i] = 0.0
                
    inbreeding_coeffs = {pedigree[i][0]: A[i, i] - 1 for i in range(n)}
    return A, inbreeding_coeffs
```

## 业务规则
- 支持多世代系谱分析
- 自动检测系谱错误和异常
- 考虑性别差异的遗传传递
- 支持不完整系谱分析
- 最大追溯世代数可配置

## 验证方法
- 系谱逻辑一致性检验
- 近交系数理论值验证
- 与遗传标记分析结果对比
- 系谱完整性评估

## 性能指标
- 处理效率 > 10000个个体/小时
- 系谱追溯深度 > 10代
- 计算精度 > 99.9%
- 内存使用与系谱大小成线性关系
