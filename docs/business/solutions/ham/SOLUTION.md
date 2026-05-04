# 🥩 火腿行业解决方案：时间与盐的数字闭环 (The Ham Cellar Arena)

## 1. 行业概览
*   **科学独特性**：火腿是“固体发酵”的艺术。核心在于通过控温、控湿实现缓慢的物理（脱水）与生化（蛋白分解）转换。
*   **核心痛点**：生猪个体差异导致的成品率不稳、长周期下的库存资金占用与估值难题。

## 2. 匹配模块与实施路径 (Capability Matching)

| 目标能力 | 匹配的已实现模块 | 实施路径 / 逻辑 |
| :--- | :--- | :--- |
| **原料继承** | `farm_livestock` | 建立 `farm.lot.ham` 对 `stock.lot` 的代理，继承生猪 DNA。 |
| **脱水核销** | `farm_processing` | 利用 `yield_analysis.py` 逻辑计算失重率。 |
| **环境防御** | `farm_iot` | `handle_cellar_telemetry` 处理湿度/霉变风险预警。 |
| **年份估值** | `farm_core` | 注入 `AgriBiologicalValuationMixin`，实现时间溢价逻辑。 |

## 3. DNA 基因注入清单
*   [x] **Level 1 (物理)**：`AgriTraceabilityMixin` (生猪到成品的数字链)
*   [x] **Level 2 (审计)**：`AgriQualityGateMixin` (含盐量/水分门控)
*   [x] **Level 3 (价值)**：`AgriBiologicalValuationMixin` (年份资产重估)
*   [x] **Level 4 (编排)**：`AgriAgentInstructionMixin` (自动新风系统调控)

## 4. 去工业化语义定义
*   `Manufacturing Order` -> **Curing & Aging Job (腌制/窖藏指令)**
*   `BOM` -> **Curing Protocol (腌制配方与工艺)**
*   `Work Center` -> **Aging Cellar / Drying Rack (窖藏室/洗晒架)**

---
*最后更新：2026-02-01*
