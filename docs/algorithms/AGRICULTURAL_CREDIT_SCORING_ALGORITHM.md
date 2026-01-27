# 农业信用评分算法文档 (Agricultural Credit Scoring Algorithm)

## 算法目的
基于农业生产数据计算农户信用评分，用于农业金融信贷和保险服务。

## 输入参数
- `gps_conformance`: GPS围栏重合度数据 (float)
- `compliance_records`: 合规记录（休药期拦截等）(list)
- `yield_volatility`: 产量波动率数据 (float)
- `precision_agriculture_usage`: 变量施肥等精准农业使用情况 (float)
- `historical_data`: 历史农业生产数据 (dict)

## 输出结果
- `credit_score`: 农业信用评分 (float)
- `score_breakdown`: 各维度评分构成 (dict)
- `risk_assessment`: 风险评估结果 (str)
- `recommendation`: 信贷建议 (str)

## 算法流程
1. **维度评分**: 计算各维度得分
   - 真实性（GPS围栏重合度，权重30%）: PostGIS ST_Contains 验证
   - 合规性（休药期拦截记录，权重30%）: 检查违规记录
   - 稳产性（产量波动率，权重20%）: 历史标准差分析
   - 环保性（变量施肥比例，权重20%）: 精准农业技术应用比例
2. **权重计算**: 加权计算综合信用分
3. **风险评估**: 根据信用分进行风险等级划分
4. **动态更新**: 定期运行 Cron 任务刷新信用评分

## 具体实现 (Implementation)
```python
def calculate_agricultural_credit_score(data):
    """
    计算农业信用评分的核心逻辑
    data: {
        'gps_conformance': 0.95, 
        'violations_count': 0, 
        'yield_cv': 0.12, 
        'vra_usage': 0.8
    }
    """
    # 1. 真实性得分 (权重 30%)
    authenticity_score = data['gps_conformance'] * 100
    
    # 2. 合规性得分 (权重 30%)
    # 基础分 100，每次违规扣 20 分
    compliance_score = max(100 - (data['violations_count'] * 20), 0)
    
    # 3. 稳产性得分 (权重 20%)
    # 变异系数 CV 越低，得分越高
    stability_score = max(100 * (1 - data['yield_cv']), 0)
    
    # 4. 环保性得分 (权重 20%)
    environmental_score = data['vra_usage'] * 100
    
    # 综合得分
    final_score = (
        authenticity_score * 0.3 +
        compliance_score * 0.3 +
        stability_score * 0.2 +
        environmental_score * 0.2
    )
    
    risk_level = 'Low' if final_score > 80 else 'Medium' if final_score > 60 else 'High'
    
    return {
        'credit_score': round(final_score, 2),
        'risk_assessment': risk_level,
        'breakdown': {
            'authenticity': authenticity_score,
            'compliance': compliance_score,
            'stability': stability_score,
            'environmental': environmental_score
        }
    }
```

## 业务规则
- 真实性维度权重 30%（GPS 围栏重合度）
- 合规性维度权重 30%（休药期拦截记录）
- 稳产性维度权重 20%（产量波动率 CV）
- 环保性维度权重 20%（变量施肥比例）
- 定期自动更新农户信用评分

## 验证方法
- 与历史违约率数据相关性分析
- 与传统信用评估方法对比
- 实际信贷风险验证

## 性能指标
- 信用评分计算响应时间 < 3秒
- 风险预测准确性 > 80%
- 支持大规模农户批量评分
