# 🏛️ Odoo 农业生态系统：ISL 架构与垂直行业细分全图谱 (V6.0)

本文件汇总了系统中所有基于 **ISL (Industry Standard Layer)** 架构的实现，明确了 Odoo 标准模型、农业代理模型（Domain Models）以及垂直行业扩展之间的 `_inherits` 映射关系。

---

## 1. 行业架构总览：ISL 代理路径

系统通过 `_inherits` (代理继承) 实现了从 Odoo 标准工业模型或域模型到农业垂直细分的透明映射。

| 行业分类 (Industry) | 实现模块 (Path) | 核心代理模型 (ISL Model) | 业务职责 | 已注入的 DNA (Mixin) |
| :--- | :--- | :--- | :--- | :--- |
| **种植业 (Planting)** | `farm_field_crops` | `farm.crop.production` | 大田作物、生产季管理。 | `AgriWeatherSensitive`, `AgriAgentInstruction` |
| **生态共生 (Symbiosis)**| `farm_symbiosis` | `farm.symbiotic.order` | 稻渔/稻虾、生态拦截。 | `NutrientMixin`, `AgriQualityGate` |
| **工厂化渔业 (RAS)** | `farm_aquaculture` | `farm.ras.production` | 循环水系统、能效优化。 | `AgriResourceConsumption`, `AgriIncidentAlert` |
| **畜牧业 (Livestock)** | `farm_livestock` | `farm.lot.livestock` | 个体档案、料肉比计算。 | `AgriBiologicalInventory`, `AgriBiologicalValuation` |
| **水产业 (Aquaculture)** | `farm_aquaculture` | `farm.lot.aquaculture` | 池塘载荷、水质联动。 | `AgriBiologicalInventory`, `AgriBiologicalValuation` |
| **酿造业 (Winery)** | `farm_winery` | `farm.winery.production` | 红酒发酵、陈酿管理。 | `AgriTraceability`, `AgriIncidentAlert` |
| **发酵业 (Ferment)**| `farm_fermentation` | `farm.fermentation.order` | 窖池酿造、年份增值。 | `AgriBiologicalValuation`, `GeoSpatialMixin` |
| **加工业 (Processing)** | `farm_processing` | `farm.processing.production` | 批次指纹、HACCP 门控。 | `AgriQualityGate` |
| **智能层 (Intelligence)**| `farm_ai_llm_integration` | `agri.llm.configuration` | AI 模型配置与架构适配。 | `AgriAiBaseMixin` |

---

## 2. 已实现的垂直行业细分详情 (Implemented Sub-sectors - Detailed)

### **A. 精密环境控制与花卉 (Precision Climate & Floriculture)**
*   **花卉与观赏园艺 (Floriculture)**
    *   *路径*：`farm_floriculture/models/flower_isl.py`
    *   *代理*：`farm.flower.order` (代理 `mrp.production`), `farm.lot.flower` (代理 `stock.lot`)
    *   *特征*：**DIF (昼夜温差) 驱动的开花诱导控制**、基于采收状态的**瓶插寿命 (Vase-life) 动态预测**、极致冷链红线拦截、**采后保鲜处理 (Preservation) 闭环**（保鲜后寿命 +3 天）。

### **B. 传统发酵、酿造与深加工 (Traditional Brewing & Refining)**
*   **传统发酵工业 (Vinegar/Soy/Baijiu)**
    *   *路径*：`farm_fermentation/models/fermentation_isl.py`
    *   *特征*：**窖池 (Pit DNA) 数字化档案**、发酵品温实时预警与主动冷却、**陈年原浆资产年化增值模型**、勾调指纹链式聚合。
*   **葡萄酒酿造 (Winery & Enology)**
    *   *路径*：`farm_winery/models/winery_isl.py`
    *   *特征*：**发酵动力学监控**（糖醇转换曲线）、橡木桶陈酿资产追踪、多级调配 DNA 聚合。
*   **火腿加工与窖藏 (Dry-Cured Ham)**
    *   *特征*：生猪批次 DNA 链式继承、**脱水率 (Weight Loss) 动态核销**、年份资产自动增值。
*   **水产加工与冷冻 (Aquatic Processing)**
    *   *特征*：**包冰率 (Glazing %) 自动核销**、速冻机中心温度强制门控、捕捞水质指纹继承。

### **C. 生态协同与工业化水产 (Eco-Symbiosis & Industrial Aquaculture)**
*   **稻渔/稻虾综合种养 (Symbiosis)**
    *   *路径*：`farm_symbiosis/models/symbiosis_isl.py`
    *   *特征*：**生态协同养分核算**（鱼粪抵扣肥力）、**高毒农药硬拦截 (Ecological Gate)**、双产物同步核销。
*   **工厂化循环水养殖 (RAS)**
    *   *路径*：`farm_aquaculture/models/ras_isl.py`
    *   *特征*：**维生系统 (LSS) 组件寿命追踪**、氨氮代谢负荷实时预测、极致能效比 (kWh/kg) 核算、水循环故障“生存模式”防御。

### **D. 基础种植、育种与畜牧 (Planting & Animal Husbandry)**
*   **商业种子产业 (Seed Industry)**：种子“四检”数字化、亲本哈希指纹、品种权 (PVP) 分销合规核验。
*   **果园与园艺 (Orchard)**：单株资产管理 (Digital Twin)、积温驱动的成熟度预测、多年生资产估值。
*   **大田作物 (Field Crops)**：变量作业 (VRA) 指令闭环、生产季驱动。
*   **家畜养殖 (Livestock)**：个体档案、FCR 与 ADG 自动计算、**休药期 (PHI) 强制门控**。

---

## 3. 已实现的 ISL 技术成就总结 (Implementation Achievements)

### **A. 双基线安全内核 (Dual Baseline)**
系统已建立 **ESG (可持续性)** 与 **HACCP (食品安全)** 双重 DNA 基线，作为非功能性需求贯穿全业态。

### **B. 订单与库存商业衔接 (Order & Inventory Bridge)**
通过 `farm_isl` 提供的自动钩子，实现了垂直行业 DNA 在商业流中的透明流转：
1.  **收货自动转型**：采购入库时，标准 `stock.lot` 自动向上转型为行业代理批次（如 `farm.lot.ham`）。
2.  **调拨硬红线**：移库确认前强制校验行业安全门控（如 PHI、冷链红线）。
3.  **销售品质锁定**：销售确认前核验行业品质指标（如 Vase-life）。

### **C. 语义去工业化**
用户界面已完全屏蔽工业术语（MO/BOM/Work Center），实现了“工业底座，农业/智能感官”的极致体验。

---

## 4. 规划中的垂直行业路线图 (Future Roadmap)

以下行业已完成架构预研，处于待实施状态：
*   **林业与木材管理 (Forestry & Timber)**：轮伐期管理、单株原木溯源、固碳核算。
*   **蚕桑丝绸 (Sericulture)**：蚕龄状态机 (Instar)、桑园与养蚕协同。
*   **城市与社区农业 (Urban Agriculture)**：立体空间映射、微型传感器接入。
*   **昆虫蛋白养殖 (Insect Farming)**：资源转化率 (BCR) 量化、生命周期加速。

---
*最后更新：2026-02-01 (V6.0 垂直细分与商业衔接全对齐版)*