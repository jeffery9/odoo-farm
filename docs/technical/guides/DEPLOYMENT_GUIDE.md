# Odoo 19 农场管理系统部署手册

## 1. 模块安装顺序 (Dependency Order)
由于模块间存在强依赖，请务必按照以下顺序在 Odoo 应用中心进行安装：

1. **核心**：`farm_core` -> `farm_certification`
2. **基础作业**：`farm_operation`
3. **专业领域**：`farm_livestock`, `farm_breeding`, `farm_safety`, `farm_quality`, `farm_supply`
4. **物联（可选）**：`industrial_iot` -> `farm_iot`
5. **商务与移动**：`farm_agritourism`, `farm_marketing`, `farm_mobile`, `farm_pos`
6. **核算**：`farm_financial`, `farm_hr`, `farm_sustainability`

## 2. 物联网桥接器 (MQTT Bridge) 启动
物联网模块依赖于位于 `industrial_iot/mqtt_bridge` 的外部 FastAPI 服务。

### 启动步骤：
1. `cd industrial_iot/mqtt_bridge`
2. `pip install -r requirements.txt`
3. 配置 `.env` 文件（设置你的 MQTT Broker 地址及 Odoo Webhook 密钥）
4. 执行 `python main.py`

## 3. 系统初始化配置 (Admin Only)
安装完成后，请在 Odoo 中完成以下关键配置：
- **Analytic Plans**：确保已创建 `Agri-Projects` 计划。
- **Agri Skills**：在 `Labor & HR` 配置中录入农场特有的技能。
- **Properties**：根据不同地块类型定义其特有字段组。

## 4. 角色指派
进入用户设置，将用户指派到对应的“农场管理”组：
- **农场经理**：拥有全权限及成本看板。
- **农事专家**：负责 QCP 和防疫模板配置。
- **农场工人**：仅移动端工作台及任务录入。
