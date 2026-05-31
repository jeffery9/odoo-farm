# Odoo Farm 政府监管平台数据交换接口规范 (V1.0)

*状态: 草案 / 2026-05-31*

## 1. 概述
本规范旨在定义 Odoo Farm 实例与政府集中式监管平台（如省级“肥药两制”平台、国家追溯平台）之间的数据交换标准。系统支持 **Push（主动上报）** 与 **Pull（被动调用）** 两种模式。

## 2. 安全与认证

### 2.1 身份认证
所有 API 请求必须在 HTTP Header 中携带身份凭证：
- `X-API-KEY`: 政府平台分配给每个农场实体的唯一识别密钥。
- `Authorization`: 支持 Bearer Token (OAuth2) 模式。

### 2.2 数据完整性 (不可篡改)
每一份上报的“审计快照 (Audit Snapshot)”均包含数字签名：
- **算法**: SHA-256
- **签名对象**: 原始 JSON Payload 的序列化字符串。
- **验证**: 监管平台接收到数据后，应重新计算 Hash 值并与 Header 中的 `X-DIGITAL-SIGNATURE` 进行比对。

---

## 3. 上报模式 (Push Mode) - 自动汇报
当农场完成关键作业（CTE 事件）时，Odoo Farm 会将加密后的数据推送至政府指定的 Endpoint。

### 3.1 农事干预快照上报
**Endpoint**: `POST {gov_platform_url}/api/v1/ingest/intervention`

**数据格式 (JSON-LD / EPCIS 2.0 兼容)**:
```json
{
  "@context": "https://ref.gs1.org/standards/epcis/2.0.0/epcis-context.jsonld",
  "type": "TransformationEvent",
  "eventID": "GOV-INT-2026-0001",
  "eventTime": "2026-05-31T20:00:00Z",
  "bizStep": "processing",
  "disposition": "active",
  "readPoint": {"id": "urn:epc:id:sgln:6901234567890.0"},
  "bizTransactionList": [
    {"type": "inv", "id": "INT/2026/001"}
  ],
  "payload": {
    "intervention_name": "春季小麦病虫害防治",
    "intervention_type": "protection",
    "location": "城南 1 号地块",
    "operator_id": "3305231990********",
    "inputs": [
      {
        "product": "20% 吡虫啉",
        "reg_no": "PD20152433",
        "dosage": 1.5,
        "unit": "L"
      }
    ],
    "evidence_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
  }
}
```

---

## 4. 查询模式 (Pull Mode) - 监管审计
政府平台可通过 API 穿透式查询特定农场的运行数据。

### 4.1 获取已存证的干预列表
**Endpoint**: `POST {odoo_farm_url}/agri/gov/api/v1/interventions`
**Auth**: 用户级认证 (Auditor Account)

**请求参数**:
- `start_date`: 开始日期 (YYYY-MM-DD)
- `end_date`: 结束日期
- `farm_code`: 农场唯一代码

### 4.2 获取特定快照详情
**Endpoint**: `GET {odoo_farm_url}/agri/gov/api/v1/snapshot/{ref}`

**返回示例**:
```json
{
  "status": "success",
  "ref": "GOV-INT/2026/001",
  "signature": "sha256:...",
  "verified": true,
  "data": { ... 原始作业详情 ... }
}
```

---

## 5. 数据元定义 (KDE - Key Data Elements)

| 字段名 | 说明 | 标准对标 |
| :--- | :--- | :--- |
| `gs1_gln` | 全球位置编码（13位） | GS1 GLN |
| `gs1_gtin` | 全球贸易项目代码（14位） | GS1 GTIN |
| `operator_id` | 操作人身份证号（已脱敏或加密） | 中国农业实名制标准 |
| `reg_no` | 农药/肥料登记证号 | 国家农资登记标准 |
| `gep_score` | 生态价值评分（0-100） | 安吉模式 GEP 标准 |

---
*版本: 1.0.0 | 2026-05-31 | Odoo Farm 架构委员会发布*
