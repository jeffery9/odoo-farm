# 视觉质量评估算法 (Quality Assessment Algorithm)

## 算法目的
利用计算机视觉技术对收获后的农产品进行自动化外观、尺寸及缺陷检测，实现客观、标准化的质量分级。

## 输入参数
- `image_frame`: 工业相机或 PDA 采集的产品原始图像 (Binary/Array)
- `grading_standards`: 行业质量分级参数（大小、色泽阈值） (Dict)
- `defect_library`: 常见缺陷（病斑、裂痕）特征库 (Model/Tensor)

## 输出结果
- `product_grade`: 最终判定的质量等级 (Selection: A, B, C, Unqualified)
- `defect_score`: 缺陷密度评分 (Float)
- `shelf_life_prediction`: 基于表观状态的预计剩余货架期 (Integer)

## 算法流程
1. **几何特征提取**: 测量长径、横径及体积，判定尺寸级别。
2. **色泽分布分析**: 计算 HIS 色彩空间分布，对比品种标准熟度模型。
3. **缺陷分割**: 使用卷积神经网络（CNN）定位表皮病斑、虫咬或机械损伤区域。
4. **分级判定**: 综合尺寸、颜色及缺陷评分，映射至对应的商贸等级。
5. **溯源绑定**: 将分级结果写入批次（Lot）属性，自动打印分级标签。

## 具体实现 (Implementation)
```python
def classify_grade(size_mm, defect_ratio, color_score, standards):
    """
    质量分级决策树实现
    standards: {'min_size_A': 80, 'max_defect_A': 0.05, 'target_color': 0.9}
    """
    # 1. 判定 A 级
    if (size_mm >= standards['min_size_A'] and 
        defect_ratio <= standards['max_defect_A'] and 
        color_score >= standards['target_color']):
        return 'A'
        
    # 2. 判定 B 级
    if (size_mm >= standards.get('min_size_B', 60) and 
        defect_ratio <= 0.15):
        return 'B'
        
    # 3. 判定 C 级
    if defect_ratio <= 0.30:
        return 'C'
        
    return 'unqualified'
```

## 业务规则
- **模糊判定回退**: 若 AI 置信度 < 0.7，系统需强制生成“人工复核”Activity 并挂起该批次。
- **动态阈值**: 根据不同销售渠道（如出口 vs 内销）的要求，动态载入对应的 `grading_standards`。

## 验证方法
- 使用带有专家标签的真值数据集进行混淆矩阵分析。

## 性能指标
- 单个样本推理时间 < 100ms。
- 与人工专家分级的一致性 > 92%。