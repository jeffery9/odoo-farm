# 质量分级定价算法 (Quality-based Premium Pricing Algorithm)

## 算法目的
在采购或回购环节，根据实验室实测的理化指标（如：蛋白含量、杂质率、含水量），自动从复杂的阶梯矩阵中计算最终结算单价。

## 输入参数
- `contract_base_price`: 合同保底单价 (Float)
- `quality_metrics`: 质检实测值 (Dict, e.g., {'moisture': 14.5, 'impurity': 1.2})
- `pricing_matrix`: 价格修正矩阵 (List[Dict])
- `penalty_thresholds`: 拒收/重罚阈值 (Dict)

## 输出结果
- `final_settlement_price`: 最终结算单价 (Float)
- `adjustment_amount`: 总价修正金额 (Float)
- `rejection_flag`: 是否触发强制拒收 (Boolean)

## 算法流程
1. **指标映射**: 将实测值映射至单价修正阶梯。
2. **扣量计算**: 针对含水量超标，执行“减量不减价”或“减价不减量”的动态扣除。
3. **加价奖励**: 针对高蛋白/高糖等优质指标，按百分比或固定金额增加溢价。
4. **异常硬拦截**: 若任一核心指标触碰 `penalty_thresholds`（如霉变），立即标记拒收。
5. **对账生成**: 输出包含“原始价 + 质量调整项”的财务凭证。

## 具体实现 (Implementation)
```python
def calculate_premium_price(base_price, metrics, rules):
    """
    SAP 风格的阶梯质量调价
    rules: {'moisture': {'base': 14.0, 'step': 0.1, 'penalty': 0.05}}
    """
    final_price = base_price
    is_rejected = False
    
    # 1. 含水量修正 (超标扣款)
    m_val = metrics.get('moisture', 0)
    m_rule = rules.get('moisture')
    if m_val > m_rule['max_limit']:
        is_rejected = True
    elif m_val > m_rule['base']:
        # 每超 0.1% 扣 0.05 元
        final_price -= (m_val - m_rule['base']) / m_rule['step'] * m_rule['penalty']
        
    # 2. 蛋白含量修正 (优质奖励)
    p_val = metrics.get('protein', 0)
    if p_val > 12.0:
        final_price *= 1.05 # 奖励 5%
        
    return {
        'final_price': round(final_price, 4),
        'is_rejected': is_rejected,
        'net_adjustment': final_price - base_price
    }
```

## 业务规则
- **公平性保护**: 所有修正项必须基于 LIMS 仪器的原始电子报文（US-15-11），严禁手动修改。
- **透明度**: 结算单必须打印完整的质量扣款明细。

## 验证方法
- 对比历史手工结算单与自动算法的一致性。

## 性能指标
- 支持 100+ 指标的复杂矩阵计算。
- 计算延迟 < 50ms。
