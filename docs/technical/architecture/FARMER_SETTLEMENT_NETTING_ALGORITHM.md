# 农户对冲结算算法 (Farmer Settlement Netting Algorithm)

## 算法目的
处理“公司+农户”模式下的双向账务：自动抵减农户前期的农资赊销款、预付款与当前的交售货款，输出净额支付指令。

## 输入参数
- `gross_purchase_value`: 本次交售总金额 (Float)
- `outstanding_loan_balance`: 历史赊销农资余额 (Float)
- `prepayment_balance`: 已付定金/预付款余额 (Float)
- `service_fee_rate`: 管理/技术服务费率 (Float)

## 输出结果
- `net_payout_amount`: 最终实付净额 (Float)
- `loan_repayment_allocated`: 归还的赊销款 (Float)
- `statement_summary`: 对账汇总 (Dict)

## 算法流程
1. **债权确权**: 检索该农户在 Odoo 财务模块中的所有 `open` 状态的应收凭证。
2. **优先级排序**: 按照“定金 -> 农资款 -> 服务费”的顺序进行扣除。
3. **阶梯扣除**:
   - 首先冲抵 `prepayment_balance`。
   - 其次从余款中代扣 `outstanding_loan_balance`。
4. **净额计算**: `Net = Gross - Deductions`。
5. **凭证闭环**: 自动生成 `account.payment` 记录，并标记对应的 invoice 为已对销。

## 具体实现 (Implementation)
```python
def calculate_net_settlement(purchase_val, loans, prepayments, service_fee_pct):
    """
    用友风格的“农资换产品”对冲结算
    """
    fee = purchase_val * service_fee_pct
    available_for_netting = purchase_val - fee
    
    repayment = 0.0
    prepayment_cleared = 0.0
    
    # 1. 优先冲抵预付款
    prepayment_cleared = min(available_for_netting, prepayments)
    remains = available_for_netting - prepayment_cleared
    
    # 2. 其次偿还农资款
    repayment = min(remains, loans)
    net_payout = remains - repayment
    
    return {
        'net_payout': round(net_payout, 2),
        'deductions': {
            'service_fee': fee,
            'prepayment_deducted': prepayment_cleared,
            'loan_repaid': repayment
        },
        'farmer_balance_remaining': prepayments + loans - prepayment_cleared - repayment
    }
```

## 业务规则
- **熔断机制**: 若 `Net_Payout < 0`（即农户欠款超过货款），系统必须生成“坏账预警”Activity。
- **关联追溯**: 每一个扣除项必须能够穿透回原始的农资发货单（Picking）。

## 验证方法
- 验证对冲后的会计科目余额是否平衡。

## 性能指标
- 批量结算支持 500+ 农户/秒。
- 零对冲错误率。
