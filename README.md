# Odoo Farm: 智慧农业全链路数字化解决方案 / Full-Chain Smart Agriculture Solution

[Chinese](#chinese) | [English](#english)

---

<a name="chinese"></a>
## 中文版 (Chinese)

### 1. 方案愿景 (Vision)
在数字化转年的浪潮中，传统农业面临着生产过程“黑盒”、管理术语“工业化”以及合规追溯成本高昂等核心挑战。**Odoo Farm** 基于 **Odoo 19 社区版**，深度复刻并优化了欧洲领先的农业 ERP（Ekylibre）能力，打造了一套专为中国农业设计的**全链路数字化底座**。我们不仅仅是记录数据，更是通过内置的农业算法与 IoT 感知，实现从地块规划、精准作业、合规加工到消费者营销的闭环管理。

### 2. 核心痛点与解决之道 (Pain Points & Solutions)
*   **痛点 A：ERP 术语与农业习惯的“水土不服”**
    *   **解决之道**：**全站去工业化 UX**。系统自动将工业术语映射为“农事干预”、“生产配方”、“任务产量”。通过智能感知界面，技术员看到的是 N/P/K 养分平衡，而工人看到的是极简的移动端打卡按钮。
*   **痛点 B：生产计划与生物生长周期的“脱节”**
    *   **解决之道**：**MTO 生产提前期智能校验**。系统内置作物品种生长模型，在确认销售订单时自动计算“交货剩余天数”是否足以覆盖“作物生长周期”，从源头规避违约风险。
*   **痛点 C：养分投入与成本核算的“模糊账”**
    *   **解决之道**：**自动化养分平衡算法**。在确认施肥作业时，系统自动根据化肥成分换算为“纯养分”投入量，并实时汇总至地块 GIS。财务端同步实现水电能耗向具体批次的精细化分摊。

### 3. 核心亮点 (Key Highlights)
*   🚀 **全链路数字孪生溯源**：每一颗果实都有它的“履历”。扫描二维码，回溯**具体地块、天气曲线、施用清单及农工资质**。
*   🌍 **GIS 与 IoT 智慧感知**：地块是活的“生产单元”，实时显示温湿度、土壤情，并在异常时联动控制设备。
*   🏭 **农产品深加工的一入多出管理**：支持 **Mass Balance（物料平衡）校验**，建立加工环节的批次父子继承，确保追溯不断链。
*   🌐 **多业态融合与全行业覆盖**：通过“农业活动家族”架构，覆盖**大田种植、畜牧养殖、水产、食品加工（烘焙/酿酒）及农旅融合**。
*   ☁️ **SAAS 架构支持**：支持多农场独立运行、合作社级数据汇总，适合集团化或产业园部署。
*   🛡️ **中国特色合规与安全**：内置 GB 7718 标签标准、农药实名制登记及畜禽粪污资源化台账。

### 4. 顶级菜单预览 (App Directory)
```
农场管理 (Farm)
├── 基础数据 (Master Data)
├── 种植管理 (Planting)
├── 畜牧管理 (Livestock)
├── 水产养殖 (Aquaculture)
├── 观光农业 (Agritourism)
├── 农产品加工 (Processing)
├── 供应链管理 (Supply Chain)
├── 质量与安全 (Quality & Safety)
├── 物联网与自动化 (IoT)
├── 财务与成本 (Finance)
└── 加盟与合作社 (Cooperative)
```

### 5. 🚀 核心功能矩阵 (Feature Matrix)
*   **🌾 种植与生产**：生产季规划、农事干预记录、收获分级、N/P/K 养分平衡自动计算。
*   **🐄 畜牧与水产**：个体耳标/群组管理、ADG 预测模型、自动化饲喂核销、环境预警。
*   **🏭 农产品加工**：多级配方 (BOM)、精细化能耗成本分摊、QCP 检查点、留样管理。
*   **📡 智慧物联**：工业级 MQTT 集成、多租户隔离 Topic、远程下控、智慧决策看板。
*   **🏪 商业与合规**：CSA 会员订阅、直播带货订单同步、中国合规包、二维码溯源营销。

---

<a name="english"></a>
## English Version

### 1. Solution Vision
Traditional agriculture faces challenges like "black box" production, industrialized terminology mismatch, and high compliance costs. **Odoo Farm**, built on **Odoo 19**, replicates and optimizes top-tier European Agri-ERP (Ekylibre) capabilities into a **full-chain digital foundation**. We transform data into insights through built-in algorithms and IoT, covering everything from land planning to consumer marketing.

### 2. Core Pain Points & Solutions
*   **Pain Point A: Terminology Mismatch**
    *   **Solution**: **De-industrialized UX**. Automatically maps "MO/BOM" to "Agri-Interventions" and "Recipes." Context-aware interfaces show N/P/K for technicians and big-button mobile apps for workers.
*   **Pain Point B: Biological Cycle vs. Planning Gap**
    *   **Solution**: **Smart MTO Lead-time Validation**. Built-in growth models verify if delivery dates cover the biological growth period during order confirmation.
*   **Pain Point C: Vague Costing & Nutrient Tracking**
    *   **Solution**: **Automated Nutrient Balance**. Fertilization tasks automatically convert chemical usage into "pure nutrient" inputs on the parcel GIS. Processing costs are precisely allocated to lots based on meter readings.

### 3. Key Highlights
*   🚀 **Full-Chain Digital Twin Traceability**: Trace every batch back to its **land parcel, weather history, inputs used, and worker qualifications**.
*   🌍 **GIS & IoT Smart Sensing**: Parcels act as "living units" with real-time telemetry and automated threshold-based device control.
*   🏭 **Agri-Processing One-in-Multi-out**: Supports **Mass Balance validation** and parent-child lot inheritance to ensure zero gaps in the supply chain.
*   🌐 **Multi-Sector Full Coverage**: Engineered for crops, livestock, aquaculture, food processing (Baking/Winery), and agritourism.
*   ☁️ **SAAS Ready**: Native multi-tenant isolation and cooperative-level aggregation, ideal for groups or industrial parks.
*   🛡️ **China Compliance Pack**: Built-in GB 7718 standards, pesticide real-name registration, and manure ledger compliance.

### 4. App Directory (Menu Preview)
```
Farm Management (Farm)
├── Master Data (基础数据)
├── Planting (种植管理)
├── Livestock (畜牧管理)
├── Aquaculture (水产养殖)
├── Agritourism (观光农业)
├── Processing (农产品加工)
├── Supply Chain (供应链管理)
├── Quality & Safety (质量与安全)
├── IoT & Automation (物联网与自动化)
├── Finance & Costs (财务与成本)
└── Cooperative (加盟与合作社)
```

### 5. 🚀 Core Feature Matrix
*   **🌾 Planting & Production**: Campaign planning, intervention logs, harvest grading, auto N/P/K calculation.
*   **🐄 Livestock & Aquaculture**: Ear tag/Group tracking, ADG prediction models, automated feeding depletion.
*   **🏭 Agri-Processing**: Multi-stage BOMs, refined energy cost allocation, QCP inspection, sample management.
*   **📡 Smart IoT**: Industrial MQTT integration, multi-tenant Topic isolation, remote control, and KPI dashboards.
*   **🏪 Commerce & Marketing**: CSA subscriptions, live streaming order sync, QR story-telling marketing.

---

## 🛠️ Deployment & Installation / 部署与安装

### 1. Requirements (环境要求)
*   **OS**: Linux (Ubuntu 22.04+) or macOS.
*   **Engine**: Odoo 19.0 Community Edition.
*   **Python**: 3.12+ / **PostgreSQL**: 16+.

### 2. Installation Steps (安装步骤)
1.  **Clone code**: 
    ```bash
    git clone https://github.com/jeffery9/odoo-farm
    ```
2.  **Configure Addons Path**:
    Add the repository root to your `odoo.conf`:
    ```text
    addons_path = /path/to/odoo/addons, /your/path/odoo-farm
    ```
3.  **Install Dependencies**:
    ```bash
    pip install requests lxml jsonpath-ng jinja2
    ```
4.  **Initialize**:
    Update apps list in Odoo and install **farm_core**.

---

## ⚖️ License
Licensed under **GNU Affero General Public License v3 (AGPLv3)**. SaaS providers **must** disclose source code. See [LICENSE](LICENSE).

## 📩 Contact
**genin IT, 亘盈信息技术**, jeffery <jeffery9@gmail.com>
Website: [http://www.geninit.cn](http://www.geninit.cn)
