# 基因组选择算法文档 (Genomic Selection Algorithm)

## 算法目的
利用全基因组标记信息预测个体育种值，加速育种进程。

## 输入参数
- `genomic_data`: 全基因组标记数据 (SNP芯片或重测序)
- `phenotypic_data`: 表型数据
- `training_population`: 训练群体
- `validation_population`: 验证群体
- `prediction_population`: 待预测群体
- `model_type`: 预测模型类型 (GBLUP, BayesA, BayesB等)
- `cross_validation_folds`: 交叉验证折数

## 输出结果
- `gEBV`: 基因组育种值 (Genomic Estimated Breeding Values)
- `prediction_accuracy`: 预测准确性
- `genomic_relationship`: 基因组关系矩阵
- `marker_effects`: 标记效应估计
- `selection_candidates`: 选择候选个体
- `variance_components`: 方差组分估计

## 算法流程
1. **数据预处理**: 标记数据质控、缺失值填充、标准化
2. **基因组关系矩阵构建**: 计算个体间基因组关系
3. **模型训练**: 使用训练群体估计标记效应
4. **参数估计**: 估计方差组分和模型参数
5. **基因组育种值预测**: 预测个体gEBV
6. **准确性评估**: 交叉验证评估预测准确性
7. **结果验证**: 与传统方法结果对比

## 具体实现 (Implementation)
```python
def calculate_grm(genotypes):
    """
    计算基因组关系矩阵 (G-matrix)
    genotypes: numpy array (n_individuals, m_markers), 编码为 -1, 0, 1 (或 0, 1, 2)
    """
    n, m = genotypes.shape
    
    # 1. 计算等位基因频率 p_j
    p = (np.sum(genotypes, axis=0) + n) / (2 * n)
    
    # 2. 矩阵 Z 的标准化
    # Z_ij = M_ij - 2(p_j - 0.5)  (针对 -1, 0, 1 编码)
    P = 2 * (p - 0.5)
    Z = genotypes - P
    
    # 3. 计算 G 矩阵
    # G = ZZ' / [2 * Σ p_j(1 - p_j)]
    sum_pq = 2 * np.sum(p * (1 - p))
    G = np.dot(Z, Z.T) / sum_pq
    
    return G

def predict_gebv(G, phenotypes, h2):
    """
    简化的 GBLUP 预测 (Ridge Regression BLUP)
    h2: 遗传力
    """
    n = G.shape[0]
    # lambda = (1 - h2) / h2
    lam = (1 - h2) / h2
    
    # 构建混合线性模型方程 (MME) 简化版
    # (G + I*lambda) * u = y
    I = np.eye(n)
    u = np.linalg.solve(G + I * lam, phenotypes)
    
    return u
```

## 业务规则
- 支持多种基因组选择模型
- 考虑显性效应和上位性效应
- 自动选择最优模型参数
- 支持多性状基因组选择
- 预测准确性阈值 > 0.6

## 验证方法
- 交叉验证评估预测准确性
- 与表型数据相关性验证
- 与系谱BLUP结果对比
- 育种项目验证

## 性能指标
- 预测准确性 > 0.7 (理想条件下)
- 处理效率 > 50000个标记/小时
- 支持 > 10000 个个体分析
- 响应时间 < 30分钟 (1000个个体)
