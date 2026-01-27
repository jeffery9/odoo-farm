# 叶面积指数(LAI)反演算法文档 (Leaf Area Index Retrieval from Satellite Algorithm)

## 算法目的
从卫星遥感数据反演叶面积指数，评估作物冠层结构和生长状态。

## 输入参数
- `spectral_data`: 光谱数据
- `solar_angle`: 太阳角度参数
- `view_angle`: 卫星观测角度
- `crop_parameters`: 作物参数 (叶倾角分布、反射率等)
- `atmospheric_data`: 大气校正参数
- `field_polygon`: 地块边界 (PostGIS geometry)

## 输出结果
- `lai_values`: 叶面积指数值
- `canopy_cover`: 冠层覆盖度
- `biomass_estimate`: 生物量估算
- `growth_stage`: 生长阶段评估
- `lai_accuracy`: 反演精度评估
- `quality_flag`: 数据质量标志

## 算法流程
1. **光谱建模**: 建立光谱-叶面积指数的物理或统计模型
2. **参数反演**: 使用光谱数据反演叶面积指数
3. **质量控制**: 数据筛选和异常值处理
4. **精度评估**: 误差估计和不确定性分析
5. **后处理**: 空间插值和平滑处理
6. **生物量转换**: 将LAI转换为生物量估算

## 具体实现 (Implementation)
```python
import numpy as np

def retrieve_lai_empirical(ndvi_raster):
    """
    基于 NDVI 的经验模型反演 LAI
    模型: LAI = 3.61 * NDVI^2 + 0.11 * NDVI (Clevers et al.)
    或者经典的指数模型: LAI = -1/k * ln((NDVI_max - NDVI)/(NDVI_max - NDVI_soil))
    """
    # 采用指数模型实现
    k = 0.8 # 消光系数
    ndvi_max = 0.92
    ndvi_soil = 0.15
    
    # 裁剪并防错
    ndvi = np.clip(ndvi_raster, ndvi_soil + 0.01, ndvi_max - 0.01)
    
    # 计算 LAI
    lai = -(1/k) * np.log((ndvi_max - ndvi) / (ndvi_max - ndvi_soil))
    
    return {
        'lai_raster': lai.tolist(),
        'mean_lai': np.mean(lai),
        'canopy_cover': (1 - np.exp(-k * lai)).tolist(), # 基于 Beer 定律估算覆盖度
        'max_lai': np.max(lai)
    }
```

## 业务规则
- 支持多种反演模型 (经验模型、物理模型、神经网络)
- 考虑观测几何影响
- 提供精度评估和质量标志
- 不同作物类型使用不同反演参数
- 支持时间序列LAI分析

## 验证方法
- 与地面实测LAI对比
- 与其他遥感产品对比
- 时间序列一致性验证
- 不同传感器交叉验证

## 性能指标
- 反演精度R² > 0.7
- 处理效率 > 200平方公里/小时
- 响应时间 < 45秒
- LAI值范围: 0-10 (典型农作物)
