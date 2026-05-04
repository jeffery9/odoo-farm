# 🌿 药用植物解决方案：道地性全过程存证 (Authentic Medicinal Assets)

## 1. 行业概览
*   **科学独特性**：中药材的价值不在于“产量”，而在于“成分”与“来源”。
*   **核心痛点**：非产地药材冒充道地药材，以及炮制过程缺乏数据存证导致的质量波动。

## 2. 匹配模块与实施路径 (Capability Mapping)

| 目标能力 | 匹配的已实现模块 | 实施路径 / 逻辑 |
| :--- | :--- | :--- |
| **道地性核验** | `farm_core` | `GeoSpatialMixin` 关联海拔/土质 + 品种 DNA。 |
| **成分积累追踪** | `farm_core` | `AgriGrowthCycleMixin` (GDD) 与成分浓度模型联动。 |
| **GMP 炮制管控** | `farm_processing` | `farm.medicinal.production` 代理 `mrp.production`，注入 `AgriQualityGateMixin`。 |
| **数字化审计** | `farm_esg_compliance` | 生成符合药典标准的 Traceability Hash 指纹。 |

## 3. DNA 基因注入清单
*   [x] **Level 1 (物理)**：`AgriGrowthCycleMixin` (生长进度与成分高峰)
*   [x] **Level 1 (物理)**：`AgriTraceabilityMixin` (道地性哈希)
*   [x] **Level 2 (审计)**：`AgriQualityGateMixin` (GMP 门控)
*   [x] **Level 2 (决策)**：`AgriIncidentAlertMixin` (异常重金属/农残拦截)

## 4. 去工业化语义定义
*   `Manufacturing Order` -> **Medicinal Processing (药材炮制)**
*   `BOM` -> **Processing Protocol (炮制规范)**
*   `Work Center` -> **Processing Station (炮制位)**

---
*最后更新：2026-02-01*
