# Odoo Farm: 智慧农业全链路数字化解决方案 / Full-Chain Smart Agriculture Solution

[Chinese](#chinese) | [English](#english)

---

<a name="chinese"></a>
## 中文版 (Chinese)

### 1. 方案愿景 (Vision)
在数字化转年的浪潮中，传统农业面临着生产过程“黑盒”、管理术语“工业化”以及合规追溯成本高昂等核心挑战。**Odoo Farm** 基于 **Odoo 19 社区版**，深度复刻并优化了欧洲领先的农业 ERP（Ekylibre）能力，打造了一套专为中国农业设计的**全链路数字化底座**。我们不仅仅是记录数据，更是通过内置的农业算法与 IoT 感知，实现从地块规划、精准作业、合规加工到消费者营销的闭环管理。



### 🎯 价值主张 (Value Proposition)

**Odoo Farm 不仅仅是一个软件系统，它是驱动现代农业向 L5 级完全自主化迈进的数字引擎。**
我们将农业从“靠天吃饭”的经验主义，升级为由数据、AI 和智能装备驱动的确定性科学。通过这套系统，您将获得：

1.  **💰 商业溢价与品牌跃升 (Brand Premium)**：通过区块链级不可篡改的全息溯源和国际 ESG 认证报告，让您的农产品轻松跨越进入高端零售与出口市场的门槛。
2.  **📉 边际成本的指数级下降 (Cost Reduction)**：借助 AI 视觉病害诊断、VRA（变量施药）处方图以及基于气象预测的主动干预调度，避免盲目投入，精准节约水、肥、药的每一分成本。
3.  **🤖 劳动力结构的彻底颠覆 (Workforce Transformation)**：告别繁重的人工记录。IoT 传感器、边缘控制网关、以及未来的无人机和农业机器人蜂群，将直接接入系统总线，实现从“人管机器”到“系统调度智能体 (Agent to Agent)”的跨越。
4.  **📈 实时透明的金融信用资产 (Bankable Assets)**：将地块的生长周期和生态投入转化为实时可视的生物资产估值图谱。让农场拥有清晰的数字账本，彻底打通农业信贷保险与供应链融资的“最后一公里”。


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


> **💡 UX 设计哲学: "工具箱, 而非百科全书" (Tools, Not Trees)**
> 本系统彻底摒弃了传统 ERP 庞大深邃、让农民感到畏惧的“巨石型树状菜单”。我们采用现代 SaaS 的“独立工具化”设计：需要操作温室，就打开【温室应用】；需要分析病虫害，就打开【AI 视觉应用】。所有的 App 层级不超过 3 层，真正的做到了“开箱即用，降低认知负荷”。更多详见 `docs/business/UX_MENU_ARCHITECTURE_PRINCIPLES.md`。


### 4. 顶级菜单预览 (App Directory)
```
🌐 Odoo 农业矩阵 (App Ecosystem)
由于采用“工具化”设计，系统不再提供大一统的“基础数据”菜单。主数据跟随业务归口：

🌿 种植管理 (Planting)
   ├── 生产季规划 (Campaigns)
   ├── 农事干预 (Interventions)
   └── 配置：地块GIS、作物品种、生长基点

🐄 畜牧管理 (Livestock)
   ├── 个体/群组档案 (Herds)
   ├── 繁育与配种 (Breeding)
   └── 配置：动物血统、健康标准

🏭 农产品加工 (Processing)
   ├── 批次加工单 (Processing Orders)
   └── 配置：转化配方 (BOM)、加工车间

📡 物联网与自动化 (IoT)
   ├── 数字孪生看板 (Digital Twin)
   └── 配置：传感器资产、网关路由、规则引擎

质量安全、农旅、供应链等其余 15+ 核心业务域均遵循此“高内聚”设计模式。
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



### 🎯 Value Proposition

**Odoo Farm is not just a software system; it is the digital engine driving modern agriculture towards L5 full autonomy.**
We upgrade agriculture from experience-based "weather-dependent" practices to a deterministic science driven by data, AI, and smart equipment.

1.  **💰 Brand Premium & Market Access**: With blockchain-level immutable holographic traceability and international ESG certification reporting, your produce can easily cross the threshold into premium retail and export markets.
2.  **📉 Exponential Cost Reduction**: Leverage AI vision for disease diagnosis, VRA (Variable Rate Application) prescription maps, and active intervention scheduling based on weather forecasts to eliminate blind inputs and precisely save every cent on water, fertilizer, and pesticides.
3.  **🤖 Workforce Transformation**: Say goodbye to heavy manual recording. IoT sensors, edge control gateways, and future swarms of drones and agricultural robots connect directly to the system bus, leaping from "human managing machines" to "System Orchestrating Agents (A2A)".
4.  **📈 Real-time Bankable Assets**: Transform plot growth cycles and ecological inputs into real-time visual biological asset valuations. Give farms a clear digital ledger, completely bridging the "last mile" of agricultural credit, insurance, and supply chain financing.

> **💡 UX Philosophy: "A Toolbox, Not an Encyclopedia" (Tools, Not Trees)**
> We have completely abandoned the massive, intimidating "monolithic tree menus" of traditional ERPs. We adopt modern SaaS "independent tool" design: need to operate a greenhouse? Open the [Greenhouse App]. Need to analyze pests? Open the [AI Vision App]. All App depths are capped at 3 levels, achieving true "out-of-the-box" usability to minimize cognitive load for agricultural workers.

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
🌐 Odoo Agri Matrix (App Ecosystem)
Following the "Tools, not Trees" philosophy, there is no monolithic "Master Data" menu. Data is managed where it belongs:

🌿 Planting
   ├── Campaigns & Planning
   ├── Field Interventions
   └── Config: Parcels GIS, Crop Varieties, Growth Stages

🐄 Livestock
   ├── Herd & Individual Records
   ├── Breeding Operations
   └── Config: Pedigree, Health Standards

🏭 Processing
   ├── Processing Orders
   └── Config: Recipes (BOM), Workcenters

📡 IoT & Automation
   ├── Digital Twin Dashboard
   └── Config: Sensor Assets, Gateways, Automation Rules

Quality, Agritourism, Supply Chain, and 15+ other core domains follow this highly cohesive design pattern.
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
