# 方向三：金融贸易——碳足迹与信用评分技术细节

## 1. 碳足迹核算架构 (Carbon Ledger)
### 1.1 排放因子库 (Emission Factor DB)
- **模型**：`agri.carbon.factor`
- **关键数据**：
  - 尿素：`2.14 kg CO2e / kg`
  - 柴油：`2.63 kg CO2e / L`
  - 电力：`0.5271 kg CO2e / kWh`（按区域电网动态调整）。

### 1.2 核算逻辑 (Batch-level LCA)
- **触发器**：每当 `stock.lot` 关联的生产单完成时执行。
- **公式**：`Total_Carbon = Σ (Input_Qty * Factor) + Σ (Energy_Usage * Factor) - Σ (Sequestration_Gain)`。
- **归口管理**：将总排放量平摊至该 Lot 下的每个 `product.uom`，生成 `CO2e_per_unit` 指标。

## 2. 农业信用评分卡 (Credit Scoring Matrix)
### 2.1 指标权重定义
| 维度 | 指标项 | 权重 | 验证手段 |
| :--- | :--- | :--- | :--- |
| **真实性** | GPS 围栏重合度 | 30% | PostGIS `ST_Contains` |
| **合规性** | 休药期拦截记录 | 30% | 检查是否有强制提前收割报警 |
| **稳产性** | 产量波动率 (CV) | 20% | 历史三年收成标准差分析 |
| **环保性** | 变量施肥比例 | 20% | 处方图执行覆盖面积 |

### 2.2 信用分计算 Job
- 定期运行 Python `Cron` 任务，刷新 `res.partner` (农户/基地) 的 `agri_credit_score`。

## 3. 指数保险理赔流 (Index Insurance API)
### 3.1 触发器配置
- **事件模型**：`agri.insurance.trigger`
- **参数**：`field_id`, `index_type` (降雨/高温), `threshold`, `duration`。
- **自动报案**：系统通过 Webhook 向保险公司 API 发送“理赔触发数据包”，包含该时刻气象站原始签名数据。