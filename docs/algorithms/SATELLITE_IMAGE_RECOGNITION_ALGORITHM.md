# 卫星图像识别算法文档 (Satellite Image Recognition Algorithm)

## 算法目的
基于卫星遥感数据进行作物长势监测、作物类型识别、植被健康评估等农业应用，支持精准农业决策。

## 输入参数
- `satellite_image`: 多光谱卫星图像数据 (dict包含B4红光波段和B8近红外波段)
- `cloud_cover`: 云层覆盖率阈值 (float, 默认 < 10%)
- `bounding_box`: 地块边界坐标 (dict 包含经纬度边界)
- `grid_resolution`: 网格分辨率 (float, 米)
- `field_polygon`: 地块多边形边界 (PostGIS geometry)
- `multi_spectral_data`: 多光谱数据 (包含多个波段)
- `crop_type`: 作物类型
- `growth_stage`: 生长阶段
- `solar_angle`: 太阳角度参数
- `view_angle`: 卫星观测角度

## 输出结果
- `ndvi_raster`: NDVI栅格数组 (numpy array)
- `vegetation_mask`: 植被覆盖区域掩码 (numpy array)
- `health_zones`: 健康状况分类区域 (dict)
- `growth_anomaly`: 生长异常区域识别 (dict)
- `vra_prescription`: 变量作业处方图 (dict)
- `change_map`: 变化检测结果图
- `crop_map`: 作物类型分类图
- `health_score`: 健康评分 (0-100)
- `lai_values`: 叶面积指数值
- `classification_confidence`: 分类置信度

## 算法流程
1. **数据获取**: 从Sentinel-2或Landsat卫星数据中提取多光谱波段
2. **预处理**: 质量控制、云层掩码、几何校正、辐射校正
3. **植被指数计算**: 计算NDVI、EVI、SAVI等植被指数
4. **空间分析**: 通过PostGIS将卫星栅格数据映射到地块网格
5. **变化检测**: 检测不同时期卫星图像之间的变化
6. **作物分类**: 使用机器学习算法识别作物类型
7. **健康评估**: 综合多种指数评估植被健康状况
8. **叶面积指数反演**: 反演叶面积指数和生物量
9. **统计分析**: 计算各网格的统计指标和趋势分析
10. **异常检测**: 识别NDVI值异常的区域
11. **处方生成**: 基于分析结果生成变量作业处方

## 具体实现 (Implementation)
```python
import numpy as np

def analyze_vegetation_health(spectral_bands):
    """
    植被健康综合评分算法 (VCI - Vegetation Condition Index)
    spectral_bands: {'red': array, 'nir': array, 'blue': array}
    """
    red = spectral_bands['red'].astype(float)
    nir = spectral_bands['nir'].astype(float)
    blue = spectral_bands['blue'].astype(float)
    
    # 1. 计算 NDVI
    ndvi = (nir - red) / (nir + red + 1e-10)
    
    # 2. 计算 EVI (增强植被指数, 减少大气和背景干扰)
    # EVI = G * (NIR - RED) / (NIR + C1 * RED - C2 * BLUE + L)
    evi = 2.5 * (nir - red) / (nir + 6 * red - 7.5 * blue + 1 + 1e-10)
    
    # 3. 综合健康评分 (0-100)
    # 基于 NDVI 和 EVI 的加权组合
    health_score = (0.6 * np.mean(ndvi) + 0.4 * np.mean(evi)) * 100
    
    return {
        'ndvi_avg': np.mean(ndvi),
        'evi_avg': np.mean(evi),
        'health_score': np.clip(health_score, 0, 100),
        'anomaly_ratio': np.sum(ndvi < 0.2) / ndvi.size
    }
```

## 业务规则
- NDVI值范围: -1.0 到 +1.0
- 绿色植被: NDVI > 0.2
- 健康植被: NDVI > 0.5
- 高密度植被: NDVI > 0.7
- 支持多种卫星源数据 (Sentinel-2, Landsat, MODIS)
- 自动过滤云层覆盖区域
- 支持时间序列分析
- 不同作物类型使用不同健康评估模型
- 考虑生长阶段的动态评估标准

## 验证方法
- 与地面实测数据对比验证
- 时间序列一致性检查
- 邻近地块对比验证
- 历史数据回归分析
- 独立验证样本验证
- 交叉验证
- 混淆矩阵分析

## 性能指标
- NDVI计算响应时间 < 60秒
- 处理效率 > 1000公顷/分钟
- 分类精度 > 85%
- NDVI计算精度 > 95%
- 健康评估准确率 > 80%
- 反演精度R² > 0.7
- 支持大规模区域批量处理
- 支持并发处理多区域数据
