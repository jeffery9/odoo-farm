# 养分平衡算法文档 (Nutrient Balance Algorithm Documentation)

## 算法目的
计算施肥前后土壤养分变化，推荐最优施肥方案，确保作物获得充足养分的同时避免过度施肥造成环境污染。

## 输入参数
- `soil_analysis`: 土壤检测结果，包含 N、P、K 等养分含量 (dict)
- `crop_requirements`: 作物养分需求，包含目标产量下的养分需求量 (dict)
- `fertilizer_inventory`: 可用肥料库存及成分信息 (list)
- `target_yield`: 目标产量 (float)

## 输出结果
- `recommended_fertilization`: 推荐施肥方案 (dict)
- `post_fertilization_balance`: 施肥后养分平衡预测 (dict)
- `environmental_risk`: 环境风险评估 (dict)

## 算法流程
1. **土壤养分评估**: 分析当前土壤养分状况
2. **作物需求计算**: 根据目标产量计算作物总养分需求
3. **养分缺口计算**: 计算土壤养分与作物需求的差值
4. **肥料配比优化**: 基于可用肥料计算最优配比方案
5. **环境影响评估**: 评估施肥方案对环境的潜在影响
6. **方案推荐**: 生成施肥建议及施用时间表

## 具体实现 (Implementation)
```python
import numpy as np

def calculate_nutrient_balance(soil_data, requirements, fertilizers, area):
    """
    计算养分平衡与施肥建议
    soil_data: {'N': 150, 'P': 20, 'K': 180} (单位: mg/kg)
    requirements: {'N': 200, 'P': 40, 'K': 220} (总需求 单位: kg)
    fertilizers: [{'id': 1, 'name': 'Urea', 'N_pct': 0.46, 'P_pct': 0, 'K_pct': 0}, ...]
    """
    # 1. 简化的土壤有效养分折算 (mg/kg -> kg/地块)
    # 假设耕层深度 20cm, 土壤密度 1.3g/cm3
    soil_weight_per_unit = area * 260 # 260 ton/unit approx
    current_nutrients = {k: (v * soil_weight_per_unit / 1000) for k, v in soil_data.items()}
    
    # 2. 计算缺口
    gaps = {k: max(requirements[k] - current_nutrients.get(k, 0), 0) for k in requirements}
    
    # 3. 简单的肥料组合选择 (贪心法或线性规划初步)
    # 此处示例仅针对单一元素缺口填充
    recommendation = []
    for element, gap in gaps.items():
        if gap > 0:
            # 找到该元素含量最高的肥料
            best_fit = max(fertilizers, key=lambda x: x.get(f'{element}_pct', 0))
            pct = best_fit.get(f'{element}_pct', 0)
            if pct > 0:
                qty = gap / pct
                recommendation.append({
                    'fertilizer_id': best_fit['id'],
                    'qty': qty,
                    'element': element
                })
                
    return recommendation
```

## 业务规则
- 严格遵循国家施肥标准和环保要求
- 优先使用有机肥，合理搭配化肥
- 考虑土壤 pH 值对养分吸收的影响
- 避免养分拮抗作用（如磷锌拮抗）

## 验证方法
- 与农业专家经验数据对比验证
- 历史施肥效果回溯分析
- 田间试验数据验证

## 性能指标
- 计算时间 < 1秒
- 推荐准确性 > 90%
- 与实际效果的偏差 < 10%
