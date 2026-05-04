# 作物类型识别与分类算法文档 (Satellite-based Crop Type Classification Algorithm)

## 算法目的
基于卫星光谱特征识别和分类不同作物类型，支持作物分布制图和种植结构分析。

## 输入参数
- `multi_spectral_data`: 多光谱数据 (包含多个波段)
- `training_samples`: 训练样本 (已知作物类型区域)
- `classification_method`: 分类方法 (SVM、随机森林、深度学习)
- `crop_types`: 目标作物类型列表
- `phenological_info`: 物候期信息
- `spatial_resolution`: 空间分辨率 (米)

## 输出结果
- `crop_map`: 作物类型分类图
- `classification_confidence`: 分类置信度
- `crop_area_statistics`: 作物面积统计
- `phenological_stage`: 物候期识别
- `accuracy_assessment`: 分类精度评估
- `mixed_pixel_analysis`: 混合像元分析结果

## 算法流程
1. **特征提取**: 提取光谱、纹理、时序特征
2. **模型训练**: 使用已知样本训练分类模型
3. **分类预测**: 对整个区域进行作物类型分类
4. **后处理**: 空间滤波和边界优化
5. **精度评估**: 计算分类精度和混淆矩阵
6. **结果验证**: 使用独立样本验证分类结果

## 具体实现 (Implementation)
```python
from sklearn.ensemble import RandomForestClassifier
import numpy as np

def classify_crop_types(bands_data, labels, locations):
    """
    基于随机森林的作物分类实现
    bands_data: numpy array (n_pixels, n_bands)
    labels: 训练标签
    locations: 训练位置索引
    """
    # 1. 提取训练特征
    X_train = bands_data[locations]
    y_train = labels
    
    # 2. 训练分类器 (Random Forest)
    clf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    clf.fit(X_train, y_train)
    
    # 3. 执行全场预测
    full_crop_map = clf.predict(bands_data)
    probabilities = clf.predict_proba(bands_data)
    
    # 4. 统计结果
    unique, counts = np.unique(full_crop_map, return_counts=True)
    stats = dict(zip(unique.tolist(), counts.tolist()))
    
    return {
        'crop_map': full_crop_map.tolist(),
        'area_stats': stats,
        'mean_confidence': np.mean(np.max(probabilities, axis=1)),
        'feature_importance': clf.feature_importances_.tolist()
    }
```

## 业务规则
- 支持主要农作物类型识别 (玉米、小麦、水稻、大豆等)
- 时序特征提高分类精度
- 支持混合像元分解
- 根据作物物候期优化分类
- 分类结果支持人工校正

## 验证方法
- 独立验证样本验证
- 交叉验证
- 混淆矩阵分析
- 与农业统计数据对比
- 专家评估验证

## 性能指标
- 分类精度 > 85%
- 处理速度 > 500公顷/分钟
- 支持大区域并行处理
- 模型训练时间 < 30分钟
