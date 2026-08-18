# 🌌 Agri-OS 农业计算引擎学术白皮书：2v. IAS 41 生物资产公允价值评估与重估折现端到端可计算金融级解决方案 (IAS 41 Biological Asset Valuation & Fair Value Accounting)

> **学术与工业发布级别**: [PUBLIC RELEASE / OPEN-SOURCE]
> **参考设计体系**: Computable Smart Agri-OS V19.0CE (IAS 41 Agriculture)
> **脱敏状态**: 已通过物理防泄密检验，所有调试密钥及开发日志已完全安全隔离

---

## 🏛️ 1. 行业宏观背景与第一性原理挑战 (Industry Background)

在现代农业金融、生物科技上市集团审计及多主体农业合资经营中，**生物资产公允价值评估（Biological Asset Valuation）与重估损益过账** 处于金融级农业 ERP 系统的最高算法顶峰。生物资产（如：在田作物、多年生果树、消耗性林木、胎牛及泌乳牛）具有极其显著的“活体成长性”特征，其底层计算受到《国际会计准则第41号——农业》（IAS 41 Agriculture）的严格约束。然而，在传统会计 ERP 系统中，面临着三大物理与精算瓶颈：

1.  **历史成本法无法体现生物体公允成长溢价（Historical Cost Limitations）**：作物在长达数月的生长期中，其账面原值若仅记录种子、肥料、人工等历史累计投入，无法体现因“生理发育跃迁”带来的巨大公允价值（Fair Value）增值，导致农场资产负债表（Balance Sheet）发生严重低估，阻断了农业供应链信贷与生物资产抵押融资。
2.  **生理发育阶段与市场价格乘数的非线性匹配（Non-linear Biological Multiplying Model）**：在未成熟期、半成熟期和完全成熟期，作物的“可变现产出潜能（Yield Potential）”和“折现率（Discount Rate）”差异极大。如何引入“发育阶段调节系数（Growth Stage Coefficient）”和“预期产量曲线（Target Yield）”，对生物资产公允价值进行动态收敛计算，是 IAS 41 准则精确落地的数学核心。
3.  **重估增值/减值的频繁震荡与利润表波动（Revaluation Volatility & General Ledger Integration）**：生物资产每季或每月均随行就市重估。重估增值（Revaluation Gain）或减值（Revaluation Loss）必须精确核算并自动推导，产生清晰的非现金盈余记录，直接桥接到总账总账模块（General Ledger）。

**Computable Agri-OS** 的 `farm_biological_valuation` 模块，通过构建 `agri.biological.asset.valuation` 核心计量模型和 `agri.valuation.stage.coefficient` 发育期折算引擎，完全遵循 IAS 41 准则底层底盘，将生物学长势与金融精算完美超链。本白皮书将对该解决方案的底层评估模型、重估算法和操作 SOP 进行公开学术剖析。

---

## 🎨 生物资产公允价值重估与折现核算控制总线 (ASCII Topology Graph)

```text
+========================================================================================+
|                        Agri-OS IAS 41 生物资产金融估值与重估过账中枢                        |
+========================================================================================+
| [物理生物资产长势] ──► [当前发育度 %: Growth Progress] ──► [预期产量潜力: Yield Potential]  |
|  - 在田小麦/林木         - 关联农科生物孪生 GDD 进度        - 乘以 Growth Stage Coefficient    |
|                                                                    │                   |
|                                                                    ▼                   |
| [GL 模块: 总账凭证] ◄── [重估损益 Gain/Loss] ◄────────────── [计算公允 Fair Value = 产量 * 价格] |
|  - 计入本期未实现损益      - 自动对比 previous_valuation        - 实时接入市场价格 API           |
+========================================================================================+
```

---

## 2v.1 IAS 41 公允价值与成本历史模型双轨底盘 (Dual-Method Underwriting)

系统支持“市场公允价值法（Fair Value）”、“历史成本折旧法（Cost Model）”以及“混合法（Hybrid）”三种评估体系，实现不同成熟度资产的无缝兼容。

### 2v.1.1 消耗性/生产性生物资产估值操作规程 (SOP)

1.  **创建生物资产评估单**：
    *   登录 Agri-OS，导航至“生物资产估值 -> 资产价值评估”菜单，点击“新建”。系统自动初始化评估单凭证（如：`VAL-BIO-2026-0042`）。
    *   选择投保的生物资产账户（`asset_id`，如：`Lot-CHERRY-2026-A2 车厘子林段`）。
    *   设定评估基准日、评估方法（例如：`市场价格公允价值法 market_price`）。
2.  **获取生理长势与产量系数**：
    *   录入当前作物的生理长势进度（`current_growth_progress`，如：`65.0%`）。
    *   系统自适应带出该品种在成熟期的目标产量（Target Yield，如：`25,000` kg）。
3.  **加载市场波动价格**：
    *   系统关联 `farm_exchange` 或外部大宗农产品交易行情 API，自动抓取最新的当前市场价（`market_price`，如：`¥ 42.00` /公斤），记录价格数据源（`market_price_source`）。
    *   点击“重算公允价值”，系统动态完成加权估值，并自动测算出相较于上期评估值（`previous_valuation`）的净重估盈亏额（`revaluation_amount`）和重估方向类型（Gain 盈余/ Loss 亏损）。

---

## 2v.2 生物资产重估精算与折算模型 (Mathematical Formulations)

对于未成熟的生物资产，其估值必须乘以当前发育期的生理价值转换系数。

### 2v.2.1 未成熟生物资产公允价值加权测算数学模型 (Fair Value Calculus)

设某生物资产当前发育进度为 $P_{growth} \in [0, 100]$，其完全熟化时的预期目标产量为 $Y_{target}$，当前生理发育阶段对应的长势调节价值系数为 $C_{stage}$（由 `agri.valuation.stage.coefficient` 在 0.1 到 1.0 之间阶梯性分配）。

我们定义当前阶段的**预期等效产量潜力** $Y_{current}$ 为：

$$Y_{current} = Y_{target} \times \frac{P_{growth}}{100.0} \times C_{stage}$$

引入当前市场大宗即期价格 $Price_{market}$，则该资产当前的**IAS 41 公允价值** $Value_{fair}$ 自动测算公式为：

$$Value_{fair} = Y_{current} \times Price_{market}$$

若该资产采用历史成本折旧法（Cost Model），则账面价值采用**净折余净值** $Value_{net}$ 算法：

$$Value_{net} = Value_{original} - \left(Value_{original} \times \frac{\text{Years}_{elapsed}}{\text{Years}_{depreciation}} \times Rate_{depreciation}\right)$$

通过 **Odoo 强依赖计算链（@api.depends）**，一旦市场价格发生毫秒级跳变或作物发育进度发生物理跃迁，系统会自动瞬间刷写全量在田生物资产的 Fair Value 和 Net Book Value，100% 杜绝因会计记账滞后而导致企业资产账实不符。

---

## 2v.3 重估增值与亏损的自动清算过账逻辑 (Accounting Automation)

在评估单表单中，重估额 `revaluation_amount` 自动重算：

```python
    @api.depends('fair_value', 'net_book_value', 'valuation_method', 'previous_valuation')
    def _compute_revaluation_amount(self):
        """
        IAS 41 Revaluation Cleaving Engine: Detect variation between 
        current calculated valuation (Fair Value or Net Book Value) and previous historical valuation,
        marking it automatically as Unrealized Gain or Loss.
        """
        for valuation in self:
            current_val = valuation.fair_value if valuation.valuation_method == 'market_price' else valuation.net_book_value
            valuation.revaluation_amount = current_val - valuation.previous_valuation
            if valuation.revaluation_amount > 0:
                valuation.revaluation_type = 'gain'
            else:
                valuation.revaluation_type = 'loss'
```

当评估单状态被确认为 `过账（posted）` 时，Agri-OS 会通过桥接模块，自动在会计总账中产生一张非现金公允价值变动凭证（Unrealized Revaluation Journal Entry）：
*   **借 (Dr)**：生物资产——公允价值重估值 （资产负债表科目）
*   **贷 (Cr)**：公允价值变动损益——未实现生物资产增值 （利润表科目）

通过这种**将农业生物发育学特征、高频价格网关、与严格的国际会计准则（IAS 41）多维数据无缝穿透**的可计算机制，**Agri-OS** 为现代化大型生态农场和跨国农业投资集团，构建了真正阳光、可追溯、可审计、且能无缝对接金融资本的**数字化信用基石**。

---

> **Agri-OS IAS 41 Biological Asset Valuation Sheet | Computable Finance | Audit-Ready**
