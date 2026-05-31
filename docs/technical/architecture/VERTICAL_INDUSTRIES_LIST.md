# Odoo Farm 垂直行业模块汇总 (Vertical Industry Inventory)

*更新日期: 2026-05-31 | 架构版本: V4.0 (De-industrialized)*

以下是 Odoo Farm 系统中已实现的垂直行业特化模块列表。这些模块通过 **ISL (Industry Specialized Layer)** 代理机制挂载于核心引擎之上。

## 1. 种植业 (Planting & Crops)
*   **`farm_field_crops`**: 大田作物（玉米、小麦、大豆等）。支持 VRA 变量处方与气象门控。
*   **`farm_crop`**: 基础种植逻辑，提供作物生长周期、积温 (GDD) 等科学模型支持。
*   **`farm_orchard_horticulture`**: 果园与园艺。支持果树单株管理、修剪计划及采收分级。
*   **`farm_viticulture`**: 葡萄种植业。专注于葡萄园微气候、糖度 (Brix) 指纹及修剪系统。
*   **`farm_greenhouse`**: 设施农业/温室。集成环境控制、光照补偿及无土栽培营养液管理。
*   **`farm_medicinal_plants`**: 中药材种植。支持道地性验证、GAP 合规性及活性成分追踪。
*   **`farm_floriculture`**: 花卉产业。支持鲜切花分级、花期控制及种球管理。
*   **`farm_protected_cultivation`**: 受保护耕作，专注于高附加值作物的物理保护措施。

## 2. 养殖业 (Livestock & Animal Husbandry)
*   **`farm_livestock`**: 核心畜牧业。支持个体动物档案、FCR/ADG 算法、繁育周期及生物安全。
*   **`farm_breeding`**: 育种管理。支持谱系追踪、选种选配及基因档案记录。
*   **`farm_apiculture`**: 蜂业。支持蜂群数字孪生、迁徙路径追踪及蜂蜜感官 DNA。
*   **`farm_aquaculture`**: 水产业。支持溶氧防御、自动增氧、放养密度控制及冷链闭环。

## 3. 特色行业 (Specialized Sectors)
*   **`farm_mushroom`**: 食用菌产业。支持接种批次追踪、菌料配方及环境模拟。
*   **`farm_winery`**: 酿酒业。连接葡萄产出与酿造工艺，支持 Vintage 年份管理及木桶追溯。
*   **`farm_agritourism`**: 观光农业。支持农场采摘预约、CSA 会员互动及体验式农事任务。

## 4. 跨行业加工 (Secondary Processing)
*   **`farm_agricultural_processing`**: 农业深加工。支持季节性配方、盲样保密、净菜加工及加工损耗审计。

---
*备注：所有上述模块均已对齐 `agri.intervention.base` 引擎，并支持全息 DNA 溯源。*
