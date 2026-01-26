# 克里金插值算法文档 (Kriging Interpolation Algorithm)

## 算法目的
利用离散的土壤采样点数据，通过克里金插值算法转化为覆盖全网格的连续养分分布图层。

## 输入参数
- `sample_points`: 采样点坐标和数值数据 (list of dict with x, y, value)
- `grid_boundary`: 目标网格边界 (Polygon geometry)
- `variogram_model`: 变差图模型类型（如 spherical, exponential, gaussian）(str)
- `resolution`: 插值网格分辨率 (float)

## 输出结果
- `interpolated_grid`: 插值后的网格数据 (2D array)
- `uncertainty_map`: 不确定性评估图 (2D array)
- `variogram_params`: 变差图模型参数 (dict)
- `interpolation_accuracy`: 插值精度评估 (dict)

## 算法流程
1. **变差图建模**: 计算样本点间的距离和方差，拟合变差图模型
2. **权重计算**: 根据变差图模型计算每个采样点对目标位置的权重
3. **克里金估计**: 使用加权线性组合计算目标位置的预测值
4. **不确定性评估**: 计算插值结果的方差和置信区间
5. **网格化输出**: 将插值结果映射到目标网格系统

## 业务规则
- 支持多种变差图模型：球面模型、指数模型、高斯模型
- 考虑空间自相关性和各向异性
- 提供插值不确定性评估
- 支持大规模采样点数据处理

## 验证方法
- 交叉验证（留一法验证）
- 与实际采样点数据对比
- 与传统插值方法（反距离权重等）对比验证

## 性能指标
- 大持数千个采样点的高效插值
- 计算响应时间 < 30秒（针对中等规模数据）
- 插值精度高于传统方法 10-15%