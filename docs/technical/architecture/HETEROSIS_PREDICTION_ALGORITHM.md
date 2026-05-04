# 杂种优势预测算法文档 (Heterosis Prediction Algorithm)

## 算法目的
预测杂交组合的杂种优势，优化杂交育种策略。

## 输入参数
- `parent_genotypes`: 亲本基因型数据
- `parent_phenotypes`: 亲本表型数据
- `combining_ability_data`: 配合力数据
- `genetic_distance`: 遗传距离矩阵
- `hybrid_combinations`: 杂交组合
- `trait_data`: 目标性状数据
- `dominance_effects`: 显性效应参数

## 输出结果
- `heterosis_prediction`: 杂种优势预测值
- `mid_parent_heterosis`: 中亲优势
- `high_parent_heterosis`: 超亲优势
- `best_combinations`: 最优杂交组合
- `genetic_compatibility`: 遗传兼容性评分
- `breeding_strategy`: 育种策略建议

## 算法流程
1. **亲本评估**: 分析亲本一般配合力和特殊配合力
2. **遗传距离计算**: 计算亲本间遗传距离
3. **优势预测**: 基于基因型和表型数据预测杂种优势
4. **组合优化**: 评估所有可能的杂交组合
5. **模型验证**: 验证预测模型的准确性
6. **策略制定**: 生成杂交育种策略
7. **结果排序**: 按预期优势排序杂交组合

## 具体实现 (Implementation)
```python
def predict_heterosis(male_phenotype, female_phenotype, combining_ability):
    """
    预测杂交优势
    combining_ability: {'gca_male': float, 'gca_female': float, 'sca': float}
    """
    # 1. 计算中亲均值 (Mid-Parent Value, MPV)
    mpv = (male_phenotype + female_phenotype) / 2.0
    
    # 2. 计算预期杂交值 (Predicted Hybrid Value, PHV)
    # PHV = General Combining Ability (GCA) + Specific Combining Ability (SCA)
    phv = combining_ability['gca_male'] + combining_ability['gca_female'] + combining_ability['sca']
    
    # 3. 计算杂种优势百分比
    # MPH = (PHV - MPV) / MPV * 100
    mph = ((phv - mpv) / mpv) * 100 if mpv != 0 else 0.0
    
    return {
        'predicted_value': phv,
        'mid_parent_value': mpv,
        'heterosis_percent': mph,
        'recommendation': 'High' if mph > 15 else 'Standard'
    }
```

## 业务规则
- 考虑加性和显性遗传效应
- 支持多性状杂种优势预测
- 遗传距离与杂种优势关系建模
- 考虑亲本特异性状互补
- 预测准确性 > 70%

## 验证方法
- 与实际杂交结果对比验证
- 历史杂交数据验证
- 不同性状预测准确性评估
- 遗传模型验证

## 性能指标
- 杂种优势预测准确性 > 0.7
- 处理效率 > 1000杂交组合/小时
- 支持多性状同时预测
- 响应时间 < 1分钟 (100个组合)
