# 多时相卫星变化检测算法文档 (Multi-temporal Satellite Change Detection Algorithm)

## 算法目的
检测不同时期卫星图像之间的变化，识别作物生长变化、病虫害发展等，为农业管理决策提供支持。

## 输入参数
- `image_t1`: 时相1的卫星图像
- `image_t2`: 时相2的卫星图像
- `analysis_period`: 分析周期 (天)
- `change_threshold`: 变化阈值 (float)
- `field_polygon`: 地块多边形边界 (PostGIS geometry)
- `cloud_cover_threshold`: 云层覆盖率阈值 (float)

## 输出结果
- `change_map`: 变化检测结果图
- `change_type`: 变化类型分类 (植被增加/减少、病虫害、其他)
- `change_intensity`: 变化强度 (百分比)
- `temporal_trend`: 时间趋势分析
- `alert_zones`: 需要关注的区域 (dict)
- `severity_index`: 变化严重程度指数

## 算法流程
1. **图像配准**: 对不同时期图像进行几何配准和辐射校正
2. **光谱指数计算**: 计算NDVI、EVI等植被指数差值
3. **变化检测**: 计算差值图像和变化比率
4. **变化分类**: 使用分类算法识别变化类型
5. **统计分析**: 计算变化面积和强度
6. **置信度评估**: 评估变化检测的可信度
7. **预警生成**: 基于变化强度生成预警信息

## 具体实现 (Implementation)
```python
import numpy as np

def detect_ndvi_change(ndvi_t1, ndvi_t2, threshold=0.15):
    """
    基于 NDVI 差值的植被变化检测
    ndvi_t1: 前期 NDVI 矩阵
    ndvi_t2: 后期 NDVI 矩阵
    """
    # 1. 计算差值矩阵
    diff = ndvi_t2 - ndvi_t1
    
    # 2. 识别显著变化区域
    # Positive Change (长势增加): diff > threshold
    # Negative Change (长势衰减/受灾): diff < -threshold
    
    significant_increase = diff > threshold
    significant_decrease = diff < -threshold
    
    # 3. 统计指标
    n_pixels = diff.size
    pct_increase = np.sum(significant_increase) / n_pixels * 100
    pct_decrease = np.sum(significant_decrease) / n_pixels * 100
    
    # 4. 生成警报级别
    severity = 0
    if pct_decrease > 30: # 超过 30% 面积严重衰减
        severity = 3 # 高危
    elif pct_decrease > 10:
        severity = 2 # 预警
        
    return {
        'diff_matrix': diff.tolist(),
        'pct_increase': pct_increase,
        'pct_decrease': pct_decrease,
        'severity_index': severity,
        'alert_needed': severity >= 2
    }
```

## 业务规则
- 支持多种植被指数用于变化检测
- 变化阈值可配置，考虑作物类型差异
- 季节性变化自动校正，避免假阳性
- 自动过滤云层影响区域
- 变化严重程度分级管理

## 验证方法
- 与地面调查数据对比
- 现场验证变化区域
- 时间序列一致性验证
- 历史变化模式验证

## 性能指标
- 处理效率 > 1000公顷/分钟
- 检测精度 > 90%
- 响应时间 < 120秒
- 支持大规模区域批量处理
