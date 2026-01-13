# Odoo Farm: 智慧农业全链路数字化解决方案

## 1. 方案愿景
在数字化转型的浪潮中，传统农业面临着生产过程“黑盒”、管理术语“工业化”以及合规追溯成本高昂等核心挑战。**Odoo Farm** 基于 **Odoo 19 社区版**，深度复刻并优化了欧洲领先的农业 ERP（Ekylibre）能力，打造了一套专为中国农业设计的**全链路数字化底座**。

---

## 2. 核心亮点

*   🚀 **全链路数字孪生溯源**：每一颗果实都有它的“履历”。扫描二维码，回溯**具体地块、天气曲线、施用清单及农工资质**。
*   🌍 **GIS 与 IoT 智慧感知**：地块是活的“生产单元”，实时显示温湿度、土壤墒情，并在异常时联动控制设备。
*   🏭 **农产品深加工管理**：支持 **Mass Balance（物料平衡）校验**，建立加工环节的批次父子继承，确保追溯不断链。
*   🌐 **多业态融合与全行业覆盖**：覆盖**大田种植、畜牧养殖、水产、食品加工（烘焙/酿酒）及农旅融合**。
*   ☁️ **SAAS 架构支持**：支持多农场独立运行、合作社级数据汇总，适合集团化或产业园部署。
*   🛡️ **中国合规适配**：内置 GB 7718 标签标准、农药实名制登记及畜禽粪污资源化台账。

---

## 🚀 核心功能矩阵 (Feature Matrix)

### 🌾 种植与生产 (Planting & Production)
*   **全生命周期管理**：生产季规划、农事干预、收获分级、N/P/K 养分平衡自动计算。
*   **MTO 智能调度**：基于品种生长周期自动校验销售订单可行性。

### 🐄 畜牧与水产 (Livestock & Aquaculture)
*   **生物资产数字化**：个体耳标、群组变动记录、ADG (平均日增重) 预测模型。
*   **自动化饲喂**：结合配方自动冲减饲料库存，环境预警联动。

### 🏭 食品深加工 (Agri-Processing)
*   **多级配方 (BOM)**：支持烘焙、酿酒等行业参数，精细化水电能耗成本分摊。
*   **质量合规**：内置 QCP 检查点、留样管理、不合格品锁定机制。

### 🏪 商业与营销 (Commerce & Marketing)
*   **全渠道触达**：CSA 会员订阅、直播带货订单同步、二维码溯源营销。

---

## 🛠️ 部署与安装说明 (Deployment)

### 1. 环境要求
*   **操作系统**: Linux (推荐 Ubuntu 22.04) 或 macOS。
*   **核心引擎**: Odoo 19.0 Community Edition。
*   **Python 版本**: 3.12+。
*   **数据库**: PostgreSQL 16+。

### 2. 安装步骤
1.  **克隆代码**: 
    ```bash
    git clone https://github.com/jeffery9/odoo-farm
    ```
2.  **配置 Addons 路径**:
    在您的 `odoo.conf` 文件中，将本仓库的根目录添加到 `addons_path` 中。
    ```text
    addons_path = /path/to/odoo/addons, /your/path/farm-standalone-repo
    ```
3.  **安装依赖**:
    ```bash
    pip install requests lxml jsonpath-ng jinja2
    ```
4.  **初始化模块**:
    启动 Odoo 后，进入 Apps 菜单，点击 "Update Apps List"，搜索并安装 **farm_core**。安装 core 后，可以根据业务需求选择性安装 farm_operation, farm_livestock, farm_processing 等模块。

### 3. IOT 桥接设置
若需启用 IoT 自动化，请参考 industrial_iot/mqtt_bridge 目录下的部署文档搭建 MQTT 代理。

---

## ⚖️ 许可证 (License)
本项目采用 **GNU Affero General Public License v3 (AGPLv3)**。
*   允许商业使用。
*   **重要义务**：如果您将本软件进行二次开发并作为 SaaS 服务提供给他人，您**必须**向用户公开您的源代码。
详情请参阅 [LICENSE](LICENSE) 文件。

## 📩 联系方式
Jeffery - [项目团队]
