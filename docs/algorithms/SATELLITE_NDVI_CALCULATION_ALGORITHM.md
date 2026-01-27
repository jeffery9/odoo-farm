# 卫星NDVI植被指数算法文档 (Satellite NDVI Calculation Algorithm)

## 算法目的
基于卫星遥感数据计算植被指数(NDVI)，用于监测作物长势、识别问题区域并支持变量作业决策。

## 输入参数
- `satellite_image`: 多光谱卫星图像数据 (dict包含B4红光波段和B8近红外波段)
- `cloud_cover`: 云层覆盖率阈值 (float, 默认 < 10%)
- `bounding_box`: 地块边界坐标 (dict 包含经纬度边界)
- `grid_resolution`: 网格分辨率 (float, 米)
- `field_polygon`: 地块多边形边界 (PostGIS geometry)

## 输出结果
- `ndvi_raster`: NDVI栅格数组 (numpy array)
- `vegetation_mask`: 植被覆盖区域掩码 (numpy array)
- `health_zones`: 健康状况分类区域 (dict)
- `growth_anomaly`: 生长异常区域识别 (dict)
- `vra_prescription`: 变量作业处方图 (dict)

## 算法流程
1. **数据获取**: 从Sentinel-2或Landsat卫星数据中提取近红外和红光波段
2. **预处理**: 质量控制、云层掩码、几何校正
3. **NDVI计算**: 使用公式 `NDVI = (NIR - Red) / (NIR + Red)`
4. **空间分析**: 通过PostGIS将卫星栅格数据映射到地块网格
5. **统计分析**: 计算各网格的统计指标（均值、标准差、变异系数）
6. **异常检测**: 识别NDVI值异常的区域
7. **处方生成**: 基于NDVI分析结果生成变量作业处方

## 具体实现 (Implementation)
```python
import numpy as np

def calculate_ndvi(red_band, nir_band):
    """
    计算 NDVI 矩阵
    red_band: numpy array (波段 4)
    nir_band: numpy array (波段 8)
    """
    # 1. 浮点化与防零处理
    red = red_band.astype(float)
    nir = nir_band.astype(float)
    
    # 2. 执行公式: (NIR - Red) / (NIR + Red)
    # 使用 np.divide 的 where 参数处理分母为 0 的情况
    numerator = nir - red
    denominator = nir + red
    
    ndvi = np.divide(numerator, denominator, out=np.zeros_like(numerator), where=denominator!=0)
    
    # 3. 长势分级映射
    # 0.2 以下: 裸土/建筑; 0.2-0.5: 长势一般; > 0.5: 健康
    status_map = np.zeros_like(ndvi)
    status_map[ndvi > 0.2] = 1 # 一般
    status_map[ndvi > 0.5] = 2 # 良好
    status_map[ndvi > 0.7] = 3 # 极佳
    
    return {
        'ndvi_matrix': ndvi,
        'mean_ndvi': np.mean(ndvi[ndvi > 0]),
        'health_zones': status_map.tolist()
    }
```

## 业务规则
- NDVI值范围: -1.0 到 +1.0
- 绿色植被: NDVI > 0.2
- 健康植被: NDVI > 0.5
- 高密度植被: NDVI > 0.7
- 支持多种卫星源数据
- 自动过滤云层覆盖区域
- 支持时间序列分析

## 验证方法
- 与地面实测数据对比验证
- 时间序列一致性检查
- 邻近地块对比验证
- 历史数据回归分析

## 性能指标
- 卫星数据处理响应时间 < 60秒
- NDVI计算精度 > 95%
- 支持大规模区域批量处理
