# 农场管理系统：数据架构与接口规格 (Data Schema & API Spec)

## 1. 核心模型扩展字段定义

### 1.1 农业活动 (project.project)
| 字段名 | 类型 | 说明 | 业务规则 |
| :--- | :--- | :--- | :--- |
| `is_agri_activity` | Boolean | 是否农业项目 | 默认为 False，勾选后启用农业视图。 |
| `activity_family` | Selection | 活动家族 | 选项：planting, livestock, aquaculture, agritourism。 |
| `production_cycle` | Selection | 生产周期 | annual (一年生), perennial (多年生)。 |

### 1.2 生产实施 (project.task)
| 字段名 | 类型 | 说明 | 业务规则 |
| :--- | :--- | :--- | :--- |
| `campaign_id` | Many2one | 生产季 | 必填，关联 `agricultural.campaign`。 |
| `land_parcel_id` | Many2one | 生产载体 | 关联 `stock.location`。种植业为地块，水产为池塘。 |
| `size_value` | Float | 规模数值 | 面积、体积或头数。 |
| `size_unit_id` | Many2one | 规模单位 | 关联 `uom.uom` (如：亩, 立方米, 头)。 |

### 1.3 生物品种 (product.template)
| 字段名 | 类型 | 说明 | 业务规则 |
| :--- | :--- | :--- | :--- |
| `is_variety` | Boolean | 是否生物品种 | 区分常规物资（如化肥）与生物资产。 |
| `variety_type` | Selection | 品种分类 | crop, livestock, fish, service。 |
| `life_duration_days` | Integer | 标准生命周期 | 用于预测收获日期和生产阶段。 |
| `prevention_template_id`| Many2one | 防疫/植保模板 | 关联标准作业序列。 |

### 1.4 生物资产/加工批次 (stock.lot)
| 字段名 | 类型 | 说明 | 业务规则 |
| :--- | :--- | :--- | :--- |
| `father_id` | Many2one | 父本/原始批次 | 关联自身。用于系谱跟踪或加工溯源（指向原产品批次）。 |
| `mother_id` | Many2one | 母本批次 | 关联自身。 |
| `birth_date` | Date | 出生/收获日期 | |
| `certification_status` | Selection | 认证状态 | conventional, transitioning, organic, green. |

## 2. 农业活动与认证扩展 (project.project)
| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| `certification_level` | Selection | 有机、绿色、常规 |
| `transition_start_date`| Date | 有机转换开始日期 |

## 3. 加工能耗与质量记录 (mrp.production)
| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| `energy_meter_start` | Float | 加工前仪表读数 |
| `energy_meter_end` | Float | 加工后仪表读数 |
| `process_temperature` | Float | 关键工艺温度 (如杀菌/烘干) |
| `moisture_content` | Float | 出厂水分含量 (针对干制/谷物) |

## 2. IIOT 遥测与 MQTT 配置 (farm.telemetry & iot.device)

### 2.1 IOT 设备配置 (iot.device 扩展)
| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| `mqtt_topic` | Char | 订阅的 Topic (如: `farm/p01/s/do`) |
| `is_actuator` | Boolean | 是否为控制器 (如阀门/增氧机) |
| `command_topic` | Char | 控制指令发送 Topic |

### 2.2 遥测数据架构 (farm.telemetry)

## 3. IIOT 数据接入接口 (External API)

系统开放标准的 JSON-RPC 接口供外部网关或传感器调用。

### 3.1 遥测数据上传
- **方法**: `farm.telemetry.log_telemetry`
- **参数示例**:
```json
{
    "device_id": "POND_01_SENSOR",
    "sensor_type": "dissolved_oxygen",
    "value": 6.5,
    "unit_name": "mg/L"
}
```

## 4. 移动端扫码跳转规格
- **二维码内容**: `https://farm.example.com/agri/scan/<model>/<id>`
- **行为**:
    - 若 `<model>` 为 `location` (地块)，跳转至该地块当前的 `project.task` 概览页。
    - 若 `<model>` 为 `lot` (动物/批次)，跳转至该生物资产的生命档案页。
