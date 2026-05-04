# 植被健康状况评估算法文档 (Satellite-based Vegetation Health Assessment Algorithm)

## 算法目的
综合多种植被指数评估作物健康状况，识别胁迫区域并提供管理建议。

## 输入参数
- `ndvi`: NDVI植被指数
- `evi`: 增强植被指数
- `savi`: 土壤调节植被指数
- `crop_type`: 作物类型
- `growth_stage`: 生长阶段
- `field_polygon`: 地块边界 (PostGIS geometry)
- `historical_data`: 历史植被指数数据

## 输出结果
- `health_score`: 健康评分 (0-100)
- `stress_indicators`: 胁迫指标
- `health_zones`: 健康分区
- `intervention_recommendation`: 干预建议
- `stress_type`: 胁迫类型分类 (干旱、病虫害、营养缺乏等)
- `trend_analysis`: 健康趋势分析

## 算法流程
1. **指数计算**: 计算多种植被健康指数
2. **标准化处理**: 将各指数标准化到统一尺度
3. **权重融合**: 结合作物类型和生长阶段权重
4. **健康评估**: 生成健康评分和分区
5. **胁迫识别**: 识别不同类型胁迫
6. **建议生成**: 基于健康状况生成管理建议
7. **趋势分析**: 分析健康状况的时间趋势

## 具体实现 (Implementation)
```python
import numpy as np

def evaluate_health_index(metrics, stage_weights):
    """
    植被健康加权评分
    metrics: {'ndvi': 0.65, 'evi': 0.45, 'savi': 0.55}
    stage_weights: {'ndvi': 0.5, 'evi': 0.3, 'savi': 0.2}
    """
    score = 0.0
    for key, weight in stage_weights.items():
        score += metrics.get(key, 0.0) * weight
        
    # 标准化到 0-100
    final_score = score * 100
    
    # 胁迫识别逻辑 (示例：若 NDVI 低于 0.3 则标记风险)
    stress_detected = False
    if metrics.get('ndvi', 1.0) < 0.3:
        stress_detected = True
        
    return {
        'health_score': round(final_score, 2),
        'status': 'Healthy' if final_score > 70 else 'Monitor' if final_score > 40 else 'Stressed',
        'stress_warning': stress_detected
    }
```

## 业务规则
- 不同作物类型使用不同健康评估模型
- 考虑生长阶段对健康评估的影响
- 健康评分分级管理 (优、良、中、差)
- 自动识别胁迫类型
- 结合历史数据进行比较分析

## 验证方法
- 与田间实测健康状况对比
- 专家评估验证
- 与农事活动记录关联验证
- 历史数据一致性验证

## 性能指标
- 评估准确率 > 80%
- 响应时间 < 30秒
- 支持实时健康状态更新
- 胁迫识别准确率 > 75%
