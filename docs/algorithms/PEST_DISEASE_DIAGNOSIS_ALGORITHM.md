# 病虫害诊断算法文档 (Pest & Disease Diagnosis Algorithm Documentation)

## 算法目的
基于图像识别、环境数据和症状描述，诊断作物病虫害类型并提供防治建议。

## 输入参数
- `image_data`: 植株图像数据 (dict)
- `symptom_description`: 症状描述信息 (dict)
- `environmental_conditions`: 环境条件，如温湿度、降雨等 (dict)
- `crop_type`: 作物类型信息 (str)

## 输出结果
- `diagnosis_result`: 诊断结果，包含病虫害类型和置信度 (dict)
- `severity_assessment`: 危害严重程度评估 (dict)
- `control_recommendations`: 防治建议和方案 (dict)

## 算法流程
1. **图像预处理**: 对输入图像进行预处理和特征提取
2. **特征匹配**: 将提取特征与病虫害特征库进行匹配
3. **多模态融合**: 结合图像、症状描述、环境数据进行综合判断
4. **诊断确认**: 生成诊断结果和置信度评估
5. **防治建议生成**: 基于诊断结果生成防治方案
6. **风险评估**: 评估病虫害传播风险

## 具体实现 (Implementation)
```python
def fusion_diagnosis(cv_results, environmental_risk, user_notes):
    """
    多模态病虫害综合诊断逻辑
    cv_results: AI 视觉识别置信度列表 [{'pest': 'aphid', 'conf': 0.85}, ...]
    environmental_risk: 气象触发风险 {'powdery_mildew': 0.9, 'locust': 0.1}
    """
    final_score = {}
    
    # 1. 基础分值取自视觉识别
    for res in cv_results:
        final_score[res['pest']] = res['conf'] * 0.7 # 视觉权重 70%
        
    # 2. 结合气象风险调整 (环境因素可能显著增加某些病害概率)
    for pest, risk in environmental_risk.items():
        if pest in final_score:
            final_score[pest] += risk * 0.3 # 环境权重 30%
        else:
            final_score[pest] = risk * 0.2
            
    # 3. 排序并返回最高置信度结果
    best_match = max(final_score.items(), key=lambda x: x[1])
    
    return {
        'pest_id': best_match[0],
        'confidence': min(best_match[1], 1.0),
        'status': 'confirmed' if best_match[1] > 0.8 else 'requires_review'
    }
```

## 业务规则
- 严格遵循植物保护法规和用药指南
- 优先推荐生物防治和绿色防控方法
- 考虑当地病虫害发生规律
- 支持不同作物的特定病虫害识别

## 验证方法
- 与植物保护专家诊断结果对比
- 田间验证试验
- 识别准确率持续评估

## 性能指标
- 病虫害识别准确率 > 85%
- 诊断响应时间 < 3秒
- 防治建议采纳率 > 70%
