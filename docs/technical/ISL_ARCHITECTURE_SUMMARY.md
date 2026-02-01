# 🏛️ Odoo 农业生态系统：ISL 架构与垂直行业细分全图谱 (V4.2)

本文件汇总了系统中所有已实现的 **垂直行业 (Vertical Industries)** 及其 **子行业细分 (Sub-sectors)**，并前瞻性地定义了尚未纳入但处于规划路径中的行业蓝图。

---

## 1. 行业架构总览：ISL 代理路径

系统通过 `_inherits` (代理继承) 实现了从 Odoo 标准工业模型到农业垂直细分的透明映射。

| 行业分类 (Industry) | 实现模块 (Path) | 核心代理模型 (ISL Model) | 业务职责 | 已注入的 DNA (Mixin) |
| :--- | :--- | :--- | :--- | :--- |
| **种植业 (Planting)** | `farm_field_crops` | `farm.crop.production` | 大田作物、生产季管理。 | `AgriWeatherSensitive`, `AgriAgentInstruction` |
| **畜牧业 (Livestock)** | `farm_livestock` | `farm.lot.livestock` | 个体档案、料肉比计算。 | `AgriBiologicalInventory`, `AgriBiologicalValuation` |
| **水产业 (Aquaculture)** | `farm_aquaculture` | `farm.lot.aquaculture` | 池塘载荷、水质联动。 | `AgriBiologicalInventory`, `AgriBiologicalValuation` |
| **加工业 (Processing)** | `farm_processing` | `farm.processing.production` | 批次指纹、HACCP 门控。 | `AgriQualityGate` |

---

## 2. 已实现的垂直行业细分详情 (Implemented Sub-sectors - Detailed)

### **A. 种植、育种与经济作物 (Planting & Specialty Crops)**
*   **大田作物 (Field Crops)**
    *   *路径*：`farm_field_crops/models/crop_isl.py`
    *   *特征*：粮食/油料作物、生产季驱动、地块级养分平衡核销。
*   **果园与园艺 (Orchard & Horticulture)**
    *   *路径*：`farm_orchard_horticulture/models/orchard_operation.py`
    *   *特征*：多年生果树建模、单株资产管理、成熟度动态监控。
*   **苗圃与育种 (Breeding & Nursery)**
    *   *路径*：`farm_breeding/models/farm_nursery_batch.py`
    *   *逻辑*：苗龄追踪、成活率评估、**一键移栽任务转化并自动生成移库单** [US-10-01]。
*   **药用植物 (Medicinal Plants)**
    *   *路径*：`farm_medicinal_plants/models/medicinal_plants_operation.py`
    *   *逻辑*：**有效成分 (Active Ingredients) 含量监测**、道地性要求核验、GMP 合规管控。
*   **茶叶精制 (Tea)**
    *   *路径*：`farm_agricultural_processing/models/seasonal/`
    *   *特征*：季节性采摘 (Flush) 管理、摊青/杀青/发酵工艺 Recipe 建模。

### **B. 畜牧、水产与特种养殖 (Animal Husbandry & Specialty)**
*   **家畜养殖 (Livestock)**
    *   *路径*：`farm_livestock/models/livestock_isl.py`
    *   *细分*：猪 (Swine)、牛 (Cattle)、羊 (Sheep) 的个体档案、繁殖状态机、FCR 与 ADG 自动计算。
*   **水产养殖 (Aquaculture/养鱼)**
    *   *路径*：`farm_aquaculture/models/aquaculture_isl.py`
    *   *特征*：**水质实时监测**（溶氧、pH、水温）、池塘/网箱载荷管理、均重与存活率追踪。
*   **养蜂业 (Apiculture)**
    *   *路径*：`farm_apiculture/models/apiculture_operation.py`
    *   *逻辑*：**蜂群强度 (Colony Strength) 监测**、蜜源植物追踪、转场迁徙调度、蜂蜜采收品质分级。
*   **食用菌 (Mushroom)**
    *   *路径*：`farm_mushroom/models/mushroom_operation.py`
    *   *逻辑*：基质配方管理、**潮次 (Flush) 产量追踪**、环境（CO2/湿度）敏感性建模。

### **C. 农产品深加工细分 (Deep Processing)**
*   **精油提取 (Essential Oils)**
    *   *路径*：`farm_agricultural_processing/models/formula_management/`
    *   *特征*：萃取率分析、**蒸馏工艺工艺参数 (Recipe)**、原料指纹向产成品指纹的自动继承。
*   **净菜与半成品 (Net Vegetables)**
    *   *路径*：`farm_agricultural_processing/models/net_vegetables/`
    *   *特征*：加工损耗率 (Yield) 分析、**多级包装嵌套逻辑**（内包 -> 外包 -> 托盘）。
*   **HACCP 质检精制**
    *   *路径*：`farm_agricultural_processing/models/processing_standards/`
    *   *特征*：关键控制点 (CCP) 强制核验、HACCP 指令自动下达。

### **D. 现代服务与消费模式 (Modern Agri-Services)**
*   **社区支持农业 (CSA)**
    *   *路径*：`farm_csa/models/csa_subscription.py`
    *   *逻辑*：订阅计划引擎、**资产认养 (Adoption)** 绑定、共享工具借还管理 [US-36-02]。
*   **农旅融合 (Agritourism)**
    *   *路径*：`farm_agritourism/models/agritourism_operation.py`
    *   *逻辑*：活动预约 (Booking) 引擎、**资源日历冲突管理**、游客体验评分与忠诚度计算。

---

## 3. 已实现的 ISL 技术成就总结 (Implementation Achievements)

1.  **后端合一**：通过 `_inherits` 代理模式，所有垂直行业数据与 Odoo 标准表物理隔离，实现了 100% 的标准财务与库存模块兼容性。
2.  **基因注入**：L0-L4 核心基因（如溯源指纹、生理阶段、气象门控、质量门控、动态估值）已全面注入上述垂直代理模型。
3.  **去工业化语义**：通过 Mixin 动态拦截 UI 视图，用户界面已完全屏蔽工业术语，实现了“工业底座，农业感官”的极致体验。

---

## 4. 规划中的垂直行业路线图 (Future Roadmap)

以下行业已完成架构预研，定义了未来的 ISL 实现细节：

*   **商业种子产业 (Seed Industry)**：亲本管理、发芽率检测、品种权 (PVP) 授权、种子包衣工艺。
*   **林业与木材管理 (Forestry & Timber)**：轮伐期管理、单株原木溯源、符合 IPCC 标准的碳汇核算。
*   **蚕桑丝绸 (Sericulture)**：蚕龄状态机 (Instar)、桑园与养蚕协同、蚕茧品质分级。
*   **城市与社区农业 (Urban Agriculture)**：立体空间映射、微型传感器接入、社交化远程监测。
*   **昆虫蛋白养殖 (Insect Farming)**：资源转化率 (BCR) 量化、生命周期加速、蛋白加工烘干工艺。
*   **花卉与观赏园艺 (Floriculture)**：花期人工控制、极速冷链监测、瓶插寿命预测 (Vase-life)。

---
*最后更新：2026-02-01 (V4.2 绝对无损全业态覆盖版)*