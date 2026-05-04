# 分子标记辅助选择算法文档 (Marker Assisted Selection Algorithm)

## 算法目的
基于分子标记信息进行辅助选择，提高育种效率和准确性。

## 输入参数
- `marker_genotype`: 标记基因型数据
- `trait_values`: 目标性状表型值
- `selection_intensity`: 选择强度
- `heritability`: 遗传力估计
- `marker_effects`: 标记效应值
- `population_size`: 群体大小
- `selection_cycle`: 选择世代数

## 输出结果
- `selection_index`: 选择指数
- `selected_individuals`: 选中个体
- `selection_gain`: 选择增益预测
- `molecular_score`: 分子标记评分
- `crossing_suggestions`: 杂交组合建议
- `breeding_value`: 育种值估计

## 算法流程
1. **标记筛选**: 基于效应大小和显著性筛选有效标记
2. **效应估计**: 估计标记对目标性状的效应
3. **选择指数计算**: 组合多个性状的标记信息
4. **个体排序**: 根据选择指数对个体排序
5. **选择决策**: 根据选择强度确定入选个体
6. **增益预测**: 预测选择响应和遗传增益
7. **杂交设计**: 基于互补性设计杂交组合

## 具体实现 (Implementation)
```python
def calculate_marker_score(genotypes, effects):
    """
    计算分子标记评分 (Molecular Score)
    genotypes: dict {individual_id: [m1, m2, ... mk]} (编码为 0, 1, 2)
    effects: list [e1, e2, ... ek] (对应标记的单位替代效应)
    """
    scores = {}
    for ind_id, g_vec in genotypes.items():
        # 分子评分 = Σ (基因型值 * 效应值)
        score = sum(g * e for g, e in zip(g_vec, effects))
        scores[ind_id] = score
        
    return scores

def select_candidates(scores, top_pct=0.1):
    """
    执行选择
    """
    sorted_ids = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    n_select = max(int(len(sorted_ids) * top_pct), 1)
    
    selected = sorted_ids[:n_select]
    return {
        'selected_ids': [x[0] for x in selected],
        'min_score': selected[-1][1],
        'mean_score': sum(x[1] for x in selected) / n_select
    }
```

## 业务规则
- 多性状选择考虑性状间相关性
- 标记效应显著性阈值 p < 0.05
- 支持单性状和多性状选择
- 考虑连锁不平衡和背景遗传效应
- 平衡选择强度和遗传多样性

## 验证方法
- 与表型选择结果对比
- 预测准确性验证
- 选择响应验证
- 遗传增益验证

## 性能指标
- 选择准确性 > 80%
- 计算效率 > 10000个体/小时
- 响应时间 < 10秒 (1000个体)
- 预测相关性 > 0.7
